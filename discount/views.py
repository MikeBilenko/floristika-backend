from .serializers import DiscountSerializer
from .models import Discount
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class IntroDiscountAPIView(generics.RetrieveAPIView):
    """Get the last working discount."""
    serializer_class = DiscountSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        current_datetime = timezone.now()
        queryset = Discount.objects.filter(works_from__lte=current_datetime, intro=True)
        last_discount = queryset.order_by('-created_at').first()
        return last_discount


class DiscountAPIView(APIView):
    """Get discount by code."""
    permission_classes = (AllowAny,)

    def post(self, request):
        data = self.request.data
        code = data.get("code")
        if not code:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        current_datetime = timezone.now()
        queryset = Discount.objects.filter(
            works_from__lte=current_datetime,
            works_to__gte=current_datetime,
            code=code,
        ).order_by('-created_at')
        if queryset.exists():
            serializer = DiscountSerializer(queryset.first())
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)