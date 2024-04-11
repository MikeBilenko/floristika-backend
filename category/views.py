from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from .models import Category, SubCategory
from .serializers import SubCategorySerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class CategoryListApiView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    model = Category


class CategoryDetailApiView(APIView):
    serializer_class = SubCategorySerializer
    permission_classes = [AllowAny]

    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        sub_categories = SubCategory.objects.filter(category=category)
        serializer = SubCategorySerializer(sub_categories, many=True)
        return Response(serializer.data)