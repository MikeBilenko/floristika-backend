from django.db import models
from django.utils.html import mark_safe


class Image(models.Model):
    alt = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/%Y/%m/%d", null=False, blank=False)
    
    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="width: 100px; height: auto;" />')
        return ""
    image_preview.short_description = 'Preview'

    def __str__(self):
        return self.description or "Image"


    def __str__(self):
        return self.alt
