from django.db import models
from image.models import Image
from django.contrib.auth import get_user_model


User = get_user_model()


class Discount(models.Model):
    """Combined Discount model."""

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField(default=0.00)
    image = models.ForeignKey(Image, on_delete=models.DO_NOTHING, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    works_from = models.DateTimeField(blank=False, null=True)
    works_to = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    intro = models.BooleanField(default=False)

    def __str__(self):
        return self.name
