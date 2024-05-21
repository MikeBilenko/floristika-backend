from django.db import models
from category.models import Category, SubCategory
from filters.models import Size, Color
from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator
from text.models import Text
from django.utils import timezone


class ProductDescriptionItem(models.Model):
    """Product description item."""
    text = models.TextField()

    def __str__(self):
        return self.text


class ProductDescription(models.Model):
    """Product description model."""
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    text = models.TextField()
    list = models.ManyToManyField(ProductDescriptionItem)
    additional_text = models.TextField(null=True, blank=True)


class ProductCareInstruction(models.Model):
    """Product care instruction model."""
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    text = models.ManyToManyField(Text)

    def __str__(self):
        return self.slug


class ProductDeliveryItem(models.Model):
    """Product item delivery for product."""
    name = models.CharField(max_length=200)
    text = models.ManyToManyField(Text, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductDelivery(models.Model):
    """Product delivery model that consists of items."""
    name = models.CharField(max_length=150)
    inside_delivery = models.ManyToManyField(ProductDeliveryItem, related_name="inside", null=True, blank=True)
    internal_delivery = models.ManyToManyField(ProductDeliveryItem, related_name="internal", null=True, blank=True)
    returns = models.ManyToManyField(ProductDeliveryItem, related_name="returns", null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Product image."""
    alt = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/%Y/%m/%d", null=False, blank=False)
    def __str__(self):
        return self.alt


class Product(models.Model):
    """Product model."""
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, default='')
    price = models.FloatField(default=0.00)
    price_for_authenticated = models.FloatField(default=0.00, null=True, blank=True)
    sale = models.FloatField(validators=[
        MaxValueValidator(100.00),
        MinValueValidator(0.00)
    ], null=True, blank=True)
    qty = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    images = models.ManyToManyField(
        ProductImage,
        null=True, 
        blank=True,
    )
    color = models.ForeignKey(Color,on_delete=models.DO_NOTHING, null=True, blank=True)
    size = models.ForeignKey(Size,on_delete=models.DO_NOTHING, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    rate = models.FloatField(default=0.00, validators=[
        MaxValueValidator(5.00),
        MinValueValidator(0.00)
    ])
    description = models.ForeignKey(ProductDescription, on_delete=models.DO_NOTHING,null=True, blank=True)
    care = models.ForeignKey(ProductCareInstruction, on_delete=models.DO_NOTHING,null=True, blank=True)
    delivery = models.ForeignKey(ProductDelivery, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    vendor_code = models.CharField(max_length=150)

    def __str__(self):
        return self.name
