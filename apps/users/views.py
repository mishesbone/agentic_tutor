from rest_framework import generics, permissions
from .models import User, UserProgress, LearningStyle, UserLearningStyle, Interest, UserInterest
from .serializers import (
    UserSerializer, UserProgressSerializer, LearningStyleSerializer,
    UserLearningStyleSerializer, InterestSerializer, UserInterestSerializer
)


# ----------------------------
# User Views
# ----------------------------
class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ----------------------------
# User Progress Views
# ----------------------------
class UserProgressListView(generics.ListAPIView):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)


# ----------------------------
# Learning Styles Views
# ----------------------------
class LearningStyleListView(generics.ListAPIView):
    queryset = LearningStyle.objects.all()
    serializer_class = LearningStyleSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserLearningStyleListView(generics.ListAPIView):
    serializer_class = UserLearningStyleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserLearningStyle.objects.filter(user=self.request.user)


# ----------------------------
# Interests Views
# ----------------------------
class InterestListView(generics.ListAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserInterestListView(generics.ListAPIView):
    serializer_class = UserInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user)
