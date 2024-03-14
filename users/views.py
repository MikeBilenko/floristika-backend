from rest_framework import generics
from .serializers import UserSerializer, WishListSerializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import WishList
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class CustomeUserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()


class WishListPagination(PageNumberPagination):
    page_size = 2 #5  # Number of objects per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Maximum number of objects per page
#
#
# class WishListApiView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated, ]
#     serializer_class = WishListSerializers
#     model = WishList
#     pagination_class = WishListPagination
#
#     # 15
#
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = WishList.objects.filter(user=user)
#         return queryset


class WishlistView(APIView):
    pagination_class = WishListPagination

    def get(self, request):
        sorting_option = request.query_params.get('sort',
                                                  'recently_added')  # Default sorting option is 'recently_added'

        user = request.user
        wishlist_items = WishList.objects.filter(
            user=user)  # Adjusted queryset to filter wishlist items for the current user

        # Perform sorting based on the selected option
        if sorting_option == 'recently_added':
            sorted_items = wishlist_items.order_by('-product__created_at')
        elif sorting_option == 'price_high_to_low':
            sorted_items = wishlist_items.order_by('-product__price')
        elif sorting_option == 'price_low_to_high':
            sorted_items = wishlist_items.order_by('product__price')
        elif sorting_option == 'discount_percent':
            sorted_items = wishlist_items.order_by('-product__sale_percent')
        elif sorting_option == 'stock_level':
            sorted_items = wishlist_items.order_by('-product__qty')

        # Paginate the sorted queryset
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(sorted_items, request)

        serializer = WishListSerializers(paginated_queryset,
                                         many=True)  # Assuming you have a serializer for wishlist items
        return paginator.get_paginated_response(serializer.data)