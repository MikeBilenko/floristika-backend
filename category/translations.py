from .models import (
    Category,
    SubCategory
)
from modeltranslation.translator import translator, TranslationOptions


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


translator.register(Category, CategoryTranslationOptions)
translator.register(SubCategory, SubCategoryTranslationOptions)
