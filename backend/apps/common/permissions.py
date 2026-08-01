from rest_framework import permissions
from apps.common.enums import UserType


class IsSuperAdmin(permissions.BasePermission):
    """Allows access only to Super Admins."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.user_type == UserType.SUPERADMIN or request.user.is_superuser)
        )


class IsAdminUserOrSuperAdmin(permissions.BasePermission):
    """Allows access to Admin and SuperAdmin users."""
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type in [UserType.ADMIN, UserType.SUPERADMIN]
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.user_type in [UserType.ADMIN, UserType.SUPERADMIN]:
            return True
        
        # Check if user matches object user or member
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'user_id'):
            return obj.user_id == request.user.id
            
        return False
