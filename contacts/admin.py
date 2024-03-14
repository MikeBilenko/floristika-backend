from django.contrib import admin
from .models import Contact, ContactInfoText, ContactInfo


admin.site.register(Contact)
admin.site.register(ContactInfoText)
admin.site.register(ContactInfo)