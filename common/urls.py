from .views import AuthPercentAPIView
from django.urls import path

urlpatterns = [
    path("auth-percent/", AuthPercentAPIView.as_view(), name="auth_percent_api_view"),
]