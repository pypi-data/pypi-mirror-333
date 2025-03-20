from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.tax_zones_dto import *
from webcommander.webcommander.tax_zones.admin.admin_tax_zones_api_url import AdminTaxZonesApiUrl


class AdminTaxZones(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> TaxZonesListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminTaxZonesApiUrl.ADMIN_TAX_ZONES, params=params, response_obj=TaxZonesListResponseDTO())
        return response

    def details(self, id: str) -> TaxZonesDetailsResponseDTO:
        response = self.get(url=AdminTaxZonesApiUrl.ADMIN_TAX_ZONES + f'/{id}', response_obj=TaxZonesDetailsResponseDTO())
        return response

    def create_tax_zones(self, request_data: TaxZonesDetailsRequestDTO) -> TaxZonesDetailsResponseDTO:
        response = self.post(url=AdminTaxZonesApiUrl.ADMIN_TAX_ZONES, request_obj=request_data,
                             response_obj=TaxZonesDetailsResponseDTO())
        return response

    def update_tax_zones(self, id: str, request_data: TaxZonesDetailsRequestDTO) -> TaxZonesDetailsResponseDTO:
        response = self.put(url=AdminTaxZonesApiUrl.ADMIN_TAX_ZONES + f'/{id}', request_obj=request_data,
                             response_obj=TaxZonesDetailsResponseDTO())
        return response

    def delete_tax_zones(self, id: str) -> dict:
        response = self.delete_request(url=AdminTaxZonesApiUrl.ADMIN_TAX_ZONES + f'/{id}', response_obj={})
        return response