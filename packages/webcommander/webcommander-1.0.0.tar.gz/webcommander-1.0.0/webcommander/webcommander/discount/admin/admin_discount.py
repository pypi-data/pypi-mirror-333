from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.discount_dto import DiscountsListDTO, DiscountInfoDTO
from webcommander.webcommander.discount.admin.admin_discount_api_url import AdminDiscountApiUrl


class AdminDiscount(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> DiscountsListDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminDiscountApiUrl.DISCOUNTS, params=params, response_obj=DiscountsListDTO())
        return response

    def info(self, id: str = None) -> DiscountInfoDTO:
        response = self.get(url=AdminDiscountApiUrl.DISCOUNT_DETAILS.format(id=id), response_obj=DiscountInfoDTO())
        return response

    def delete(self, id: str):
        response = self.delete_request(url=AdminDiscountApiUrl.DISCOUNT_DETAILS.format(id=id))
        return response
