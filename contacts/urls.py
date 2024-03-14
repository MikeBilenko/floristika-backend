from django.urls import path

from .views import ContactCreateApiView, ContactInfoApiView

urlpatterns = [
    path("create/",ContactCreateApiView.as_view(), name="contact_create_api_view"),
    path("info/", ContactInfoApiView.as_view(), name="contact_info_api_view"),
]