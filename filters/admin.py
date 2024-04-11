from django.contrib import admin
from .models import Color, Size
from modeltranslation.admin import TranslationAdmin
from .translations import (
    ColorTranslationOptions,
    SizeTranslationOptions
)


class ColorAdmin(TranslationAdmin):
    pass


class SizeAdmin(TranslationAdmin):
    pass


admin.site.register(Color, ColorAdmin)
admin.site.register(Size, SizeAdmin)