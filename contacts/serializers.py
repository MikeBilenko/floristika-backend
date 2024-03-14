from rest_framework import serializers

from .models import Contact, ContactInfo, ContactInfoText

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Contact


class ContactInfoTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfoText
        fields = "__all__"


class ContactInfoSerializer(serializers.ModelSerializer):
    details = ContactInfoTextSerializer(many=True)
    working_hours = ContactInfoTextSerializer(many=True)
    address = ContactInfoTextSerializer(many=True)

    class Meta:
        model = ContactInfo
        fields = "__all__"