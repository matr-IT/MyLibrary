# MyLibrary API

Это REST API приложение для управления библиотекой, написанное на Django с использованием Django REST Framework.

## Описание

**MyLibrary** - это полнофункциональная система управления библиотекой с поддержкой:
- Управления авторами и книгами
- Системы пользователей с аутентификацией JWT
- Разделения ролей (обычные пользователи и библиотекари)
- Отслеживания выданных книг

## Требования

- Python >= 3.13
- PostgreSQL

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <repository_url>
cd MyLibrary
```

### 2. Установка зависимостей

```bash
poetry install --no-root
```

### 3. Настройка переменных окружения

Скопируйте файл `.env_sample` в `.env` и заполните необходимые параметры:

```bash
cp .env_sample .env
```

Отредактируйте `.env`:

```
SECRET_KEY=your_secret_key_here
DEBUG=True
POSTGRES_NAME=MyLibrary
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4. Миграции и инициализация БД

```bash
poetry run python3 manage.py migrate
```

### 5. Создание суперпользователя

```bash
poetry run python3 manage.py createsuperuser
```

Или используйте встроенную команду для создания админа (для развития):

```bash
poetry run python3 manage.py csu
```

### 6. Запуск сервера

```bash
poetry run python3 manage.py runserver
```

Сервер запустится на `http://localhost:8000/`

## Структура проекта

```
MyLibrary/
├── config/                 # Настройки Django
│   ├── settings.py        # Основные настройки
│   ├── urls.py            # Маршруты приложения
│   ├── wsgi.py
│   └── asgi.py
├── users/                 # Приложение пользователей
│   ├── models.py          # Модель User
│   ├── views.py           # API views
│   ├── serializers.py     # Сериализаторы
│   ├── permissions.py     # Кастомные разрешения
│   ├── urls.py            # URL маршруты
│   └── admin.py
├── library/               # Приложение библиотеки
│   ├── models.py          # Модели Author и Book
│   ├── views.py           # API views
│   ├── serializers.py     # Сериализаторы
│   ├── urls.py            # URL маршруты
│   └── admin.py
├── manage.py
├── pyproject.toml         # Зависимости проекта
├── .env                   # Переменные окружения
├── .flake8                # Конфигурация линтера
└── README.md
```

## API Endpoints

### Аутентификация

- `POST /library/users/register/` - Регистрация нового пользователя
- `POST /library/users/login/` - Получение JWT токенов
- `POST /library/users/token/refresh/` - Обновление access токена

### Пользователи

- `GET /library/users/<id>/detail/` - Получить информацию о пользователе
- `PATCH /library/users/<id>/update/` - Обновить профиль
- `DELETE /library/users/<id>/delete/` - Удалить пользователя

### Авторы

- `GET /library/authors/` - Список всех авторов
- `POST /library/authors/` - Создать нового автора (только для библиотекарей)
- `GET /library/authors/<id>/` - Получить информацию об авторе
- `PUT /library/authors/<id>/` - Обновить автора (только для библиотекарей)
- `DELETE /library/authors/<id>/` - Удалить автора (только для библиотекарей)

### Книги

- `GET /library/books/` - Список всех книг
- `POST /library/books/` - Добавить новую книгу (только для библиотекарей)
- `GET /library/books/<id>/` - Получить информацию о книге
- `PUT /library/books/<id>/` - Обновить книгу (только для библиотекарей)
- `DELETE /library/books/<id>/` - Удалить книгу (только для библиотекарей)

### Документация

- `GET /swagger/` - Интерактивная документация Swagger
- `GET /redoc/` - Документация ReDoc

## Модели данных

### User

```python
- id: BigAutoField
- email: EmailField (unique)
- full_name: CharField
- phone_number: CharField
- password: CharField
- is_active: BooleanField
- is_staff: BooleanField
- is_superuser: BooleanField
```

### Author

```python
- id: BigAutoField
- name: CharField
- date_of_birth_and_death: CharField
- bio: TextField
- is_verified: BooleanField
```

### Book

```python
- id: BigAutoField
- title: CharField
- author: ForeignKey(Author)
- description: TextField
- publication_date: DateField
- is_checked_out: BooleanField
- return_date: DateTimeField
- given_to: ForeignKey(User)
```

## Разрешения (Permissions)

### IsOwner
Разрешает доступ только владельцу профиля для чтения и обновления своих данных.

### IsLibrarian
Разрешает доступ пользователям из группы `librarians` для управления авторами и книгами.

## Конфигурация

### JWT токены

- **ACCESS_TOKEN_LIFETIME**: 15 минут
- **REFRESH_TOKEN_LIFETIME**: 1 день

### Аутентификация

Используется JWT (JSON Web Token) через SimpleJWT. Передавайте токен в заголовке:

```
Authorization: Bearer <your_access_token>
```

## Примеры использования

### Регистрация

```bash
curl -X POST http://localhost:8000/library/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Получение токенов

```bash
curl -X POST http://localhost:8000/library/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### Получение списка авторов

```bash
curl -X GET http://localhost:8000/library/authors/ \
  -H "Authorization: Bearer <your_access_token>"
```

## Проверка качества кода

### Линтинг (Flake8)

```bash
poetry run flake8 .
```

### Форматирование (Black)

```bash
poetry run black .
```

### Проверка типов (MyPy)

```bash
poetry run mypy .
```

### Проверка сортировки импортов (isort)

```bash
poetry run isort .
```

## Разработка

### Запуск тестов

```bash
poetry run python3 manage.py test
```

### Проверка конфигурации Django

```bash
poetry run python3 manage.py check
```

## Лицензия

MIT

## Автор

Rybin
