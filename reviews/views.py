from rest_framework.permissions import AllowAny
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product
from django.shortcuts import get_object_or_404


class ReviewCreateApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(slug=request.data.get('product'))
        user = None
        if request.user.is_authenticated:
            user = request.user
        review = Review.objects.create(
            product=product,
            user=user,
            rate=request.data.get('rate'),
            text=request.data.get('text'),
            name=request.data.get('name'),
            email=request.data.get('email'),
        )
        total_rating = 0.0
        num_reviews = 0
        reviews = Review.objects.filter(product=product)

        for review in reviews:
            total_rating += review.rate
            num_reviews += 1

        if num_reviews > 0:
            average_rating = total_rating / num_reviews
            product.rate = round(average_rating, 1)
            product.save()

        serializer = ReviewSerializer(review, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
