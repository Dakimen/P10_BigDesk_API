"""
This module defines permission classes for the api.
"""
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import PermissionDenied


class IsProjectAuthorPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            if obj.author != request.user:
                raise PermissionDenied(
                    "You do not have permission to modify this project."
                    )
        return True


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
