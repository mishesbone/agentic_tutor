from typing import List
from apps.users.models import User
from apps.learning.models import Lesson, SubTopic
from apps.ai_engine.models import AIRecommendation

def recommend_lessons(user: User, limit: int = 5) -> List[Lesson]:
    """
    Recommend lessons for the user based on weakest subtopics.
    """
    # Sort subtopics by proficiency ascending (weakest first)
    weak_progress = sorted(user.progress.all(), key=lambda p: p.proficiency)
    recommended = []

    for progress in weak_progress:
        subtopic = progress.subtopic
        lessons = Lesson.objects.filter(subtopic=subtopic, is_active=True).order_by('difficulty')[:limit]
        for lesson in lessons:
            recommended.append(lesson)
        if len(recommended) >= limit:
            break

    # Save recommendations for analytics
    AIRecommendation.objects.bulk_create([
        AIRecommendation(user=user, lesson=l, subtopic=l.subtopic, score=1.0)
        for l in recommended[:limit]
    ])

    return recommended[:limit]