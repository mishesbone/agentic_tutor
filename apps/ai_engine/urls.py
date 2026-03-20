from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.ai_engine.services import recommend_lessons

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        lessons = recommend_lessons(user, limit=5)
        data = [{"id": l.id, "title": l.title, "subtopic": l.subtopic.name} for l in lessons]
        return Response(data)