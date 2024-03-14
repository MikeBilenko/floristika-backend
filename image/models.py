from django.db import models
from django.core.validators import FileExtensionValidator


class Image(models.Model):
    alt = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/%Y/%m/%d", null=False, blank=False)

    def __str__(self):
        return self.alt
