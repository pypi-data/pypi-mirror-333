from dataclasses import dataclass
from typing import List

from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO


@dataclass(kw_only=True)
class CountryDTO(WCBaseDTO):
    id: int = None
    name: str = None
    code: str = None


@dataclass(kw_only=True)
class CustomerShippingRuleDTO(WCBaseDTO):
    id: int = None
    name: str = None
    description: str = None
    zoneList: List[int] = None
    shippingClass: str = None
    shippingPolicy: int = None


@dataclass(kw_only=True)
class CustomerShippingProfileDTO(WCBaseDTO):
    id: int = None
    name: str = None
    description: str = None
    created: str = None
    updated: str = None
    version: str = None
    rulePrecedence: str = None
    shippingRules: list[CustomerShippingRuleDTO] = None


@dataclass(kw_only=True)
class StateDTO(WCBaseDTO):
    id: int = None
    name: str = None
    code: str = None


@dataclass(kw_only=True)
class CustomerAddressDTO(WCBaseDTO):
    id: int = None
    type: str = None
    firstName: str = None
    lastName: str = None
    email: str = None
    companyName: str = None
    addressLine1: str = None
    addressLine2: str = None
    country: CountryDTO = None
    state: StateDTO = None
    city: str = None
    postCode: str = None
    mobile: str = None
    phone: str = None
    fax: str = None


@dataclass(kw_only=True)
class AddressCreateDataDTO(WCBaseDTO):
    type: str = None
    firstName: str = None
    lastName: str = None
    companyName: str = None
    email: str = None
    addressLine1: str = None
    addressLine2: str = None
    country: int = None
    state: int = None
    city: str = None
    postCode: str = None
    mobile: str = None
    phone: str = None
    fax: str = None
    addressName: str = None


@dataclass(kw_only=True)
class CustomerAddressCreateDTO(WCBaseDTO):
    addresses: list[AddressCreateDataDTO] = None


@dataclass(kw_only=True)
class CustomerAddressCreateRequestDTO(WCBaseDTO):
    customer: CustomerAddressCreateDTO = None


@dataclass(kw_only=True)
class CustomerDataDTO(WCBaseDTO):
    id: int = None
    displayId: int = None
    status: str = None
    firstName: str = None
    lastName: str = None
    email: str = None
    sex: str = None
    parent: int = None
    company: bool = None
    companyName: str = None
    timezone: str = None
    abn: str = None
    abnBranch: str = None
    shippingProfile: CustomerShippingProfileDTO = None
    transactionNumber: str = None
    referralCode: str = None
    usedReferralCode: str = None
    countReferralCodeUsed: int = None
    allowCreditLimit: bool = None
    storeCredit: float = None
    creditLimit: float = None
    howDoYouKnow: str = None
    customerPasswordExpired: bool = None
    hidePrice: bool = None
    defaultTaxCode: str = None
    source: str = None
    baseUrl: str = None
    backgroundImage: str = None
    profilePicture: str = None
    createdAt: str = None
    version: str = None
    addresses: list[CustomerAddressDTO] = None
    activeBillingAddress: int = None
    activeShippingAddress: int = None
    isInTrash: bool = None


@dataclass(kw_only=True)
class FieldsConfigDTO(WCBaseDTO):
    firstNameOrder: str = None
    firstNameKey: str = None
    firstNameLabel: str = None
    firstNameActive: bool = None
    firstNameRequired: bool = None

    lastNameOrder: str = None
    lastNameKey: str = None
    lastNameLabel: str = None
    lastNameActive: bool = None
    lastNameRequired: bool = None

    addressLine1Order: str = None
    addressLine1Key: str = None
    addressLine1Label: str = None
    addressLine1Active: bool = None
    addressLine1Required: bool = None

    addressLine2Order: str = None
    addressLine2Key: str = None
    addressLine2Label: str = None
    addressLine2Active: bool = None
    addressLine2Required: bool = None

    postCodeOrder: str = None
    postCodeKey: str = None
    postCodeLabel: str = None
    postCodeActive: bool = None
    postCodeRequired: bool = None

    cityOrder: str = None
    cityKey: str = None
    cityLabel: str = None
    cityActive: bool = None
    cityRequired: bool = None

    phoneOrder: str = None
    phoneKey: str = None
    phoneLabel: str = None
    phoneActive: bool = None
    phoneRequired: bool = None

    mobileOrder: str = None
    mobileKey: str = None
    mobileLabel: str = None
    mobileActive: bool = None
    mobileRequired: bool = None

    faxOrder: str = None
    faxKey: str = None
    faxLabel: str = None
    faxActive: bool = None
    faxRequired: bool = None

    emailOrder: str = None
    emailKey: str = None
    emailLabel: str = None
    emailActive: bool = None
    emailRequired: bool = None

    confirmEmailOrder: str = None
    confirmEmailKey: str = None
    confirmEmailLabel: str = None
    confirmEmailActive: bool = None
    confirmEmailRequired: bool = None

    passwordOrder: str = None
    passwordKey: str = None
    passwordLabel: str = None
    passwordActive: bool = None
    passwordRequired: bool = None

    retypePasswordOrder: str = None
    retypePasswordKey: str = None
    retypePasswordLabel: str = None
    retypePasswordActive: bool = None
    retypePasswordRequired: bool = None

    countryOrder: str = None
    countryKey: str = None
    countryLabel: str = None
    countryActive: bool = None
    countryRequired: bool = None

    customerTypeOrder: str = None
    customerTypeKey: str = None
    customerTypeLabel: str = None
    customerTypeActive: bool = None
    customerTypeRequired: bool = None

    sexOrder: str = None
    sexKey: str = None
    sexLabel: str = None
    sexActive: bool = None
    sexRequired: bool = None

    abnOrder: str = None
    abnKey: str = None
    abnLabel: str = None
    abnActive: bool = None
    abnRequired: bool = None

    abnBranchOrder: str = None
    abnBranchKey: str = None
    abnBranchLabel: str = None
    abnBranchActive: bool = None
    abnBranchRequired: bool = None

    companyNameOrder: str = None
    companyNameKey: str = None
    companyNameLabel: str = None
    companyNameActive: bool = None
    companyNameRequired: bool = None


@dataclass(kw_only=True)
class RegistrationFieldsDTO(WCBaseDTO):
    fields: list = None
    fieldsConfigs: FieldsConfigDTO = None


@dataclass(kw_only=True)
class CustomersListResponseDTO(WCBaseDTO):
    customers: list[CustomerDataDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class CustomersDetailsResponseDTO(WCBaseDTO):
    customer: CustomerDataDTO = None


@dataclass(kw_only=True)
class CustomerNewsletterDTO(WCBaseDTO):
    subscribed: bool = None


@dataclass(kw_only=True)
class CustomerCreateDataDTO(WCBaseDTO):
    firstName: str = None
    lastName: str = None
    shippingProfile: int = None
    gender: str = None
    email: str = None
    companyName: str = None
    addressLine: str = None
    country: int = None
    state: int = None
    postCode: str = None
    city: str = None
    mobile: str = None
    phone: str = None
    abn: str = None
    abnBranch: str = None
    newsletter: CustomerNewsletterDTO = None
    password: str = None


@dataclass(kw_only=True)
class CustomerCreateDTO(WCBaseDTO):
    customer: CustomerCreateDataDTO = None


@dataclass(kw_only=True)
class CustomerChangePasswordDataDTO(WCBaseDTO):
    email: str = None
    oldPassword: str = None
    password: str = None


@dataclass(kw_only=True)
class CustomerPasswordResetDTO(WCBaseDTO):
    email: str = None
    newPassword: str = None
    retypeNewPassword: str = None


@dataclass(kw_only=True)
class CustomerChangePasswordRequestDTO(WCBaseDTO):
    customer: CustomerChangePasswordDataDTO = None
