from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу профиля.
    """

    def has_permission(self, request, view):
        # На уровне запроса пускаем любого авторизованного пользователя
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # На уровне объекта проверяем, что это профиль текущего пользователя
        return obj == request.user


class IsLibrarian(permissions.BasePermission):
    """
    Разрешает доступ пользователям из группы 'librarians'.
    """

    def _is_librarian(self, request):
        # Безопасная проверка: пользователь должен быть авторизован и состоять в группе
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name="librarians").exists()

    def has_permission(self, request, view):
        # Общая проверка при входе на эндпоинт
        return self._is_librarian(request)

    def has_object_permission(self, request, view, obj):
        # При проверке конкретного объекта библиотекарь тоже имеет доступ
        return self._is_librarian(request)


class IsOwnerOrLibrarian(permissions.BasePermission):
    """
    Разрешает доступ только владельцу профиля или библиотекарю.
    Комбинирует IsOwner и IsLibrarian с OR логикой.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Доступ если владелец или библиотекарь
        is_owner = obj == request.user
        is_librarian = request.user.groups.filter(name="librarians").exists()
        return is_owner or is_librarian
