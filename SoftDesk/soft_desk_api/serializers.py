"""
File containing serializers used by the soft_desk_api app.
"""
from rest_framework.serializers import ModelSerializer, ReadOnlyField

from soft_desk_api.models import Project


class ProjectSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')
    id = ReadOnlyField()

    class Meta:
        model = Project
        fields = ['id', 'author', 'name', 'description', 'created_at',
                  'updated_at', 'project_type']
