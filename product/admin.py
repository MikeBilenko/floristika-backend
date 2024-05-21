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


class ImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 1
    fields = ['image', ]  # Specify the fields to display

    def image_preview(self, obj):
        return obj.image.image_preview() if obj.image else ""


class ProductAdmin(TranslationAdmin, admin.ModelAdmin):
    readonly_fields = ['sold', 'rate']
    inlines = [ImageInline,]


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
