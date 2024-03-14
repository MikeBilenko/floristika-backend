from rest_framework.serializers import ModelSerializer
from .models import Review
from users.serializers import UserSerializer


class ReviewSerializer(ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Review
        fields = "__all__"
