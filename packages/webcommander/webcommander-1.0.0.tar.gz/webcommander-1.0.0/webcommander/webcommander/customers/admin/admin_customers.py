from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.common_dto import CommonMessageDTO
from webcommander.webcommander.common.dto.customers_dto import *
from webcommander.webcommander.customers.admin.admin_customers_api_url import AdminCustomersApiUrl


class AdminCustomers(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None, param_filters: dict = None) -> CustomersListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        if param_filters:
            for key, value in param_filters.items():
                params = SDKUtil.init_dict_if_value(params, key, value)
        response = self.get(url=AdminCustomersApiUrl.ADMIN_CUSTOMERS, params=params,
                            response_obj=CustomersListResponseDTO())
        return response

    def details(self, id: str) -> CustomersListResponseDTO:
        response = self.get(url=AdminCustomersApiUrl.ADMIN_CUSTOMERS + f"/{id}",
                            response_obj=CustomersDetailsResponseDTO())
        return response

    def customers_fields_get_list(self) -> RegistrationFieldsDTO:
        response = self.get(url=AdminCustomersApiUrl.CREATE_CUSTOMER_FIELDS, response_obj=RegistrationFieldsDTO())
        return response

    def create(self, request_data: CustomerCreateDTO) -> CustomersDetailsResponseDTO:
        response = self.post(url=AdminCustomersApiUrl.ADMIN_CUSTOMERS, request_obj=request_data,
                             response_obj=CustomersDetailsResponseDTO())
        return response

    def update(self, id: str, request_data: CustomerCreateDTO) -> CustomersDetailsResponseDTO:
        response = self.put(url=AdminCustomersApiUrl.CUSTOMER_DETAILS.format(id=id), request_obj=request_data,
                            response_obj=CustomersDetailsResponseDTO())
        return response

    def delete(self, id: str):
        response = self.delete_request(url=AdminCustomersApiUrl.CUSTOMER_DETAILS.format(id=id))
        return response

    def change_password(self, id: str, request_data: CustomerChangePasswordRequestDTO) -> CommonMessageDTO:
        response = self.post(url=AdminCustomersApiUrl.CUSTOMER_CHANGE_PASSWORD.format(id=id), request_obj=request_data,
                             response_obj=CommonMessageDTO())
        return response

    def reset_password(self, id: str, request_data: CustomerCreateDTO) -> CommonMessageDTO:
        response = self.post(url=AdminCustomersApiUrl.CUSTOMER_CHANGE_PASSWORD.format(id=id), request_obj=request_data,
                             response_obj=CommonMessageDTO())
        return response

    def add_addresses(self, id: str, request_data: CustomerAddressCreateRequestDTO) -> CustomersDetailsResponseDTO:
        response = self.post(url=AdminCustomersApiUrl.CUSTOMER_ADDRESSES.format(id=id), request_obj=request_data,
                             response_obj=CustomersDetailsResponseDTO())
        return response
