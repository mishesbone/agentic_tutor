from django.urls import path
from .views import (
    SubjectListView,
    TopicListView,
    SubTopicListView,
    LessonListView,
    PrerequisiteListView
)

urlpatterns = [
    path("subjects/", SubjectListView.as_view(), name="subject-list"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("subtopics/", SubTopicListView.as_view(), name="subtopic-list"),
    path("lessons/", LessonListView.as_view(), name="lesson-list"),
    path("prerequisites/", PrerequisiteListView.as_view(), name="prerequisite-list"),
]
