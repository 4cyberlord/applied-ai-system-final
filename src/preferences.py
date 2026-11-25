"""Deterministic, bounded natural-language preference extraction."""
import re

GENRES = ("indie pop", "afrobeats", "hip-hop", "synthwave", "classical", "country",
          "ambient", "reggae", "metal", "lofi", "rock", "pop", "jazz", "edm", "rnb")
MOODS = ("happy", "chill", "intense", "sad", "relaxed", "focused", "moody",
         "euphoric", "nostalgic", "aggressive")
ENERGY = {"high energy": .9, "energetic": .9, "low energy": .3, "calm": .3,
          "moderate energy": .5, "medium energy": .5}

def parse_preferences(query):
    """Extract explicit catalog preferences; reject ambiguous or unsupported requests."""
    if not isinstance(query, str) or not query.strip() or len(query) > 500:
        raise ValueError("Enter a music request between 1 and 500 characters.")
    text = query.casefold().replace("lo-fi", "lofi").replace("r&b", "rnb").replace("high-energy", "high energy").replace("low-energy", "low energy")
    if re.search(r"\b(?:not|no|without|avoid|except|never|don't)\b", text):
        raise ValueError("Negated preferences are not supported; describe what you want instead.")
    def matches(options):
        return [v for v in options if re.search(r"(?<!\w)" + re.escape(v) + r"(?!\w)", text)]
    genres = matches(GENRES)
    if "indie pop" in genres and "pop" in genres:
        if len(re.findall(r"\bpop\b", text)) == 1:
            genres.remove("pop")
    moods = matches(MOODS)
    if len(genres) > 1 or len(moods) > 1:
        raise ValueError("Choose one genre and one mood per request.")
    prefs = {}
    if genres:
        prefs["genre"] = genres[0]
    if moods:
        prefs["mood"] = moods[0]
    energies = {ENERGY[v] for v in matches(ENERGY)}
    if len(energies) > 1:
        raise ValueError("Choose a single energy level.")
    if energies:
        prefs["energy"] = energies.pop()
    non_acoustic = re.search(r"\bnon[- ]acoustic\b", text)
    acoustic = re.search(r"\bacoustic\b", re.sub(r"\bnon[- ]acoustic\b", "", text))
    if non_acoustic and acoustic:
        raise ValueError("Choose a single acoustic preference.")
    if non_acoustic:
        prefs["likes_acoustic"] = False
    elif acoustic:
        prefs["likes_acoustic"] = True
    if not prefs:
        raise ValueError("Specify a supported genre, mood, energy level or acoustic preference.")
    return prefs
