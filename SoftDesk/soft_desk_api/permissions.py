"""
This module defines permission classes for the api.
"""
from rest_framework.permissions import (
    IsAuthenticated, BasePermission, SAFE_METHODS
    )
from soft_desk_api.models import Contributor, Project, Issue, Comment


class IsAuthor(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(obj.author == request.user)


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        project = get_project(obj)
        if is_contributor_verifier(user, project):
            if request.method in SAFE_METHODS:
                return True
            elif request.method in ['PATCH']:
                return True
            elif request.method in ['POST', 'DELETE', 'PUT']:
                return False


def get_project(obj):
    if isinstance(obj, Project):
        return obj
    elif isinstance(obj, Issue):
        return obj.project
    elif isinstance(obj, Comment):
        return obj.issue.project
    else:
        return None


def is_contributor_verifier(user, project):
    return Contributor.objects.filter(user=user, project=project).exists()
