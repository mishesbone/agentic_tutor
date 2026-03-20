from celery import shared_task
from apps.users.models import User
from apps.ai_engine.services.recommendation import recommend_lessons

@shared_task
def generate_user_recommendations(user_id: int):
    """
    Celery task to generate AI recommendations for a user
    """
    user = User.objects.get(id=user_id)
    lessons = recommend_lessons(user)
    return [lesson.id for lesson in lessons]
