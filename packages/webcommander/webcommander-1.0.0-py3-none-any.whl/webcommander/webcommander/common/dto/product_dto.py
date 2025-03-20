from dataclasses import dataclass
from typing import List
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import CommonStructureDTO, PaginationDTO


@dataclass(kw_only=True)
class ProductPropertiesDTO(WCBaseDTO):
    featuredProduct: bool = None
    featuredProductLabel: str = None
    newProduct: bool = None
    soldOut: bool = None
    soldOutLabel: str = None
    model: str = None
    length: int = None
    width: int = None
    height: int = None
    weight: int = None


@dataclass(kw_only=True)
class VideoMetadataDTO(WCBaseDTO):
    title: str = None
    description: str = None


@dataclass(kw_only=True)
class VideoFileDTO(WCBaseDTO):
    video: str = None
    metadata: VideoMetadataDTO = None


@dataclass(kw_only=True)
class CanonicalURLsDTO(WCBaseDTO):
    enabled: bool = None
    canonicalUrls: List[str] = None


@dataclass(kw_only=True)
class SEOCustomCodeDTO(WCBaseDTO):
    header: dict = None
    footer: dict = None


@dataclass(kw_only=True)
class ThirdPartyAnalyticsDTO(WCBaseDTO):
    enableGoogleAnalytics4: bool = None
    analytics4: str = None
    conversionId: str = None
    conversionLabel: str = None
    debugMode: bool = None
    trackEvent: dict = None


@dataclass(kw_only=True)
class SEOAnalyticsDTO(WCBaseDTO):
    enableThirdPartyAnalytics: bool = None
    platform: str = None
    thirdPartyAnalytics: ThirdPartyAnalyticsDTO = None


@dataclass(kw_only=True)
class TagDTO(WCBaseDTO):
    name: str = None
    values: List[str] = None
    displayInProductPage: bool = None
    enableExpandedView: bool = None


@dataclass(kw_only=True)
class CustomPropertyDTO(WCBaseDTO):
    label: str = None
    description: str = None


@dataclass(kw_only=True)
class AdvanceInformationDataDTO(WCBaseDTO):
    globalTradeItemNumber: str = None
    productCondition: str = None
    loyalityPoints: str = None
    loyaltyPoints: str = None


@dataclass(kw_only=True)
class SelectedCustomersDataDTO(WCBaseDTO):
    customers: list[CommonStructureDTO] = None
    groups: list[CommonStructureDTO] = None


@dataclass(kw_only=True)
class SelectedCustomersCreationTO(WCBaseDTO):
    customers: List[int] = None
    groups: List[str] = None


@dataclass(kw_only=True)
class MetaTagDataDTO(WCBaseDTO):
    name: str = None
    value: str = None
    id: int = None

@dataclass(kw_only=True)
class ProductCustomInformationDataDTO(WCBaseDTO):
    shipping: str = None
    fabric: str = None


@dataclass(kw_only=True)
class ProductAdvancedDataDTO(WCBaseDTO):
    advanceInformation: AdvanceInformationDataDTO = None
    webtoolDisableTracking: bool = None
    metaTags: list[MetaTagDataDTO] = None
    customInformation: ProductCustomInformationDataDTO = None


@dataclass(kw_only=True)
class ProductSettingsDataDTO(WCBaseDTO):
    labelForCallForPrice: str = None
    labelForExpectToPay: str = None
    labelForBasePrice: str = None
    addToCart: str = None
    variationOptionView: str = None


@dataclass(kw_only=True)
class SeoMetaTagDTO(WCBaseDTO):
    enabled: bool = None
    metaTags: list[MetaTagDataDTO] = None


@dataclass(kw_only=True)
class SeoConfigDTO(WCBaseDTO):
    configKey: str = None
    metaTags: List[str] = None
    id: int = None
    type: str = None
    value: str = None
    version: str = None


@dataclass(kw_only=True)
class SeoConfigCreationDataDTO(WCBaseDTO):
    url: str = None
    overwriteSeoSettings: bool = None
    disableSearchEngineIndexing: bool = None
    seoTitle: str = None
    seoDescription: str = None
    canocialUrl: CanonicalURLsDTO = None
    metaTag: SeoMetaTagDTO = None


@dataclass(kw_only=True)
class RelatedOrSimilarProductDTO(WCBaseDTO):
    id: int = None
    name: str = None
    url: str = None


@dataclass(kw_only=True)
class ProductVariationPriceDTO(WCBaseDTO):
    label: str = None
    displayType: str = None


@dataclass(kw_only=True)
class MediaAssetDTO(WCBaseDTO):
    filename: str = None
    base64: str = None


@dataclass(kw_only=True)
class VideoAssetDTO(WCBaseDTO):
    video: str = None
    metadata: str = None


@dataclass(kw_only=True)
class ProductMediaCollectionDTO(WCBaseDTO):
    images: list[MediaAssetDTO] = None
    videos: list[VideoAssetDTO] = None
    spec: list[MediaAssetDTO] = None


@dataclass(kw_only=True)
class ProductMediaBundleDTO(WCBaseDTO):
    imageAndVideo: ProductMediaCollectionDTO = None


@dataclass(kw_only=True)
class MediaDataDTO(WCBaseDTO):
    id: int = None
    filename: str = None
    link: str = None


@dataclass(kw_only=True)
class ImageDataDTO(MediaDataDTO):
    thumbnail: str = None
    url: str = None


@dataclass(kw_only=True)
class VideoDataDTO(MediaDataDTO):
    thumbnail: str = None


@dataclass(kw_only=True)
class ReviewFileDTO(MediaDataDTO):
    thumbnail: str = None


@dataclass(kw_only=True)
class ReviewDTO(WCBaseDTO):
    id: int = None
    name: str = None
    email: str = None
    review: str = None
    file: list[ReviewFileDTO] = None
    rating: float = None


@dataclass(kw_only=True)
class ProductMediaDTO(WCBaseDTO):
    images: list[ImageDataDTO] = None
    videos: list[VideoDataDTO] = None
    specs: list[MediaDataDTO] = None


@dataclass(kw_only=True)
class ParentDataDTO(WCBaseDTO):
    id: str = None
    name: str = None
    isInTrash: str = None
    isParentInTrash: str = None
    isDisposable: str = None


@dataclass(kw_only=True)
class ProductLayoutDataDTO(WCBaseDTO):
    id: str = None
    name: str = None


@dataclass(kw_only=True)
class WeekdaysDataDTO(WCBaseDTO):
    day: str = None
    startHour: int = None
    startMinute: int = None
    endHour: int = None
    endMinute: int = None


@dataclass(kw_only=True)
class ProductAvailableWeekdaysDataDTO(WCBaseDTO):
    enabled: bool = None
    weekdays: list[WeekdaysDataDTO] = None


@dataclass(kw_only=True)
class BaseProfileDTO(WCBaseDTO):
    id: int = None
    name: str = None


@dataclass(kw_only=True)
class ShippingProfileDataDTO(BaseProfileDTO):
    pass


@dataclass(kw_only=True)
class TaxProfileDataDTO(BaseProfileDTO):
    pass


@dataclass(kw_only=True)
class ProductPricingAndStockDTO(WCBaseDTO):
    availableStock: int = None
    enableCallForPrice: bool = None
    enableMultipleOrder: bool = None
    expectedToPay: bool = None
    expectedToPayPrice: float = None
    hidePrice: bool = None
    lowLevelStock: int = None
    maximumOrderQuantity: int = None
    minimumOrderQuantity: int = None
    multipleOrderQuantity: int = None
    onSale: bool = None
    onSalePrice: float = None
    onSalePriceType: str = None
    restrictPriceFor: str = None
    restrictPriceForExceptCustomers: SelectedCustomersDataDTO = None
    restrictPurchaseFor: str = None
    restrictPurchaseForSelectedCustomers: SelectedCustomersDataDTO = None
    shippingProfile: ShippingProfileDataDTO = None
    taxProfile: str = None
    trackInventory: bool = None
    variationPrice: ProductVariationPriceDTO = None


@dataclass(kw_only=True)
class ProductCreatePricingAndStockDTO(WCBaseDTO):
    availableStock: int = None
    enableCallForPrice: bool = None
    enableMultipleOrder: bool = None
    enableLiteVariation: bool = None
    expectedToPay: bool = None
    expectedToPayPrice: float = None
    hidePrice: bool = None
    lowLevelStock: int = None
    maximumOrderQuantity: int = None
    minimumOrderQuantity: int = None
    multipleOrderQuantity: float = None
    onSale: bool = None
    onSalePrice: float = None
    onSalePriceType: str = None
    restrictPriceFor: str = None
    restrictPriceForSelectedCustomers: List[str] = None
    restrictPurchaseFor: str = None
    restrictPurchaseForSelectedCustomers: List[str] = None
    shippingProfile: ShippingProfileDataDTO = None
    taxProfile: str = None
    trackInventory: bool = None
    variationPrice: ProductVariationPriceDTO = None


@dataclass(kw_only=True)
class ProductDataDTO(WCBaseDTO):
    administrativeStatus: bool = None
    advanced: ProductAdvancedDataDTO = None
    available: str = None
    availableFor: str = None
    availableFromDate: str = None
    availableStock: int = None
    availableToDate: str = None
    availableOnDateRange: str = None
    availableOnWeekdays: ProductAvailableWeekdaysDataDTO = None
    basePrice: float = None
    costPrice: float = None
    createdBy: CommonStructureDTO = None
    createdAt: str = None
    customClass: str = None
    customProperties: str = None
    heading: str = None
    height: str = None
    id: str = None
    imageAndVideo: ProductMediaDTO = None
    isOnSale: bool = None
    length: str = None
    name: str = None
    parents: list[ParentDataDTO] = None
    password: str = None
    passwordProtected: str = None
    productPricingAndStock: ProductPricingAndStockDTO = None
    productLayout: CommonStructureDTO = None
    productSummary: str = None
    productDescription: str = None
    productPage: CommonStructureDTO = None
    productType: str = None
    productVariation: str = None
    restrictPriceFor: str = None
    restrictPurchaseFor: str = None
    restrictForSelectedCustomers: SelectedCustomersDataDTO = None
    relatedProducts: list[RelatedOrSimilarProductDTO] = None
    reviews: list[ReviewDTO] = None
    similarProducts: list[RelatedOrSimilarProductDTO] = None
    selectedCustomers: SelectedCustomersDataDTO = None
    salePrice: float = None
    seoConfigs: list[SeoConfigDTO] = None
    sku: str = None
    soldOut: bool = None
    soldOutLabel: str = None
    summary: str = None
    tags: List[str] = None
    url: str = None
    updatedAt: str = None
    videos: List[str] = None
    width: str = None
    weight: str = None


@dataclass(kw_only=True)
class ProductVariationUrlsDTO(WCBaseDTO):
    url: str = None
    productUrl: str = None


@dataclass(kw_only=True)
class VariationOptionDTO(WCBaseDTO):
    id: int = None
    label: str = None
    value: str = None
    default: bool = None


@dataclass(kw_only=True)
class VariationTypeDTO(WCBaseDTO):
    id: int = None
    name: str = None
    standard: str = None
    options: list[VariationOptionDTO] = None
    role: str = None
    isDisposable: bool = None


@dataclass(kw_only=True)
class CombinationVariationTypeDTO(WCBaseDTO):
    id: int = None
    name: str = None
    standard: str = None
    role: str = None
    isDisposable: bool = None


@dataclass(kw_only=True)
class CombinationOptionDTO(WCBaseDTO):
    id: int = None
    index: int = None
    type: list[CombinationVariationTypeDTO] = None
    label: str = None
    value: str = None
    colorHasSwatch: bool = None
    colorSwatchValue: str = None
    imageBaseUrl: str = None


@dataclass(kw_only=True)
class VariationPriceAndStockDTO(WCBaseDTO):
    trackInventory: bool = None
    availableStock: int = None
    lowLevelStock: int = None
    minimumOrderQuantity: int = None
    maximumOrderQuantity: int = None
    supportedMaxOrderQuantity: int = None
    enableMultipleOrder: bool = None
    multipleOrderQuantity: int = None
    onSale: bool = None
    soldOut: bool = None
    soldOutLabel: str = None
    onSalePriceType: str = None
    onSalePrice: float = None
    expectedToPay: bool = None
    expectedToPayPrice: float = None
    enableCallForPrice: bool = None
    hidePrice: bool = None


@dataclass(kw_only=True)
class VariationDetailsDTO(WCBaseDTO):
    variationId: int = None
    productName: str = None
    sku: str = None
    customSku: str = None
    urls: ProductVariationUrlsDTO = None
    url: str = None
    productUrl: str = None
    metaTags: List[str] = None
    isInventoryEnabled: bool = None
    availableStock: int = None
    lowStockLevel: int = None
    spec: str = None
    isMultipleOrderQuantity: bool = None
    isOnSale: bool = None
    isExpectToPay: bool = None
    isCallForPriceEnabled: bool = None
    isNew: bool = None
    onSaleAmountType: str = None
    title: str = None
    heading: str = None
    summary: str = None
    description: str = None
    model: str = None
    productCondition: str = None
    basePrice: float = None
    costPrice: float = None
    salePrice: float = None
    expectToPayPrice: float = None
    weight: float = None
    height: float = None
    length: float = None
    width: float = None
    displayPrice: float = None
    previousPrice: float = None
    minOrderQuantity: int = None
    maxOrderQuantity: int = None
    multipleOfOrderQuantity: int = None
    supportedMaxOrderQuantity: int = None
    images: list[ImageDataDTO] = None
    videos: list[VideoDataDTO] = None
    specs: list[MediaDataDTO] = None
    tax: float = None
    taxMessage: str = None
    priceAndStock: VariationPriceAndStockDTO = None


@dataclass(kw_only=True)
class AvailableCombinationDTO(WCBaseDTO):
    options: list[CombinationOptionDTO] = None
    details: VariationDetailsDTO = None


@dataclass(kw_only=True)
class ProductVariationDTO(WCBaseDTO):
    variationModel: str = None
    types: list[VariationTypeDTO] = None
    availableCombinations: list[AvailableCombinationDTO] = None


@dataclass(kw_only=True)
class ProductVariationDataDTO(WCBaseDTO):
    productId: int = None
    productVariation: ProductVariationDTO = None


@dataclass(kw_only=True)
class ProductVariationResponseDTO(WCBaseDTO):
    product: ProductVariationDataDTO = None


@dataclass(kw_only=True)
class ProductResponseDTO(WCBaseDTO):
    product: ProductDataDTO = None


@dataclass(kw_only=True)
class ProductListResponseDTO(WCBaseDTO):
    products: list[ProductDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class ParentDataDTO(WCBaseDTO):
    id: int = None


@dataclass(kw_only=True)
class ProductCreateDataDTO(WCBaseDTO):
    advanced: ProductAdvancedDataDTO = None
    availableFor: str = None
    availableFromDate: str = None
    availableOnDateRange: bool = None
    availableOnWeekdays: ProductAvailableWeekdaysDataDTO = None
    availableToDate: str = None
    available: bool = None
    basePrice: float = None
    costPrice: float = None
    createdBy: CommonStructureDTO = None
    customClass: List[str] = None
    customProperties: list[CustomPropertyDTO] = None
    heading: str = None
    imageAndVideo: ProductMediaCollectionDTO = None
    administrativeStatus: bool = None
    password: str = None
    name: str = None
    passwordProtected: bool = None
    parents: list[ParentDataDTO] = None
    productDescription: str = None
    productLayout: CommonStructureDTO = None
    productPage: CommonStructureDTO = None
    productPricingAndStock: ProductCreatePricingAndStockDTO = None
    productProperties: ProductPropertiesDTO = None
    productSummary: str = None
    productType: str = None
    relatedProducts: list[RelatedOrSimilarProductDTO] = None
    restrictForSelectedCustomers: bool = None
    selectedCustomers: SelectedCustomersCreationTO = None
    seoConfigs: SeoConfigCreationDataDTO = None
    similarProducts: list[RelatedOrSimilarProductDTO] = None
    sku: str = None
    tags: list[TagDTO] = None
    title: str = None



@dataclass(kw_only=True)
class ProductInventoryPricingAndStockDTO(WCBaseDTO):
    trackInventory: bool = None
    availableStock: str = None
    lowLevelStock: str = None
    minimumOrderQuantity: str = None
    maximumOrderQuantity: str = None


@dataclass(kw_only=True)
class ProductInventoryDTO(WCBaseDTO):
    productPricingAndStock: ProductInventoryPricingAndStockDTO = None


@dataclass(kw_only=True)
class ProductInventoryCreateDTO(WCBaseDTO):
    product: ProductInventoryDTO = None


@dataclass(kw_only=True)
class ProductImageAndVideoRequestDTO(WCBaseDTO):
    product: ProductMediaBundleDTO = None


@dataclass(kw_only=True)
class ProductImageAndVideoResponseDTO(WCBaseDTO):
    product: ProductMediaDTO = None


@dataclass(kw_only=True)
class ProductReviewDataDTO(WCBaseDTO):
    name: str = None
    email: str = None
    review: str = None
    file: list[MediaAssetDTO] = None
    rating: int = None


@dataclass(kw_only=True)
class ProductReviewDTO(WCBaseDTO):
    reviews: list[ProductReviewDataDTO] = None


@dataclass(kw_only=True)
class ProductReviewCreateDTO(WCBaseDTO):
    product: ProductReviewDTO = None
