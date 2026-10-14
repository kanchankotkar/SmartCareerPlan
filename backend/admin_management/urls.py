from django.urls import path

from .views import (
    AdminUserListView,
    AdminUserUpdateView,
    AdminJobRoleCreateView,
    AdminJobRoleSkillCreateView,
    AdminLearningResourceCreateView,
    AdminLearningResourceBySkillView,
    AdminLearningResourceUpdateView,
    AdminJobRoleListView,
    AdminLearningResourceUpdateView,
    AdminJobRoleUpdateView,
    AdminJobRoleDeleteView,
    AdminJobRoleSkillsListView,
    AdminJobRoleSkillUpdateView,
    AdminJobRoleSkillDeleteView,
    AdminSkillListView,
    AdminSkillCreateView,
    AdminSkillUpdateView,
    AdminSkillDeleteView,
    AdminDashboardStatsView,
    AdminUserDeleteView,
)


urlpatterns = [

    path(
        'users/',
        AdminUserListView.as_view(),
        name='admin-users'
    ),

    path(
    'users/<int:user_id>/',
    AdminUserUpdateView.as_view(),
    name='admin-update-user'
    ),

    path(
    'users/<int:user_id>/delete/',
    AdminUserDeleteView.as_view(),
    name='admin-delete-user'
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
        name='admin-learning-resources'
    ),

    path(
        'learning-resources/skill/<int:skill_id>/',
        AdminLearningResourceBySkillView.as_view(),
        name='admin-learning-resources-by-skill'
    ),

    path(
        'learning-resources/<int:resource_id>/',
        AdminLearningResourceUpdateView.as_view(),
        name='admin-update-learning-resource'
    ),

    path(
    'job-roles/list/',
    AdminJobRoleListView.as_view(),
    name='admin-job-role-list'
   ),

    path(
        'learning-resources/<int:resource_id>/',
        AdminLearningResourceUpdateView.as_view(),
        name='admin-update-learning-resource'
    ),
    path(
    'job-roles/<int:role_id>/',
      AdminJobRoleUpdateView.as_view(),
       name='admin-update-job-role'
    ),

    path(
    'job-roles/<int:role_id>/delete/',
    AdminJobRoleDeleteView.as_view(),
    name='admin-delete-job-role'
    ), 

    path(
    'job-roles/<int:role_id>/skills/',
    AdminJobRoleSkillsListView.as_view(),
    name='admin-job-role-skills-list'
    ), 
    path(
    'job-role-skills/<int:role_skill_id>/',
    AdminJobRoleSkillUpdateView.as_view(),
    name='admin-update-job-role-skill'
    ),

    path(
    'job-role-skills/<int:role_skill_id>/delete/',
    AdminJobRoleSkillDeleteView.as_view(),
    name='admin-delete-job-role-skill'
    ),

    path(
    'skills/',
    AdminSkillListView.as_view(),
    name='admin-skills'
   ),

   path(
    'skills/create/',
    AdminSkillCreateView.as_view(),
    name='admin-create-skill'
    ),
    path(
    'skills/<int:skill_id>/',
    AdminSkillUpdateView.as_view(),
    name='admin-update-skill'
    ),

    path(
    'skills/<int:skill_id>/delete/',
    AdminSkillDeleteView.as_view(),
    name='admin-delete-skill'
    ),

    path(
    'dashboard/stats/',
    AdminDashboardStatsView.as_view(),
    name='admin-dashboard-stats'
    ),


]