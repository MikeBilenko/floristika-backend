from .views import (
    OrderListAPIView,
    CartAPIView,
    OrderAPIView,
    OrderGuestAPIView,
    OrderInvoiceAPIView,
    OrderInvoiceSendAPIView,
)
from django.urls import path

urlpatterns = [
    path("cart/", CartAPIView.as_view(), name="cart"),
    path('orders/', OrderListAPIView.as_view(), name='orders'),
    path('order/', OrderAPIView.as_view(), name='crud_order_api_view'),
    path('order/<int:pk>/', OrderAPIView.as_view(), name='crud_order_api_view'),
    path('order/guest/', OrderGuestAPIView.as_view(), name='crud_order_guest_api_view'),
    path('order/guest/<str:number>/', OrderGuestAPIView.as_view(), name='order_success_api_view'),
    path("order/get-invoice/<int:pk>/",OrderInvoiceAPIView.as_view(),  name="order_get_invoice_api_view"),
    path("order/send-invoice/<int:pk>/",OrderInvoiceSendAPIView.as_view(), name="order_send_invoice_api_view"),
]