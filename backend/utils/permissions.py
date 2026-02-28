from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Allow write access only to admin users."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class HasModulePermission(BasePermission):
    """Check user has permission for the module specified on the view."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        module = getattr(view, 'permission_module', None)
        if not module:
            return True
        if request.user.is_superuser:
            return True
        role = getattr(request.user, 'role', None)
        if not role:
            return False
        return role.permissions.filter(module=module).exists()


class IsSuperUser(BasePermission):
    """Allow access only to superusers."""

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsOwnerOrAdmin(BasePermission):
    """Allow access to object owner or admin users."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        owner_field = getattr(view, 'owner_field', 'created_by')
        owner = getattr(obj, owner_field, None)
        return owner == request.user
