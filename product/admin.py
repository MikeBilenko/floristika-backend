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
    ProductCareInstruction,
    ProductImage,
)

class ImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image_preview', 'image', 'alt']

    def image_preview(self, obj):
        if obj.pk:  # Check if the object exists (i.e., it's not a new unsaved instance)
            return obj.productimage.image_preview()
        return ""
    image_preview.short_description = 'Preview'


class ProductAdmin(TranslationAdmin, admin.ModelAdmin):
    readonly_fields = ['sold', 'rate']
    inlines = [ImageInline, ]


class ProductDescriptionAdmin(TranslationAdmin):
    pass


class ProductDescriptionItemAdmin(TranslationAdmin):
    pass


admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDescription, ProductDescriptionAdmin)
admin.site.register(ProductDeliveryItem)
admin.site.register(ProductDescriptionItem, ProductDescriptionItemAdmin)
admin.site.register(ProductDelivery)
admin.site.register(ProductCareInstruction)
