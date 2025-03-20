from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class ShippingPolicyDTO(WCBaseDTO):
    id: int = None
    name: str = None


@dataclass(kw_only=True)
class ShippingRuleDTO(WCBaseDTO):
    id: int = None
    name: str = None
    shippingPolicy: ShippingPolicyDTO = None


@dataclass(kw_only=True)
class ShippingProfileDTO(WCBaseDTO):
    id: int = None
    name: str = None
    rulePreference: str = None
    shippingRules: list[ShippingRuleDTO] = None
    description: str = None
    createdAt: str = None
    updatedAt: str = None


@dataclass(kw_only=True)
class ProfileTypeDTO(WCBaseDTO):
    type: str = None
    select: str = None
    rule: str = None


@dataclass(kw_only=True)
class ShippingProfileRequestDataDTO(WCBaseDTO):
    id: int = None
    default: bool = None
    profileType: ProfileTypeDTO = None
    name: str = None
    rulePreference: str = None
    description: str = None


@dataclass(kw_only=True)
class ShippingProfilesListResponseDTO(WCBaseDTO):
    shippingProfiles: list[ShippingProfileDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class ShippingProfilesDetailsResponseDTO(WCBaseDTO):
    shippingProfile: ShippingProfileDTO = None


@dataclass(kw_only=True)
class ShippingProfilesRequestDTO(WCBaseDTO):
    shippingProfile: ShippingProfileRequestDataDTO = None

