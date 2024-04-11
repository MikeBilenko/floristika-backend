from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .serializers import StoreSerializer
from .models import Store


class StoresListAPIView(ListAPIView):
    """Get all stores."""
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    model = Store
    permission_classes = [AllowAny]
