import csv
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
    likes_acoustic: bool
    target_valence: Optional[float] = None
    target_danceability: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

NUMERIC_FIELDS = {"energy", "valence", "danceability", "acousticness"}
INT_FIELDS = {"id", "tempo_bpm"}


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            for key in INT_FIELDS:
                row[key] = int(row[key])
            for key in NUMERIC_FIELDS:
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user: UserProfile, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm Recipe:
      Genre match:  +2.5 points (exact match)
      Mood match:   +1.5 points (exact match)
      Energy:       up to 1.0 point  (closeness: 1 - |user - song|)
      Valence:      up to 0.5 points (closeness, if user provides it)
      Danceability: up to 0.3 points (closeness, if user provides it)
      Acoustic:     +0.5 if song acousticness aligns with likes_acoustic

    Max possible: 6.8
    """
    score = 0.0
    reasons = []

    # Genre: exact match = 2.5 pts
    if song["genre"] == user.favorite_genre:
        score += 2.5
        reasons.append(f"+2.5 genre match ({song['genre']})")

    # Mood: exact match = 1.5 pts
    if song["mood"] == user.favorite_mood:
        score += 1.5
        reasons.append(f"+1.5 mood match ({song['mood']})")

    # Energy: closeness score × 1.0
    energy_score = 1.0 - abs(user.target_energy - song["energy"])
    score += energy_score
    reasons.append(f"+{energy_score:.2f} energy closeness {energy_score:.2f}")

    # Valence: closeness score × 0.5
    if user.target_valence is not None:
        val_score = 1.0 - abs(user.target_valence - song["valence"])
        val_score *= 0.5
        score += val_score
        reasons.append(f"+{val_score:.2f} valence closeness {val_score:.2f}")

    # Danceability: closeness score × 0.3
    if user.target_danceability is not None:
        dance_score = 1.0 - abs(user.target_danceability - song["danceability"])
        dance_score *= 0.3
        score += dance_score 
        reasons.append(f"+{dance_score * 0.3:.2f} danceability closeness {dance_score:.2f}")

    # Acoustic preference: +0.5 if alignment
    is_acoustic = song["acousticness"] >= 0.5
    if user.likes_acoustic == is_acoustic:
        score += 0.5
        reasons.append("+0.5 acoustic preference match")

    return score, reasons

def recommend_songs(user: UserProfile, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user, song)
        explanation = "; ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
