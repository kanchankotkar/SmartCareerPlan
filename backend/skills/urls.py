from django.urls import path

from .views import (
    SkillListView,
    AddUserSkillView,
    MySkillsView,
    UserSkillUpdateView,
    UserSkillDeleteView,
)


urlpatterns = [

    path(
        '',
        SkillListView.as_view(),
        name='skill-list'
    ),

    path(
        'user/',
        AddUserSkillView.as_view(),
        name='add-user-skill'
    ),

    path(
    'user/my/',
    MySkillsView.as_view(),
    name='my-skills'
    ),
    path(
    'user/<int:user_skill_id>/',
    UserSkillUpdateView.as_view(),
    name='user-skill-update'
    ),
   path(
        "user/<int:user_skill_id>/delete/",
        UserSkillDeleteView.as_view(),
        name="user-skill-delete",
    ),

]