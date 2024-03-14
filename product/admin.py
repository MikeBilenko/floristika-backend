from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .translations import (
    ProductTranslationOptions,
    ProductDescriptionTranslationOptions,
    ProductDescriptionItemTranslationOptions,
)
from .models import (
    Product,
    ProductDescription,
    ProductDescriptionItem,
    ProductDeliveryItem,
    ProductDelivery,
    ProductCareInstruction
)


class ProductAdmin(TranslationAdmin):
    pass


class ProductDescriptionAdmin(TranslationAdmin):
    pass


class ProductDescriptionItemAdmin(TranslationAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDescription, ProductDescriptionAdmin)
admin.site.register(ProductDeliveryItem)
admin.site.register(ProductDescriptionItem, ProductDescriptionItemAdmin)
admin.site.register(ProductDelivery)
admin.site.register(ProductCareInstruction)
