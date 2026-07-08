from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserDestroyAPIView, UserRetrieveAPIView, UserUpdateAPIView

app_name = UsersConfig.name


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("<int:pk>/detail/", UserRetrieveAPIView.as_view(), name="detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="delete"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
