from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model for the Agentic AI Tutor system
    """

    email = models.EmailField(unique=True)

    # Aggregate performance score across all subjects
    overall_score = models.FloatField(default=0.0)

    # Engagement tracking
    streak_days = models.PositiveIntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Preferences (kept flexible for early-stage scaling)
    learning_styles = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def update_last_active(self):
        self.last_active = timezone.now()
        self.save(update_fields=["last_active"])

    def __str__(self):
        return self.email


class UserProgress(models.Model):
    """
    Tracks user proficiency and performance per subject
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="progress"
    )

    subject = models.ForeignKey(
        "learning.Subject",
        on_delete=models.CASCADE,
        related_name="user_progress"
    )

    # Core learning metrics
    proficiency = models.FloatField(default=0.0)  # 0 → 1 scale
    attempts = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)

    # Advanced tracking
    average_response_time = models.FloatField(default=0.0)  # seconds
    last_practiced = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "subject")
        indexes = [
            models.Index(fields=["user", "subject"]),
            models.Index(fields=["proficiency"]),
        ]

    def accuracy(self):
        if self.attempts == 0:
            return 0.0
        return self.correct_answers / self.attempts

    def update_progress(self, is_correct: bool, response_time: float = None):
        """
        Update user progress dynamically (used by AI tutor system)
        """
        self.attempts += 1

        if is_correct:
            self.correct_answers += 1
            self.proficiency = min(1.0, self.proficiency + 0.05)
        else:
            self.proficiency = max(0.0, self.proficiency - 0.02)

        if response_time:
            # Running average update
            total_time = self.average_response_time * (self.attempts - 1)
            self.average_response_time = (total_time + response_time) / self.attempts

        self.last_practiced = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.subject.name}"


class LearningStyle(models.Model):
    """
    Normalized learning styles for analytics and AI modeling
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class UserLearningStyle(models.Model):
    """
    Many-to-many mapping for structured learning preferences
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_learning_styles"
    )

    style = models.ForeignKey(
        LearningStyle,
        on_delete=models.CASCADE,
        related_name="users"
    )

    weight = models.FloatField(default=1.0)  # importance of this style

    class Meta:
        unique_together = ("user", "style")

    def __str__(self):
        return f"{self.user.email} - {self.style.name}"


class Interest(models.Model):
    """
    Structured interests for better recommendations
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserInterest(models.Model):
    """
    Many-to-many mapping for user interests
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_interests"
    )

    interest = models.ForeignKey(
        Interest,
        on_delete=models.CASCADE,
        related_name="users"
    )

    class Meta:
        unique_together = ("user", "interest")

    def __str__(self):
        return f"{self.user.email} - {self.interest.name}"