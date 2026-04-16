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
    tempo_bpm: int
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
    target_valence: float
    target_danceability: float

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

def load_songs(csv_path: str) -> List[Song]:
    """Load songs from a CSV file and return a list of Song objects."""
    songs = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            songs.append(Song(
                id=int(row["id"]),
                title=row["title"],
                artist=row["artist"],
                genre=row["genre"],
                mood=row["mood"],
                energy=float(row["energy"]),
                tempo_bpm=int(row["tempo_bpm"]),
                valence=float(row["valence"]),
                danceability=float(row["danceability"]),
                acousticness=float(row["acousticness"]),
            ))
    return songs

def score_song(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Score a song against a user profile and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre: exact match = 2.5 pts
    if song.genre == user.favorite_genre:
        score += 2.5
        reasons.append(f"+2.5 genre match ({song.genre})")

    # Mood: exact match = 1.5 pts
    if song.mood == user.favorite_mood:
        score += 1.5
        reasons.append(f"+1.5 mood match ({song.mood})")

    # Energy: closeness score × 1.0
    energy_score = 1.0 - abs(user.target_energy - song.energy)
    score += energy_score
    reasons.append(f"+{energy_score:.2f} energy closeness {energy_score:.2f}")

    # Valence: closeness score × 0.5
    val_score = 1.0 - abs(user.target_valence - song.valence)
    val_score *= 0.5
    score += val_score
    reasons.append(f"+{val_score:.2f} valence closeness {val_score:.2f}")

    # Danceability: closeness score × 0.3
    dance_score = 1.0 - abs(user.target_danceability - song.danceability)
    dance_score *= 0.3
    score += dance_score 
    reasons.append(f"+{dance_score:.2f} danceability closeness {dance_score:.2f}")

    # Acoustic preference: +0.5 if alignment
    is_acoustic = song.acousticness >= 0.5
    if user.likes_acoustic == is_acoustic:
        score += 0.5
        reasons.append("+0.5 acoustic preference match")

    return score, reasons

def recommend_songs(user: UserProfile, songs: List[Song], k: int = 5) -> List[Tuple[Song, float, str]]:
    """Rank all songs by score for a user and return the top k results."""
    scored = []
    for song in songs:
        score, reasons = score_song(user, song)
        explanation = "\n\t".join(["", *reasons])
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
