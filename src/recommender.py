from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float
    target_acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "valence":      user.target_valence,
            "danceability": user.target_danceability,
            "acousticness": user.target_acousticness,
        }
        scored = sorted(
            self.songs,
            key=lambda s: score_song(user_prefs, vars(s))[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "valence":      user.target_valence,
            "danceability": user.target_danceability,
            "acousticness": user.target_acousticness,
        }
        _, reasons = score_song(user_prefs, vars(song))
        return ", ".join(reasons) if reasons else "general match"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Algorithm Recipe
    ----------------
    Categorical (binary):
      +2.0  genre match
      +1.0  mood match

    Continuous similarity  (weight × (1 - |song - target|)):
      ×1.50  energy       — biggest driver of perceived intensity
      ×1.00  valence      — emotional tone
      ×0.75  danceability — groove feel
      ×0.75  acousticness — organic vs. electronic texture

    Max possible score: 7.0
    """
    score = 0.0
    reasons: List[str] = []

    # --- categorical ---
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match")

    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match")

    # --- continuous similarity ---
    numeric_weights = [
        ("energy",       "energy",       1.50),
        ("valence",      "valence",      1.00),
        ("danceability", "danceability", 0.75),
        ("acousticness", "acousticness", 0.75),
    ]
    for song_key, pref_key, weight in numeric_weights:
        similarity = 1.0 - abs(song[song_key] - user_prefs[pref_key])
        score += weight * similarity
        if similarity >= 0.85:
            reasons.append(f"close {song_key}")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Returns top-k songs as (song_dict, score, explanation).
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "general match"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
