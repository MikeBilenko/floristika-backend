from .serializers import AuthPercentSerializer
from .models import AuthPercent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class AuthPercentAPIView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        percent = AuthPercent.objects.first()
        serializer = AuthPercentSerializer(percent)
        return Response(serializer.data)