from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


from pathlib import Path
import pytest
from dataclasses import asdict
from src.recommender import load_songs, score_song, recommend_songs, MODES
from src.main import PROFILES, ADVANCED_PROFILE, format_recommendations

CATALOG = Path(__file__).resolve().parents[1] / "data" / "songs.csv"

@pytest.fixture
def catalog():
    return load_songs(CATALOG)

def test_catalog(catalog):
    assert len(catalog) == 20
    assert len({s["id"] for s in catalog}) == 20
    assert len({s["genre"] for s in catalog}) >= 12
    for s in catalog:
        assert isinstance(s["popularity"], int)
        assert isinstance(s["release_decade"], int)
        assert isinstance(s["duration_seconds"], int)
        assert isinstance(s["energy"], float)
        assert 0 <= s["energy"] <= 1
        assert 0 <= s["popularity"] <= 100

def test_exact_score(catalog):
    score, reasons = score_song(PROFILES["High-Energy Pop"], catalog[0])
    assert score == pytest.approx(4.39)
    assert len(reasons) == 4

def test_energy_proximity(catalog):
    song = catalog[0]
    assert score_song({"energy": .82}, song)[0] == 1
    assert score_song({"energy": 0}, song)[0] == pytest.approx(.18)
    assert score_song({"energy": 3}, song)[0] == 0

@pytest.mark.parametrize("name,expected", [
    ("High-Energy Pop", "Sunrise City"),
    ("Chill Lofi", "Ocean Lanterns"),
    ("Deep Intense Rock", "Storm Runner"),
    ("Conflicting Preferences", "Bittersweet Rush"),
])
def test_profiles(catalog, name, expected):
    results = recommend_songs(PROFILES[name], catalog)
    assert len(results) == 5
    assert results[0][0]["title"] == expected
    assert [v for _, v, _ in results] == sorted((v for _, v, _ in results), reverse=True)

def test_shared_engine(catalog):
    user = UserProfile("pop", "happy", .8, False)
    objects = Recommender([Song(**s) for s in catalog])
    for mode in MODES:
        for diversity in (False, True):
            assert [s.id for s in objects.recommend(user, 5, mode, diversity)] == [
                s["id"] for s, _, _ in recommend_songs(user.preferences(), catalog, 5, mode, diversity)]

def test_advanced_features(catalog):
    song = catalog[0]
    for key in ("popularity", "release_decade", "mood_tag", "duration_seconds", "language"):
        assert score_song({key: song[key]}, song)[0] == pytest.approx(.5)
    assert len(score_song(ADVANCED_PROFILE, song)[1]) >= 8

def test_modes_and_invalid_mode(catalog):
    profile = PROFILES["High-Energy Pop"]
    assert score_song(profile, catalog[0], "genre-first")[0] > score_song(profile, catalog[0])[0]
    assert recommend_songs(profile, catalog, mode="energy-focused") != recommend_songs(profile, catalog)
    with pytest.raises(ValueError):
        score_song(profile, catalog[0], "unknown")

def test_diversity():
    base = dict(id=1, title="A", artist="same", genre="pop", mood="happy", energy=.8, acousticness=.2)
    songs = [base, dict(base, id=2, title="B"), dict(base, id=3, title="C", artist="other")]
    results = recommend_songs(dict(genre="pop"), songs, diversity=True)
    assert [s["id"] for s, _, _ in results] == [1, 3, 2]
    assert "diversity penalty" in results[2][2]

def test_top_k_and_table(catalog):
    assert recommend_songs({}, catalog, 0) == []
    assert recommend_songs({}, [], 5) == []
    assert len(recommend_songs({}, catalog, 100)) == 20
    table = format_recommendations(recommend_songs(PROFILES["High-Energy Pop"], catalog))
    assert "Reasons" in table and "Sunrise City" in table and "4.390" in table
