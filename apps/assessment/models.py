from django.db import models
from apps.learning.models import Topic, SubTopic
from apps.users.models import User


class Question(models.Model):
    """
    Represents a learning assessment question
    """

    QUESTION_TYPES = (
        ("mcq", "Multiple Choice"),
        ("text", "Text Answer"),
        ("code", "Code Submission"),
    )

    DIFFICULTY_LEVELS = (
        (1, "Beginner"),
        (2, "Intermediate"),
        (3, "Advanced"),
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    subtopic = models.ForeignKey(
        SubTopic,
        on_delete=models.CASCADE,
        related_name="questions",
        null=True,
        blank=True
    )

    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default="text")
    difficulty = models.IntegerField(choices=DIFFICULTY_LEVELS, default=1)

    # For multiple choice questions
    choices = models.JSONField(blank=True, null=True)  # [{"id":1,"text":"A"}, {"id":2,"text":"B"}]

    # Correct answer(s)
    answer = models.JSONField(blank=True, null=True)  # [1] or ["42"] depending on type

    # Optional explanation for feedback
    explanation = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["topic", "difficulty"]),
            models.Index(fields=["subtopic", "difficulty"]),
        ]

    def __str__(self):
        return f"{self.topic.name} - {self.text[:50]}"


class Attempt(models.Model):
    """
    Records each user attempt for a question
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="attempts")

    # Result
    correct = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)  # can be fractional

    # Metadata for AI / analytics
    response = models.JSONField(blank=True, null=True)  # user input / choice
    time_taken = models.FloatField(default=0.0)  # seconds
    hints_used = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "question"]),
            models.Index(fields=["question", "created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.question.text[:30]} - {'Correct' if self.correct else 'Wrong'}"