from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO


@dataclass(kw_only=True)
class CommonResponseDTO(WCBaseDTO):
    status: str = None
    message: str = None
    error: str = None


@dataclass(kw_only=True)
class CommonMessageDTO(WCBaseDTO):
    status: str = None
    message: str = None


@dataclass(kw_only=True)
class CommonStructureDTO(WCBaseDTO):
    id: str = None
    name: str = None


@dataclass(kw_only=True)
class PaginationDTO(WCBaseDTO):
    records: int = None
    limit: str = None
    offset: str = None
    nextPage: str = None
    previousPage: str = None


@dataclass(kw_only=True)
class CountResponseDTO(WCBaseDTO):
    count: str = None
