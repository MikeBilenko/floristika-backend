from django.db import models
from autoslug import AutoSlugField
from colorfield.fields import ColorField


class Color(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    color = ColorField(default='#FFFFFF')

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name