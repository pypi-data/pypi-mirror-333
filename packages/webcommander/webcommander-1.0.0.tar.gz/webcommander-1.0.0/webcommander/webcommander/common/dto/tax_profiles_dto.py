from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class TaxProfileDTO(WCBaseDTO):
    id: int = None
    name: str = None
    description: str = None
    default: str = None
    createdAt: str = None
    updatedAt: str = None


@dataclass(kw_only=True)
class TaxProfileListResponseDTO(WCBaseDTO):
    taxProfiles: list[TaxProfileDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class TaxProfileDetailsResponseDTO(WCBaseDTO):
    taxProfile: TaxProfileDTO = None


@dataclass(kw_only=True)
class TaxProfileRequestDTO(WCBaseDTO):
    taxProfile: TaxProfileDTO = None

