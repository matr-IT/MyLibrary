from rest_framework.serializers import ModelSerializer
from library.models import Book, Author


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

        def __init__(self):
            super().__init__()
            if self.context.get("request").is_authenticated and not self.context.get("request").user.is_librarian:
                self.Meta.fields = "__all__"

            else:
                self.Meta.fields = (
                    "id",
                    "title",
                    "author",
                    "genre",
                    "description",
                    "publication_date",
                    "is_checked_out",
                )


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "date_of_birth_and_death", "bio")
