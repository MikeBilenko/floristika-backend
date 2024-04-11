from django.urls import path
from .views import CategoryListApiView, CategoryDetailApiView


urlpatterns = [
    path('', CategoryListApiView.as_view(), name="categories_list_api_view"),
    path('<slug:slug>/', CategoryDetailApiView.as_view(), name="category_detail_api_view"),
]