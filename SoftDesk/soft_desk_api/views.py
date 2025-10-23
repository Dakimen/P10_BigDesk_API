from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from soft_desk_api.serializers import ProjectSerializer
from soft_desk_api.models import Project, Contributor
from .permissions import IsProjectAuthorPermission


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated, IsProjectAuthorPermission]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(author=user) | Q(contributors__user=user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
        return super().perform_create(serializer)
