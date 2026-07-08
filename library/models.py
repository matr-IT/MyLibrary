from django.db import models
from django.db.models import CASCADE


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    date_of_birth_and_death = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Дата рождения и смерти автора",
        help_text="Введите дату рождения и смерти автора в формате 'ДД.ММ.ГГГГ - ДД.ММ.ГГГГ' или оставьте пустым, если автор жив",
    )
    bio = models.TextField(blank=True, null=True, verbose_name="Биография автора")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.ForeignKey(
        Author,
        on_delete=CASCADE,
        verbose_name="Автор",
        help_text="Выберите автора книги",
    )
    genre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Жанр книги")
    description = models.TextField(blank=True, null=True, verbose_name="Описание книги")
    publication_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата публикации",
        help_text="Введите дату публикации книги в формате 'ДД.ММ.ГГГГ'",
    )

    is_checked_out = models.BooleanField(
        default=False,
        verbose_name="Книга взята",
        help_text="Отметьте, если книга взята пользователем",
    )

    checking_out_date = models.CharField(
        default=None,
        blank=True,
        null=True,
        verbose_name="Дата взятия книги",
        help_text="Введите дату и время взятия книги в формате 'ДД.ММ.ГГГГГ ЧЧ:ММ' или оставьте пустым, если книга не взята",
    )

    return_date = models.CharField(
        default=None,
        blank=True,
        null=True,
        verbose_name="Дата возврата книги",
        help_text="Введите дату и время возврата книги в формате 'ДД.ММ.ГГГГ ЧЧ:ММ' или оставьте пустым, если книга не взята",
    )

    given_to = models.ForeignKey(
        "users.User",
        on_delete=CASCADE,
        blank=True,
        null=True,
        verbose_name="Выдана пользователю",
        help_text="Выберите пользователя, которому выдана книга",
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title
