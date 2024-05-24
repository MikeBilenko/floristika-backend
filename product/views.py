from rest_framework import generics, pagination
from .models import Product
from .serializers import  ProductSerializer, ProductDetailSerializer
from reviews.models import Review
from rest_framework.permissions import AllowAny
from reviews.serializers import ReviewSerializer
from django.db.models import Q
from category.models import Category, SubCategory
from filters.models import Size, Color


class ProductsHomePagination(pagination.PageNumberPagination):
    page_size = 6
    max_page_size = 1000


class ProductsPagination(pagination.PageNumberPagination):
    page_size = 15
    max_page_size = 1000


class ProductListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination

    def get_queryset(self):
        queryset = Product.objects.all()

        category_slug = self.request.query_params.get('category')
        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            queryset = queryset.filter(category=category)

        subcategory_slug = self.request.query_params.get('type')
        if subcategory_slug:
            subcategory = SubCategory.objects.filter(slug=subcategory_slug).first()
            queryset = queryset.filter(subcategory=subcategory)

        colors = self.request.query_params.get('color')
        if colors:
            color_slugs = [color.strip().lower() for color in
                           colors.split(',')]
            queryset = queryset.filter(Q(color__slug__in=color_slugs) | Q(slug__in=color_slugs))

        sizes = self.request.query_params.get('size')
        if sizes:
            size_slugs = [size.strip().lower() for size in
                          sizes.split(',')]
            queryset = queryset.filter(size__in=Size.objects.filter(slug__in=size_slugs))

        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        if price_from and price_to:
            if bool(self.request.query_params.get("auth")):
                queryset = queryset.filter(price_for_auth__range=(price_from, price_to))
            else:
                queryset = queryset.filter(price__range=(price_from, price_to))
        elif price_from and not price_to:
            if bool(self.request.query_params.get("auth")):
                queryset = queryset.filter(price_for_auth__gte=price_from)
            else:
                queryset = queryset.filter(price__gte=price_from)
        elif not price_from and price_to:
            if bool(self.request.query_params.get("auth")):
                queryset = queryset.filter(price_for_auth__lte=price_to)
            else:
                queryset = queryset.filter(price__lte=price_to)

        sale = bool(self.request.query_params.get('sale'))
        if sale:
            queryset = queryset.filter(sale=True)

        best_sellers = bool(self.request.query_params.get('best-sellers'))
        if best_sellers:
            queryset = queryset.order_by('-sold')

        new_in = bool(self.request.query_params.get('new-in'))
        if new_in:
            queryset = queryset.order_by('-created_at')

        sort_option = self.request.query_params.get('sort')
        if sort_option == 'recently_added':
            queryset = queryset.order_by('-created_at')
        elif sort_option == 'price_high_to_low':
            if bool(self.request.query_params.get("auth")):
                queryset = queryset.order_by('-price_for_auth')
            else:
                queryset = queryset.order_by('-price')
        elif sort_option == 'price_low_to_high':
            if bool(self.request.query_params.get("auth")):
                queryset = queryset.order_by('price_for_auth')
            else:
                queryset = queryset.order_by('price')
        elif sort_option == 'discount':
            queryset = queryset.order_by('-sale_percent')
        elif sort_option == 'stock_level':
            queryset = queryset.order_by('-qty')

        return queryset


class ProductNewListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    model = Product
    serializer_class = ProductSerializer
    queryset = Product.objects.order_by('-created_at')
    pagination_class = ProductsHomePagination


class ProductBestSellersListApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    pagination_class = ProductsHomePagination

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-sold')
        return queryset


class ProductDetailApiView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    model = Product
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    lookup_field = "slug"


class ReviewPagination(pagination.PageNumberPagination):
    page_size = 8
    max_page_size = 1000


class ProductReviewsApiView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination

    def get_queryset(self):
        product_slug = self.kwargs.get('slug')
        return Review.objects.filter(product__slug=product_slug)
