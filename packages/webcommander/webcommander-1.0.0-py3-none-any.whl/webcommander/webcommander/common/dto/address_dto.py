from dataclasses import dataclass
from typing import List
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.country_dto import CountryDataDTO, StateDataDTO


@dataclass(kw_only=True)
class AddressDataDTO(WCBaseDTO):
    lastName: str = None
    country: CountryDataDTO = None
    city: str = None
    companyName: str = None
    mobile: str = None
    version: int = None
    firstName: str = None
    phone: str = None
    addressLine1: str = None
    addressLine2: str = None
    postCode: str = None
    id: int = None
    state: StateDataDTO = None
    fax: str = None
    email: str = None


@dataclass(kw_only=True)
class SimpleAddressDataDTO(WCBaseDTO):
    lastName: str = None
    country: int = None
    version: str = None
    countryId: int = None
    city: str = None
    companyName: str = None
    mobile: str = None
    firstName: str = None
    phone: str = None
    addressLine1: str = None
    addressLine2: str = None
    postCode: str = None
    id: int = None
    state: str = None
    fax: str = None
    email: str = None


@dataclass(kw_only=True)
class BillingResponseDTO(WCBaseDTO):
    activeBilling: AddressDataDTO = None
    billings: List[AddressDataDTO] = None


@dataclass(kw_only=True)
class ShippingResponseDTO(WCBaseDTO):
    activeShipping: AddressDataDTO = None
    shippings: List[AddressDataDTO] = None