from apps.users.models import UserProgress
from apps.assessment.models import Attempt

def update_user_progress(user_id: int, question_id: int, correct: bool, time_taken: float):
    """
    Updates user's proficiency based on an attempt
    """
    try:
        attempt = Attempt.objects.get(id=question_id)
        progress = UserProgress.objects.get(user_id=user_id, subtopic=attempt.question.subtopic)
    except UserProgress.DoesNotExist:
        return

    progress.update_progress(is_correct=correct, response_time=time_taken)