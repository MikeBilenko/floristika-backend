from django.contrib import admin
from .models import (
    Order, 
    OrderItem, 
    Cart, 
    Guest, 
    Shipping, 
    Billing, 
    BankDetails,
)
from django import forms
from django.core.mail import EmailMessage
from django.conf import settings


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ["order"]
    

class OrderAdmin(admin.ModelAdmin):
    change_form_template = "admin/order/change_form.html"

    form = OrderAdminForm
    exclude = ("invoice",)
    inlines = [OrderItemInline,]
    readonly_fields = ('shipping_address', 'billing_address', 'store_name', "items")
    

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            email_body = (
                'Dear Customer,\n\n'
                f'Hey, the status of your order {obj.number}\n has been updated. Now it is {obj.get_status_display()}.\n\n'
                'Best regards,\n'
                'Floristika'
            )
            user = obj.user or obj.guest
            if user:
                email = EmailMessage(
                    subject=f"Order {obj.number} Status Update",
                    body=email_body,
                    to=[user.email, ],
                    from_email=settings.EMAIL_HOST_USER,
                )
                email.send()
        super().save_model(request, obj, form, change)

    def shipping_address(self, obj):
        if obj.shipping:
            return f"{obj.shipping.address}, {obj.shipping.city}, {obj.shipping.postal_code}, {obj.shipping.country}"
        return "N/A"

    shipping_address.short_description = 'Shipping Address'

    def billing_address(self, obj):
        if obj.billing:
            return f"{obj.billing.address}, {obj.billing.city}, {obj.billing.postal_code}, {obj.billing.country}"
        return "N/A"

    billing_address.short_description = 'Billing Address'

    def store_name(self, obj):
        if obj.store:
            return obj.store.name
        return "N/A"

    store_name.short_description = 'Store'

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('order_created', 'invoice_url')
        return super().get_readonly_fields(request, obj)


class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ('iban', 'swift', 'bank_name', 'legal_address', 'legal_city', 'legal_country', 'legal_postal_code')
    list_display_links = ('iban', 'swift', 'bank_name', 'legal_address', 'legal_city', 'legal_country', 'legal_postal_code')

    def save_model(self, request, obj, form, change):
        bank_iban = form.cleaned_data.get('iban')
        bank_swift = form.cleaned_data.get('swift')
        bank_name = form.cleaned_data.get('bank_name')
        legal_address = form.cleaned_data.get('legal_address')
        legal_city = form.cleaned_data.get('legal_city')
        legal_country = form.cleaned_data.get('legal_country')
        legal_postal_code = form.cleaned_data.get('legal_postal_code')

        BankDetails.objects.all().delete()

        BankDetails.objects.create(
            iban=bank_iban,
            swift=bank_swift,
            bank_name=bank_name,
            legal_address=legal_address,
            legal_city=legal_city,
            legal_country=legal_country,
            legal_postal_code=legal_postal_code,
        )


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "price", "price_for_authenticated", "sale")
    

# class OrderOrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'orderitem']

# admin.site.register(OrderOrderItem, OrderOrderItemAdmin)



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Cart)
admin.site.register(Guest)
admin.site.register(Shipping)
admin.site.register(Billing)
admin.site.register(BankDetails, BankDetailsAdmin)
