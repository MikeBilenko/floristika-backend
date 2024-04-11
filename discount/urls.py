from .views import IntroDiscountAPIView, DiscountAPIView
from django.urls import path


urlpatterns = [
    path("intro-discount/", IntroDiscountAPIView.as_view(), name="intro_discount"),
    path("check/", DiscountAPIView.as_view(), name="discount"),
]