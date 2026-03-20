from django.urls import path
from .views import (
    UserDetailView,
    UserProgressListView,
    LearningStyleListView,
    UserLearningStyleListView,
    InterestListView,
    UserInterestListView,
)

urlpatterns = [
    path("me/", UserDetailView.as_view(), name="user-detail"),
    path("progress/", UserProgressListView.as_view(), name="user-progress"),
    path("learning-styles/", LearningStyleListView.as_view(), name="learning-styles"),
    path("user-learning-styles/", UserLearningStyleListView.as_view(), name="user-learning-styles"),
    path("interests/", InterestListView.as_view(), name="interests"),
    path("user-interests/", UserInterestListView.as_view(), name="user-interests"),
]
