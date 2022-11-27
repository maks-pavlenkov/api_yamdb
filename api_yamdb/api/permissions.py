from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin_or_superuser)
