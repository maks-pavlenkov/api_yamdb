from rest_framework.permissions import BasePermission


class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin_or_superuser)
