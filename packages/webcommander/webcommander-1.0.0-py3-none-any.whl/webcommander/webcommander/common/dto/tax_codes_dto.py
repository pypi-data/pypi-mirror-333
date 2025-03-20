from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class TaxCodeDataDTO(WCBaseDTO):
    id: int = None
    name: str = None
    label: str = None
    method: str = None
    description: str = None
    rate: float = None
    resolverType: str = None
    priority: int = None
    isDefault: bool = None


@dataclass(kw_only=True)
class TaxCodesListResponseDTO(WCBaseDTO):
    taxCodes: list[TaxCodeDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class TaxCodesDetailsResponseDTO(WCBaseDTO):
    taxCode: TaxCodeDataDTO = None


@dataclass(kw_only=True)
class TaxCodesDetailsRequestDTO(WCBaseDTO):
    taxCode: TaxCodeDataDTO = None


@dataclass(kw_only=True)
class TaxCodesCreationDetailsResponseDTO(WCBaseDTO):
    taxZone: TaxCodeDataDTO = None
