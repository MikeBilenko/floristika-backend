from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Category, SubCategory
from .serializers import SubCategorySerializer, CategorySerializer


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    model = Category