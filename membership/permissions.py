from rest_framework.permissions import BasePermission


class IsAdminOrSuperAdmin(BasePermission):
    """Allow access only to users with role 'admin' or 'superadmin'."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role in ['admin', 'superadmin']
        )
