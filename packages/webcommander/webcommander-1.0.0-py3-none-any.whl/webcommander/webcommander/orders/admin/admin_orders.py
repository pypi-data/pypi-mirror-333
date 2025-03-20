from webcommander.common.sdk_util import SDKUtil
from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.common_enum import SortDirection
from webcommander.webcommander.common.dto.orders_dto import *
from webcommander.webcommander.orders.admin.admin_orders_api_url import AdminOrdersApiUrl


class AdminOrders(WCRestProcessor):

    def list(self, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> OrdersListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminOrdersApiUrl.ADMIN_ORDERS, params=params, response_obj=OrdersListResponseDTO())
        return response

    def details(self, id: str ) -> OrdersDetailsResponseDTO:
        response = self.get(url=AdminOrdersApiUrl.ADMIN_ORDERS + f"/{id}", response_obj=OrdersDetailsResponseDTO())
        return response

    def customer_orders(self, id: str) -> CustomerOrdersDetailsResponseDTO:
        response = self.get(url=AdminOrdersApiUrl.ADMIN_CUSTOMERS_ORDERS.format(id=id), response_obj=CustomerOrdersDetailsResponseDTO())
        return response

    def orders_count(self) -> OrdersCountDetailsResponseDTO:
        response = self.get(url=AdminOrdersApiUrl.ADMIN_ORDERS_COUNT, response_obj=OrdersCountDetailsResponseDTO())
        return response

    def create_orders_invoice(self, order_id: str, request_data: OrderInvoiceRequestDTO) -> OrderInvoiceResponseDTO:
        response = self.post(url=AdminOrdersApiUrl.ADMIN_ORDERS_INVOICE.format(order_id=order_id), request_obj=request_data,
                             response_obj=OrderInvoiceResponseDTO())
        return response

    def create_orders_comment(self, order_id: str, request_data: OrderCommentsDetailsRequestDTO) -> OrderCommentsDetailsResponseDTO:
        response = self.post(url=AdminOrdersApiUrl.ADMIN_ORDERS_COMMENT.format(order_id=order_id), request_obj=request_data,
                             response_obj=OrderCommentsDetailsResponseDTO())
        return response

    def orders_comment_list(self, order_id:str, max: str = None, offset: int = None, direction: SortDirection = None,
             order_by: str = None) -> OrderCommentsListResponseDTO:
        params = SDKUtil.init_pagination_params(max=max, offset=offset, direction=direction, order_by=order_by)
        response = self.get(url=AdminOrdersApiUrl.ADMIN_ORDERS_COMMENT.format(order_id=order_id), params=params, response_obj=OrderCommentsListResponseDTO())
        return response

    def orders_shipment_status(self, order_id: str) -> OrderShipmentStatusResponseDTO:
        response = self.get(url=AdminOrdersApiUrl.ADMIN_ORDERS_SHIPMENT_STATUS.format(order_id=order_id), response_obj=OrderShipmentStatusResponseDTO())
        return response

    def orders_cancel(self, id: str ) -> OrdersDetailsResponseDTO:
        response = self.get(url=AdminOrdersApiUrl.ADMIN_ORDERS + f"/{id}", response_obj=OrdersDetailsResponseDTO())
        return response