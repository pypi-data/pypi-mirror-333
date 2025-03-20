from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.categories.admin.admin_categories_api_url import AdminCategoriesApiUrl
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.categories_dto import *


class AdminCategories(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> CategoriesListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminCategoriesApiUrl.ADMIN_CATEGORIES, params=params, response_obj=CategoriesListResponseDTO())
        return response

    def details(self, id: str) -> CategoriesDetailsResponseDTO:
        response = self.get(url=AdminCategoriesApiUrl.ADMIN_CATEGORIES + f"/{id}", response_obj=CategoriesDetailsResponseDTO())
        return response

    def create_categories(self, request_data:CategoryDataDTO) -> CategoriesDetailsResponseDTO:
        response = self.post(url=AdminCategoriesApiUrl.ADMIN_CATEGORIES, request_obj=request_data, response_obj=CategoriesDetailsResponseDTO())
        return response

    def update_categories(self, id:str, request_data:CategoryDataDTO) -> CategoriesDetailsResponseDTO:
        response = self.put(url=AdminCategoriesApiUrl.ADMIN_CATEGORIES + f"/{id}", request_obj=request_data, response_obj=CategoriesDetailsResponseDTO())
        return response

    def delete_categories(self, id: str) -> dict:
        response = self.delete_request(url=AdminCategoriesApiUrl.ADMIN_CATEGORIES + f"/{id}", response_obj={})
        return response