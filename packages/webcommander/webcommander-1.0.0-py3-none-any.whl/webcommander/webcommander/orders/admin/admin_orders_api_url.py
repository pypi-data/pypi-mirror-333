class AdminOrdersApiUrl:
    ADMIN_ORDERS = '/api/v4/admin/orders'
    ADMIN_CUSTOMERS_ORDERS = '/api/v4/admin/customers/{id}/orders'
    ADMIN_ORDERS_COUNT = '/api/v4/admin/orders/count'
    ADMIN_ORDERS_INVOICE = '/api/v4/admin/orders/{order_id}/send-invoice'
    ADMIN_ORDERS_COMMENT = '/api/v4/admin/orders/{order_id}/comments'
    ADMIN_ORDERS_SHIPMENT_STATUS = '/api/v4/admin/orders/{order_id}/shipment-status'
