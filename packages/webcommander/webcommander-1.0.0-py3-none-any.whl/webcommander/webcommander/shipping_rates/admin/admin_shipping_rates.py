from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.shipping_rates_dto import *
from webcommander.webcommander.shipping_rates.admin.admin_shipping_rates_api_url import AdminShippingRatesApiUrl


class AdminShippingRates(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> ShippingRatesListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminShippingRatesApiUrl.ADMIN_SHIPPING_RATES, params=params, response_obj=ShippingRatesListResponseDTO())
        return response

    def details(self, id: str) -> ShippingRatesDetailsResponseDTO:
        response = self.get(url=AdminShippingRatesApiUrl.ADMIN_SHIPPING_RATES + f"/{id}", response_obj=ShippingRatesDetailsResponseDTO())
        return response

    def create_shipping_rates(self, request_data: ShippingRateRequestDTO) -> ShippingRatesDetailsResponseDTO:
        response = self.post(url=AdminShippingRatesApiUrl.ADMIN_SHIPPING_RATES, request_obj=request_data,
                             response_obj=ShippingRatesDetailsResponseDTO())
        return response

    def update_shipping_rates(self, id:str, request_data: ShippingRateRequestDTO) -> ShippingRatesDetailsResponseDTO:
        response = self.put(url=AdminShippingRatesApiUrl.ADMIN_SHIPPING_RATES + f"/{id}", request_obj=request_data,
                             response_obj=ShippingRatesDetailsResponseDTO())
        return response

    def shipping_rates_delete(self, id: str) -> dict:
        response = self.delete_request(url=AdminShippingRatesApiUrl.ADMIN_SHIPPING_RATES + f"/{id}", response_obj={})
        return response
