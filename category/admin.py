from django.contrib import admin
from .models import Category, SubCategory
from modeltranslation.admin import TranslationAdmin
from .translations import (
    CategoryTranslationOptions,
    SubCategoryTranslationOptions
)


class CategoryAdmin(TranslationAdmin):
    pass


class SubCategoryAdmin(TranslationAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
