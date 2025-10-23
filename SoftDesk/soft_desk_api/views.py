from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from soft_desk_api.serializers import ProjectSerializer
from soft_desk_api.models import Project


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()
