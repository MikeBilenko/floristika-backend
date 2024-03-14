from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from product.models import Product


User = get_user_model()


class Review(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    rate = models.FloatField(default=0.00, validators=[
        MaxValueValidator(5.00),
        MinValueValidator(0.00)
    ])
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.product.name
