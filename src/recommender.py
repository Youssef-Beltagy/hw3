import csv
from enum import Enum
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


class Mode(Enum):
    DEFAULT = "default"
    EXPLORE = "explore"
    DIVERSE = "diverse"
    MOOD = "mood"
    ADVANCED = "advanced"


MODE_DESCRIPTIONS = {
    Mode.DEFAULT: "closest matches based on score",
    Mode.EXPLORE: "diverse recommendations by penalizing favorite genre",
    Mode.DIVERSE: "unique artists and genres in results",
    Mode.MOOD: "prioritize mood and energy over genre",
    Mode.ADVANCED: "Advanced recommendation mode includes additional attributes like song popularity or release decade"
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
    popularity: int
    release_decade: str
    mood_tags: List[str]
    instrumentalness: float
    lyrical_theme: str

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
    min_popularity: int              # 0-100, minimum acceptable popularity
    preferred_decade: str            # e.g. "2020s"
    preferred_mood_tags: List[str]   # e.g. ["nostalgic", "warm"]
    target_instrumentalness: float   # 0-1
    preferred_lyrical_theme: str     # e.g. "love"

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
                popularity=int(row["popularity"]),
                release_decade=row["release_decade"],
                mood_tags=row["mood_tags"].split("|"),
                instrumentalness=float(row["instrumentalness"]),
                lyrical_theme=row["lyrical_theme"],
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

    # Mood tags: +0.5 per overlapping tag (max 2 = 1.0) — weighted higher in mood mode
    overlap = set(song.mood_tags) & set(user.preferred_mood_tags)
    if overlap:
        tag_score = min(len(overlap), 2) * 0.5
        score += tag_score
        reasons.append(f"+{tag_score:.2f} mood tags ({', '.join(overlap)})")

    # Instrumentalness: closeness × 0.3
    inst_score = (1.0 - abs(user.target_instrumentalness - song.instrumentalness)) * 0.3
    score += inst_score
    reasons.append(f"+{inst_score:.2f} instrumentalness closeness")

    # Lyrical theme: +0.5 if match
    if song.lyrical_theme == user.preferred_lyrical_theme:
        score += 0.5
        reasons.append(f"+0.5 lyrical theme match ({song.lyrical_theme})")

    return score, reasons

def score_song_advanced(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
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

    # Popularity: +0.5 if song meets minimum popularity threshold
    if song.popularity >= user.min_popularity:
        score += 0.5
        reasons.append(f"+0.5 popularity ({song.popularity} >= {user.min_popularity})")

    # Decade: +0.75 if release decade matches
    if song.release_decade == user.preferred_decade:
        score += 0.75
        reasons.append(f"+0.75 decade match ({song.release_decade})")

    # Mood tags: +0.3 per overlapping tag (max 2 tags = 0.6)
    overlap = set(song.mood_tags) & set(user.preferred_mood_tags)
    if overlap:
        tag_score = min(len(overlap), 2) * 0.3
        score += tag_score
        reasons.append(f"+{tag_score:.2f} mood tags ({', '.join(overlap)})")

    # Instrumentalness: closeness × 0.4
    inst_score = (1.0 - abs(user.target_instrumentalness - song.instrumentalness)) * 0.4
    score += inst_score
    reasons.append(f"+{inst_score:.2f} instrumentalness closeness")

    # Lyrical theme: +0.75 if match
    if song.lyrical_theme == user.preferred_lyrical_theme:
        score += 0.75
        reasons.append(f"+0.75 lyrical theme match ({song.lyrical_theme})")

    return score, reasons

def recommend_songs(user: UserProfile, songs: List[Song], k: int = 5, mode: Mode = Mode.DEFAULT) -> List[Tuple[Song, float, str]]:
    """Rank all songs by score for a user and return the top k results."""
    scored = []
    scoring_func = score_song
    if mode == Mode.MOOD:
        scoring_func = score_song_mood
    elif mode == Mode.ADVANCED:
        scoring_func = score_song_advanced

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
