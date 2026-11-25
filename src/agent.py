"""Plan, retrieve, rank, verify and retry once before releasing recommendations."""
import logging
from .preferences import parse_preferences
from .retriever import retrieve
from .recommender import recommend_songs, MODES
from .evaluator import evaluate

LOG = logging.getLogger(__name__)

def recommend(query, catalog, k=5, mode="balanced", diversity=False, ranker=recommend_songs):
    """Return verified, grounded results or a safe error without unverified output."""
    if not isinstance(k, int) or isinstance(k, bool) or not 1 <= k <= 20:
        raise ValueError("k must be an integer between 1 and 20.")
    if mode not in MODES:
        raise ValueError("Unknown ranking mode.")
    prefs = parse_preferences(query)
    if not catalog or len({s["id"] for s in catalog}) != len(catalog):
        raise ValueError("Catalog is empty or contains duplicate IDs.")
    candidates = retrieve(prefs, catalog, mode)
    LOG.info("Retrieved %d candidates", len(candidates))
    for attempt in (1, 2):
        try:
            results = (ranker if attempt == 1 else recommend_songs)(prefs, candidates, k, mode, diversity)
            report = evaluate(prefs, catalog, results, k, mode, diversity)
        except (ValueError, TypeError, KeyError, IndexError, AttributeError):
            report = {"passed": False, "errors": ["malformed ranking"], "checked": 0}
        LOG.info("Evaluation attempt %d: %s", attempt, "pass" if report["passed"] else "fail")
        if report["passed"]:
            return {"preferences": prefs, "results": results, "evaluation": report, "attempts": attempt}
        LOG.warning("Rejected ranking: %s", report["errors"])
    raise RuntimeError("Recommendation validation failed; no results released.")
