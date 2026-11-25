"""Retrieve candidates from the trusted local catalog."""
from .recommender import score_song

def retrieve(preferences, catalog, mode="balanced", limit=None):
    """Return catalog evidence ranked by relevance, optionally limiting candidates."""
    ranked = sorted(catalog, key=lambda song: -score_song(preferences, song, mode)[0])
    return ranked if limit is None else ranked[:max(0, limit)]
