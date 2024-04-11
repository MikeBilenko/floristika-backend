from django.contrib import admin
from .models import Discount
from .translations import DiscountTranslationOptions
from modeltranslation.admin import TranslationAdmin


class DiscountAdmin(TranslationAdmin):
    pass


admin.site.register(Discount, DiscountAdmin)
