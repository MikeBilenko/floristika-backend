from rest_framework.generics import ListAPIView
from .models import Color, Size
from .serializers import ColorSerializer, SizeSerializer
from products.models import Product


class ColorListApiView(ListAPIView):
    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    model = Color


class SizeListApiView(ListAPIView):
    serializer_class = SizeSerializer
    model = Size
    queryset = Size.objects.all()