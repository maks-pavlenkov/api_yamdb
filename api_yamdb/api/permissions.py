from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin_or_superuser)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view): # без has_permission падает 7 тестов
        return (request.method in SAFE_METHODS
        or (request.user.is_authenticated
            and request.user.is_admin_or_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin_or_superuser)) # надо подумать, точно sfaff сюда или admin_or_superuser


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AuthorAdminModeratorOrReadOnly(BasePermission):

# Без этого has_permission падают 2 теста на анонов
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin_or_superuser
        )
