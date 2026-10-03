from django.urls import path

from .views import (
    AdminUserListView,
    AdminJobRoleCreateView,
    AdminJobRoleSkillCreateView,
    AdminLearningResourceCreateView
)


urlpatterns = [

    path(
        'users/',
        AdminUserListView.as_view(),
        name='admin-users'
    ),

    path(
        'job-roles/',
        AdminJobRoleCreateView.as_view(),
        name='admin-create-job-role'
    ),

    path(
        'job-role-skills/',
        AdminJobRoleSkillCreateView.as_view(),
        name='admin-add-job-role-skill'
    ),
    path(
    'learning-resources/',
    AdminLearningResourceCreateView.as_view(),
    name='admin-create-learning-resource'
    ),

]