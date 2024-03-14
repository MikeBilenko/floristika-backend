from rest_framework.serializers import ModelSerializer
from .models import Color, Size


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"
