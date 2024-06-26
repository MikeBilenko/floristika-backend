from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from supersecret.admin import manager_admin_site

schema_view = get_schema_view(
    openapi.Info(
        title="Floristika Api",
        default_version="v1",
        description="API endpoints for Floristika API",
        contact=openapi.Contact(email="mike@codnity.com"),
        license=openapi.License(name="MIT License")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/v1/accounts/', include('allauth.urls')),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
    path('manager-admin/', manager_admin_site.urls),
    path('api/v1/api-auth/', include('rest_framework.urls')),
    path("api/v1/setup/", include("setup.urls")),
    path("api/v1/products/", include('product.urls')),
    path("api/v1/contacts/", include('contacts.urls')),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/filters/", include("filters.urls")),
    path("api/v1/categories/", include("category.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/discounts/", include("discount.urls")),
    path("api/v1/orders/", include("orders.urls")),
    path("api/v1/search/", include("search.urls")),
    path("api/v1/stores/", include("store.urls")),
]

admin.site.site_header = "Floristika Admin"

admin.site.site_title = "Floristika Admin Portal"

admin.site.index_title = "Welcome to Floristika Admin Portal"
