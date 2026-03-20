from django.urls import path
from .views import (
    RecommendationView,
    NextLessonView,
    PeerMatchingView,
)

app_name = "ai_engine"  # Namespacing for reverse lookups

urlpatterns = [
    # Returns AI-generated lesson recommendations for the logged-in user
    path("recommendations/", RecommendationView.as_view(), name="recommendations"),
    
    # Returns the next lesson(s) selected by the tutor agent
    path("next_lesson/", NextLessonView.as_view(), name="next_lesson"),
    
    # Returns a list of recommended study partners for the user
    path("peer_matching/", PeerMatchingView.as_view(), name="peer_matching"),
]
