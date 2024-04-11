from rest_framework.serializers import ModelSerializer
from .models import AuthPercent


class AuthPercentSerializer(ModelSerializer):

    class Meta:
        model = AuthPercent
        fields = ("percent", )