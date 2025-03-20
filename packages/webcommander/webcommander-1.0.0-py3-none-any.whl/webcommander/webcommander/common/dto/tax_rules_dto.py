from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class TaxCodeDTO(WCBaseDTO):
    id: int = None
    name: str = None
    isDefault: bool = None


@dataclass(kw_only=True)
class TaxZoneDTO(WCBaseDTO):
    id: int = None
    name: str = None
    isSystemGenerated: bool = None
    isDefault: bool = None


@dataclass(kw_only=True)
class TaxRuleDTO(WCBaseDTO):
    id: int = None
    name: str = None
    code: TaxCodeDTO = None
    description: str = None
    default: bool = None
    roundingType: str = None
    decimalPoint: int = None
    zones: list[TaxZoneDTO] = None
    createdAt: str = None
    updatedAt: str = None
    taxProfileId: str = None


@dataclass(kw_only=True)
class TaxRulesListResponseDTO(WCBaseDTO):
    taxRules: list[TaxRuleDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class TaxRulesDetailsResponseDTO(WCBaseDTO):
    taxRule: TaxRuleDTO = None


@dataclass(kw_only=True)
class TaxRulesDetailsRequestDTO(WCBaseDTO):
    taxRule: TaxRuleDTO = None
