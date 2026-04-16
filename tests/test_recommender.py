from src.recommender import Song, UserProfile, score_song, recommend_songs

POP_SONG = Song(id=1, title="Test Pop Track", artist="Test Artist",
                genre="pop", mood="happy", energy=0.8, tempo_bpm=120,
                valence=0.9, danceability=0.8, acousticness=0.2)

LOFI_SONG = Song(id=2, title="Chill Lofi Loop", artist="Test Artist",
                 genre="lofi", mood="chill", energy=0.4, tempo_bpm=80,
                 valence=0.6, danceability=0.5, acousticness=0.9)

POP_USER = UserProfile(favorite_genre="pop", favorite_mood="happy",
                       target_energy=0.8, likes_acoustic=False,
                       target_valence=0.9, target_danceability=0.8)


def test_genre_match_adds_points():
    _, reasons = score_song(POP_USER, POP_SONG)
    assert any("genre match" in r for r in reasons)


def test_genre_mismatch_gives_lower_score():
    pop_score, _ = score_song(POP_USER, POP_SONG)
    lofi_score, _ = score_song(POP_USER, LOFI_SONG)
    assert pop_score > lofi_score


def test_recommend_returns_k_results():
    songs = [POP_SONG, LOFI_SONG]
    results = recommend_songs(POP_USER, songs, k=2)
    assert len(results) == 2


def test_recommend_sorted_by_score_descending():
    songs = [POP_SONG, LOFI_SONG]
    results = recommend_songs(POP_USER, songs, k=2)
    assert results[0][1] >= results[1][1]


def test_recommend_best_match_is_pop_for_pop_user():
    songs = [POP_SONG, LOFI_SONG]
    results = recommend_songs(POP_USER, songs, k=2)
    assert results[0][0].genre == "pop"
