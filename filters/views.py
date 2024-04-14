from rest_framework.generics import ListAPIView
from .serializers import ColorSerializer, SizeSerializer
from .models import Size, Color
from django.db.models import Min, Max
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Product
from category.models import Category


class ColorListApiView(ListAPIView):
    serializer_class = ColorSerializer
    model = Color
    queryset = Color.objects.all()
    permission_classes = [AllowAny]


class CategoryColorListApiView(APIView):
    serializer_class = ColorSerializer
    permission_classes = [AllowAny]

    def get(self, request, category):
        category_item = Category.objects.get(slug=category)
        products = Product.objects.filter(category=category_item)
        colors = Color.objects.filter(product__in=products).distinct()
        serializer = ColorSerializer(colors, many=True)
        return Response(serializer.data)


class CategorySizeListApiView(APIView):
    serializer_class = SizeSerializer
    permission_classes = [AllowAny]

    def get(self,request, category):
        category_item = Category.objects.get(slug=category)
        products = Product.objects.filter(category=category_item)
        sizes = Size.objects.filter(product__in=products).distinct()
        serializer = SizeSerializer(sizes, many=True)
        return Response(serializer.data)


class SizeListApiView(ListAPIView):
    serializer_class = SizeSerializer
    model = Size
    queryset = Size.objects.all()
    permission_classes = [AllowAny]


class PriceRangeView(APIView):
    """
    API view to retrieve the minimum and maximum prices of all products.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        price_range = Product.objects.aggregate(Min('price'), Max('price'))
        min_price = price_range['price__min']
        max_price = price_range['price__max']
        return Response({'min_price': min_price, 'max_price': max_price})