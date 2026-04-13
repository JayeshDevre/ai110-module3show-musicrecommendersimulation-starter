# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube combine two strategies: collaborative filtering (learning from what millions of similar users enjoy) and content-based filtering (matching the actual attributes of songs to a user's taste profile). Our version focuses on content-based filtering — no other users needed. Each song is described by a set of numeric and categorical features, and the system scores every song by measuring how closely it matches what the user prefers. The closer the match across all features, the higher the score. Songs are then ranked by score and the top results are returned as recommendations. This approach is transparent, explainable, and works even for a brand-new user with no listening history.

### Scoring Rule (one song)

For each numeric feature, we use a proximity score — not "higher is better," but "closer to the user's preference is better." The formula for a single numeric feature is:

```
proximity = 1 - |song_value - user_preference|
```

This gives 1.0 for a perfect match and approaches 0.0 as the values diverge. Each feature is then multiplied by its weight and summed into a final score:

```
score = (w_energy   × proximity(energy))
      + (w_valence  × proximity(valence))
      + (w_acoustic × proximity(acousticness))
      + (w_dance    × proximity(danceability))
      + (w_genre    × exact_match(genre))
      + (w_mood     × exact_match(mood))
```

Categorical features (genre, mood) use a binary match: 1.0 if they match, 0.0 if not.

### Weights

Genre carries the highest weight because it represents the broadest stylistic boundary — recommending a metal track to a lofi listener is a bigger miss than a slight energy mismatch. Mood is weighted second because it captures emotional intent (a user wanting "chill" music doesn't want "intense" regardless of genre). Numeric features like energy and valence are weighted next since they define the emotional texture within a genre. Danceability and acousticness are supporting signals.

| Feature       | Weight | Rationale |
|---------------|--------|-----------|
| genre         | 3.0    | Broadest stylistic boundary |
| mood          | 2.0    | Emotional intent of the listening session |
| energy        | 1.5    | Core intensity signal |
| valence       | 1.5    | Emotional tone (dark vs. bright) |
| acousticness  | 1.0    | Texture signal (organic vs. electronic) |
| danceability  | 0.5    | Supporting signal, partially redundant with energy |

### Ranking Rule (list of songs)

The scoring rule produces a number for one song. The ranking rule applies that scoring rule to every song in the catalog, sorts the results in descending order, and returns the top N. Without the ranking step, a score is just a number with no context — ranking is what turns individual scores into a recommendation list.

### Song and UserProfile Features

`Song` object fields:
- `id`, `title`, `artist`
- `genre` (categorical)
- `mood` (categorical)
- `energy` (float, 0–1)
- `valence` (float, 0–1)
- `danceability` (float, 0–1)
- `acousticness` (float, 0–1)
- `tempo_bpm` (int, used as soft filter only)

`UserProfile` object fields:
- `preferred_genre` (categorical)
- `preferred_mood` (categorical)
- `preferred_energy` (float, 0–1)
- `preferred_valence` (float, 0–1)
- `preferred_danceability` (float, 0–1)
- `preferred_acousticness` (float, 0–1)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

