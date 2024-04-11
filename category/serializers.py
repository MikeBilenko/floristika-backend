from rest_framework import serializers
from .models import Category, SubCategory
from image.serializers import ImageSerializer


class CategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=False)
    image_best_sellers = ImageSerializer(many=False)
    image_new_in = ImageSerializer(many=False)
    image_sale = ImageSerializer(many=False)

    class Meta:
        model = Category
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = SubCategory
        fields = "__all__"
