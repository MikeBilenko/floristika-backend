from rest_framework import serializers
from .models import PricePercent


class PricePercentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePercent
        fields = "__all__"