def normalize_score(score: float) -> float:
    """Normalize score to 0-1 scale"""
    return max(0.0, min(1.0, score))