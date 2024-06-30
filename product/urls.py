from django.urls import path

from .views import (
    ProductListApiView,
    ProductDetailApiView,
    ProductReviewsApiView,
    ProductNewListApiView,
    ProductBestSellersListApiView,
    ProductVendorDetailApiView,
)

urlpatterns = [
    path("", ProductListApiView.as_view(), name="product_list_api_view"),
    path("new-in/", ProductNewListApiView.as_view(), name="product_new_in_list_api_view"),
    path("best-sellers/", ProductBestSellersListApiView.as_view(), name="product_best_sellers_list_api_view"),
    path("<slug:slug>/", ProductDetailApiView.as_view(), name="product_detail_api_view"),
    path("<slug:slug>/reviews/", ProductReviewsApiView.as_view(), name="product_reviews_api"),
    path("telegram/get/<str:vendor_code_public>/", ProductVendorDetailApiView.as_view(), name="product_detail_api_view"),
]