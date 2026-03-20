from celery import shared_task
from apps.ai_engine.services.recommendation import recommend_lessons
from apps.users.models import User

@shared_task
def generate_user_recommendations(user_id: int):
    user = User.objects.get(id=user_id)
    lessons = recommend_lessons(user)
    return [lesson.id for lesson in lessons]
