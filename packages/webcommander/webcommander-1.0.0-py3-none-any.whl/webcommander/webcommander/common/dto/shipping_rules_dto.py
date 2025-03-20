from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class ShippingPolicyDTO(WCBaseDTO):
    id: int = None
    name: str = None


@dataclass(kw_only=True)
class ShippingZoneDTO(WCBaseDTO):
    id: int = None
    name: str = None


@dataclass(kw_only=True)
class ShippingRuleDTO(WCBaseDTO):
    id: int = None
    name: str = None
    shippingPolicy: ShippingPolicyDTO = None
    shippingClass: dict = None
    zones: list[ShippingZoneDTO] = None
    description: str = None
    createdAt: str = None
    updatedAt: str = None


@dataclass(kw_only=True)
class ShippingRuleTypeDTO(WCBaseDTO):
    create: bool = None
    useExisting: bool = None


@dataclass(kw_only=True)
class ShippingRuleOptionDTO(WCBaseDTO):
    type: str = None
    choices: list = None
    value: str = None


@dataclass(kw_only=True)
class ShippingRuleRequestDataDTO(WCBaseDTO):
    type: ShippingRuleTypeDTO = None
    apply: ShippingRuleOptionDTO = None
    rule: ShippingRuleOptionDTO = None
    name: str = None
    className: ShippingRuleOptionDTO = None
    description: str = None

    _custom_field_mapping = {
        "class": "className"
    }


@dataclass(kw_only=True)
class ShippingRuleUpdateRequestDataDTO(WCBaseDTO):
    type: str = None
    apply: str = None
    rule: str = None
    name: str = None
    className: str = None
    description: str = None


@dataclass(kw_only=True)
class ShippingRuleRequestDTO(WCBaseDTO):
    shippingRule: ShippingRuleRequestDataDTO = None

    _custom_field_mapping = {
        "class": "className"
    }


@dataclass(kw_only=True)
class ShippingRuleUpdateRequestDTO(WCBaseDTO):
    shippingRule: ShippingRuleUpdateRequestDataDTO = None

    _custom_field_mapping = {
        "class": "className"
    }


@dataclass(kw_only=True)
class ShippingRulesListResponseDTO(WCBaseDTO):
    shippingRules: list[ShippingRuleDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class ShippingRulesDetailsResponseDTO(WCBaseDTO):
    shippingRule: ShippingRuleDTO = None
