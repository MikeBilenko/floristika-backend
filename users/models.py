import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from product.models import Product


class AddressBook(models.Model):
    address = models.CharField(verbose_name=_("Address"), max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name=_("City"), max_length=150, null=True, blank=True)
    postal_code = models.CharField(max_length=120, verbose_name=_("Postal Code"), null=True, blank=True)
    country = CountryField(null=True, blank=True)
    phone = PhoneNumberField(verbose_name=_("Phone number"), max_length=15, null=True, blank=True)
    delivery = models.BooleanField(default=False)
    billing = models.BooleanField(default=False)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)
    email = models.EmailField(verbose_name=_("email address"), db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(verbose_name=_("Phone number"), max_length=15, null=True, blank=True)
    country = CountryField(null=True, blank=True)
    address = models.CharField(verbose_name=_("Address"), max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name=_("City"), max_length=150, null=True, blank=True)
    postal_code = models.CharField(max_length=120, verbose_name=_("Postal Code"), null=True, blank=True)
    address_book_phone = models.CharField(verbose_name=_("Address Phone number"), max_length=15, null=True, blank=True)
    address_books = models.ManyToManyField(AddressBook, null=True, blank=True)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.first_name

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return self.first_name


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    country = CountryField(null=True, blank=True)
    email = models.EmailField(verbose_name=_("email address"), db_index=True, unique=True)
    phone = PhoneNumberField(verbose_name=_("Phone number"), max_length=15, null=True, blank=True)
    city = models.CharField(verbose_name=_("City"), max_length=150, null=True, blank=True)
    company_name = models.CharField(verbose_name=_("Company Name"), max_length=150, null=True, blank=True)
    vat = models.CharField(verbose_name=_("VAT"), max_length=150, null=True, blank=True)
    address = models.CharField(verbose_name=_("Address"), max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=120, verbose_name=_("Postal Code"), null=True, blank=True)
    sale_percent = models.FloatField(default=0.00)

    def __str__(self):
        return self.company_name


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True, blank=False)

    def __str__(self):
        return f"{self.user.first_name}"
