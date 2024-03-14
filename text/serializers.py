from rest_framework.serializers import ModelSerializer
from .models import Text


class TextSerializer(ModelSerializer):
    """Text model."""
    class Meta:
        fields = "__all__"
        model = Text
