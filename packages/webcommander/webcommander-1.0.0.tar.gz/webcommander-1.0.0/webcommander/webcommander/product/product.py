from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.common_dto import CountResponseDTO
from webcommander.webcommander.common.dto.product_dto import *
from webcommander.webcommander.product.product_api_url import ProductApiUrl


class Product(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> ProductListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=ProductApiUrl.PRODUCT_LIST, params=params, response_obj=ProductListResponseDTO())
        return response

    def info(self, id: str = None) -> ProductResponseDTO:
        response = self.get(url=ProductApiUrl.PRODUCT_INFO.format(product_id=id), response_obj=ProductResponseDTO())
        return response

    def count(self) -> CountResponseDTO:
        response = self.get(url=ProductApiUrl.PRODUCT_COUNT, response_obj=CountResponseDTO())
        return response

    def settings(self) -> ProductSettingsDataDTO:
        response = self.get(url=ProductApiUrl.PRODUCT_SETTINGS, response_obj=ProductSettingsDataDTO())
        return response
