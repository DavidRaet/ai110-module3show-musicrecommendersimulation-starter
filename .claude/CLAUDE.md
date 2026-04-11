# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI 110 course assignment: a transparent, explainable content-based music recommender simulation. The goal is to score songs against a user profile using audio features and genre/mood preferences, then explain why each song was recommended.

## Commands

```bash
# Setup (Windows)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Run the app
python -m src.main

# Run all tests
pytest

# Run a single test
pytest tests/test_recommender.py::test_recommend_returns_songs_sorted_by_score -v
```

## Architecture

### Data Layer

- `data/songs.csv` — 18 songs with columns: `id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness` (audio features are 0.0–1.0 floats)
- `data/userProfile.csv` — 3 sample user profiles with genre preference scores (0–5 scale) and target audio feature values

### Core Module: `src/recommender.py`

Two parallel implementations exist — OOP and functional:

**Data classes:**
- `Song` — immutable dataclass representing a song with metadata + audio features
- `UserProfile` — dataclass with `genre_scores: Dict[str, float]`, `preferred_mood: Optional[str]`, and target feature floats (`pref_energy`, `pref_valence`, `pref_danceability`, `pref_acousticness`)

**OOP approach:**
- `Recommender(songs: List[Song])` — holds the song catalog
  - `recommend(user: UserProfile, k: int = 5) -> List[Song]` — returns top-k songs ranked by score
  - `explain_recommendation(user: UserProfile, song: Song) -> str` — returns human-readable explanation

**Functional approach:**
- `load_songs(csv_path: str) -> List[Dict]` — loads CSV via pandas
- `recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]` — returns `(song_dict, score, explanation)` tuples

### Entry Point: `src/main.py`

Loads songs from CSV, constructs a sample `user_prefs` dict (`{"genre": "pop", "mood": "happy", "energy": 0.8}`), calls `recommend_songs()`, and prints results.

## What's Implemented vs. TODO

**Implemented:** `Song` and `UserProfile` dataclasses, `load_songs()`, test scaffolding, sample data, README/model_card templates.

**Not implemented (stub/placeholder returns):**
- `Recommender.recommend()` — currently returns `self.songs[:k]` unsorted
- `Recommender.explain_recommendation()` — returns `"Explanation placeholder"`
- `recommend_songs()` — returns `[]`
- Scoring logic — no function exists yet to score songs against user preferences

## Scoring Design Intent

The scoring function should combine:
- Genre match: look up `user.genre_scores[song.genre]` (0–5 scale)
- Mood match: boolean/soft match between `user.preferred_mood` and `song.mood`
- Feature distance: closeness of `song.energy` to `user.pref_energy`, same for valence, danceability, acousticness

The system must be **transparent and explainable** — each recommendation score should decompose into named factors that can be surfaced to the user.

## Tests

`tests/test_recommender.py` has two tests:
1. Verifies that a pop/happy/high-energy user gets a pop song ranked above a lofi/chill/low-energy song
2. Verifies that `explain_recommendation()` returns a non-empty, non-placeholder string

Both tests currently fail because the scoring/recommendation logic is not implemented.
