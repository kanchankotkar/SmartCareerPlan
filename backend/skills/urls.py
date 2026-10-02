from django.urls import path

from .views import (
    SkillListView,
    AddUserSkillView,
    MySkillsView
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

]