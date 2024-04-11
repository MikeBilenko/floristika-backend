from .views import (
    GeneratePDFAPIView,
    OrderListAPIView,
    CartAPIView,
    OrderAPIView,
    OrderGuestAPIView
)
from django.urls import path

urlpatterns = [
    path("cart/", CartAPIView.as_view(), name="cart"),
    path('generate-pdf/', GeneratePDFAPIView.as_view(), name='generate_pdf'),
    path('orders/', OrderListAPIView.as_view(), name='orders'),
    path('order/', OrderAPIView.as_view(), name='crud_order_api_view'),
    path('order/<int:pk>/', OrderAPIView.as_view(), name='crud_order_api_view'),
    path('order/guest/', OrderGuestAPIView.as_view(), name='crud_order_guest_api_view'),
    path('order/guest/<str:number>/', OrderGuestAPIView.as_view(), name='order_success_api_view'),
]