import pytest
from src.agent import recommend
from src.preferences import parse_preferences
from src.evaluator import evaluate
from src.main import CATALOG
from src.recommender import load_songs, recommend_songs, MODES
from src.applied import main

@pytest.fixture
def catalog():
    return load_songs(CATALOG)

@pytest.mark.parametrize("query,expected", [
    ("happy pop high energy", {"genre":"pop","mood":"happy","energy":.9}),
    ("chill lo-fi acoustic", {"genre":"lofi","mood":"chill","likes_acoustic":True}),
    ("indie pop", {"genre":"indie pop"}),
    ("intense rock non-acoustic", {"genre":"rock","mood":"intense","likes_acoustic":False}),
])
def test_parse(query, expected):
    assert parse_preferences(query) == expected

@pytest.mark.parametrize("query", ["", "unknown", "pop rock", "happy sad", "not pop", "high energy low energy", "x"*501])
def test_reject(query):
    with pytest.raises(ValueError):
        parse_preferences(query)

@pytest.mark.parametrize("mode", list(MODES))
@pytest.mark.parametrize("diversity", [False, True])
def test_pipeline(catalog, mode, diversity):
    result = recommend("happy pop high energy", catalog, mode=mode, diversity=diversity)
    assert result["evaluation"]["passed"]
    assert len(result["results"]) == 5
    assert result["attempts"] == 1

def test_fault_recovery(catalog):
    def faulty(prefs, songs, k, mode, diversity):
        results = recommend_songs(prefs, songs, k, mode, diversity)
        return list(reversed(results))
    result = recommend("happy pop", catalog, ranker=faulty)
    assert result["attempts"] == 2
    assert result["evaluation"]["passed"]

def test_wrong_but_plausible_ranking(catalog):
    prefs = parse_preferences("happy pop")
    wrong = recommend_songs(prefs, catalog, 20)[-5:]
    assert not evaluate(prefs, catalog, wrong, 5)["passed"]

def test_altered_score_and_reason(catalog):
    prefs = parse_preferences("happy pop")
    results = recommend_songs(prefs, catalog, 5)
    s, v, reason = results[0]
    results[0] = (s, v + 1, "invented reason")
    report = evaluate(prefs, catalog, results, 5)
    assert "invalid score" in report["errors"]
    assert "unsupported explanation" in report["errors"]

def test_unknown_song(catalog):
    prefs = parse_preferences("happy pop")
    results = recommend_songs(prefs, catalog, 5)
    s, v, reason = results[0]
    results[0] = (dict(s, id=999), v, reason)
    assert not evaluate(prefs, catalog, results, 5)["passed"]

def test_cli(capsys):
    assert main(["chill lofi acoustic", "--k", "3"]) == 0
    assert "Reliability: PASS (3 checked; attempts: 1)" in capsys.readouterr().out
    assert main(["unknown"]) == 1
    assert "Error:" in capsys.readouterr().out

def test_invalid_k(catalog):
    with pytest.raises(ValueError):
        recommend("pop", catalog, k=0)

def test_empty_catalog():
    with pytest.raises(ValueError):
        recommend("pop", [])


def test_conflicting_acoustic():
    with pytest.raises(ValueError, match="single acoustic"):
        parse_preferences("pop acoustic non-acoustic")

def test_mutating_ranker(catalog):
    original_title = catalog[0]["title"]
    def faulty(prefs, songs, k, mode, diversity):
        prefs["genre"] = "metal"
        songs[0]["title"] = "Invented track"
        return recommend_songs(prefs, songs, k, mode, diversity)
    result = recommend("happy pop", catalog, ranker=faulty)
    assert result["attempts"] == 2
    assert result["preferences"]["genre"] == "pop"
    assert result["results"][0][0]["title"] == original_title
    assert catalog[0]["title"] == original_title

def test_retry_fails_closed(catalog, monkeypatch):
    import src.agent as agent
    def faulty(*args):
        return []
    monkeypatch.setattr(agent, "recommend_songs", faulty)
    with pytest.raises(RuntimeError, match="no results released"):
        recommend("pop", catalog, ranker=faulty)

def test_duplicate_or_nonfinite_results(catalog):
    prefs = parse_preferences("happy pop")
    results = recommend_songs(prefs, catalog, 5)
    s, v, reason = results[0]
    results[0] = (s, float("nan"), reason)
    results[1] = results[0]
    report = evaluate(prefs, catalog, results, 5)
    assert "invalid score" in report["errors"]
    assert "unknown, altered or duplicate song" in report["errors"]
