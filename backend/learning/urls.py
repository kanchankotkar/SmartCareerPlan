from django.urls import path

from .views import (
    LearningRoadmapView,
    LearningProgressView
)


urlpatterns = [

    path(
        'roadmap/',
        LearningRoadmapView.as_view(),
        name='learning-roadmap'
    ),

    path(
        'progress/',
        LearningProgressView.as_view(),
        name='learning-progress'
    ),
]