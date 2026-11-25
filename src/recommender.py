"""Transparent content-based music ranking."""
from dataclasses import dataclass, asdict
import csv

MODES = {
    "balanced": (2.0, 1.0, 1.0),
    "genre-first": (3.0, 1.0, 1.0),
    "mood-first": (1.0, 3.0, 1.0),
    "energy-focused": (1.0, 1.0, 2.0),
}

@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 0
    release_decade: int = 2020
    mood_tag: str = ""
    duration_seconds: int = 0
    language: str = ""

@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

    def preferences(self):
        """Convert the object profile to shared scoring inputs."""
        return dict(genre=self.favorite_genre, mood=self.favorite_mood,
                    energy=self.target_energy, likes_acoustic=self.likes_acoustic)

def load_songs(csv_path):
    """Read a CSV catalog and convert numeric columns."""
    with open(csv_path, newline="", encoding="utf-8") as file:
        songs = []
        for row in csv.DictReader(file):
            for key in ("id", "popularity", "release_decade", "duration_seconds"):
                if key in row:
                    row[key] = int(row[key])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs, song, mode="balanced"):
    """Return relevance and a complete breakdown of awarded points."""
    if mode not in MODES:
        raise ValueError(f"Unknown scoring mode: {mode}")
    genre, mood, energy = MODES[mode]
    reasons = []
    points = []
    def award(label, value):
        points.append(value)
        reasons.append(f"{label} (+{value:.3f})")
    for key, weight in (("genre", genre), ("mood", mood),
                        ("mood_tag", 0.5), ("language", 0.5)):
        if key in user_prefs and str(song.get(key, "")).casefold() == str(user_prefs[key]).casefold():
            award(f"{key} match", weight)
    for key, scale, weight in (("energy", 1, energy), ("popularity", 100, 0.5),
                               ("release_decade", 50, 0.5), ("duration_seconds", 300, 0.5)):
        if key in user_prefs and key in song:
            similarity = max(0.0, 1.0 - abs(float(song[key]) - float(user_prefs[key])) / scale)
            award(f"{key} similarity", weight * similarity)
    if user_prefs.get("likes_acoustic") is not None:
        acoustic = song["acousticness"]
        award("acoustic preference", 0.5 * (acoustic if user_prefs["likes_acoustic"] else 1-acoustic))
    return sum(points), reasons

def recommend_songs(user_prefs, songs, k=5, mode="balanced", diversity=False):
    """Rank candidates by relevance, optionally penalizing repeated artists and genres."""
    if k <= 0:
        return []
    candidates = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode)
        candidates.append((song, score, reasons))
    if not diversity:
        return [(s, v, "; ".join(r)) for s, v, r in sorted(candidates, key=lambda item: -item[1])[:k]]
    selected = []
    artists, genres = {}, {}
    def penalty(song):
        return 0.75 * artists.get(song["artist"].casefold(), 0) + 0.25 * genres.get(song["genre"].casefold(), 0)
    while candidates and len(selected) < k:
        index = max(range(len(candidates)), key=lambda i: candidates[i][1] - penalty(candidates[i][0]))
        song, score, reasons = candidates.pop(index)
        cost = penalty(song)
        if cost:
            reasons = reasons + [f"diversity penalty (-{cost:.3f})"]
        selected.append((song, score-cost, "; ".join(reasons)))
        artist, genre = song["artist"].casefold(), song["genre"].casefold()
        artists[artist] = artists.get(artist, 0) + 1
        genres[genre] = genres.get(genre, 0) + 1
    return selected

class Recommender:
    """Object interface backed by the same functional scoring engine."""
    def __init__(self, songs):
        self.songs = songs

    def recommend(self, user, k=5, mode="balanced", diversity=False):
        """Return ranked Song objects without duplicating the scoring formula."""
        by_id = {song.id: song for song in self.songs}
        return [by_id[row["id"]] for row, _, _ in recommend_songs(
            user.preferences(), [asdict(song) for song in self.songs], k, mode, diversity)]

    def explain_recommendation(self, user, song, mode="balanced"):
        """Explain the shared relevance score."""
        _, reasons = score_song(user.preferences(), asdict(song), mode)
        return "; ".join(reasons) or "No matching preferences"
