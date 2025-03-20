from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.currency_dto import CurrencyListDTO, CurrencyInfoResponseDTO, CurrencyCreateDataDTO
from webcommander.webcommander.currency.admin.admin_currency_api_url import AdminCurrencyApiUrl


class AdminCurrency(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> CurrencyListDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminCurrencyApiUrl.CURRENCIES, params=params, response_obj=CurrencyListDTO())
        return response

    def info(self, id: str = None) -> CurrencyInfoResponseDTO:
        response = self.get(url=AdminCurrencyApiUrl.CURRENCY_DETAIL.format(id=id),
                            response_obj=CurrencyInfoResponseDTO())
        return response

    def create(self, request_data: CurrencyCreateDataDTO) -> CurrencyInfoResponseDTO:
        response = self.post(url=AdminCurrencyApiUrl.CURRENCIES, request_obj=request_data,
                             response_obj=CurrencyInfoResponseDTO())
        return response

    def update(self, id: str, request_data: CurrencyCreateDataDTO) -> CurrencyInfoResponseDTO:
        response = self.put(url=AdminCurrencyApiUrl.CURRENCY_DETAIL.format(id=id), request_obj=request_data,
                            response_obj=CurrencyInfoResponseDTO())
        return response

    def delete(self, id: str):
        response = self.delete_request(url=AdminCurrencyApiUrl.CURRENCY_DETAIL.format(id=id))
        return response
