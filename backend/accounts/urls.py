from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    CustomTokenRefreshView
)

urlpatterns = [

    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),

    path(
        "token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token_refresh"
    ),
]