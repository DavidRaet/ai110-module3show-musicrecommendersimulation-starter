## 3pts Clear Explanation of How Music Recommendation Systems Work
- [X] Student provides a short explanation of how real-world recommenders (Spotify, YouTube, etc.) use data features (genre, mood, tempo, user history).
- [X] Explanation correctly distinguishes between input data, user preferences, and ranking/selection.
- [X] Explanation is specific, coherent, and consistent with basic ML literacy concepts (not generic or incorrect).

## 3pts Creation of a Structured Song Dataset
- [ ] A dataset of at least 15-20 songs is created, either as a list of dicts, list of objects, or loaded from a CSV.
- [ ] Each song includes at least 3 meaningful attributes (e.g., genre, mood, energy, tempo, era).
- [ ] Dataset is valid and loads/runs without errors.

## 3pts Scoring Function Accurately Reflects User Preferences
- [ ] A clear scoring function (e.g., score_song(user_prefs, song)) is implemented using weighting, matching, or similarity logic.
- [ ] Scoring logic works for all songs and returns consistent numeric output.
- [ ] Scoring reflects the designed features (e.g., if preferences emphasize "high energy," scoring actually incorporates energy).

## 3pts Recommendation Function Produces a Sorted List of Songs
- [ ] A function like recommend_songs(user_prefs, songs) is implemented that ranks or sorts songs by score.
- [ ] Output includes at least top 3 recommendations with a screenshot of the terminal output included in the README.
- [ ] Function runs without errors and works for different user profiles.

## 3pts Explanations Are Provided for Recommended Songs
- [ ] Each recommended song includes a short explanation of why it was selected (e.g., "high energy + matching genre").
- [ ] Explanations accurately reflect the scoring function (not generic statements).
- [ ] At least three explanations are provided and are clear and readable.

## 3pts Experiments with Multiple User Profiles
- [ ] At least three distinct user profiles are created (e.g., hip-hop fan, acoustic low-energy listener, high-tempo EDM listener).
- [ ] The recommender is run for each profile and screenshots of the terminal output for each profile are included in the README.
- [ ] Student comments on differences between outputs (e.g., "EDM profile prefers high energy songs; acoustic profile shifts toward low energy guitars").

## 3pts Completed Model Card
- [ ] Model card includes a description of dataset, attributes used, and intended purpose.
- [ ] Model card includes an explanation of the algorithmic approach in plain language.
- [ ] Model card identifies limitations/biases (e.g., genre imbalance, small dataset, popularity bias) and at least one improvement idea.