from rest_framework import generics
from rest_framework.response import Response
from .models import Contact, ContactInfo
from .serializers import ContactSerializer, ContactInfoSerializer
from rest_framework.permissions import AllowAny


class ContactCreateApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactSerializer
    model = Contact
    queryset = Contact.objects.all()


class ContactInfoApiView(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        instance = ContactInfo.objects.first()
        serializer = ContactInfoSerializer(instance)
        return Response(serializer.data)