from dataclasses import dataclass
from typing import List
from webcommander.sdlize.wc_base_dto import WCBaseDTO


@dataclass(kw_only=True)
class DiscountDetailsDTO(WCBaseDTO):
    amountType: str = None
    singleAmountType: str = None
    tiers: List[int] = None
    minimumQty: int = None
    singleAmount: float = None
    capAmount: float = None
    type: str = None
    applyTo: str = None
    minimumQtyOn: str = None
    maximumTime: int = None
    zone: str = None
    minimumAmount: float = None
    minimumAmountOn: str = None
    id: int = None
    shippingClass: str = None


@dataclass(kw_only=True)
class DiscountCustomerCouponDTO(WCBaseDTO):
    code: str = None
    customerEmail: str = None


@dataclass(kw_only=True)
class DiscountDataDTO(WCBaseDTO):
    id: int = None
    name: str = None
    type: str = None
    isActive: bool = None
    isSpecifyEndDate: bool = None
    startFrom: str = None
    startTo: str = None
    detailsId: int = None
    details: DiscountDetailsDTO = None
    isCouponCodeAutoGenerate: bool = None
    isApplyCouponCode: bool = None
    isExcludeProductsOnSale: bool = None
    assoc: int = None
    customerCoupons: list[DiscountCustomerCouponDTO] = None
    coupon: int = None
    defaultCouponCode: str = None
    isMaximumUseTotal: bool = None
    isMaximumUseCustomer: bool = None
    isMaximumDiscountAllowed: bool = None
    maximumDiscountAllowedAmount: float = None
    maximumUseCount: int = None
    maximumUseCustomerCount: int = None
    discountDetailsType: str = None
    isDisplayDiscountInformationProdDetail: bool = None
    isCreateUniqueCouponEachCustomer: bool = None
    isDiscountUsedWithOtherDiscount: bool = None
    excludeProducts: List[int] = None
    displayTextCoupon: str = None
    displayTextPartialDiscountCondition: str = None
    displayTextCart: str = None
    isDisplayTextCoupon: bool = None
    isDisplayTextPartialDiscountCondition: bool = None
    isDisplayTextCart: bool = None
    isImportedCoupon: bool = None
    usage: List[int] = None


@dataclass(kw_only=True)
class DiscountsListDTO(WCBaseDTO):
    discounts: list[DiscountDataDTO] = None


@dataclass(kw_only=True)
class DiscountInfoDTO(WCBaseDTO):
    discount: DiscountDataDTO = None
