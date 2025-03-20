from dataclasses import dataclass

from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class ProductDTO(WCBaseDTO):
    id: int = None
    name: str = None

@dataclass(kw_only=True)
class CreatedByDTO(WCBaseDTO):
    id: int = None
    name: str = None

@dataclass(kw_only=True)
class CategoryReferenceDTO(WCBaseDTO):
    id: int = None
    name: str = None
    isInTrash: bool = None
    isParentInTrash: bool = None
    isDisposable: bool = None

@dataclass(kw_only=True)
class LayoutDTO(WCBaseDTO):
    id: int = None
    name: str = None

@dataclass(kw_only=True)
class CategoryDTO(WCBaseDTO):
    id: int = None
    name: str = None
    sku: str = None
    title: str = None
    heading: str = None
    url: str = None
    available: bool = None
    visible: bool = None
    parentCategory: CategoryReferenceDTO = None
    layout: LayoutDTO = None
    productPage: LayoutDTO = None
    productLayout: LayoutDTO = None
    availableOnDateRange: bool = None
    availableFromDate: str = None
    availableToDate: str = None
    availableFor: str = None
    selectedCategories: list = None
    passwordProtected: bool = None
    password: str = None
    imageUrl: str = None
    backgroundImageUrl: str = None
    summary: str = None
    description: str = None
    products: list[ProductDTO] = None
    shippingProfile: dict = None
    taxProfile: dict = None
    disableTracking: bool = None
    seoConfigs: list = None
    transactionNo: str = None
    isDisposable: bool = None
    isInTrash: bool = None
    isParentInTrash: bool = None
    createdBy: CreatedByDTO = None
    createdOn: str = None
    updatedOn: str = None


@dataclass(kw_only=True)
class CategoriesListResponseDTO(WCBaseDTO):
    categories: list[CategoryDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class CategoriesDetailsResponseDTO(WCBaseDTO):
    category: CategoryDTO = None


@dataclass(kw_only=True)
class ParentCategoryDTO(WCBaseDTO):
    id: str = None
    name: str = None


@dataclass(kw_only=True)
class PageDTO(WCBaseDTO):
    id: str = None


@dataclass(kw_only=True)
class AvailabilityDTO(WCBaseDTO):
    onDateRange: bool = None
    fromDate: str = None
    toDate: str = None


@dataclass(kw_only=True)
class AvailabilityDetailsDTO(WCBaseDTO):
    availableFor: str = None
    selectedCustomers: list[int] = None
    restrictSelectedCustomers: bool = None


@dataclass(kw_only=True)
class ProtectionDetailsDTO(WCBaseDTO):
    codeProtected: bool = None
    codeToProtect: str = None


@dataclass(kw_only=True)
class ImagesDTO(WCBaseDTO):
    url: str = None
    baseUrl: str = None
    thumbUrl: str = None
    backgroundImage: str = None


@dataclass(kw_only=True)
class ProductDTO(WCBaseDTO):
    id: int = None


@dataclass(kw_only=True)
class CanonicalUrlDTO(WCBaseDTO):
    enable: bool = None
    url: list[str] = None


@dataclass(kw_only=True)
class SEOConfigurationsDTO(WCBaseDTO):
    url: str = None
    overwriteSeoSettings: bool = None
    seoTitle: str = None
    seoDescription: str = None
    searchEngineIndexing: bool = None
    canonicalUrl: CanonicalUrlDTO = None


@dataclass(kw_only=True)
class MetaInfoDTO(WCBaseDTO):
    tagName: str = None
    tagContent: str = None
    name: str = None
    value: str = None


@dataclass(kw_only=True)
class AdditionalMetaInfoDTO(WCBaseDTO):
    enable: bool = None
    metaInfo: list[MetaInfoDTO] = None


@dataclass(kw_only=True)
class TrackEventsDTO(WCBaseDTO):
    enable: bool = None
    events: dict = None


@dataclass(kw_only=True)
class ThirdPartyAnalyticsDTO(WCBaseDTO):
    enable: bool = None
    platform: str = None
    enableGoogleAnalytics: bool = None
    googleAnalysis: str = None
    googleAdsConversionId: str = None
    googleAdsConversionLabel: str = None
    debugMode: bool = None
    facebookPixelId: str = None
    trackEvent: TrackEventsDTO = None


@dataclass(kw_only=True)
class SEOCustomCodeDTO(WCBaseDTO):
    enable: bool = None
    customCodeInHeader: str = None
    customCodeInFooter: str = None


@dataclass(kw_only=True)
class AnalyticsDTO(WCBaseDTO):
    defaultProductListingConfigurations: bool = None
    thirdPartyAnalytics: ThirdPartyAnalyticsDTO = None
    seoCustomCode: SEOCustomCodeDTO = None
    customFieldsForOrder: list = None


@dataclass(kw_only=True)
class CategoryDataDTO(WCBaseDTO):
    name: str = None
    sku: str = None
    title: str = None
    heading: str = None
    available: bool = None
    categoryAvailable: bool = None
    parentCategory: ParentCategoryDTO = None
    productPage: PageDTO = None
    categoryLayout: PageDTO = None
    productLayout: PageDTO = None
    availability: AvailabilityDTO = None
    availabilityDetails: AvailabilityDetailsDTO = None
    protectionDetails: ProtectionDetailsDTO = None
    images: ImagesDTO = None
    summary: str = None
    description: str = None
    products: list[ProductDTO] = None
    taxProfile: str = None
    shippingProfile: str = None
    productSorting: str = None
    disableTracking: bool = None
    loyaltyPoints: int = None
    seoConfigurations: SEOConfigurationsDTO = None
    additionalMetaInfo: AdditionalMetaInfoDTO = None
    analytics: AnalyticsDTO = None

    url: str = None

