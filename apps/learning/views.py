from rest_framework import generics, permissions
from .models import Subject, Topic, SubTopic, Lesson, Prerequisite
from .serializers import SubjectSerializer, TopicSerializer, SubTopicSerializer, LessonSerializer, PrerequisiteSerializer


# ----------------------------
# Subjects
# ----------------------------
class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


# ----------------------------
# Topics
# ----------------------------
class TopicListView(generics.ListAPIView):
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        subject_id = self.request.query_params.get("subject_id")
        queryset = Topic.objects.all()
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)
        return queryset


# ----------------------------
# SubTopics
# ----------------------------
class SubTopicListView(generics.ListAPIView):
    serializer_class = SubTopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic_id")
        queryset = SubTopic.objects.all()
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        return queryset


# ----------------------------
# Lessons
# ----------------------------
class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        subtopic_id = self.request.query_params.get("subtopic_id")
        queryset = Lesson.objects.filter(is_active=True, approved=True)
        if subtopic_id:
            queryset = queryset.filter(subtopic_id=subtopic_id)
        return queryset


# ----------------------------
# Prerequisites
# ----------------------------
class PrerequisiteListView(generics.ListAPIView):
    serializer_class = PrerequisiteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        lesson_id = self.request.query_params.get("lesson_id")
        queryset = Prerequisite.objects.all()
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        return queryset
