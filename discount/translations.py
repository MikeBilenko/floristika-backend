from .models import Discount
from modeltranslation.translator import translator, TranslationOptions


class DiscountTranslationOptions(TranslationOptions):
    fields = ('description',)


translator.register(Discount, DiscountTranslationOptions)
