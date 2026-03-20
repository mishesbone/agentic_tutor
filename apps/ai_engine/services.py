from typing import List
from apps.users.models import User
from apps.learning.models import Lesson, SubTopic
from apps.ai_engine.models import AIRecommendation

def recommend_lessons(user: User, limit: int = 5) -> List[Lesson]:
    """
    Simple example: recommend lessons based on weakest subtopics
    """
    # Find user's weakest subtopics
    weak_subtopics = sorted(
        user.progress.all(),
        key=lambda p: p.proficiency
    )

    recommended = []
    for progress in weak_subtopics:
        subtopic = progress.subtopic
        lessons = Lesson.objects.filter(subtopic=subtopic, is_active=True).order_by('difficulty')[:limit]
        recommended.extend(list(lessons))

        if len(recommended) >= limit:
            break

    # Save recommendations
    AIRecommendation.objects.bulk_create([
        AIRecommendation(user=user, lesson=l, subtopic=l.subtopic, score=1.0)
        for l in recommended
    ])

    return recommended[:limit]