"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Dict, List

from recommender import load_songs, recommend_songs
from user_preferences import user_preferences

def runRecommender(user_prefs: Dict, songs: List[Dict]) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()

def main() -> None:
    songs = load_songs("../data/songs.csv")
    # Starter example profile
    user_prefsOne = user_preferences[1]
    user_prefsTwo = user_preferences[2]
    user_prefsThree = user_preferences[3]

    runRecommender(user_prefsOne, songs)
    runRecommender(user_prefsTwo, songs)
    runRecommender(user_prefsThree, songs)


if __name__ == "__main__":
    main()


