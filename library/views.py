from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from library.models import Book, Author
from library.serializers import BookSerializer, AuthorSerializer
from users.permissions import IsLibrarian

User = get_user_model()


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = [
        "title",
        "author",
        "publication_date",
        "checking_out_date",
        "return_date",
        "is_checked_out",
        "given_to",
    ]
    ordering_fields = ["title", "author", "publication_date"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Book.objects.all()

        return Book.objects.none()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsLibrarian]
        elif self.action == "destroy":
            self.permission_classes = [IsLibrarian]
        elif self.action == "update":
            self.permission_classes = [IsLibrarian]
        elif self.action in ["retrieve", "list"]:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["name", "date_of_birth_and_death"]
    ordering_fields = ["name", "date_of_birth_and_death"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Author.objects.all()
        return Author.objects.none()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsLibrarian]
        elif self.action == "destroy":
            self.permission_classes = [IsLibrarian]
        elif self.action == "update":
            self.permission_classes = [IsLibrarian]
        elif self.action in ["retrieve", "list"]:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()
