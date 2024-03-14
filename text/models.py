from django.db import models
from autoslug import AutoSlugField

class Text(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    text = models.TextField()

    def __str__(self):
        return self.slug