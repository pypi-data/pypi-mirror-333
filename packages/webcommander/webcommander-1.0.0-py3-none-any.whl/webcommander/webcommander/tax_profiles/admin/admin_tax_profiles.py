from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.tax_profiles_dto import *
from webcommander.webcommander.tax_profiles.admin.admin_tax_profiles_api_url import AdminTaxProfilesApiUrl


class AdminTaxProfiles(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> TaxProfileListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminTaxProfilesApiUrl.ADMIN_TAX_PROFILES, params=params, response_obj=TaxProfileListResponseDTO())
        return response

    def details(self, id: str) -> TaxProfileDetailsResponseDTO:
        response = self.get(url=AdminTaxProfilesApiUrl.ADMIN_TAX_PROFILES + f'/{id}', response_obj=TaxProfileDetailsResponseDTO())
        return response

    def create_tax_profiles(self, request_data: TaxProfileRequestDTO) -> TaxProfileDetailsResponseDTO:
        response = self.post(url=AdminTaxProfilesApiUrl.ADMIN_TAX_PROFILES, request_obj=request_data,
                             response_obj=TaxProfileDetailsResponseDTO())
        return response

    def update_tax_profiles(self, id: str, request_data: TaxProfileRequestDTO) -> TaxProfileDetailsResponseDTO:
        response = self.put(url=AdminTaxProfilesApiUrl.ADMIN_TAX_PROFILES + f'/{id}', request_obj=request_data,
                             response_obj=TaxProfileDetailsResponseDTO())
        return response
