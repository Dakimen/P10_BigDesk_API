from django.db import models
from custom_auth.models import User
import uuid


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='contributors')
    project = models.ForeignKey('Project', on_delete=models.CASCADE,
                                related_name='contributors')

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.name}"


class Project(models.Model):
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('android', 'Android')
    ]

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='project_author')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_type = models.CharField(choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Issue(models.Model):
    STATUS_CHOICES = [
        ('to do', 'To Do'),
        ('in progress', 'In Progress'),
        ('finished', 'Finished')
    ]

    PRIORITY_CHOICES = [
        ('low', 'LOW'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    FLAG_CHOICES = [
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('task', 'Task')
    ]

    author = models.ForeignKey(Contributor, on_delete=models.CASCADE,
                               related_name='issue_author')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,
                                related_name='issues')
    status = models.CharField(choices=STATUS_CHOICES,
                              default='to do')
    priority = models.CharField(choices=PRIORITY_CHOICES,
                                default='low')
    attribution = models.ForeignKey(Contributor, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='issues')
    flag = models.CharField(choices=FLAG_CHOICES,
                            default='task')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status} - {self.priority}"


class Comment(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE,
                              related_name='comments')
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE,
                               related_name='comment_author')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.issue}"
