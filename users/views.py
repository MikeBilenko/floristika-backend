from rest_framework import generics
from .serializers import UserSerializer, WishListSerializers, CompanySerializer, AddressBookSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import WishList, Company, AddressBook
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.models import Product


class CustomUserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()


class AddressBookDetail(APIView):
    serializer_class = AddressBookSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        address_book = get_object_or_404(AddressBook, id=pk, user=request.user)
        serializer = AddressBookSerializer(address_book)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        address_book = user.address_books.get(pk=pk)
        address_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressBookView(APIView):
    def get(self, request):
        user = request.user
        address_books = user.address_books.all()
        serializer = AddressBookSerializer(address_books, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data
        address_book = user.address_books.create(
            delivery=data.get('delivery'),
            billing=data.get('billing'),
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            postal_code=data.get('postal_code'),
            country=data.get('country')
        )
        serializer = AddressBookSerializer(address_book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = request.user
        data = request.data
        address_book = user.address_books.get(pk=data.get('id'))
        for key, value in data.items():
            setattr(address_book, key, value)
        address_book.save()
        serializer = AddressBookSerializer(address_book)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CompanyView(APIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        company = Company.objects.filter(user=request.user)
        if company.exists():
            company = Company.objects.get(user=request.user)
            serializer = CompanySerializer(company, many=False)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = self.request.user
        data = request.data  # Retrieve request data
        if Company.objects.filter(user=user).exists():
            # If company exists for the user, update it
            company = Company.objects.get(user=user)
            for key, value in data.items():
                setattr(company, key, value)
            company.save()
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            company = Company.objects.create(
                user=user,
                email=data.get('email'),
                phone=data.get('phone'),
                company_name=data.get('company_name'),
                vat=data.get('vat'),
                country=data.get('country'),
                city=data.get('city'),
                address=data.get('address'),
                postal_code=data.get('postal_code'),
            )
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        if request.user:
            company = Company.objects.get(user=request.user)
            company.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        wishlist_items = WishList.objects.filter(user=user)
        serializer = WishListSerializers(wishlist_items, many=True)
        return Response(serializer.data)


class DetailWishListAPIView(APIView):
    def get(self, request, slug):
        try:
            user = self.request.user
            product = Product.objects.get(slug=slug)
            wishlist = WishList.objects.get(user=user, product=product)
            serializer = WishListSerializers(wishlist)
            return Response(serializer.data)
        except:
            return Response(None)

    def delete(self, request, slug):
        user = self.request.user
        product = Product.objects.get(slug=slug)
        wishlist = WishList.objects.get(user=user, product=product).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, slug):

        user = self.request.user
        product = Product.objects.get(slug=slug)
        if WishList.objects.filter(user=user, product=product).exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        wishlist = WishList.objects.create(user=user, product=product)
        return Response(status=status.HTTP_201_CREATED)
