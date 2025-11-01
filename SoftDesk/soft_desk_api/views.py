from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status

from soft_desk_api.serializers import (
    ProjectSerializer,
    ProjectDetailSerializer,
    IssueSerializer,
    IssueDetailSerializer,
    CommentSerializer,
    CommentDetailSerializer
    )
from soft_desk_api.models import Project, Contributor, Issue, Comment
from .permissions import IsAuthor, IsContributor
from custom_auth.models import User


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            if self.detail_serializer_class is not None:
                return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(author=user) | Q(contributors__user=user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
        return super().perform_create(serializer)

    @action(detail=True, methods=['PATCH'], url_name='add_contributors')
    def add_contributors(self, request, pk=None):
        project = self.get_object()
        usernames = request.data.get('usernames', [])
        usernames = usernames.split(', ')
        for username in usernames:
            user, error_message = check_user_exists(username)
            if error_message:
                return handle_contributor_response(error_message,
                                                   status.HTTP_400_BAD_REQUEST)
            try:
                Contributor.objects.create(user=user, project=project)
            except IntegrityError:
                error_message = f'{username} is already a contributor'
                return handle_contributor_response(error_message,
                                                   status.HTTP_400_BAD_REQUEST)
        data = {'detail': 'Contributor(s) created successfully'}
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PATCH'], url_name='remove_contributors')
    def remove_contributors(self, request, pk=None):
        project = self.get_object()
        usernames = request.data.get('usernames', [])
        usernames = usernames.split(', ')
        for username in usernames:
            user, error_message = check_user_exists(username)
            if error_message:
                return handle_contributor_response(error_message,
                                                   status.HTTP_400_BAD_REQUEST)
            contributor, error_message = check_contributor_exists(user,
                                                                  project)
            if error_message:
                return handle_contributor_response(error_message,
                                                   status.HTTP_400_BAD_REQUEST)
            contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated, (IsAuthor | IsContributor)]

    def get_queryset(self):
        user = self.request.user
        project_author = Q(project__author=user)
        project_contributor = Q(project__contributors__user=user)
        return Issue.objects.filter(
            project_author | project_contributor,
            project_id=self.kwargs['project_pk']).distinct()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_id'] = self.kwargs['project_pk']
        return context

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.context['project_id'] = self.kwargs['project_pk']
        author = self.request.user
        attribution = serializer.validated_data.get('attribution')
        serializer.save(project=project,
                        author=author,
                        attribution=attribution)
        return super().perform_create(serializer)


class CommentViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentSerializer
    detail_serializer_class = CommentDetailSerializer

    permission_classes = [IsAuthenticated, (IsAuthor | IsContributor)]

    def get_queryset(self):
        user = self.request.user
        project_author = Q(issue__project__author=user)
        project_contributor = Q(issue__project__contributors__user=user)
        return Comment.objects.filter(
            project_author | project_contributor,
            issue_id=self.kwargs['issue_pk']).distinct()

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        author = self.request.user
        serializer.save(author=author, issue=issue)
        return super().perform_create(serializer)


def check_user_exists(username):
    try:
        user = User.objects.get(username=username)
        return user, None
    except User.DoesNotExist:
        return None, f"{username} is not a User"


def check_contributor_exists(user, project):
    try:
        contributor = Contributor.objects.get(user=user, project=project)
        return contributor, None
    except Contributor.DoesNotExist:
        return None, f"{user.username} is not a contributor to this project"


def handle_contributor_response(message, status_code):
    """ Helper function to handle repetitive response structure """
    return Response({'content': message}, status=status_code)
