from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination


class SearchView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        data = self.request.data
        search = data.get("search")

        if search:
            queryset = Product.objects.filter(
                name__icontains=search) | Product.objects.filter(
                name_lv__icontains=search) | Product.objects.filter(
                name_ru__icontains=search)
            paginator = PageNumberPagination()
            paginator.page_size = 1  # 16 Set the number of items per page

            result_page = paginator.paginate_queryset(queryset, request)
            serializer = ProductSerializer(result_page, many=True)

            return paginator.get_paginated_response(serializer.data)
        else:
            return Response("Please provide a 'query' parameter in the query string.", status=status.HTTP_400_BAD_REQUEST)
