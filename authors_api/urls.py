from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Authors Haven Api",
        default_version="v1",
        description="API endpoints for Authors Haven API",
        contact=openapi.Contact(email="mike@codnity.com"),
        license=openapi.License(name="MIT License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/v1/accounts/', include('allauth.urls')),
    path("redoc/",schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
    path('api/v1/api-auth/', include('rest_framework.urls')),
	path("api/v1/setup/", include("setup.urls")),
	path("api/v1/products/", include('product.urls')),
	path("api/v1/contacts/", include('contacts.urls')),
	path("api/v1/users/", include("users.urls")),
    path("api/v1/filters/",include("filters.urls")),
    path("api/v1/categories/",include("category.urls")),
]

admin.site.site_header = "Authors Haven Api Admin"

admin.site.site_title = "Authores Haven Api Admin Portal"

admin.site.index_title = "Welcome to Authores Haven Api"