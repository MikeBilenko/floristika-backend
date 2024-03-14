from django.urls import path

from .views import PricePercentView

urlpatterns = [
    path("price-percent/", PricePercentView.as_view(), name="price_percent_api_view"),
]
