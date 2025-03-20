from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.common_dto import CountResponseDTO, CommonMessageDTO
from webcommander.webcommander.common.dto.product_dto import ProductListResponseDTO, ProductResponseDTO, \
    ProductSettingsDataDTO, ProductVariationResponseDTO, ProductDataDTO, ProductCreateDataDTO, \
    ProductInventoryCreateDTO, ProductImageAndVideoRequestDTO, ProductImageAndVideoResponseDTO, ProductReviewCreateDTO
from webcommander.webcommander.product.admin.admin_product_api_url import AdminProductApiUrl


class AdminProduct(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> ProductListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminProductApiUrl.PRODUCT, params=params, response_obj=ProductListResponseDTO())
        return response

    def info(self, id: str = None) -> ProductResponseDTO:
        response = self.get(url=AdminProductApiUrl.PRODUCT_INFO.format(product_id=id),
                            response_obj=ProductResponseDTO())
        return response

    def count(self) -> CountResponseDTO:
        response = self.get(url=AdminProductApiUrl.PRODUCT_COUNT, response_obj=CountResponseDTO())
        return response

    def product_variations(self, id: str = None) -> ProductVariationResponseDTO:
        response = self.get(url=AdminProductApiUrl.PRODUCT_VARIATION.format(product_id=id),
                            response_obj=ProductVariationResponseDTO())
        return response

    def create(self, request_data: ProductCreateDataDTO) -> ProductResponseDTO:
        response = self.post(url=AdminProductApiUrl.PRODUCT, request_obj=request_data, response_obj=ProductResponseDTO())
        return response

    def delete(self, id: str):
        response = self.delete_request(url=AdminProductApiUrl.PRODUCT_DELETE.format(product_id=id))
        return response

    def adjust_inventory(self, id: str, request_data: ProductInventoryCreateDTO) -> CommonMessageDTO:
        response = self.post(url=AdminProductApiUrl.PRODUCT_INVENTORIES.format(product_id=id), request_obj=request_data,
                             response_obj=CommonMessageDTO())
        return response

    def create_image(self, id: str, request_data: ProductImageAndVideoRequestDTO) -> ProductImageAndVideoResponseDTO:
        response = self.post(url=AdminProductApiUrl.PRODUCT_IMAGES.format(product_id=id), request_obj=request_data,
                             response_obj=ProductImageAndVideoResponseDTO())
        return response

    def image_delete(self, id: str, image_id: str):
        response = self.delete_request(url=AdminProductApiUrl.PRODUCT_IMAGE_DELETE.format(product_id=id,
                                                                                          image_id=image_id))
        return response

    def add_review(self, id: str, request_data: ProductReviewCreateDTO) -> ProductReviewCreateDTO:
        response = self.post(url=AdminProductApiUrl.PRODUCT_ADD_REVIEWS.format(product_id=id), request_obj=request_data,
                             response_obj=ProductReviewCreateDTO())
        return response

    def update(self, id: str, request_data: ProductCreateDataDTO) -> ProductResponseDTO:
        response = self.put(url=AdminProductApiUrl.PRODUCT_INFO.format(product_id=id), request_obj=request_data,
                            response_obj=ProductResponseDTO())
        return response

