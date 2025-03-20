from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO
from webcommander.webcommander.common.dto.country_dto import CountryDataDTO


@dataclass(kw_only=True)
class CurrencyCommonDataDTO(WCBaseDTO):
    active: bool = None
    code: str = None
    name: str = None
    precision: int = None
    rounding: str = None
    symbol: str = None


@dataclass(kw_only=True)
class CurrencyDataDTO(CurrencyCommonDataDTO):
    id: str = None
    country: CountryDataDTO = None
    updatedAt: str = None


@dataclass(kw_only=True)
class CurrencyCreateDataDTO(CurrencyCommonDataDTO):
    country: str = None
    countryCode: str = None


@dataclass(kw_only=True)
class CurrencyInfoResponseDTO(WCBaseDTO):
    currency: CurrencyDataDTO = None


@dataclass(kw_only=True)
class CurrencyListDTO(WCBaseDTO):
    currencies: list[CurrencyDataDTO] = None
    pagination: PaginationDTO = None
