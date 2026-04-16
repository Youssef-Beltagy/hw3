"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

from recommender import load_songs, recommend_songs, UserProfile, Mode, MODE_DESCRIPTIONS
from tabulate import tabulate
import argparse


def main() -> None:
    mode_help = "\n".join(f"  {m.value}: {desc}" for m, desc in MODE_DESCRIPTIONS.items())
    parser = argparse.ArgumentParser(description="Music Recommender Simulation",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--mode", choices=[m.value for m in Mode], default=Mode.DEFAULT.value,
                        help="recommendation mode:\n" + mode_help)
    args = parser.parse_args()
    mode = Mode(args.mode)

    songs = load_songs("data/songs.csv")

    # --- Taste Profiles ---
    profiles = [
        # Profile A: Upbeat pop listener (gym / party)
        UserProfile(
        favorite_genre="pop", favorite_mood="happy", target_energy=0.85,
        likes_acoustic=False, target_valence=0.80, target_danceability=0.80),

        # Profile B: Chill lofi listener (study / focus)
        UserProfile(
            favorite_genre="lofi", favorite_mood="chill", target_energy=0.35,
            likes_acoustic=True, target_valence=0.58, target_danceability=0.55),
            
        # Profile C: Intense rock listener (workout / driving)
        UserProfile(
            favorite_genre="rock", favorite_mood="intense", target_energy=0.90,
            likes_acoustic=False, target_valence=0.45, target_danceability=0.70),

        # Profile D: Mellow jazz listener (evening wind-down)
        UserProfile(
            favorite_genre="jazz", favorite_mood="relaxed", target_energy=0.35,
            likes_acoustic=True, target_valence=0.72, target_danceability=0.50),

        # Profile E (adversarial): High energy + sad mood + wants danceability
        # These preferences conflict — sad songs are rarely high-energy or danceable.
        # Tests whether the system blindly adds up scores or produces nonsensical results.
        UserProfile(
            favorite_genre="pop", favorite_mood="sad", target_energy=0.95,
            likes_acoustic=False, target_valence=0.30, target_danceability=0.85)
    ]

    recommendations = [recommend_songs(user_pref, songs, k=5, mode=mode) for user_pref in profiles]

    print("\nTop recommendations:\n")
    for i, recs in enumerate(recommendations):
        print(f"--- Profile {i + 1} ---")
        table = [[song.title, song.artist, song.genre, song.mood, f"{score:.2f}", explanation]
                 for song, score, explanation in recs]
        print(tabulate(table, headers=["Title", "Artist", "Genre", "Mood", "Score", "Reasons"], tablefmt="grid"))
        print()


if __name__ == "__main__":
    main()
