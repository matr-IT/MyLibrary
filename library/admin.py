from django.contrib import admin

from library.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "is_checked_out", "genre", "publication_date", "return_date")
    search_fields = ("title", "author__name", "genre")
    list_filter = ("is_checked_out", "genre")
    readonly_fields = ("return_date",)
