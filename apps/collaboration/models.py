from django.db import models
from apps.users.models import User
from apps.learning.models import Lesson


class StudyRoom(models.Model):
    """
    Represents a collaborative study room
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)

    # Owner of the room
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_rooms"
    )

    # Optional linked lesson for topic-focused study
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="study_rooms"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["owner"]),
        ]

    def __str__(self):
        return self.name


class RoomMember(models.Model):
    """
    Tracks users in a study room
    """
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_rooms")

    joined_at = models.DateTimeField(auto_now_add=True)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        unique_together = ("room", "user")
        indexes = [
            models.Index(fields=["room", "user"]),
        ]

    def __str__(self):
        return f"{self.user.email} in {self.room.name}"


class PeerReview(models.Model):
    """
    Allows users to review content or performance of peers
    """
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews_given"
    )
    reviewee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews_received"
    )

    room = models.ForeignKey(
        StudyRoom,
        on_delete=models.CASCADE,
        related_name="peer_reviews"
    )

    rating = models.PositiveSmallField(default=5)  # 1-5 scale
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "reviewee", "room")
        indexes = [
            models.Index(fields=["reviewer", "reviewee"]),
            models.Index(fields=["room"]),
        ]

    def __str__(self):
        return f"{self.reviewer.email} → {self.reviewee.email} ({self.rating})"


class ActivityLog(models.Model):
    """
    Tracks user actions for analytics and AI personalization
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_logs")
    room = models.ForeignKey(StudyRoom, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=200)  # e.g., "joined_room", "sent_message"
    metadata = models.JSONField(blank=True, null=True)  # extra info

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["room", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"