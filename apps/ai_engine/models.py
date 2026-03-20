from django.db import models
from apps.users.models import User
from apps.learning.models import Lesson, SubTopic

class AIRecommendation(models.Model):
    """
    Logs AI-generated lesson recommendations for a user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(SubTopic, on_delete=models.SET_NULL, null=True, blank=True)
    score = models.FloatField(help_text="Confidence or relevance score")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "score"]),
        ]

    def __str__(self):
        return f"Recommendation for {self.user.email} -> {self.lesson.title} ({self.score})"