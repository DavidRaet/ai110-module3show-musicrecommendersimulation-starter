from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import pandas as pd

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
    Represents a user's taste preferences using weighted genre scores
    and target audio feature values.
    """
    genre_scores: Dict[str, float]  # {"pop": 4.5, "lofi": 3.2, ...}
    preferred_mood: Optional[str] = None
    pref_energy: float = 0.6
    pref_valence: float = 0.65
    pref_danceability: float = 0.65
    pref_acousticness: float = 0.5


def score_song(user: UserProfile, song: Song) -> float:
    """
    Scores a song against a user profile using a weighted sum of:
      - Genre preference (40%): how much the user likes this genre (0–5 scale)
      - Mood match (20%): whether the song's mood matches the user's preferred mood
      - Energy closeness (10%): how close the song's energy is to the user's target
      - Valence closeness (10%): how close the song's valence is to the user's target
      - Danceability closeness (10%): how close the song's danceability is to the user's target
      - Acousticness closeness (10%): how close the song's acousticness is to the user's target

    Returns a float between 0.0 and 1.0 that is rounded to 4 decimal places.
    """
    genre_raw = user.genre_scores.get(song.genre, 0.0)
    genre_component = (genre_raw / 5.0) * 0.40

    mood_match = 1.0 if (user.preferred_mood and song.mood == user.preferred_mood) else 0.0
    mood_component = mood_match * 0.20

    energy_component = (1.0 - abs(song.energy - user.pref_energy)) * 0.10
    valence_component = (1.0 - abs(song.valence - user.pref_valence)) * 0.10
    dance_component = (1.0 - abs(song.danceability - user.pref_danceability)) * 0.10
    acoustic_component = (1.0 - abs(song.acousticness - user.pref_acousticness)) * 0.10

    song_score = genre_component + mood_component + energy_component + valence_component + dance_component + acoustic_component

    return round(song_score, 4)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        topSongs = sorted(self.songs, key=lambda s: score_song(user, s), reverse=True)
        return topSongs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        genre_raw = user.genre_scores.get(song.genre, 0.0)
        mood_matched = user.preferred_mood and song.mood == user.preferred_mood

        def proximity(attr: str, song_val: float, user_val: float) -> str:
            if abs(song_val - user_val) <= 0.20:
                return f"The song's {attr} ({song_val:.2f}) score and your preferred {attr} ({user_val:.2f}) score seems to be close"
            return f"The song's {attr} ({song_val:.2f}) score and your preferred {attr} ({user_val:.2f}) score doesn't seem to match your style"

        parts = [
            f"Genre ({song.genre}): {genre_raw:.1f}/5",
            f"Mood ({song.mood}): {'matched' if mood_matched else 'no match'}",
            proximity("energy", song.energy, user.pref_energy),
            proximity("valence", song.valence, user.pref_valence),
            proximity("danceability", song.danceability, user.pref_danceability),
            proximity("acousticness", song.acousticness, user.pref_acousticness),
        ]
        return " | ".join(parts)


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    df = pd.read_csv(csv_path)
    return df.to_dict(orient='records')



def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    user_prefs keys: "genre" (str), "mood" (str, optional), "energy" (float, optional)
    Returns a list of (song_dict, score, explanation) tuples sorted by score descending.
    """
    # Build a UserProfile from the simple dict used by main.py
    genre = user_prefs.get("genre", "")
    user = UserProfile(
        genre_scores={genre: 5.0} if genre else {},
        preferred_mood=user_prefs.get("mood"),
        pref_energy=user_prefs.get("energy", 0.6),
    )

    def dict_to_song(d: Dict) -> Song:
        return Song(
            id=int(d.get("id", 0)),
            title=str(d.get("title", "")),
            artist=str(d.get("artist", "")),
            genre=str(d.get("genre", "")),
            mood=str(d.get("mood", "")),
            energy=float(d.get("energy", 0.0)),
            tempo_bpm=float(d.get("tempo_bpm", 0.0)),
            valence=float(d.get("valence", 0.0)),
            danceability=float(d.get("danceability", 0.0)),
            acousticness=float(d.get("acousticness", 0.0)),
        )

    rec = Recommender([dict_to_song(d) for d in songs])
    top_songs = rec.recommend(user, k=k)
    
    results = []
    original_by_id = {int(d.get("id", 0)): d for d in songs}
    for song in top_songs:
        sc = score_song(user, song)
        explanation = rec.explain_recommendation(user, song)
        results.append((original_by_id[song.id], sc, explanation))
    return results
