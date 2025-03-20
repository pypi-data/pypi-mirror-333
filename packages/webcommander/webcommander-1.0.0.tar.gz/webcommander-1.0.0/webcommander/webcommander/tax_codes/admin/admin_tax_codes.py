from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.tax_codes_dto import *
from webcommander.webcommander.tax_codes.admin.admin_tax_codes_api_url import AdminTaxCodesApiUrl


class AdminTaxCodes(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> TaxCodesListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminTaxCodesApiUrl.ADMIN_TAX_CODES, params=params, response_obj=TaxCodesListResponseDTO())
        return response

    def details(self, id: str) -> TaxCodesDetailsResponseDTO:
        response = self.get(url=AdminTaxCodesApiUrl.ADMIN_TAX_CODES + f'/{id}', response_obj=TaxCodesDetailsResponseDTO())
        return response

    def create_tax_codes(self, request_data: TaxCodesDetailsRequestDTO) -> TaxCodesCreationDetailsResponseDTO:
        response = self.post(url=AdminTaxCodesApiUrl.ADMIN_TAX_CODES, request_obj=request_data,
                             response_obj=TaxCodesCreationDetailsResponseDTO())
        return response

    def update_tax_codes(self, id:str, request_data: TaxCodesDetailsRequestDTO) -> TaxCodesCreationDetailsResponseDTO:
        response = self.put(url=AdminTaxCodesApiUrl.ADMIN_TAX_CODES + f'/{id}', request_obj=request_data,
                             response_obj=TaxCodesCreationDetailsResponseDTO())
        return response

    def delete_tax_code(self, id: str) -> dict:
        response = self.delete_request(url=AdminTaxCodesApiUrl.ADMIN_TAX_CODES + f'/{id}', response_obj={})
        return response