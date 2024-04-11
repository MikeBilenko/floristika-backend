from django.db import models
from autoslug import AutoSlugField
from image.models import Image


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    image = models.ForeignKey(Image,related_name="all", on_delete=models.SET_NULL, null=True, blank=True)
    image_best_sellers = models.ForeignKey(Image,related_name="best_sellers", on_delete=models.SET_NULL, null=True, blank=True)
    image_new_in = models.ForeignKey(Image,related_name="new_in", on_delete=models.SET_NULL, null=True, blank=True)
    image_sale = models.ForeignKey(Image,related_name="sale", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name