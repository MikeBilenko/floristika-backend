from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField()
    answered = models.BooleanField(default=False)
    created_at = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return self.email


class ContactInfoText(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class ContactInfo(models.Model):
    email = models.EmailField(max_length=150)
    phone = PhoneNumberField(max_length=15, null=True, blank=True)
    address = models.ManyToManyField(ContactInfoText, related_name="address")
    working_hours = models.ManyToManyField(ContactInfoText, related_name="working_hours")
    details = models.ManyToManyField(ContactInfoText, related_name="details")

    def __str__(self):
        return "Contact Info"

