"""
URL configuration for SoftDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from rest_framework_nested.routers import NestedSimpleRouter

from custom_auth.views import UserCreateView
from soft_desk_api.views import ProjectViewset, IssueViewset, CommentViewset

router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects')

projects_router = NestedSimpleRouter(router, 'projects',
                                     lookup='project')
projects_router.register('issues', IssueViewset, basename='issues')

issues_router = NestedSimpleRouter(projects_router, 'issues', lookup='issue')
issues_router.register('comments', CommentViewset, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', UserCreateView.as_view(), name='register'),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/', include(issues_router.urls)),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
