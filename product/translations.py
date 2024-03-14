from .models import (
    Product,
    ProductDescription,
    ProductDescriptionItem,
)
from modeltranslation.translator import translator, TranslationOptions


class ProductTranslationOptions(TranslationOptions):
    fields = ('name', )


class ProductDescriptionItemTranslationOptions(TranslationOptions):
    fields = ('text', )


class ProductDescriptionTranslationOptions(TranslationOptions):
    fields = ('text','additional_text',)


translator.register(Product, ProductTranslationOptions)
translator.register(ProductDescription, ProductDescriptionTranslationOptions)
translator.register(ProductDescriptionItem, ProductDescriptionItemTranslationOptions)
