from django.conf import settings
from rest_framework import serializers
from .models import Image


class ImageURLField(serializers.Field):
    def to_representation(self, obj):
        if obj:
            base_url = settings.BASE_URL_PATH + obj.url
            return base_url
        return None


class ImageSerializer(serializers.ModelSerializer):
    image = ImageURLField()
    class Meta:
        fields = "__all__"
        model = Image