from rest_framework import serializers
from .models import User, UserProgress, LearningStyle, UserLearningStyle, Interest, UserInterest
from apps.learning.models import Subject


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "email", "username", "overall_score", "streak_days",
            "last_active", "learning_styles", "interests",
        ]


class UserProgressSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = UserProgress
        fields = [
            "id", "user", "subject", "subject_name", "proficiency",
            "attempts", "correct_answers", "average_response_time",
            "last_practiced",
        ]


class LearningStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningStyle
        fields = ["id", "name"]


class UserLearningStyleSerializer(serializers.ModelSerializer):
    style_name = serializers.CharField(source="style.name", read_only=True)

    class Meta:
        model = UserLearningStyle
        fields = ["id", "user", "style", "style_name", "weight"]


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ["id", "name"]


class UserInterestSerializer(serializers.ModelSerializer):
    interest_name = serializers.CharField(source="interest.name", read_only=True)

    class Meta:
        model = UserInterest
        fields = ["id", "user", "interest", "interest_name"]
