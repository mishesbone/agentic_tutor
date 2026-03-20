from apps.users.models import User
from apps.learning.models import SubTopic
from apps.ai_engine.models import UserProgress

def find_study_partners(user: User, subtopic: SubTopic, max_results: int = 5):
    """
    Matches users with similar skill levels for collaborative study
    """
    target_progress = UserProgress.objects.filter(user=user, subtopic=subtopic).first()
    if not target_progress:
        return []

    all_users = UserProgress.objects.filter(subtopic=subtopic).exclude(user=user)
    # Match users with proficiency within +/- 10% of current user
    matched = [
        p.user for p in all_users
        if abs(p.proficiency - target_progress.proficiency) <= 0.1
    ]
    return matched[:max_results]