# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeSight**

---

## 2. Intended Use

This system suggests 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and other taste attributes. It is designed for classroom exploration of content-based recommendation systems, not for real users or production deployment. It assumes each user has a single, static taste profile and does not learn or adapt over time.

---

## 3. How the Model Works

The system compares every song in the catalog to a user's taste profile and assigns a score. Songs that closely match the user's preferences get higher scores.

The biggest factor is genre — if a song's genre matches the user's favorite, it gets a large bonus. Mood match is the second biggest factor. After that, numerical features like energy, valence (positivity), and danceability are scored by how close the song's value is to the user's target. A song with energy 0.82 and a user targeting 0.85 scores almost perfectly; a song at 0.30 scores poorly.

The advanced mode adds more attributes: whether the song meets a popularity threshold, whether it's from the user's preferred decade, whether its mood tags (like "euphoric" or "nostalgic") overlap with the user's preferences, how close its instrumentalness is to the target, and whether its lyrical theme matches.

Different modes change the scoring strategy. Explore mode penalizes same-genre songs to surface new discoveries. Diverse mode penalizes repeat artists and genres. Mood mode flips the priorities so mood and energy matter most and genre barely matters.

All songs are scored, sorted highest to lowest, and the top 5 are returned.

---

## 4. Data

The catalog contains 20 songs in `data/songs.csv`, expanded from an original 10. It covers 12 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, electronic, classical, r&b, hip hop, country) and 8 moods (happy, chill, intense, relaxed, moody, focused, sad, energetic).

Each song has 14 attributes: title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness, popularity, release_decade, mood_tags, instrumentalness, and lyrical_theme.

The dataset is small and reflects a narrow slice of musical taste. It skews toward English-language, Western genres. There are no songs in genres like K-pop, reggaeton, Afrobeats, or metal. The mood tags and lyrical themes were assigned manually and reflect the author's interpretation, not objective labels.

---

## 5. Strengths

- Users with clear, mainstream preferences (pop/happy, lofi/chill, rock/intense) get intuitive results. The top recommendation consistently matches what a human would pick.
- The scoring is fully transparent — every recommendation comes with a breakdown showing exactly how many points each feature contributed.
- Multiple modes let users explore different recommendation strategies without changing their profile.
- The system handles new songs immediately (no cold-start problem) since scoring is purely attribute-based.

---

## 6. Limitations and Bias

- **Genre dominance**: Genre match is worth 2.5 points, the single largest factor. This means same-genre songs almost always win, even when a cross-genre song might be a better emotional fit.
- **Independent scoring**: Features are scored and summed independently. The system cannot detect that "high energy + sad mood" is contradictory — it just adds up whatever points it can find.
- **Static weights**: Every user gets the same weight distribution. A user who cares deeply about lyrics but not energy is treated identically to one with opposite priorities.
- **Popularity bias**: In advanced mode, songs above the popularity threshold get a flat bonus, systematically suppressing lesser-known tracks regardless of how well they match.
- **Underrepresented tastes**: With only 20 songs and 12 genres, many user profiles (metal fans, classical enthusiasts) have zero or one genre match, producing weak recommendations.
- **No cultural context**: The system cannot understand that a song is good for a road trip, a breakup, or a workout. It only sees numbers and labels.

---

## 7. Evaluation

Five user profiles were tested across all modes:
- Profile A (pop/happy) — consistently returned "Sunrise City" as the top match, which felt correct.
- Profile B (lofi/chill) — "Library Rain" and "Midnight Coding" dominated, matching expectations for a study-music listener.
- Profile C (rock/intense) — "Storm Runner" was the clear winner, the only rock song in the catalog.
- Profile D (jazz/relaxed) — "Coffee Shop Stories" ranked first, the only jazz track. This exposed how sparse the catalog is for niche genres.
- Profile E (adversarial: pop + sad + high energy) — returned cheerful pop songs, ignoring the "sad" mood entirely. This confirmed the independent-scoring limitation.

Unit tests verify that genre matches produce higher scores, results are sorted correctly, and the correct number of results are returned.

---

## 8. Future Work

- **Collaborative filtering**: Use listening patterns from multiple users to discover "people like you also liked X" relationships.
- **Dynamic weights**: Let users indicate which features matter most to them, or learn weights from their feedback.
- **Coherence checking**: Detect contradictory preferences and either warn the user or adjust scoring to handle them.
- **Larger catalog**: 20 songs is too few for meaningful recommendations. A real system would need hundreds or thousands.
- **Context awareness**: Factor in time of day, activity, or recent listening history to adapt recommendations.
- **Explanation quality**: Instead of showing raw score breakdowns, generate natural-language explanations like "Because you like upbeat pop and this has a similar vibe."

---

## 9. Personal Reflection

Building this system made it clear that recommendations are just weighted arithmetic on features. The system feels intelligent when the weights happen to align with human intuition, but it has no understanding of music — it cannot tell that a nostalgic synthwave track and a nostalgic country ballad share an emotional quality that transcends genre.

The adversarial profile was the most revealing experiment. Asking for "sad + high energy" produced cheerful pop songs because the math worked out. In a real product, this kind of silent failure could push users toward content that doesn't match their emotional state. The weights encode assumptions about what matters in music preference, and those assumptions are baked in by the designer, not learned from the people the system serves. That gap between "mathematically optimal" and "actually good" is where human judgment still matters.
