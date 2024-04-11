from .models import (
    Color,
    Size
)
from modeltranslation.translator import translator, TranslationOptions


class ColorTranslationOptions(TranslationOptions):
    fields = ('name', )


class SizeTranslationOptions(TranslationOptions):
    fields = ('name', )


translator.register(Color, ColorTranslationOptions)
translator.register(Size, SizeTranslationOptions)