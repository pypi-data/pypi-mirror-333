from dataclasses import dataclass

from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class VariationOptionDTO(WCBaseDTO):
    id: int = None
    label: str = None
    value: str = None
    order: int = None
    default: bool = None


@dataclass(kw_only=True)
class VariationDataDTO(WCBaseDTO):
    id: int = None
    name: str = None
    standard: str = None
    isDisposable: bool = None
    options: list[VariationOptionDTO] = None


@dataclass(kw_only=True)
class VariationsListDTO(WCBaseDTO):
    variations: list[VariationDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class VariationInfoDTO(WCBaseDTO):
    variation: VariationDataDTO = None
