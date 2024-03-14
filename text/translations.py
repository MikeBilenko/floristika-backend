from .models import (
    Text
)
from modeltranslation.translator import translator, TranslationOptions


class TextTranslationOptions(TranslationOptions):
    fields = ('text', )


translator.register(Text, TextTranslationOptions)
