from django.contrib import admin
from .models import AuthPercent


class AuthPercentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        percent_value = form.cleaned_data.get('percent')

        # Delete all previous AuthPercent instances
        AuthPercent.objects.all().delete()

        # Create a new AuthPercent instance with the user-entered percent value
        AuthPercent.objects.create(percent=percent_value)


admin.site.register(AuthPercent, AuthPercentAdmin)