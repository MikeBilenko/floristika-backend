from rest_framework.generics import ListAPIView
from .serializers import ColorSerializer, SizeSerializer
from .models import Size, Color
from rest_framework.permissions import AllowAny


class ColorListApiView(ListAPIView):
    serializer_class = ColorSerializer
    model = Color
    queryset = Color.objects.all()
    permission_classes = [AllowAny]


class SizeListApiView(ListAPIView):
    serializer_class = SizeSerializer
    model = Size
    queryset = Size.objects.all()
    permission_classes = [AllowAny]

