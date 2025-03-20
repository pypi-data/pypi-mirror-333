from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.shipping_profiles_dto import *
from webcommander.webcommander.shipping_profiles.admin.admin_shipping_profiles_api_url import AdminShippingProfilesApiUrl


class AdminShippingProfiles(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> ShippingProfilesListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminShippingProfilesApiUrl.ADMIN_SHIPPING_PROFILES, params=params, response_obj=ShippingProfilesListResponseDTO())
        return response

    def details(self, id: str) -> ShippingProfilesDetailsResponseDTO:
        response = self.get(url=AdminShippingProfilesApiUrl.ADMIN_SHIPPING_PROFILES + f"/{id}", response_obj=ShippingProfilesDetailsResponseDTO())
        return response

    def create_shipping_profiles(self, request_data: ShippingProfilesRequestDTO) -> ShippingProfilesDetailsResponseDTO:
        response = self.post(url=AdminShippingProfilesApiUrl.ADMIN_SHIPPING_PROFILES, request_obj=request_data,
                             response_obj=ShippingProfilesDetailsResponseDTO())
        return response

    def update_shipping_profiles(self, id: str, request_data: ShippingProfilesRequestDTO) -> ShippingProfilesDetailsResponseDTO:
        response = self.put(url=AdminShippingProfilesApiUrl.ADMIN_SHIPPING_PROFILES + f"/{id}", request_obj=request_data,
                             response_obj=ShippingProfilesDetailsResponseDTO())
        return response

    def shipping_profiles_delete(self, id: str) -> dict:
        response = self.delete_request(url=AdminShippingProfilesApiUrl.ADMIN_SHIPPING_PROFILES + f"/{id}", response_obj={})
        return response