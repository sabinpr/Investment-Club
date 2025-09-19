from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsMember(BasePermission):
    """Allow access only to authenticated users with role 'member'."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'member')


class IsAdminOrSuperAdmin(BasePermission):
    """Allow access only to users with role 'admin' or 'superadmin'."""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and
            request.user.role in ['admin', 'superadmin']
        )


class IsSelfOrAdmin(BasePermission):
    """
    Allow access to the object owner (self) or users with role 'admin' or 'superadmin'.
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.is_authenticated and (
                obj == request.user or request.user.role in ['admin', 'superadmin']
            )
        )


class IsAdminOrMemberGetPostOnly(BasePermission):
    """
    - Admin/SuperAdmin: allow all HTTP methods
    - Member: allow only GET and POST methods
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.role in ['admin', 'superadmin']:
            return True

        if user.role == 'member' and request.method in ['GET', 'POST']:
            return True

        return False


class IsAdminOrReadOnly(BasePermission):
    """
    Allow full access to users with role 'admin' or 'superadmin'.
    Allow only safe methods (GET, HEAD, OPTIONS) to others.
    """
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated and user.role in ['admin', 'superadmin']:
            return True
        return request.method in SAFE_METHODS
