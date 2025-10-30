from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
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
from .permissions import IsAuthor, IsAdminUser, IsContributor
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

    permission_classes = [IsAuthenticated, IsAuthor | IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(author=user) | Q(contributors__user=user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
        return super().perform_create(serializer)

    @action(detail=True, methods=['PUT'], url_name='add_contributors')
    def add_contributors(self, request, pk=None):
        project = self.get_object()
        usernames = request.data.get('usernames', [])
        usernames = usernames.split(', ')
        users = []
        for username in usernames:
            user = User.objects.get(username=username)
            users.append(user)
        contributors = []
        for user in users:
            contributor = Contributor.objects.create(user=user,
                                                     project=project)
            contributors.append(contributor)
        data = {'detail': 'Contributor(s) created successfully'}
        return Response(data=data, status=status.HTTP_201_CREATED)


class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated, (IsAuthor | IsContributor)]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project_id'] = self.kwargs['project_pk']
        return context

    def perform_create(self, serializer):
        project = Project.objects.get(pk=self.kwargs['project_pk'])
        serializer.context['project_id'] = self.kwargs['project_pk']
        author = Contributor.objects.get(user=self.request.user,
                                         project=project)
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
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_pk'])
        project = issue.project
        author = Contributor.objects.get(user=self.request.user,
                                         project=project)
        serializer.save(author=author, issue=issue)
        return super().perform_create(serializer)
