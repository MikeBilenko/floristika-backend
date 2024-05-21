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

class ProductImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.pk:  # Check if the object exists (i.e., it's not a new unsaved instance)
            product_image = ProductImage.objects.get(pk=obj.productimage_id)
            return product_image.image_preview()
        return ""
    image_preview.short_description = 'Preview'


class ProductAdmin(TranslationAdmin, admin.ModelAdmin):
    readonly_fields = ['sold', 'rate']
    inlines = [ProductImageInline, ]


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
