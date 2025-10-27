"""
File containing serializers used by the soft_desk_api app.
"""
from rest_framework.serializers import (
    ModelSerializer, CharField, SlugRelatedField
    )

from soft_desk_api.models import Project, Contributor


class ContributorSerializer(ModelSerializer):
    username = CharField(source='user.username', read_only=True)

    class Meta:
        model = Contributor
        fields = ['username', 'id']
        read_only_fields = ['username', 'id']


class ProjectSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Project
        fields = ['name', 'id', 'author']
        read_only_fields = ['author', 'id']


class ProjectDetailSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['author', 'id', 'created_at', 'updated_at']
