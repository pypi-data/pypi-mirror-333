from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.variation_dto import VariationsListDTO, VariationInfoDTO
from webcommander.webcommander.variation.admin.admin_variation_api_url import AdminVariationApiUrl


class AdminVariation(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> VariationsListDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminVariationApiUrl.VARIATIONS, params=params, response_obj=VariationsListDTO())
        return response

    def info(self, id: str = None) -> VariationInfoDTO:
        response = self.get(url=AdminVariationApiUrl.VARIATION_DETAILS.format(id=id),
                            response_obj=VariationInfoDTO())
        return response

    def create(self, request_data: VariationInfoDTO) -> VariationInfoDTO:
        response = self.post(url=AdminVariationApiUrl.VARIATIONS, request_obj=request_data,
                             response_obj=VariationInfoDTO())
        return response

    def delete(self, id: str):
        response = self.delete_request(url=AdminVariationApiUrl.VARIATION_DETAILS.format(id=id))
        return response

    def update(self, id: str, request_data: VariationInfoDTO) -> VariationInfoDTO:
        response = self.delete_request(url=AdminVariationApiUrl.VARIATION_DETAILS.format(id=id),
                                       request_obj=request_data, response_obj=VariationInfoDTO())
        return response
