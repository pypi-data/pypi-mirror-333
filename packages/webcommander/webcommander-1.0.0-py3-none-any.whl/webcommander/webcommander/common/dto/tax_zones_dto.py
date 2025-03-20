from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class CountryDataDTO(WCBaseDTO):
    id: int = None
    name: str = None
    code: str = None


@dataclass(kw_only=True)
class TaxZoneDataDTO(WCBaseDTO):
    id: int = None
    name: str = None
    isSystemGenerated: bool = None

    default: bool = None
    useRadius: bool = None
    radius: float = None
    startLocation: str = None
    countries: list[CountryDataDTO] = None
    states: list = None
    postCode: list = None
    createdAt: str = None
    updatedAt: str = None


@dataclass(kw_only=True)
class TaxZonesListResponseDTO(WCBaseDTO):
    taxZones: list[TaxZoneDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class TaxZonesDetailsResponseDTO(WCBaseDTO):
    taxZone: TaxZoneDataDTO = None

@dataclass(kw_only=True)
class TaxZonesDetailsRequestDTO(WCBaseDTO):
    taxZone: TaxZoneDataDTO = None
