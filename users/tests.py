import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from rest_framework import status

from users.serializers import UserSerializer

User = get_user_model()


class TestUserModel:
    """Тесты для модели User"""

    @pytest.mark.django_db
    def test_create_user(self):
        """Тест создания пользователя"""
        user = User.objects.create_user(
            email="test@test.com",
            password="testpass123",
            full_name="Иван Петров"
        )
        assert user.email == "test@test.com"
        assert user.full_name == "Иван Петров"
        assert str(user) == "test@test.com"
        assert user.check_password("testpass123")

    @pytest.mark.django_db
    def test_user_without_username(self):
        """Тест что username установлен в None"""
        user = User.objects.create_user(email="test@test.com", password="pass123")
        assert user.username is None

    @pytest.mark.django_db
    def test_email_unique(self):
        """Тест что email должен быть уникальным"""
        User.objects.create_user(email="test@test.com", password="pass123")
        with pytest.raises(Exception):
            User.objects.create_user(email="test@test.com", password="pass123")

    @pytest.mark.django_db
    def test_user_phone_number(self):
        """Тест сохранения номера телефона"""
        user = User.objects.create_user(
            email="test@test.com",
            password="pass123",
            phone_number="+79991234567"
        )
        assert user.phone_number == "+79991234567"

    @pytest.mark.django_db
    def test_user_is_librarian(self):
        """Тест флага библиотекаря"""
        user = User.objects.create_user(
            email="librarian@test.com",
            password="pass123",
            is_librarian=True
        )
        assert user.is_librarian is True

    @pytest.mark.django_db
    def test_user_verbose_name(self):
        """Тест verbose_name модели"""
        assert User._meta.verbose_name == "Пользователь"
        assert User._meta.verbose_name_plural == "Пользователи"

    @pytest.mark.django_db
    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        user = User.objects.create_superuser(
            email="admin@test.com",
            password="adminpass123"
        )
        assert user.is_superuser is True
        assert user.is_staff is True


class TestUserSerializer:
    """Тесты для UserSerializer"""

    @pytest.mark.django_db
    def test_serialize_user(self):
        """Тест сериализации пользователя"""
        user = User.objects.create_user(
            email="test@test.com",
            password="pass123",
            full_name="Иван"
        )
        serializer = UserSerializer(user)
        assert serializer.data['email'] == "test@test.com"
        assert serializer.data['full_name'] == "Иван"

    @pytest.mark.django_db
    def test_create_user_via_serializer(self):
        """Тест создания пользователя через сериализатор"""
        data = {
            'email': 'new@test.com',
            'password': 'testpass123',
            'full_name': 'Петр'
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()


class TestUserCreateAPIView:
    """Тесты для создания пользователя"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.mark.django_db
    def test_create_user_api(self, client):
        """Тест создания пользователя через API"""
        data = {
            'email': 'newuser@test.com',
            'password': 'testpass123',
            'full_name': 'Новый пользователь'
        }
        response = client.post('/users/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        user = User.objects.get(email='newuser@test.com')
        assert user.check_password('testpass123')

    @pytest.mark.django_db
    def test_create_user_without_email(self, client):
        """Тест создания пользователя без email"""
        data = {'password': 'testpass123'}
        response = client.post('/users/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_duplicate_email(self, client):
        """Тест создания пользователя с существующим email"""
        User.objects.create_user(email="exists@test.com", password="pass123")
        data = {
            'email': 'exists@test.com',
            'password': 'newpass123'
        }
        response = client.post('/users/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestUserRetrieveAPIView:
    """Тесты для получения данных пользователя"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="test@test.com",
            password="pass123",
            full_name="Иван"
        )

    @pytest.fixture
    def librarian_user(self):
        user = User.objects.create_user(
            email="librarian@test.com",
            password="pass123",
            is_librarian=True
        )
        group, _ = Group.objects.get_or_create(name="librarians")
        user.groups.add(group)
        return user

    @pytest.mark.django_db
    def test_retrieve_user_as_owner(self, client, user):
        """Тест получения своего профиля"""
        client.force_authenticate(user=user)
        response = client.get(f'/users/{user.id}/detail/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email

    @pytest.mark.django_db
    def test_retrieve_other_user_as_librarian(self, client, user, librarian_user):
        """Тест получения профиля другого пользователя библиотекарем"""
        client.force_authenticate(user=librarian_user)
        response = client.get(f'/users/{user.id}/detail/')
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_retrieve_unauthenticated(self, client, user):
        """Тест получения профиля без авторизации"""
        response = client.get(f'/users/{user.id}/detail/')
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


class TestUserUpdateAPIView:
    """Тесты для обновления пользователя"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="test@test.com",
            password="pass123"
        )

    @pytest.fixture
    def librarian_user(self):
        user = User.objects.create_user(
            email="librarian@test.com",
            password="pass123",
            is_librarian=True
        )
        group, _ = Group.objects.get_or_create(name="librarians")
        user.groups.add(group)
        return user

    @pytest.mark.django_db
    def test_update_own_profile(self, client, user):
        """Тест обновления своего профиля"""
        client.force_authenticate(user=user)
        data = {'full_name': 'Новое имя'}
        response = client.patch(f'/users/{user.id}/update/', data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.full_name == 'Новое имя'

    @pytest.mark.django_db
    def test_update_other_user_as_librarian(self, client, user, librarian_user):
        """Тест обновления другого пользователя библиотекарем"""
        client.force_authenticate(user=librarian_user)
        data = {'full_name': 'Обновленное имя'}
        response = client.patch(f'/users/{user.id}/update/', data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_update_unauthenticated(self, client, user):
        """Тест обновления без авторизации"""
        data = {'full_name': 'Имя'}
        response = client.patch(f'/users/{user.id}/update/', data)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]


class TestUserDestroyAPIView:
    """Тесты для удаления пользователя"""

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email="test@test.com",
            password="pass123"
        )

    @pytest.fixture
    def librarian_user(self):
        user = User.objects.create_user(
            email="librarian@test.com",
            password="pass123",
            is_librarian=True
        )
        group, _ = Group.objects.get_or_create(name="librarians")
        user.groups.add(group)
        return user

    @pytest.mark.django_db
    def test_delete_own_profile(self, client, user):
        """Тест удаления своего профиля"""
        client.force_authenticate(user=user)
        response = client.delete(f'/users/{user.id}/delete/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user.id).exists()

    @pytest.mark.django_db
    def test_delete_other_user_as_librarian(self, client, user, librarian_user):
        """Тест удаления другого пользователя библиотекарем"""
        client.force_authenticate(user=librarian_user)
        user_id = user.id
        response = client.delete(f'/users/{user_id}/delete/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user_id).exists()

    @pytest.mark.django_db
    def test_delete_unauthenticated(self, client, user):
        """Тест удаления без авторизации"""
        response = client.delete(f'/users/{user.id}/delete/')
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]
