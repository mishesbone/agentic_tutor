from rest_framework import serializers
from .models import Subject, Topic, SubTopic, Lesson, Prerequisite


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name", "description"]


class TopicSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source="subject.name", read_only=True)

    class Meta:
        model = Topic
        fields = ["id", "subject", "subject_name", "name", "description", "order"]


class SubTopicSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source="topic.name", read_only=True)
    subject_name = serializers.CharField(source="topic.subject.name", read_only=True)

    class Meta:
        model = SubTopic
        fields = ["id", "topic", "topic_name", "subject_name", "name", "order"]


class LessonSerializer(serializers.ModelSerializer):
    subtopic_name = serializers.CharField(source="subtopic.name", read_only=True)
    topic_name = serializers.CharField(source="subtopic.topic.name", read_only=True)
    subject_name = serializers.CharField(source="subtopic.topic.subject.name", read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id", "title", "content", "difficulty", "estimated_time",
            "order", "is_active", "version", "language", "approved",
            "subtopic", "subtopic_name", "topic_name", "subject_name"
        ]


class PrerequisiteSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    required_lesson_title = serializers.CharField(source="required_lesson.title", read_only=True)

    class Meta:
        model = Prerequisite
        fields = ["id", "lesson", "lesson_title", "required_lesson", "required_lesson_title"]
