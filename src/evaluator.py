"""Runtime reliability checks integrated into the recommendation pipeline."""
import math
from .recommender import score_song

def evaluate(preferences, catalog, results, k, mode="balanced", diversity=False):
    """Independently verify identity, scores, ordering, explanations and completeness."""
    errors = []
    remaining = {s["id"]: s for s in catalog}
    artists, genres = {}, {}
    if len(results) != min(k, len(catalog)):
        errors.append("wrong result count")
    def adjusted(song):
        base, reasons = score_song(preferences, song, mode)
        penalty = 0.75 * artists.get(song["artist"].casefold(), 0) + 0.25 * genres.get(song["genre"].casefold(), 0) if diversity else 0
        return base - penalty, "; ".join(reasons + ([f"diversity penalty (-{penalty:.3f})"] if penalty else []))
    for song, score, reason in results:
        sid = song.get("id")
        if sid not in remaining or song != remaining[sid]:
            errors.append("unknown, altered or duplicate song")
            continue
        expected, explanation = adjusted(remaining[sid])
        best = max(adjusted(s)[0] for s in remaining.values())
        if not math.isfinite(score) or not math.isclose(score, expected, abs_tol=1e-9):
            errors.append("invalid score")
        if not math.isclose(expected, best, abs_tol=1e-9):
            errors.append("incorrect ranking")
        if reason != explanation:
            errors.append("unsupported explanation")
        remaining.pop(sid)
        for field, counts in (("artist", artists), ("genre", genres)):
            value = song[field].casefold()
            counts[value] = counts.get(value, 0) + 1
    return {"passed": not errors, "errors": errors, "checked": len(results)}
