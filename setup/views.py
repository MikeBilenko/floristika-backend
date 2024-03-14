from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PricePercentSerializer
from .models import PricePercent


class PricePercentView(APIView):
    queryset = PricePercent.objects.all()
    model = PricePercent
    serializer_class = PricePercentSerializer
    def get(self, request):
        obj = PricePercent.objects.first()
        serializer = PricePercentSerializer(obj, many=False)
        return Response(serializer.data)
