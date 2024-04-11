from django.urls import path
from .views import StoresListAPIView

urlpatterns = [
    path("", StoresListAPIView.as_view(), name="stores_list_api_view"),
]
