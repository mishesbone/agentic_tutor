from django.db import models


class Subject(models.Model):
    """
    Top-level category (e.g. Math, Science, Programming)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Topic(models.Model):
    """
    Mid-level grouping inside a subject
    """
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="topics"
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("subject", "name")
        ordering = ["order"]
        indexes = [
            models.Index(fields=["subject"]),
        ]

    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class SubTopic(models.Model):
    """
    Fine-grained breakdown for adaptive learning
    """
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="subtopics"
    )

    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("topic", "name")
        ordering = ["order"]

    def __str__(self):
        return f"{self.topic.name} - {self.name}"


class Lesson(models.Model):
    """
    Core learning unit
    """

    DIFFICULTY_LEVELS = (
        (1, "Beginner"),
        (2, "Intermediate"),
        (3, "Advanced"),
    )

    subtopic = models.ForeignKey(
        SubTopic,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(max_length=200)

    # Flexible structured content
    content = models.JSONField()  # supports text, video, code blocks, etc.

    difficulty = models.IntegerField(choices=DIFFICULTY_LEVELS)

    estimated_time = models.PositiveIntegerField(
        help_text="Estimated time in minutes",
        default=5
    )

    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    version = models.IntegerField(default=1)         # lesson versioning
    language = models.CharField(max_length=10, default="en")  # multi-language support
    approved = models.BooleanField(default=False)    # content moderation flag

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["subtopic", "difficulty"]),
            models.Index(fields=["difficulty"]),
        ]

    def __str__(self):
        return self.title


class Prerequisite(models.Model):
    """
    Defines learning dependencies (graph structure)
    """

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="prerequisites"
    )

    required_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="required_for"
    )

    class Meta:
        unique_together = ("lesson", "required_lesson")

    def __str__(self):
        return f"{self.required_lesson} → {self.lesson}"