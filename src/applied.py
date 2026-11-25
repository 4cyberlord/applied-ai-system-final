"""Main entry point for VibeFinder AI 2.0."""
import argparse
import logging
from .main import CATALOG, format_recommendations
from .recommender import MODES, load_songs
from .agent import recommend

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Music preferences in plain language")
    parser.add_argument("--mode", choices=MODES, default="balanced")
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--diversity", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        result = recommend(args.query, load_songs(CATALOG), args.k, args.mode, args.diversity)
    except (ValueError, RuntimeError, OSError, KeyError, TypeError) as exc:
        print(f"Error: {exc}")
        return 1
    print("Preferences:", result["preferences"])
    print(format_recommendations(result["results"]))
    print(f"Reliability: PASS ({result['evaluation']['checked']} checked; attempts: {result['attempts']})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
