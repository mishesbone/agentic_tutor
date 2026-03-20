from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Optional: DRF routers (if using ViewSets)
router = DefaultRouter()

# Example:
# from apps.learning.views import TopicViewSet
# router.register(r'topics', TopicViewSet, basename='topics')

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API root
    path("api/", include(router.urls)),

    # App endpoints
    path("api/users/", include("apps.users.urls")),
    path("api/learning/", include("apps.learning.urls")),
    path("api/assessment/", include("apps.assessment.urls")),
    path("api/ai/", include("apps.ai_engine.urls")),
    path("api/collaboration/", include("apps.collaboration.urls")),
    path("api/gamification/", include("apps.gamification.urls")),

    # Auth (JWT)
    path("api/auth/", include("apps.users.auth_urls")),

    # DRF browsable API login (optional)
    path("api-auth/", include("rest_framework.urls")),
]