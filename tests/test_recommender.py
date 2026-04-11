from src.recommender import Song, UserProfile, Recommender, score_song


def make_pop_song(id=1) -> Song:
    return Song(
        id=id,
        title="Test Pop Track",
        artist="Test Artist",
        genre="pop",
        mood="happy",
        energy=0.8,
        tempo_bpm=120,
        valence=0.9,
        danceability=0.8,
        acousticness=0.2,
    )


def make_lofi_song(id=2) -> Song:
    return Song(
        id=id,
        title="Chill Lofi Loop",
        artist="Test Artist",
        genre="lofi",
        mood="chill",
        energy=0.4,
        tempo_bpm=80,
        valence=0.6,
        danceability=0.5,
        acousticness=0.9,
    )


def make_pop_user() -> UserProfile:
    """User who strongly prefers pop/happy/high-energy/non-acoustic songs."""
    return UserProfile(
        genre_scores={"pop": 4.5, "lofi": 1.0},
        preferred_mood="happy",
        pref_energy=0.8,
        pref_valence=0.8,
        pref_danceability=0.75,
        pref_acousticness=0.2,
    )


def make_small_recommender() -> Recommender:
    return Recommender([make_pop_song(), make_lofi_song()])



def test_recommend_returns_songs_sorted_by_score():
    user = make_pop_user()
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # The pop/happy/high-energy song should rank above the lofi/chill/low-energy song
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = make_pop_user()
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "Explanation placeholder" not in explanation



def test_score_song_genre_is_primary_factor():
    """A song whose genre the user loves should score much higher than one they don't."""
    user = UserProfile(genre_scores={"pop": 5.0, "rock": 0.0})
    pop_song = make_pop_song()
    rock_song = Song(
        id=3, title="Rock Track", artist="A", genre="rock", mood="happy",
        energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2,
    )
    assert score_song(user, pop_song) > score_song(user, rock_song)


def test_score_song_mood_match_boosts_score():
    """Matching the user's preferred mood should produce a higher score."""
    user = UserProfile(genre_scores={"pop": 3.0}, preferred_mood="happy")
    happy_song = make_pop_song(id=1)
    chill_song = Song(
        id=4, title="Chill Pop", artist="A", genre="pop", mood="chill",
        energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2,
    )
    assert score_song(user, happy_song) > score_song(user, chill_song)


def test_score_song_audio_features_contribute():
    """A song with energy closer to the user's target should score higher."""
    user = UserProfile(genre_scores={}, pref_energy=0.8)
    close_energy = Song(
        id=5, title="Close Energy", artist="A", genre="unknown", mood="neutral",
        energy=0.8, tempo_bpm=120, valence=0.65, danceability=0.65, acousticness=0.5,
    )
    far_energy = Song(
        id=6, title="Far Energy", artist="A", genre="unknown", mood="neutral",
        energy=0.2, tempo_bpm=120, valence=0.65, danceability=0.65, acousticness=0.5,
    )
    assert score_song(user, close_energy) > score_song(user, far_energy)


def test_score_song_range():
    """score_song should always return a value between 0.0 and 1.0."""
    user = make_pop_user()
    for song in [make_pop_song(), make_lofi_song()]:
        s = score_song(user, song)
        assert 0.0 <= s <= 1.0
