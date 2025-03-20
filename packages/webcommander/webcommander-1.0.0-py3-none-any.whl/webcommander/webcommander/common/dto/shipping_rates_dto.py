from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class ShippingPolicyDTO(WCBaseDTO):
    id: int = None


@dataclass(kw_only=True)
class ShippingConditionDTO(WCBaseDTO):
    id: int = None
    fromAmount: float = None
    toAmount: float = None
    packetWeight: float = None
    handlingCost: float = None
    shippingCost: float = None
    shippingCostType: str = None
    handlingCostType: str = None
    apiType: str = None
    apiServiceType: str = None
    extraCover: str = None
    packingAlgorithm: str = None
    itemAttributes: str = None
    shippingPolicy: list[ShippingPolicyDTO] = None


@dataclass(kw_only=True)
class ShippingRateDTO(WCBaseDTO):
    id: int = None
    name: str = None
    policyType: str = None
    additionalAmount: float = None
    additionalCost: float = None
    isCumulative: bool = None
    includesTax: bool = None
    isAdditional: bool = None
    conditions: list[ShippingConditionDTO] = None
    createdAt: str = None
    updatedAt: str = None


@dataclass(kw_only=True)
class ShippingRatesListResponseDTO(WCBaseDTO):
    shippingRates: list[ShippingRateDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class ShippingRatesDetailsResponseDTO(WCBaseDTO):
    shippingRate: ShippingRateDTO = None


@dataclass(kw_only=True)
class ShippingRateRequestDTO(WCBaseDTO):
    shippingRate: ShippingRateDTO = None
