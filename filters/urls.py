from django.urls import path
from .views import SizeListApiView, ColorListApiView


urlpatterns = [
    path("color/list/", ColorListApiView.as_view(), name="color_list_api_view"),\
    path("size/list/", SizeListApiView.as_view(), name="size_list_api_view")
]