from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from product.translations import (
    ProductTranslationOptions,
    ProductDescriptionTranslationOptions,
    ProductDescriptionItemTranslationOptions,
)
from filters.translations import (
    ColorTranslationOptions,
    SizeTranslationOptions
)
from category.translations import (
    CategoryTranslationOptions,
    SubCategoryTranslationOptions
)
from text.translations import (
    TextTranslationOptions
)

from product.models import (
    Product,
    ProductDelivery,
    ProductDescription,
    ProductDeliveryItem,
    ProductCareInstruction,
    ProductDescriptionItem,
)
from image.models import Image
from filters.models import Size, Color
from category.models import Category, SubCategory
from text.models import Text


class TextAdmin(TranslationAdmin):
    pass


class CategoryAdmin(TranslationAdmin):
    pass


class SubCategoryAdmin(TranslationAdmin):
    pass


class ColorAdmin(TranslationAdmin):
    pass


class SizeAdmin(TranslationAdmin):
    pass


class ProductAdmin(TranslationAdmin):
    pass


class ProductDescriptionAdmin(TranslationAdmin):
    pass


class ProductDescriptionItemAdmin(TranslationAdmin):
    pass


class ManagerAdminSite(admin.AdminSite):
    site_header = 'Manager Admin'
    site_title = 'Manager Admin Panel'
    index_title = 'Welcome to the Manager Admin Panel'


manager_admin_site = ManagerAdminSite(name='manager_admin')

manager_admin_site.register(Product,ProductAdmin)
manager_admin_site.register(ProductDescription, ProductDescriptionAdmin)
manager_admin_site.register(ProductDeliveryItem)
manager_admin_site.register(ProductDescriptionItem, ProductDescriptionItemAdmin)
manager_admin_site.register(ProductDelivery)
manager_admin_site.register(ProductCareInstruction)
manager_admin_site.register(Image)
manager_admin_site.register(Color, ColorAdmin)
manager_admin_site.register(Size, SizeAdmin)
manager_admin_site.register(SubCategory, SubCategoryAdmin)
manager_admin_site.register(Category, CategoryAdmin)
manager_admin_site.register(Text, TextAdmin)
