from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.blog.admin.admin_blog_api_url import AdminBlogApiUrl
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.blog_dto import BlogListDTO, BlogInfoResponseDTO, BlogCommentsListDTO, \
    BlogCommentInfoDTO, BlogCommentCreateDTO, BlogCategoriesListDTO, BlogCategoriesInfoDTO
from webcommander.webcommander.common.dto.common_dto import CountResponseDTO


class AdminBlog(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> BlogListDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminBlogApiUrl.BLOGS, params=params, response_obj=BlogListDTO())
        return response

    def info(self, id: str = None) -> BlogInfoResponseDTO:
        response = self.get(url=AdminBlogApiUrl.BLOG_DETAILS.format(id=id),
                            response_obj=BlogInfoResponseDTO())
        return response

    def count(self) -> CountResponseDTO:
        response = self.get(url=AdminBlogApiUrl.BLOG_COUNT, response_obj=CountResponseDTO())
        return response

    def delete(self, id: str):
        response = self.delete_request(url=AdminBlogApiUrl.BLOG_DETAILS.format(id=id))
        return response

    def comments_list(self, id: str = None) -> BlogCommentsListDTO:
        response = self.get(url=AdminBlogApiUrl.BLOG_COMMENTS.format(id=id), response_obj=BlogCommentsListDTO())
        return response

    def create_comment(self, id: str, request_data: BlogCommentCreateDTO) -> BlogCommentInfoDTO:
        response = self.post(url=AdminBlogApiUrl.BLOG_COMMENTS.format(id=id), request_obj=request_data,
                             response_obj=BlogCommentInfoDTO())
        return response

    def approve_comment(self, id: str, comment_id: str) -> BlogCommentInfoDTO:
        response = self.post(url=AdminBlogApiUrl.BLOG_COMMENT_APPROVE.format(id=id, comment_id=comment_id),
                             response_obj=BlogCommentInfoDTO())
        return response

    def spam_comment(self, id: str, comment_id: str) -> BlogCommentInfoDTO:
        response = self.post(url=AdminBlogApiUrl.BLOG_COMMENT_SPAM.format(id=id, comment_id=comment_id),
                             response_obj=BlogCommentInfoDTO())
        return response

    def categories_list(self) -> BlogCategoriesListDTO:
        response = self.get(url=AdminBlogApiUrl.BLOG_CATEGORIES, response_obj=BlogCategoriesListDTO())
        return response

    def category_info(self, id: str = None) -> BlogCategoriesInfoDTO:
        response = self.get(url=AdminBlogApiUrl.BLOG_CATEGORY_DETAILS.format(category_id=id),
                            response_obj=BlogCategoriesInfoDTO())
        return response

    def category_delete(self, id: str = None):
        response = self.delete_request(url=AdminBlogApiUrl.BLOG_CATEGORY_DETAILS.format(category_id=id))
        return response
