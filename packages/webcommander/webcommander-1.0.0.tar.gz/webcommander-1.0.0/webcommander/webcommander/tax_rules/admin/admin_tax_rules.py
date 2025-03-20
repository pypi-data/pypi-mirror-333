from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.tax_rules_dto import *
from webcommander.webcommander.tax_rules.admin.admin_tax_rules_api_url import AdminTaxRulesApiUrl


class AdminTaxRules(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> TaxRulesListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminTaxRulesApiUrl.ADMIN_TAX_RULES, params=params, response_obj=TaxRulesListResponseDTO())
        return response

    def details(self, id: str) -> TaxRulesDetailsResponseDTO:
        response = self.get(url=AdminTaxRulesApiUrl.ADMIN_TAX_RULES + f'/{id}', response_obj=TaxRulesDetailsResponseDTO())
        return response

    def create_tax_rules(self, request_data: TaxRulesDetailsRequestDTO) -> TaxRulesDetailsResponseDTO:
        response = self.post(url=AdminTaxRulesApiUrl.ADMIN_TAX_RULES, request_obj=request_data,
                             response_obj=TaxRulesDetailsResponseDTO())
        return response

    def update_tax_rules(self, id: str, request_data: TaxRulesDetailsRequestDTO) -> TaxRulesDetailsResponseDTO:
        response = self.put(url=AdminTaxRulesApiUrl.ADMIN_TAX_RULES + f'/{id}', request_obj=request_data,
                             response_obj=TaxRulesDetailsResponseDTO())
        return response

    def tax_rules_delete(self, id: str) -> dict:
        response = self.delete_request(url=AdminTaxRulesApiUrl.ADMIN_TAX_RULES + f'/{id}', response_obj={})
        return response
