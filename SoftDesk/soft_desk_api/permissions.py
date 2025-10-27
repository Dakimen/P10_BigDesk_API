"""
This module defines permission classes for the api.
"""
from rest_framework.permissions import (
    IsAuthenticated, BasePermission, SAFE_METHODS
    )


class IsAuthorPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return True
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.author == request.user:
                return True
            else:
                return False


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
