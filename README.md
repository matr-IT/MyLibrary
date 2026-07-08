# 📚 MyLibrary API

Полнофункциональная REST API система управления библиотекой, разработанная на **Django** и **Django REST Framework**. Приложение позволяет управлять авторами, книгами, пользователями и отслеживать выданные книги с системой ролей и аутентификацией JWT.

**Стек технологий:** Python 3.13 | Django 6.0 | DRF 3.17 | PostgreSQL | JWT

---

## 🎯 Основные возможности

✅ **Управление авторами** — создание, редактирование, удаление авторов  
✅ **Управление книгами** — каталог книг с отслеживанием статуса  
✅ **Система пользователей** — регистрация, аутентификация JWT, профили  
✅ **Разделение ролей** — обычные пользователи и библиотекари  
✅ **Выдача книг** — отслеживание кому выданы книги и сроки возврата  
✅ **Интерактивная документация** — Swagger UI и ReDoc  
✅ **Администраторский интерфейс** — Django Admin  

---

## 📋 Требования

- **Python** >= 3.13
- **PostgreSQL** >= 12
- **Poetry** (управление зависимостями)

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/matr-IT/MyLibrary.git
cd MyLibrary
```

### 2. Установка зависимостей

```bash
poetry install --no-root
```

### 3. Конфигурация окружения

Скопируйте шаблон и заполните переменные окружения:

```bash
cp .env_sample .env
```

Отредактируйте `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

# PostgreSQL
POSTGRES_NAME=MyLibrary
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 4. Применение миграций

```bash
poetry run python3 manage.py migrate
```

### 5. Создание суперпользователя

**Вариант 1:** Интерактивная команда

```bash
poetry run python3 manage.py createsuperuser
```

**Вариант 2:** Автоматическое создание (для разработки)

```bash
poetry run python3 manage.py csu
# Email: HTadmin@example.com
# Password: 1234
```

### 6. Запуск сервера

```bash
poetry run python3 manage.py runserver
```

Сервер будет доступен по адресу: **http://localhost:8000**

---

## 📁 Структура проекта

```
MyLibrary/
├── config/                          # Конфигурация Django
│   ├── settings.py                 # Основные настройки
│   ├── urls.py                     # Главные URL маршруты
│   ├── wsgi.py                     # WSGI приложение
│   └── asgi.py                     # ASGI приложение
│
├── users/                          # Приложение пользователей
│   ├── models.py                   # Модель User (расширена AbstractUser)
│   ├── views.py                    # API views для пользователей
│   ├── serializers.py              # Сериализаторы (User, JWT)
│   ├── permissions.py              # Пользовательские разрешения
│   ├── urls.py                     # URL маршруты
│   ├── admin.py                    # Админ-панель
│   └── management/commands/
│       └── csu.py                  # Команда создания суперпользователя
│
├── library/                        # Приложение библиотеки
│   ├── models.py                   # Модели Author и Book
│   ├── views.py                    # ViewSets для авторов и книг
│   ├── serializers.py              # Сериализаторы
│   ├── urls.py                     # URL маршруты
│   ├── admin.py                    # Админ-панель
│   └── migrations/                 # Миграции БД
│
├── manage.py                       # Утилита управления Django
├── pyproject.toml                  # Зависимости проекта (Poetry)
├── poetry.lock                     # Зафиксированные версии
├── .env                            # Переменные окружения
├── .env_sample                     # Шаблон переменных окружения
├── .flake8                         # Конфигурация линтера
└── README.md                       # Документация
```

---

## 📡 API Endpoints

### 🔐 Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|---------|
| POST | `/library/users/register/` | Регистрация нового пользователя |
| POST | `/library/users/login/` | Получение JWT токенов (access + refresh) |
| POST | `/library/users/token/refresh/` | Обновление access токена |

### 👤 Пользователи

| Метод | Endpoint | Описание | Разрешение |
|-------|----------|---------|-----------|
| POST | `/library/users/register/` | Создать пользователя | AllowAny |
| GET | `/library/users/<id>/detail/` | Получить профиль | IsOwner ∣ IsLibrarian |
| PATCH | `/library/users/<id>/update/` | Обновить профиль | IsOwner ∣ IsLibrarian |
| DELETE | `/library/users/<id>/delete/` | Удалить пользователя | IsLibrarian |

### 📖 Авторы

| Метод | Endpoint | Описание | Разрешение |
|-------|----------|---------|-----------|
| GET | `/library/authors/` | Список авторов | IsAuthenticated |
| POST | `/library/authors/` | Создать автора | IsLibrarian |
| GET | `/library/authors/<id>/` | Получить автора | IsAuthenticated |
| PUT | `/library/authors/<id>/` | Обновить автора | IsLibrarian |
| PATCH | `/library/authors/<id>/` | Частичное обновление | IsLibrarian |
| DELETE | `/library/authors/<id>/` | Удалить автора | IsLibrarian |

### 📚 Книги

| Метод | Endpoint | Описание | Разрешение |
|-------|----------|---------|-----------|
| GET | `/library/books/` | Список книг | IsAuthenticated |
| POST | `/library/books/` | Добавить книгу | IsLibrarian |
| GET | `/library/books/<id>/` | Получить книгу | IsAuthenticated |
| PUT | `/library/books/<id>/` | Обновить книгу | IsLibrarian |
| PATCH | `/library/books/<id>/` | Частичное обновление | IsLibrarian |
| DELETE | `/library/books/<id>/` | Удалить книгу | IsLibrarian |

### 📚 Документация

| Endpoint | Описание |
|----------|---------|
| `/swagger/` | Интерактивная документация Swagger UI |
| `/redoc/` | Документация ReDoc |
| `/admin/` | Django Admin панель |

---

## 🔧 Модели данных

### User (Пользователь)

```python
class User(AbstractUser):
    email              # EmailField, unique
    full_name          # CharField, опционально
    phone_number       # CharField, опционально
    is_active          # BooleanField
    is_staff           # BooleanField
    is_superuser       # BooleanField
```

### Author (Автор)

```python
class Author(Model):
    name                        # CharField, до 100 символов
    date_of_birth_and_death    # CharField, опционально (ДД.ММ.ГГГГ - ДД.ММ.ГГГГ)
    bio                         # TextField, опционально
    is_verified                 # BooleanField (проверенный автор)
```

### Book (Книга)

```python
class Book(Model):
    title              # CharField, до 200 символов
    author             # ForeignKey(Author)
    description        # TextField, опционально
    publication_date   # DateField, опционально (ДД.ММ.ГГГГ)
    is_checked_out     # BooleanField (выдана ли книга)
    return_date        # DateTimeField, опционально
    given_to           # ForeignKey(User), опционально (кому выдана)
```

---

## 🔐 Система разрешений

### IsOwner
Разрешает доступ только владельцу профиля.
- **Уровень запроса:** Требует аутентификацию
- **Уровень объекта:** Сравнивает `obj == request.user`

### IsLibrarian
Разрешает доступ пользователям из группы `librarians`.
- **Уровень запроса:** Проверяет наличие в группе `librarians`
- **Уровень объекта:** Проверяет наличие в группе `librarians`

---

## 🔑 Аутентификация JWT

Проект использует **SimpleJWT** для управления токенами.

### Конфигурация токенов

```python
ACCESS_TOKEN_LIFETIME: 15 минут
REFRESH_TOKEN_LIFETIME: 1 день
```

### Использование токенов

После логина получите:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Передавайте `access` токен в заголовке всех защищенных запросов:

```
Authorization: Bearer <access_token>
```

### Обновление токена

```bash
curl -X POST http://localhost:8000/library/users/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

---

## 💡 Примеры использования

### 1️⃣ Регистрация пользователя

```bash
curl -X POST http://localhost:8000/library/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### 2️⃣ Логин и получение токенов

```bash
curl -X POST http://localhost:8000/library/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

Ответ:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "email": "user@example.com"
}
```

### 3️⃣ Получение списка авторов

```bash
curl -X GET http://localhost:8000/library/authors/ \
  -H "Authorization: Bearer <access_token>"
```

### 4️⃣ Создание автора (только для библиотекарей)

```bash
curl -X POST http://localhost:8000/library/authors/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Лев Толстой",
    "date_of_birth_and_death": "09.09.1828 - 20.11.1910",
    "bio": "Русский писатель-реалист",
    "is_verified": true
  }'
```

### 5️⃣ Добавление книги (только для библиотекарей)

```bash
curl -X POST http://localhost:8000/library/books/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Война и мир",
    "author": 1,
    "description": "Исторический роман",
    "publication_date": "01.01.1869",
    "is_checked_out": false
  }'
```

### 6️⃣ Выдача книги пользователю

```bash
curl -X PATCH http://localhost:8000/library/books/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "is_checked_out": true,
    "given_to": 2,
    "return_date": "2026-07-15T23:59:59Z"
  }'
```

---

## ✅ Проверка качества кода

### Линтинг (Flake8)

Проверка стиля кода согласно PEP 8:

```bash
poetry run flake8 .
```

### Форматирование (Black)

Автоматическое форматирование кода:

```bash
poetry run black .
```

### Проверка типов (MyPy)

Статическая проверка типов:

```bash
poetry run mypy .
```

### Сортировка импортов (isort)

Автоматическая организация импортов:

```bash
poetry run isort .
```

---

## 🧪 Тестирование

### Запуск тестов

```bash
poetry run python3 manage.py test
```

### Запуск тестов с покрытием

```bash
poetry run python3 manage.py test --verbosity=2
```

### Django система проверок

```bash
poetry run python3 manage.py check
```

---

## 🐳 Развертывание

### Подготовка к производству

1. Установите `DEBUG = False` в `.env`
2. Сгенерируйте надежный `SECRET_KEY`
3. Установите правильные `ALLOWED_HOSTS`
4. Используйте более надежную БД (PostgreSQL в production)
5. Настройте веб-сервер (Gunicorn + Nginx)

### Пример запуска с Gunicorn

```bash
poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## 📦 Зависимости

### Основные

- **Django** 6.0.6 — веб-фреймворк
- **djangorestframework** 3.17.1 — REST API
- **djangorestframework-simplejwt** 5.5.1 — JWT аутентификация
- **psycopg2-binary** 2.9.12 — драйвер PostgreSQL
- **python-dotenv** 1.2.2 — управление переменными окружения
- **drf-yasg** 1.21.15 — Swagger/OpenAPI документация
- **django-filter** 25.2 — фильтрация данных

### Разработка

- **flake8** 7.3.0 — линтер
- **black** 26.5.1 — форматер кода
- **isort** 8.0.1 — сортировка импортов
- **mypy** 2.1.0 — проверка типов

Полный список смотрите в `pyproject.toml`

---

## 🔍 Решение проблем

### Ошибка подключения к БД

```
psycopg2.OperationalError: could not connect to server: Connection refused
```

**Решение:**
- Убедитесь, что PostgreSQL запущен
- Проверьте учетные данные в `.env`
- Проверьте HOST и PORT в `.env`

### Ошибка 401 Unauthorized

```json
{"detail":"Authentication credentials were not provided."}
```

**Решение:**
- Убедитесь, что токен передан в заголовке `Authorization: Bearer <token>`
- Проверьте, что токен не истек (15 минут для access токена)
- Используйте refresh токен для получения нового access токена

### Ошибка 403 Permission Denied

```json
{"detail":"You do not have permission to perform this action."}
```

**Решение:**
- Убедитесь, что пользователь в группе `librarians` для операций редактирования
- Используйте суперпользователя для администрирования

---

## 📞 Поддержка и контакты

- **Автор:** Rybin
- **Email:** rybin.32@gmail.com
- **Repository:** https://github.com/matr-IT/MyLibrary

---

## 📜 Лицензия

Проект распространяется под лицензией **MIT**. Подробнее смотрите в файле `LICENSE`.

---

## 📝 Логирование

По умолчанию Django логирует события в консоль. Для более подробного логирования отредактируйте `LOGGING` в `config/settings.py`.

---

## 🚦 Статус проекта

✅ **Production Ready** — проект готов к развертыванию  
✅ **All Tests Passing** — все проверки пройдены  
✅ **Documentation Complete** — документация полная  

---

**Счастливого кодирования! 🎉**
