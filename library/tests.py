import pytest
from datetime import date
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from library.models import Author, Book
from library.serializers import AuthorSerializer, BookSerializer

User = get_user_model()


class TestAuthorModel:
    """Тесты для модели Author"""

    @pytest.mark.django_db
    def test_create_author(self):
        """Тест создания автора"""
        author = Author.objects.create(
            name="Лев Толстой",
            date_of_birth_and_death="09.09.1828 - 20.11.1910",
            bio="Русский писатель"
        )
        assert author.name == "Лев Толстой"
        assert author.bio == "Русский писатель"
        assert str(author) == "Лев Толстой"

    @pytest.mark.django_db
    def test_author_without_dates(self):
        """Тест создания автора без дат"""
        author = Author.objects.create(
            name="Современный автор",
            bio="Жив и здоров"
        )
        assert author.date_of_birth_and_death is None
        assert author.name == "Современный автор"

    @pytest.mark.django_db
    def test_author_verbose_name(self):
        """Тест verbose_name модели"""
        assert Author._meta.verbose_name == "Автор"
        assert Author._meta.verbose_name_plural == "Авторы"


class TestBookModel:
    """Тесты для модели Book"""

    @pytest.mark.django_db
    def test_create_book(self):
        """Тест создания книги"""
        author = Author.objects.create(name="Лев Толстой")
        book = Book.objects.create(
            title="Война и мир",
            author=author,
            genre="Роман",
            description="Величайший роман",
            publication_date=date(1869, 1, 1),
            is_checked_out=False
        )
        assert book.title == "Война и мир"
        assert book.author == author
        assert book.genre == "Роман"
        assert str(book) == "Война и мир"

    @pytest.mark.django_db
    def test_book_checked_out(self):
        """Тест состояния книги при выдаче"""
        author = Author.objects.create(name="Автор")
        user = User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )
        book = Book.objects.create(
            title="Книга",
            author=author,
            is_checked_out=True,
            given_to=user,
            checking_out_date="09.08.2026 10:00"
        )
        assert book.is_checked_out is True
        assert book.given_to == user
        assert book.checking_out_date == "09.08.2026 10:00"

    @pytest.mark.django_db
    def test_book_return(self):
        """Тест возврата книги"""
        author = Author.objects.create(name="Автор")
        user = User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )
        book = Book.objects.create(
            title="Книга",
            author=author,
            is_checked_out=True,
            given_to=user,
            checking_out_date="01.08.2026 10:00",
            return_date="09.08.2026 15:00"
        )
        book.is_checked_out = False
        book.given_to = None
        book.save()
        
        book.refresh_from_db()
        assert book.is_checked_out is False
        assert book.given_to is None
        assert book.return_date == "09.08.2026 15:00"

    @pytest.mark.django_db
    def test_cascade_delete_author(self):
        """Тест каскадного удаления при удалении автора"""
        author = Author.objects.create(name="Автор")
        Book.objects.create(title="Книга 1", author=author)
        Book.objects.create(title="Книга 2", author=author)
        
        assert Book.objects.count() == 2
        author.delete()
        assert Book.objects.count() == 0

    @pytest.mark.django_db
    def test_book_verbose_name(self):
        """Тест verbose_name модели"""
        assert Book._meta.verbose_name == "Книга"
        assert Book._meta.verbose_name_plural == "Книги"


class TestBookSerializer:
    """Тесты для сериализатора Book"""

    @pytest.mark.django_db
    def test_book_serializer_valid_data(self):
        """Тест сериализации валидных данных"""
        author = Author.objects.create(name="Автор")
        book = Book.objects.create(
            title="Книга",
            author=author,
            genre="Жанр",
            description="Описание"
        )
        serializer = BookSerializer(book)
        assert serializer.data['title'] == "Книга"
        assert serializer.data['genre'] == "Жанр"

    @pytest.mark.django_db
    def test_create_book_via_serializer(self):
        """Тест создания книги через сериализатор"""
        author = Author.objects.create(name="Автор")
        data = {
            'title': 'Новая книга',
            'author': author.id,
            'genre': 'Жанр',
            'description': 'Описание'
        }
        serializer = BookSerializer(data=data)
        assert serializer.is_valid()
        book = serializer.save()
        assert book.title == 'Новая книга'


class TestAuthorSerializer:
    """Тесты для сериализатора Author"""

    @pytest.mark.django_db
    def test_author_serializer_valid_data(self):
        """Тест сериализации автора"""
        author = Author.objects.create(
            name="Автор",
            date_of_birth_and_death="01.01.1900 - 01.01.1980",
            bio="Биография"
        )
        serializer = AuthorSerializer(author)
        assert serializer.data['name'] == "Автор"
        assert serializer.data['bio'] == "Биография"

    @pytest.mark.django_db
    def test_create_author_via_serializer(self):
        """Тест создания автора через сериализатор"""
        data = {
            'name': 'Новый автор',
            'date_of_birth_and_death': '01.01.1900 - 01.01.1980',
            'bio': 'Биография'
        }
        serializer = AuthorSerializer(data=data)
        assert serializer.is_valid()
        author = serializer.save()
        assert author.name == 'Новый автор'


class TestBookViewSet:
    """Тесты для BookViewSet"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def librarian_user(self):
        user = User.objects.create_user(
            email="librarian@test.com",
            password="testpass123",
            is_librarian=True
        )
        group, _ = Group.objects.get_or_create(name="librarians")
        user.groups.add(group)
        return user

    @pytest.fixture
    def regular_user(self):
        return User.objects.create_user(
            email="user@test.com",
            password="testpass123",
            is_librarian=False
        )

    @pytest.mark.django_db
    def test_list_books_authenticated(self, client, regular_user):
        """Тест получения списка книг авторизованным пользователем"""
        client.force_authenticate(user=regular_user)
        author = Author.objects.create(name="Автор")
        Book.objects.create(title="Книга 1", author=author)
        
        response = client.get('/library/books/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_retrieve_book(self, client, regular_user):
        """Тест получения отдельной книги"""
        client.force_authenticate(user=regular_user)
        author = Author.objects.create(name="Автор")
        book = Book.objects.create(title="Книга", author=author)
        
        response = client.get(f'/library/books/{book.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "Книга"

    @pytest.mark.django_db
    def test_create_book_non_librarian(self, client, regular_user):
        """Тест создания книги обычным пользователем"""
        client.force_authenticate(user=regular_user)
        author = Author.objects.create(name="Автор")
        data = {'title': 'Новая книга', 'author': author.id}
        response = client.post('/library/books/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_create_book_librarian(self, client, librarian_user):
        """Тест создания книги библиотекарем"""
        client.force_authenticate(user=librarian_user)
        author = Author.objects.create(name="Автор")
        data = {
            'title': 'Новая книга',
            'author': author.id,
            'genre': 'Жанр',
            'description': 'Описание'
        }
        response = client.post('/library/books/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.count() == 1

    @pytest.mark.django_db
    def test_update_book_librarian(self, client, librarian_user):
        """Тест обновления книги библиотекарем"""
        client.force_authenticate(user=librarian_user)
        author = Author.objects.create(name="Автор")
        book = Book.objects.create(title="Старое название", author=author)
        data = {'title': 'Новое название'}
        response = client.patch(f'/library/books/{book.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        book.refresh_from_db()
        assert book.title == "Новое название"

    @pytest.mark.django_db
    def test_delete_book_librarian(self, client, librarian_user):
        """Тест удаления книги библиотекарем"""
        client.force_authenticate(user=librarian_user)
        author = Author.objects.create(name="Автор")
        book = Book.objects.create(title="Книга", author=author)
        response = client.delete(f'/library/books/{book.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.count() == 0

    @pytest.mark.django_db
    def test_ordering_books(self, client, regular_user):
        """Тест сортировки книг"""
        client.force_authenticate(user=regular_user)
        author = Author.objects.create(name="Автор")
        Book.objects.create(title="A Книга", author=author)
        Book.objects.create(title="B Книга", author=author)
        
        response = client.get('/library/books/?ordering=title')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


class TestAuthorViewSet:
    """Тесты для AuthorViewSet"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def librarian_user(self):
        user = User.objects.create_user(
            email="librarian@test.com",
            password="testpass123",
            is_librarian=True
        )
        group, _ = Group.objects.get_or_create(name="librarians")
        user.groups.add(group)
        return user

    @pytest.fixture
    def regular_user(self):
        return User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )

    @pytest.mark.django_db
    def test_list_authors_authenticated(self, client, regular_user):
        """Тест получения списка авторов авторизованным пользователем"""
        client.force_authenticate(user=regular_user)
        Author.objects.create(name="Автор 1")
        Author.objects.create(name="Автор 2")
        
        response = client.get('/library/authors/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    @pytest.mark.django_db
    def test_retrieve_author(self, client, regular_user):
        """Тест получения отдельного автора"""
        client.force_authenticate(user=regular_user)
        author = Author.objects.create(name="Автор")
        
        response = client.get(f'/library/authors/{author.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Автор"

    @pytest.mark.django_db
    def test_create_author_librarian(self, client, librarian_user):
        """Тест создания автора библиотекарем"""
        client.force_authenticate(user=librarian_user)
        data = {
            'name': 'Новый автор',
            'bio': 'Биография'
        }
        response = client.post('/library/authors/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Author.objects.count() == 1

    @pytest.mark.django_db
    def test_create_author_non_librarian(self, client, regular_user):
        """Тест создания автора обычным пользователем"""
        client.force_authenticate(user=regular_user)
        data = {'name': 'Новый автор'}
        response = client.post('/library/authors/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_author_librarian(self, client, librarian_user):
        """Тест обновления автора библиотекарем"""
        client.force_authenticate(user=librarian_user)
        author = Author.objects.create(name="Старое имя")
        data = {'name': 'Новое имя'}
        response = client.patch(f'/library/authors/{author.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        author.refresh_from_db()
        assert author.name == "Новое имя"

    @pytest.mark.django_db
    def test_delete_author_librarian(self, client, librarian_user):
        """Тест удаления автора библиотекарем"""
        client.force_authenticate(user=librarian_user)
        author = Author.objects.create(name="Автор")
        response = client.delete(f'/library/authors/{author.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Author.objects.count() == 0
