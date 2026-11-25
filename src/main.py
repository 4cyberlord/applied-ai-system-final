"""CLI-first simulation with selectable strategies and reproducible evaluation."""
import argparse
from pathlib import Path
try:
    from .recommender import MODES, load_songs, recommend_songs
except ImportError:
    from recommender import MODES, load_songs, recommend_songs

CATALOG = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
PROFILES = {
    "High-Energy Pop": dict(genre="pop", mood="happy", energy=0.8, likes_acoustic=False),
    "Chill Lofi": dict(genre="lofi", mood="chill", energy=0.4, likes_acoustic=True),
    "Deep Intense Rock": dict(genre="rock", mood="intense", energy=0.9, likes_acoustic=False),
    "Conflicting Preferences": dict(genre="pop", mood="sad", energy=0.9, likes_acoustic=False),
}
ADVANCED_PROFILE = dict(PROFILES["High-Energy Pop"], popularity=80,
                        release_decade=2020, mood_tag="bright",
                        duration_seconds=210, language="tw")

def format_recommendations(results):
    """Format rankings as an aligned table with complete score explanations."""
    rows = [("Rank", "Song", "Artist", "Score", "Reasons")]
    rows.extend((str(i), s["title"], s["artist"], f"{score:.3f}", reasons)
                for i, (s, score, reasons) in enumerate(results, 1))
    widths = [max(len(row[i]) for row in rows) for i in range(5)]
    def line(row):
        return " | ".join(value.ljust(widths[i]) for i, value in enumerate(row)).rstrip()
    return "\n".join([line(rows[0]), "-+-".join("-"*w for w in widths)] +
                     [line(row) for row in rows[1:]])

def main(argv=None):
    """Run every evaluation profile or select a profile and ranking strategy."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=MODES, default="balanced")
    parser.add_argument("--profile", choices=[*PROFILES, "Advanced"])
    parser.add_argument("--diversity", action="store_true")
    parser.add_argument("--experiment", action="store_true",
                        help="Compare balanced and energy-focused rankings.")
    args = parser.parse_args(argv)
    songs = load_songs(CATALOG)
    profiles = {**PROFILES, "Advanced": ADVANCED_PROFILE} if args.profile else PROFILES
    if args.profile:
        profiles = {args.profile: profiles[args.profile]}
    for name, prefs in profiles.items():
        for mode in (("balanced", "energy-focused") if args.experiment else (args.mode,)):
            print(f"\n{name} profile: {prefs}")
            print(f"Mode: {mode}; diversity: {args.diversity}")
            print(format_recommendations(recommend_songs(prefs, songs, 5, mode, args.diversity)))

if __name__ == "__main__":
    main()
