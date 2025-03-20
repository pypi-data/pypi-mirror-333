from dataclasses import dataclass
from typing import List

from webcommander.sdlize.wc_base_dto import WCBaseDTO


@dataclass(kw_only=True)
class CountryDataDTO(WCBaseDTO):
    isDefault: bool = None
    code: str = None
    name: str = None
    id: int = None
    state: List[str] = None
    isActive: bool = None

@dataclass(kw_only=True)
class StateDataDTO(WCBaseDTO):
    country: int = None
    isDefault: bool = None
    code: str = None
    name: str = None
    id: int = None
    isActive: bool = None