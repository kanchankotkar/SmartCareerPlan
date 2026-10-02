from django.urls import path

from .views import (
    JobRoleListView,
    RequiredSkillsView,
    SkillGapAnalysisView
)

urlpatterns = [

    path(
        '',
        JobRoleListView.as_view(),
        name='job-role-list'
    ),

    path(
        '<int:role_id>/skills/',
        RequiredSkillsView.as_view(),
        name='required-skills'
    ),

    path(
        'skill-gap/analyze/',
        SkillGapAnalysisView.as_view(),
        name='skill-gap-analysis'
    ),

]