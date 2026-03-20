from django.db import models
from apps.users.models import User
from apps.learning.models import Lesson, SubTopic


class Badge(models.Model):
    """
    Represents a badge / achievement a user can earn
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """
    Tracks badges earned by a user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="users")
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "badge")
        indexes = [
            models.Index(fields=["user", "earned_at"]),
        ]

    def __str__(self):
        return f"{self.user.email} earned {self.badge.name}"


class PointEvent(models.Model):
    """
    Records point-earning actions by users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="point_events")
    points = models.IntegerField(default=0)
    action = models.CharField(max_length=200)  # e.g., "completed_lesson", "answered_correctly"
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True)
    subtopic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["points"]),
        ]

    def __str__(self):
        return f"{self.user.email} +{self.points} pts for {self.action}"


class Level(models.Model):
    """
    Represents user levels in the gamification system
    """
    level_number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    min_points = models.PositiveIntegerField(help_text="Minimum points required to reach this level")

    class Meta:
        ordering = ["level_number"]

    def __str__(self):
        return f"Level {self.level_number}: {self.name}"


class UserLevel(models.Model):
    """
    Tracks current level of each user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="level")
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)  # current total points
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.level.name} ({self.points} pts)"