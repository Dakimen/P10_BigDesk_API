"""
File containing serializers used by the soft_desk_api app.
"""
from rest_framework.serializers import ModelSerializer

from soft_desk_api.models import Project


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['author', 'name', 'description', 'created_at',
                  'updated_at', 'project_type']
