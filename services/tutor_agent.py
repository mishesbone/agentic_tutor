from apps.ai_engine.services.recommendation import recommend_lessons
from apps.assessment.models import Attempt
from apps.users.models import User

def generate_next_lesson(user: User):
    """
    Decide the next lesson dynamically for the user.
    """
    lessons = recommend_lessons(user, limit=3)
    next_lessons = []

    for lesson in lessons:
        prereqs = lesson.prerequisites.all()
        if all(Attempt.objects.filter(user=user, question__lesson=p.required_lesson, correct=True).exists() for p in prereqs):
            next_lessons.append(lesson)
    return next_lessons
