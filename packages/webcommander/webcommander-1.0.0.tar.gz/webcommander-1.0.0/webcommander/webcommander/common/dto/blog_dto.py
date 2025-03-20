from dataclasses import dataclass

from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class BlogImageDTO(WCBaseDTO):
    title: str = None
    alternativeText: str = None
    fileName: str = None
    link: str = None


@dataclass(kw_only=True)
class BlogCategoryDTO(WCBaseDTO):
    id: int = None
    name: str = None
    isDisposible: bool = None
    isInTrash: bool = None


@dataclass(kw_only=True)
class BlogCreatorDTO(WCBaseDTO):
    id: int = None
    name: str = None


@dataclass(kw_only=True)
class BlogCustomerDTO(WCBaseDTO):
    id: int = None
    name: str = None


@dataclass(kw_only=True)
class BlogSelectedCustomersDTO(WCBaseDTO):
    customers: list[BlogCustomerDTO] = None
    groups: list[dict] = None


@dataclass(kw_only=True)
class BlogSEOConfigDTO(WCBaseDTO):
    id: int = None
    value: str = None
    type: str = None
    configKey: str = None


@dataclass(kw_only=True)
class BlogDataDTO(WCBaseDTO):
    id: int = None
    name: str = None
    url: str = None
    content: str = None
    date: str = None
    isPublished: bool = None
    visibility: str = None
    categories: list[BlogCategoryDTO] = None
    createdAt: str = None
    isDisposible: bool = None
    isInTrash: bool = None
    image: BlogImageDTO = None
    createdBy: BlogCreatorDTO = None
    selectedCustomers: BlogSelectedCustomersDTO = None
    seoConfigs: list[BlogSEOConfigDTO] = None


@dataclass(kw_only=True)
class BlogCommentDTO(WCBaseDTO):
    id: int = None
    status: str = None
    name: str = None
    email: str = None
    postTitle: str = None
    content: str = None
    spam: bool = None
    likes: int = None
    totalReply: int = None
    updatedAt: str = None
    replies: list[dict] = None


@dataclass(kw_only=True)
class BlogCategoryDataDTO(WCBaseDTO):
    id: int = None
    name: str = None
    url: str = None
    description: str = None
    isDisposible: bool = None
    isInTrash: bool = None
    createdAt: str = None
    updatedAt: str = None
    image: BlogImageDTO = None
    seoConfigs: list[BlogSEOConfigDTO] = None


@dataclass(kw_only=True)
class BlogInfoResponseDTO(WCBaseDTO):
    blog: BlogDataDTO = None


@dataclass(kw_only=True)
class BlogListDTO(WCBaseDTO):
    blogs: list[BlogDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class BlogCommentsListDTO(WCBaseDTO):
    comments: list[BlogCommentDTO] = None
    id: int = None


@dataclass(kw_only=True)
class BlogCommentInfoDTO(WCBaseDTO):
    comment: BlogCommentDTO = None
    id: int = None


@dataclass(kw_only=True)
class BlogCommentCreateDTO(WCBaseDTO):
    blog: BlogCommentInfoDTO = None


@dataclass(kw_only=True)
class BlogCategoriesListDTO(WCBaseDTO):
    blogs: list[BlogCategoryDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class BlogCategoriesInfoDTO(WCBaseDTO):
    category: BlogCategoryDataDTO = None
