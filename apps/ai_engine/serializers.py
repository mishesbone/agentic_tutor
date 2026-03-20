from rest_framework import serializers
from apps.ai_engine.models import AIRecommendation
from apps.learning.models import Lesson, SubTopic

class LessonSerializer(serializers.ModelSerializer):
    subtopic = serializers.CharField(source="subtopic.name")

    class Meta:
        model = Lesson
        fields = ["id", "title", "subtopic", "difficulty", "estimated_time"]

class AIRecommendationSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)
    subtopic = serializers.CharField(source="subtopic.name", read_only=True)

    class Meta:
        model = AIRecommendation
        fields = ["id", "lesson", "subtopic", "score", "created_at"]
