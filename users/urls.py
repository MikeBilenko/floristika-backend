from django.urls import path, include
from django.urls import reverse
from .views import CustomeUserDetailView, WishlistView
from dj_rest_auth.views import PasswordResetConfirmView
from dj_rest_auth.registration.views import VerifyEmailView

# from dj_rest_auth.registration.views import (
#     SocialAccountListView, SocialAccountDisconnectView
# )


urlpatterns = [
    path("auth/",include("dj_rest_auth.urls")),
    path("user/",CustomeUserDetailView.as_view(), name="users_list_api_view"),
    path(
        "auth/registration/",
        include("dj_rest_auth.registration.urls")
    ),
    path('auth/registration/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # path(
    #     'socialaccounts/',
    #     SocialAccountListView.as_view(),
    #     name='social_account_list'
    # ),
    # path(
    #     'socialaccounts/<int:pk>/disconnect/',
    #     SocialAccountDisconnectView.as_view(),
    #     name='social_account_disconnect'
    # ),
    path(
        "auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),

    path("all-auth/", include("allauth.urls")),
    path("wishlist/", WishlistView.as_view(), name="wishlist_list_api"),
]