from django.db import models
from django_countries.fields import CountryField


class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = CountryField()
    postal_code = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} in {self.city}, {self.country} on {self.address}"
