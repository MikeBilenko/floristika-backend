from rest_framework import serializers
from .models import (
    Order,
    Cart,
    OrderItem,
    Billing,
    Shipping,
    Guest,
)
from discount.serializers import DiscountSerializer
from users.serializers import CompanySerializer
from product.serializers import ProductSerializer


class GuestSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Guest


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        fields = "__all__"
        model = OrderItem


class BillingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Billing


class ShippingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = "__all__"
        model = Shipping


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    billing = BillingSerializer()
    shipping = ShippingSerializer()
    discount = DiscountSerializer()
    company = CompanySerializer()
    guest = GuestSerializer()

    class Meta:
        fields = "__all__"
        model = Order


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        fields = "__all__"
        model = Cart
