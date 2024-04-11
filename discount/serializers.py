from rest_framework.serializers import ModelSerializer
from image.serializers import ImageSerializer
from .models import Discount


class DiscountSerializer(ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Discount
        fields = "__all__"
