from rest_framework import serializers
from django.db.models import Q
from .models import (
    Product,
    ProductDescription,
    ProductDescriptionItem,
    ProductDeliveryItem,
    ProductCareInstruction,
    ProductDelivery,
    ProductImage
)
from image.serializers import ImageURLField
from text.serializers import TextSerializer
from filters.serializers import ColorSerializer, SizeSerializer
from category.serializers import CategorySerializer, SubCategorySerializer
from reviews.models import Review


class ProductImageSerializer(serializers.ModelSerializer):
    image = ImageURLField()
    class Meta:
        fields = "__all__"
        model = ProductImage


class ProductDescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDescriptionItem
        fields = "__all__"


class ProductDescriptionSerializer(serializers.ModelSerializer):
    list = ProductDescriptionItemSerializer(many=True)

    class Meta:
        model = ProductDescription
        fields = "__all__"


class ProductCareInstructionSerializer(serializers.ModelSerializer):
    text = TextSerializer(many=True)

    class Meta:
        model = ProductCareInstruction
        fields = "__all__"


class ProductDeliveryItemSerializer(serializers.ModelSerializer):
    text = TextSerializer(many=True)

    class Meta:
        model = ProductDeliveryItem
        fields = "__all__"


class ProductDeliverySerializer(serializers.ModelSerializer):
    inside_delivery = ProductDeliveryItemSerializer(many=True)
    internal_delivery = ProductDeliveryItemSerializer(many=True)
    returns = ProductDeliveryItemSerializer(many=True)

    class Meta:
        model = ProductDelivery
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    color = ColorSerializer(many=False)
    size = SizeSerializer(many=False)
    category = CategorySerializer(many=False)
    subcategory = SubCategorySerializer(many=False)

    class Meta:
        model = Product
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    description = ProductDescriptionSerializer(many=False)
    care = ProductCareInstructionSerializer(many=False)
    delivery = ProductDeliverySerializer(many=False)
    color = ColorSerializer(many=False)
    size = SizeSerializer(many=False)
    category = CategorySerializer(many=False)
    subcategory = SubCategorySerializer(many=False)
    reviews = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_reviews(self,obj):
        reviews = len(Review.objects.filter(product=obj))
        return reviews

    def get_related_products(self, obj):
        related_products = Product.objects.filter(
            Q(category=obj.category) & Q(subcategory=obj.subcategory)
        ).exclude(pk=obj.pk)[:4]

        serializer = ProductSerializer(related_products, many=True)
        return serializer.data
