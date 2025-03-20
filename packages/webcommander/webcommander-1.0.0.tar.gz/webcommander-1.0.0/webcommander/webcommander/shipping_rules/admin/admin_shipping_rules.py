from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.shipping_rules_dto import *
from webcommander.webcommander.shipping_rules.admin.admin_shipping_rules_api_url import AdminShippingRulesApiUrl


class AdminShippingRules(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> ShippingRulesListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminShippingRulesApiUrl.ADMIN_SHIPPING_RULES, params=params, response_obj=ShippingRulesListResponseDTO())
        return response

    def details(self, id: str) -> ShippingRulesDetailsResponseDTO:
        response = self.get(url=AdminShippingRulesApiUrl.ADMIN_SHIPPING_RULES + f"/{id}", response_obj=ShippingRulesDetailsResponseDTO())
        return response

    def create_shipping_profiles(self, request_data: ShippingRuleRequestDTO) -> ShippingRulesDetailsResponseDTO:
        response = self.post(url=AdminShippingRulesApiUrl.ADMIN_SHIPPING_RULES, request_obj=request_data,
                             response_obj=ShippingRulesDetailsResponseDTO())
        return response

    def update_shipping_profiles(self, id:str, request_data: ShippingRuleUpdateRequestDTO) -> ShippingRulesDetailsResponseDTO:
        response = self.put(url=AdminShippingRulesApiUrl.ADMIN_SHIPPING_RULES + f"/{id}", request_obj=request_data,
                             response_obj=ShippingRulesDetailsResponseDTO())
        return response

    def delete_shipping_rules(self, id: str) -> dict:
        response = self.delete_request(url=AdminShippingRulesApiUrl.ADMIN_SHIPPING_RULES + f"/{id}", response_obj={})
        return response