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
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

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
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
