from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsOwner, IsLibrarian
from users.serializers import MyTokenObtainPairSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = IsOwner | IsLibrarian


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsLibrarian,)


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = IsOwner | IsLibrarian


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = IsOwner | IsLibrarian
