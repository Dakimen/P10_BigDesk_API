from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status

from soft_desk_api.serializers import ProjectSerializer, ProjectDetailSerializer
from soft_desk_api.models import Project, Contributor
from .permissions import IsAuthorPermission, IsAdminUser
from custom_auth.models import User


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated, IsAuthorPermission | IsAdminUser]

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
