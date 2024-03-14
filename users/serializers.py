from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import  AddressBook, WishList
from product.serializers import ProductSerializer


User = get_user_model()


class AddressBookSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = AddressBook


class UserSerializer(serializers.ModelSerializer):
    address_books = AddressBookSerializer

    class Meta:
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
            "address_books",
        ]
        model = User

    def create(self, validated_data):
        address_books_data = validated_data.pop('address_books', [])
        user = User.objects.create(**validated_data)
        for address_book_data in address_books_data:
            AddressBook.objects.create(user=user, **address_book_data)
        return user

    def update(self, instance, validated_data):
        address_books_data = validated_data.pop('address_books', [])
        address_books = (instance.address_books).all()
        address_books = list(address_books)
        instance = super(UserSerializer, self).update(instance, validated_data)

        for address_book_data in address_books_data:
            address_book = address_books.pop(0)
            AddressBook.objects.update_or_create(user=instance, **address_book_data)
        return instance

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation['admin'] = True
        if instance.is_staff:
            representation['staff'] = True
        return representation


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=False)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "password1": self.validated_data.get("password1", ""),
            "phone": self.validated_data.get("phone", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self)
        user.save()

        setup_user_email(request, user, [])
        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.password1 = self.cleaned_data.get("password1")
        user.phone = self.cleaned_data.get("phone")

        return user


class WishListSerializers(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = WishList
        fields = "__all__"
