import json
from dataclasses import dataclass

from webcommander.common.sdk_conf import SDKConfig
from webcommander.common.sdk_console import SDKConsole
from webcommander.common.sdk_const import SDKConst
from webcommander.common.sdk_util import SDKUtil
from webcommander.common.wc_exception import WCException
from webcommander.http.http_const import RequestType
from webcommander.http.http_requester import HTTPRequester, HTTPResponse
from webcommander.sdlize.dto_base import DTOBase
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.auth.auth_api_url import AuthApiUrl
from webcommander.webcommander.auth.dto.token_dto import TokenResponseDTO, RequestTokenDTO, RefreshTokenDTO


@dataclass
class HTTPRequestData:
    url: str
    request_type: RequestType
    json_dict: dict = None
    data: dict = None
    params: dict = None
    file: dict = None
    exception: bool = True


class WCRestProcessor:
    http_requester: HTTPRequester = HTTPRequester()
    rest_token: WCBaseDTO = None
    request_token_dto: RequestTokenDTO = None
    first_stage_authentication: bool = False

    def __init__(self, request_token_dto: RequestTokenDTO):
        self.request_token_dto = request_token_dto

    def process_error_response(self, response: HTTPResponse, response_data: dict):
        exception_message = "Something happened wrong!"
        http_code = response.httpCode
        if http_code == 400:
            exception_message = "Validation Errors"
        if http_code == 403:
            exception_message = "Access denied"

        exception = WCException(exception_message).add_raw_response(response_data)
        errors = SDKUtil.get_dict_value(response_data, "errors")
        if isinstance(errors, list):
            for error in errors:
                message = SDKUtil.get_dict_value(error, "message")
                if message:
                    exception.add_error(message)
        raise exception

    def _get_data(self, response: HTTPResponse, response_obj: DTOBase, exception=True):
        response_data = response.data
        SDKConsole.log(response_data, is_print=SDKConfig.PRINT_RAW_RESPONSE)
        if response.status != SDKConst.SUCCESS or not response_data:
            if exception:
                self.process_error_response(response=response, response_data=response_data)
            return None

        # Check if data is dict Format if not convert it
        if not isinstance(response_data, dict):
            try:
                response_data = json.loads(response_data)
            except json.JSONDecodeError as e:
                self.process_error_response(response=response, response_data=response_data)
                return None

        if response_obj:
            return response_obj.load_dict(response_data)
        return response_data

    def _set_token(self, api_response):
        response: TokenResponseDTO = self._get_data(api_response, response_obj=TokenResponseDTO())
        if not response:
            raise WCException("Unable to set token")
        if not response.accessToken or not response.refreshToken:
            raise WCException("Unable to set token")
        self.rest_token = response

    def _init_auth(self):
        api_response = self.http_requester.post(url=AuthApiUrl.GET_TOKEN, json_dict=self.request_token_dto.to_dict())
        self._set_token(api_response=api_response)

    def _renew_token(self):
        refresh_token = RefreshTokenDTO(
            clientId=self.request_token_dto.clientId,
            clientSecret=self.request_token_dto.clientSecret,
            redirectUri=self.request_token_dto.redirectUri,
            refreshToken=self.rest_token.refreshToken
        )
        api_response = self.http_requester.post(url=AuthApiUrl.GET_TOKEN, json_dict=refresh_token.to_dict())
        self._set_token(api_response=api_response)
        self.http_requester.add_bearer_token(self.rest_token.accessToken)

    def _init_config(self):
        self.http_requester.baseUrl = self.request_token_dto.webCommanderUrl
        if not self.rest_token or not self.rest_token.accessToken:
            self._init_auth()
        self.http_requester.add_bearer_token(self.rest_token.accessToken)

    def _send_request(self, request_data: HTTPRequestData) -> HTTPResponse:
        response = None
        if request_data.request_type == RequestType.POST:
            response = self.http_requester.post(url=request_data.url, json_dict=request_data.json_dict,
                                                data=request_data.data, file=request_data.file)
        elif request_data.request_type == RequestType.PUT:
            response = self.http_requester.put(url=request_data.url, json_dict=request_data.json_dict,
                                               data=request_data.data, file=request_data.file)
        elif request_data.request_type == RequestType.PATCH:
            response = self.http_requester.patch(url=request_data.url, json_dict=request_data.json_dict,
                                                 data=request_data.data, file=request_data.file)
        elif request_data.request_type == RequestType.DELETE:
            response = self.http_requester.delete(url=request_data.url, json_dict=request_data.json_dict,
                                                  params=request_data.params)
        else:
            response = self.http_requester.get(url=request_data.url, params=request_data.params)
        request_summary = f"URL: {self.http_requester.baseUrl} \nURL Postfix: {request_data.url} \nparams: {request_data.params} \nJSON Data: {request_data.json_dict}"
        SDKConsole.log(message=request_summary, is_print=SDKConfig.PRINT_REQUEST_DATA)
        return response

    def process_rest_request(self, request_data: HTTPRequestData, response_obj: DTOBase = None):
        self._init_config()
        response: HTTPResponse = self._send_request(request_data=request_data)
        if response.httpCode == 401:
            self._renew_token()
            response: HTTPResponse = self._send_request(request_data=request_data)
        if response.httpCode == 204:
            print("Request was successful, but there is no content to display.")
            return None
        return self._get_data(response=response, response_obj=response_obj, exception=request_data.exception)

    def get(self, url: str, params: dict = None, request_obj: DTOBase = None, json_dict: dict = None, response_obj: DTOBase = None, exception: bool = True):
        if request_obj and not json_dict:
            json_dict = request_obj.to_dict()
        return self.process_rest_request(
            request_data=HTTPRequestData(url=url, params=params, json_dict=json_dict, request_type=RequestType.GET, exception=exception),
            response_obj=response_obj)

    def delete_request(self, url: str, params: dict = None, request_obj: WCBaseDTO = None, json_dict: dict = None,
                       response_obj: WCBaseDTO = None,
                       exception: bool = True):
        if request_obj and not json_dict:
            json_dict = request_obj.to_dict()
        return self.process_rest_request(
            request_data=HTTPRequestData(url=url, params=params, json_dict=json_dict, request_type=RequestType.DELETE,
                                         exception=exception),
            response_obj=response_obj)

    def post(self, url: str, request_obj: WCBaseDTO = None, json_dict: dict = None, data: dict = None,
             file: dict = None, response_obj: DTOBase = None, exception: bool = True):
        if request_obj and not json_dict:
            json_dict = request_obj.to_dict()
        return self.process_rest_request(
            request_data=HTTPRequestData(url=url, json_dict=json_dict, data=data, file=file,
                                         request_type=RequestType.POST, exception=exception), response_obj=response_obj)

    def put(self, url: str, request_obj: WCBaseDTO = None, json_dict: dict = None, data: dict = None, file: dict = None,
            response_obj: WCBaseDTO = None, exception: bool = True):
        if request_obj and not json_dict:
            json_dict = request_obj.to_dict()
        return self.process_rest_request(
            request_data=HTTPRequestData(url=url, json_dict=json_dict, data=data, file=file,
                                         request_type=RequestType.PUT, exception=exception), response_obj=response_obj)

    def patch(self, url: str, request_obj: WCBaseDTO = None, json_dict: dict = None, data: dict = None,
              file: dict = None, response_obj: WCBaseDTO = None, exception: bool = True):
        if request_obj and not json_dict:
            json_dict = request_obj.to_dict()
        return self.process_rest_request(
            request_data=HTTPRequestData(url=url, json_dict=json_dict, data=data, file=file,
                                         request_type=RequestType.PATCH, exception=exception),
            response_obj=response_obj)
