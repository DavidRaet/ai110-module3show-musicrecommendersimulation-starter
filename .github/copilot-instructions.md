# Music Recommender Simulation — Copilot Instructions

## Project Summary

This is an AI 110 course assignment to build and evaluate a music recommender system. The system scores songs based on user preferences and returns ranked recommendations with explanations.

**Key Goal:** Implement a transparent, explainable recommendation engine and reflect on how it mirrors real-world systems like Spotify.

See [README.md](../README.md) for full project overview and rubric requirements.

---

## Architecture & Key Components

### Data Layer
- **Song Dataset:** `data/songs.csv` — 10+ songs with features: genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- **Dataclasses** (`src/recommender.py`):
  - `Song` — Immutable song representation with id, title, artist, and 7 feature attributes
  - `UserProfile` — User preferences: favorite_genre, favorite_mood, target_energy, likes_acoustic

### Core Logic Layer (`src/recommender.py`)
- **`load_songs(csv_path)`** — Parses CSV, returns List[Dict] or List[Song]
- **`Recommender` class** — Main recommendation engine:
  - `recommend(user, k=5)` — Returns top-k Song objects ranked by score
  - `explain_recommendation(user, song)` — Returns human-readable explanation string
- **Scoring Function** (your design):
  - Must weight multiple features (genre match, mood match, energy preference, etc.)
  - Return numeric score (higher = better match)
  - Be transparent and explainable

### Entry Point (`src/main.py`)
- Loads songs, creates sample UserProfile, calls `recommend_songs()`
- Prints top recommendations with (song, score, explanation) tuples
- Run with: `python -m src.main`

---

## Development Workflow

### Setup
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running & Testing
- **Run app:** `python -m src.main`
- **Run tests:** `pytest` or `pytest -v`
- **View test file:** `tests/test_recommender.py` defines expected behavior

### Key Test Expectations
- `recommend()` must return Song objects sorted by score (highest first)
- Pop + happy + high energy songs should score higher for "pop/happy/0.8 energy" users
- `explain_recommendation()` must return non-empty strings with specific reasoning
- All code must run without errors across multiple user profiles

---

## Design Patterns & Conventions

### Type Hints
All functions use Python type hints. Maintain this throughout:
```python
def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
    pass

def score_song(user: UserProfile, song: Song) -> float:
    pass
```

### Dataclass Usage
Use `@dataclass` for data structures; provides automatic `__init__`, comparison, and repr:
```python
from dataclasses import dataclass

@dataclass
class Song:
    id: int
    title: str
    # ... other fields
```

### CSV Handling
- Use `pandas` (already in requirements) or `csv` module
- Songs.csv uses comma-separated fields; first row is header
- Return structured data (list of dicts or Song objects), not raw strings

### Scoring Philosophy
- **Transparent:** Scoring must reflect the features you use (no "black box")
- **Explainable:** Your `explain_recommendation()` should cite which features matched
- **Examples of scoring approaches:**
  - Weighted sum: `score = w_genre * genre_match + w_energy * energy_match + ...`
  - Distance-based: `score = 1 / (1 + distance(user_prefs, song_features))`
  - Matching logic: `score = base_score + bonus_if_genre_matches + bonus_if_mood_matches`

---

## Rubric Focus Areas

See [rubric.md](../rubric.md) for full requirements. Key checkpoints:

1. **Clear explanation** of real-world recommenders (use README section)
2. **Structured dataset** with ≥15-20 songs and ≥3 meaningful attributes
3. **Scoring function** that accurately weights user preferences
4. **Recommendation function** that sorts by score, returns top-k with explanations
5. **Experiments** — Run recommender on ≥3 distinct user profiles (hip-hop fan, acoustic listener, EDM fan, etc.) and document in README
6. **Model card** (model_card.md) — Include dataset description, approach, limitations, and improvement ideas

---

## Common Implementation Patterns

### Pattern 1: Simple Weighted Scoring
```python
def score_song(user, song):
    score = 0
    if song.genre == user.favorite_genre:
        score += 2.0
    if song.mood == user.favorite_mood:
        score += 1.5
    # Higher target_energy = prefer energetic songs
    score += abs(song.energy - user.target_energy) * -0.5
    if song.acousticness > 0.5 and user.likes_acoustic:
        score += 1.0
    return score
```

### Pattern 2: Normalized Distance-Based Scoring
```python
def score_song(user, song):
    genre_match = 1.0 if song.genre == user.favorite_genre else 0.0
    energy_diff = abs(song.energy - user.target_energy)
    acoustic_bonus = 1.0 if (song.acousticness > 0.5) == user.likes_acoustic else 0.0
    return genre_match + (1 - energy_diff) + acoustic_bonus
```

### Pattern 3: OOP Approach (if completing the Recommender class)
```python
class Recommender:
    def __init__(self, songs):
        self.songs = songs
    
    def score_song(self, user, song):
        # Your scoring logic
        return score
    
    def recommend(self, user, k=5):
        scores = [(song, self.score_song(user, song)) for song in self.songs]
        sorted_songs = sorted(scores, key=lambda x: x[1], reverse=True)
        return [song for song, score in sorted_songs[:k]]
    
    def explain_recommendation(self, user, song):
        return f"This song matches your preference for {user.favorite_genre} genre and has {song.energy:.1f} energy."
```

---

## Testing Your Implementation

### Run Individual Tests
```bash
pytest tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score -v
pytest tests/test_recommender.py::test_explain_recommendation_returns_non_empty_string -v
```

### Debug Tips
- Use `print()` statements in scoring function to see intermediate scores
- Create a small test dataset with 2-3 songs to trace logic
- Verify that UserProfile preferences actually influence song scores
- Check that recommendation output changes for different user profiles

---

## Documentation Artifacts

You will create or update:
- **README.md** — Explain your design, show terminal output screenshots, document experiments
- **model_card.md** — Describe dataset, approach, limitations, improvements
- **src/recommender.py** — Docstrings for Song, UserProfile, Recommender, and all functions

---

## Key Files to Edit

| File | Purpose |
|------|---------|
| `src/recommender.py` | Implement Song, UserProfile, Recommender, load_songs(), scoring logic |
| `src/main.py` | Already scaffolded; calls your functions and prints results |
| `tests/test_recommender.py` | Read to understand expected behavior; add your own tests |
| `data/songs.csv` | May expand from 10 to 15-20 songs for richer recommendations |
| `README.md` | Document your design, experiments, and results |
| `model_card.md` | Explain dataset, approach, limitations |

---

## Quick Start Checklist

- [ ] Activate virtual environment and install dependencies
- [ ] Read `tests/test_recommender.py` to understand expected interfaces
- [ ] Implement `load_songs()` to parse CSV into Song objects
- [ ] Design and implement scoring function (decide which features to weight)
- [ ] Implement `Recommender.recommend()` to sort songs by score
- [ ] Implement `Recommender.explain_recommendation()` with meaningful explanations
- [ ] Run `pytest` — all tests should pass
- [ ] Create ≥3 user profiles and test in `main.py`; save terminal output
- [ ] Document experiments in README.md
- [ ] Write model_card.md with dataset, approach, limitations
- [ ] Final check: run `python -m src.main` and verify output looks good

---

## Tips for Success

1. **Start with scoring logic** — This is the heart of the system. Design it clearly before coding.
2. **Explain as you go** — If you can't explain why a song scored high, your scoring function is unclear.
3. **Test with diverse users** — A hip-hop fan should get different recommendations than an acoustic lover.
4. **Iterate on weights** — Try different weight values in the scoring function; document what you experiment with.
5. **Call out limitations** — Real recommenders show bias, miss niche users, depend on data quality. Be honest about yours.
