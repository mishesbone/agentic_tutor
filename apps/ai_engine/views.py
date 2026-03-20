from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.ai_engine.services.recommendation import recommend_lessons
from apps.ai_engine.services.tutor_agent import generate_next_lesson
from apps.ai_engine.services.peer_matching import find_study_partners
from apps.ai_engine.serializers import LessonSerializer

class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lessons = recommend_lessons(request.user, limit=5)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class NextLessonView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lessons = generate_next_lesson(request.user)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class PeerMatchingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subtopic_id = request.query_params.get("subtopic_id")
        if not subtopic_id:
            return Response({"error": "subtopic_id query param required"}, status=400)

        matched_users = find_study_partners(request.user, subtopic_id)
        data = [{"id": u.id, "email": u.email, "name": u.full_name} for u in matched_users]
        return Response(data)
