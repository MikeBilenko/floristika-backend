from django.db import models
from product.models import Product
from users.models import Company
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from discount.models import Discount
from store.models import Store

User = get_user_model()


class BankDetails(models.Model):
    iban = models.CharField(max_length=255)
    swift = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    legal_address = models.CharField(max_length=255)
    legal_city = models.CharField(max_length=255)
    legal_country = CountryField()
    legal_postal_code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.bank_name} - {self.iban}"


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} for {self.user.email}"


class Guest(models.Model):
    email = models.EmailField(unique=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = CountryField()
    zip_code = models.CharField(max_length=255)

    def __str__(self):
        return f"guest: {self.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True, blank=True)
    sale = models.FloatField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    price_for_authenticated = models.FloatField(null=True, blank=True)


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PROCESSING = 'processing', 'Processing'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'
    REFUNDED = 'refunded    ', 'Refunded'
    ON_HOLD = 'on-hold', 'On Hold'
    READY_FOR_PICKUP = 'ready-for-pickup', 'Ready for Pickup'
    COMPLETED = 'completed', 'Completed'


class Shipping(models.Model):
    address = models.CharField(verbose_name=_("Address"), max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name=_("City"), max_length=150, null=True, blank=True)
    postal_code = models.CharField(max_length=120, verbose_name=_("Postal Code"), null=True, blank=True)
    country = CountryField(null=True, blank=True)
    phone = models.CharField(verbose_name=_("Phone number"), max_length=15, null=True, blank=True)


class Billing(models.Model):
    address = models.CharField(verbose_name=_("Address"), max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name=_("City"), max_length=150, null=True, blank=True)
    postal_code = models.CharField(max_length=120, verbose_name=_("Postal Code"), null=True, blank=True)
    country = CountryField(null=True, blank=True)
    phone = models.CharField(verbose_name=_("Phone number"), max_length=15, null=True, blank=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True, blank=True)
    items = models.ManyToManyField(OrderItem, related_name="order_items")
    number = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    company_total_auth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, blank=True)
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        max_length=255
    )
    invoice = models.FileField(upload_to="invoices/", null=True, blank=True)
    invoice_url = models.URLField(null=True, blank=True)
    order_created = models.DateTimeField(default=None, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number


# class OrderOrderItem(models.Model):
#     order = models.ForeignKey(
#         Order, 
#         on_delete=models.CASCADE, 
#         null=True, 
#         blank=True,
#     )
#     orderitem = models.ForeignKey(
#         OrderItem, 
#         on_delete=models.CASCADE, 
#         null=True, 
#         blank=True,
#     )
