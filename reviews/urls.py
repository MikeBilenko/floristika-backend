from .views import ReviewCreateApiView
from django.urls import path


urlpatterns = [
    path('create/', ReviewCreateApiView.as_view(), name='create'),
]