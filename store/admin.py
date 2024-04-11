from django.contrib import admin
from .models import Store


class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "city", "country", "postal_code", "phone_number")
    search_fields = ("name", "address", "city", "country", "postal_code", "phone_number")
    list_filter = ("city", "country")
    list_display_links = ("name", "address", "city", "country", "postal_code", "phone_number")


admin.site.register(Store, StoreAdmin)
