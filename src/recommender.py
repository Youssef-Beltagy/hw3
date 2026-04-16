import csv
from enum import Enum
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


class Mode(Enum):
    DEFAULT = "default"
    EXPLORE = "explore"
    DIVERSE = "diverse"
    MOOD = "mood"


MODE_DESCRIPTIONS = {
    Mode.DEFAULT: "closest matches based on score",
    Mode.EXPLORE: "diverse recommendations by penalizing favorite genre",
    Mode.DIVERSE: "unique artists and genres in results",
    Mode.MOOD: "prioritize mood and energy over genre",
}



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
    reasons.append(f"+{energy_score:.2f} energy closeness")

    # Valence: closeness score × 0.5
    val_score = 1.0 - abs(user.target_valence - song.valence)
    val_score *= 0.5
    score += val_score
    reasons.append(f"+{val_score:.2f} valence closeness")

    # Danceability: closeness score × 0.3
    dance_score = 1.0 - abs(user.target_danceability - song.danceability)
    dance_score *= 0.3
    score += dance_score 
    reasons.append(f"+{dance_score:.2f} danceability closeness")

    # Acoustic preference: +0.5 if alignment
    is_acoustic = song.acousticness >= 0.5
    if user.likes_acoustic == is_acoustic:
        score += 0.5
        reasons.append("+0.5 acoustic preference match")

    return score, reasons

def score_song_mood(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Score a song prioritizing mood and energy over genre."""
    score = 0.0
    reasons = []

    # Mood: dominant factor = 3.0 pts
    if song.mood == user.favorite_mood:
        score += 3.0
        reasons.append(f"+3.0 mood match ({song.mood})")

    # Energy: high weight = × 2.0
    energy_score = 1.0 - abs(user.target_energy - song.energy)
    energy_score *= 2.0
    score += energy_score
    reasons.append(f"+{energy_score:.2f} energy closeness")

    # Valence: × 1.0
    val_score = 1.0 - abs(user.target_valence - song.valence)
    score += val_score
    reasons.append(f"+{val_score:.2f} valence closeness")

    # Genre: minor bonus = 0.5 pts
    if song.genre == user.favorite_genre:
        score += 0.5
        reasons.append(f"+0.5 genre match ({song.genre})")

    return score, reasons

def recommend_songs(user: UserProfile, songs: List[Song], k: int = 5, mode: Mode = Mode.DEFAULT) -> List[Tuple[Song, float, str]]:
    """Rank all songs by score for a user and return the top k results."""
    scored = []
    scoring_func = score_song_mood if mode == Mode.MOOD else score_song
    for song in songs:
        score, reasons = scoring_func(user, song)
        scored.append((song, score, reasons))

    if mode == Mode.EXPLORE:
        # Penalize songs that match the user's genre to surface new results
        for i, (song, score, reasons) in enumerate(scored):
            if song.genre == user.favorite_genre:
                reasons.append(f"-{ score* 0.5 :.2f} (explore penalty: -50%)")
                scored[i] = (song, score * 0.5, reasons)

    if mode == Mode.DIVERSE:
        # sort so the best matches are not the ones penalized
        scored.sort(key=lambda x: x[1], reverse=True)
        seen_artists = set()
        seen_genres = set()
        result = []
        for song, score, reasons in scored:
            if song.artist in seen_artists:
                reasons.append(f"-{ score * 0.3 :.2f} (diverse penalty: repeat artist -30%)")
                score *= 0.7
            if song.genre in seen_genres:
                reasons.append(f"-{ score * 0.2 :.2f} (diverse penalty: repeat genre -20%)")
                score *= 0.8
            seen_artists.add(song.artist)
            seen_genres.add(song.genre)
            result.append((song, score, reasons))
        scored = result

    scored.sort(key=lambda x: x[1], reverse=True)

    scored = [(song, score, "\n".join(["", *reasons])) for (song, score, reasons) in scored]

    return scored[:k]
