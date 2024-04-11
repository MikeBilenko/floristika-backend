from django.urls import path, include
from .views import (
    CustomUserDetailView,
    WishlistView,
    CompanyView,
    DetailWishListAPIView,
    AddressBookView,
    AddressBookDetail,
)
from dj_rest_auth.views import PasswordResetConfirmView
from dj_rest_auth.registration.views import VerifyEmailView


urlpatterns = [
    path("company/", CompanyView.as_view(), name="company_list_api_view"),
    path("address-book/<int:pk>/", AddressBookDetail.as_view(), name="address_book_detail_api_view"),
    path("address-book/", AddressBookView.as_view(), name="address_book_crud_api_view"),
    path("auth/",include("dj_rest_auth.urls")),
    path("user/",CustomUserDetailView.as_view(), name="users_list_api_view"),
    path(
        "auth/registration/",
        include("dj_rest_auth.registration.urls")
    ),
    path('auth/registration/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path(
        "auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("all-auth/", include("allauth.urls")),
    path("wishlist/", WishlistView.as_view(), name="wishlist_list_api"),
    path("wishlist/<slug:slug>/", DetailWishListAPIView.as_view(), name="wishlist_add_delete_api"),
]