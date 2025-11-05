"""
File containing serializers used by the soft_desk_api app.
"""
from rest_framework.serializers import (
    ModelSerializer, CharField, SlugRelatedField, SerializerMethodField
    )
from rest_framework.exceptions import ValidationError

from soft_desk_api.models import Project, Contributor, Issue, Comment
from custom_auth.models import User


class ContributorSerializer(ModelSerializer):
    username = CharField(source='user.username', read_only=True)

    class Meta:
        model = Contributor
        fields = ['username']
        read_only_fields = ['username']


class CommentSerializer(ModelSerializer):
    author = CharField(source='author.user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'uuid', 'author', 'description', 'created_at']
        read_only_fields = ['id', 'uuid', 'author', 'created_at']


class CommentDetailSerializer(ModelSerializer):
    author = CharField(source='author.user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'uuid', 'issue', 'author', 'description',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'uuid', 'issue', 'author',
                            'created_at', 'updated_at']


class IssueSerializer(ModelSerializer):
    attribution = CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    description = CharField(
        allow_blank=True, allow_null=True, write_only=True, required=False
    )

    class Meta:
        model = Issue
        fields = ['id', 'name', 'status', 'attribution', 'description']
        read_only_fields = ['id']

    def validate_attribution(self, value):
        contributor = check_contributor(self.context['project_id'], value)
        return contributor


class IssueLightSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'name', 'status']
        read_only_fields = ['id']

    def validate_attribution(self, value):
        contributor = check_contributor(self.context['project_id'], value)
        return contributor


class IssueDetailSerializer(ModelSerializer):
    attribution = CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    author = CharField(source='author.user.username', read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_attribution(self, value):
        contributor = check_contributor(self.context['project_id'], value)
        return contributor


class ProjectSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    description = CharField(
        allow_blank=True, allow_null=True, write_only=True, required=False
    )
    project_type = CharField(write_only=True, required=True)

    class Meta:
        model = Project
        fields = ['name', 'id', 'author', 'description', 'project_type']
        read_only_fields = ['author', 'id']


class ProjectDetailSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    contributors = ContributorSerializer(many=True, read_only=True)
    issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['author', 'id', 'created_at',
                            'updated_at', 'issues']

    def get_issues(self, obj):
        queryset = obj.issues.filter(status__in=['to do', 'in progress'])
        return IssueLightSerializer(queryset, many=True).data


def check_contributor(project_id, value):
    if not value:
        return None
    try:
        user = User.objects.get(username=value)
    except User.DoesNotExist:
        raise ValidationError(
            f"User with username '{value}' does not exist."
            )
    try:
        contributor = Contributor.objects.get(
            user=user, project=project_id
            )
    except Contributor.DoesNotExist:
        raise ValidationError(
            f"User '{value}' is not a contributor to this project."
            )
    return contributor
