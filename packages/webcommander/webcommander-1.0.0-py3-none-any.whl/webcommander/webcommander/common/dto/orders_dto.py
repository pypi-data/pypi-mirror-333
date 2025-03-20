from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import WCBaseDTO
from webcommander.webcommander.common.dto.common_dto import PaginationDTO

@dataclass(kw_only=True)
class CountryDTO(WCBaseDTO):
    id: int = None
    name: str = None
    code: str = None

@dataclass(kw_only=True)
class StateDTO(WCBaseDTO):
    id: int = None
    name: str = None
    code: str = None

@dataclass(kw_only=True)
class CustomerSummaryDTO(WCBaseDTO):
    firstName: str = None
    lastName: str = None
    customerGroup: str = None
    gender: str = None
    email: str = None
    addressLine1: str = None
    addressLine2: str = None
    city: str = None
    country: CountryDTO = None
    state: StateDTO = None
    postCode: str = None
    phone: str = None
    mobile: str = None
    fax: str = None
    companyName: str = None

@dataclass(kw_only=True)
class OrderLineDetailDTO(WCBaseDTO):
    itemId: int = None
    productName: str = None
    productId: int = None
    quantity: int = None
    price: float = None
    totalAmount: float = None
    tax: float = None
    discount: float = None
    taxDiscount: float = None
    isTaxable: bool = None
    isShippable: bool = None

@dataclass(kw_only=True)
class OrderDTO(WCBaseDTO):
    orderId: int = None
    orderStatus: str = None
    subTotal: float = None
    shippingCost: float = None
    shippingTax: float = None
    handlingCost: float = None
    totalSurcharge: float = None
    totalDiscount: float = None
    totalTax: float = None
    grandTotal: float = None
    paid: float = None
    due: float = None
    itemsTotal: int = None
    paymentStatus: str = None
    ipAddress: str = None
    customerSummary: CustomerSummaryDTO = None
    orderLineDetails: list[OrderLineDetailDTO] = None


@dataclass(kw_only=True)
class OrderInvoicePaymentSettingsDTO(WCBaseDTO):
    paymentMethodOptions: str = None


@dataclass(kw_only=True)
class OrderInvoiceRequestDTO(WCBaseDTO):
    orderId: str = None
    paymentSettings: OrderInvoicePaymentSettingsDTO = None
    paymentStatus: str = None
    notes: str = None


@dataclass(kw_only=True)
class OrderCommentDTO(WCBaseDTO):
    id: int = None
    content: str = None
    adminName: str = None
    isVisibleToCustomer: bool = None
    isAdmin: bool = None
    created: str = None


@dataclass(kw_only=True)
class OrderCommentsListResponseDTO(WCBaseDTO):
    comments: list[OrderCommentDTO] = None


@dataclass(kw_only=True)
class OrderCommentsDetailsResponseDTO(WCBaseDTO):
    comment: OrderCommentDTO = None


@dataclass(kw_only=True)
class OrderCommentsDetailsRequestDTO(WCBaseDTO):
    saveAndSend: str = None
    content: str = None


@dataclass(kw_only=True)
class OrderInvoiceResponseDTO(WCBaseDTO):
    status: str = None


@dataclass(kw_only=True)
class ShipmentStatusInfoDTO(WCBaseDTO):
    shippingProvider: str = None
    trackingNumber: str = None
    lastUpdated: str = None


@dataclass(kw_only=True)
class OrderShipmentStatusResponseDTO(WCBaseDTO):
    orderId: int = None
    shipmentStatus: str = None
    shipmentsInfo: list[ShipmentStatusInfoDTO] = None


@dataclass(kw_only=True)
class OrdersListResponseDTO(WCBaseDTO):
    orders: list[OrderDTO] = None
    pagination: PaginationDTO = None


@dataclass(kw_only=True)
class OrdersDetailsResponseDTO(WCBaseDTO):
    order: OrderDTO = None


@dataclass(kw_only=True)
class CustomerOrdersDetailsResponseDTO(WCBaseDTO):
    customerId: str = None
    orders: list[OrderDTO] = None


@dataclass(kw_only=True)
class OrdersCountDetailsResponseDTO(WCBaseDTO):
    count: str = None
