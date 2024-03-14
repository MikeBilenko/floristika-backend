from django.contrib import admin
from .models import Text
from modeltranslation.admin import TranslationAdmin
from .translations import (
    TextTranslationOptions
)


class TextAdmin(TranslationAdmin):
    pass


admin.site.register(Text, TextAdmin)
