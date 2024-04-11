from django.urls import path
from .views import (
    SizeListApiView,
    ColorListApiView,
    PriceRangeView,
    CategoryColorListApiView,
    CategorySizeListApiView
)

urlpatterns = [
    path(
        "color/list/",
        ColorListApiView.as_view(),
        name="color_list_api_view"
    ),
    path(
        "<slug:category>/color/list/",
         CategoryColorListApiView.as_view(),
         name="category_color_list_api_view"
    ),
    path(
        "<slug:category>/size/list/",
         CategorySizeListApiView.as_view(),
         name="category_sizes_list_api_view"
    ),
    path("size/list/", SizeListApiView.as_view(), name="size_list_api_view"),
    path("price-range/", PriceRangeView.as_view(), name="price_range_view"),
]
