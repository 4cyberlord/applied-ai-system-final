# Model Card — VibeFinder 1.0

## Model Name
VibeFinder 1.0.

## Goal / Task
Recommend the five songs most relevant to a listener's stated preferences and explain every awarded point.

## Data Used
20 synthetic songs across 15 genres, including ten added tracks. Each has ID, title, artist, genre, mood, energy, tempo, valence, danceability, acousticness, popularity, release decade, detailed mood tag, duration and language. The metadata is invented for classroom testing, not measured from recordings or real listeners. Tempo, valence and danceability are descriptive only.

## Algorithm Summary
Balanced mode awards two points for genre, one for mood, up to one for energy proximity and half a point for acoustic preference. Optional advanced preferences each add up to half a point. Four selectable modes change the relative weights. Optional diversity reranking subtracts 0.75 for each already-selected song by the same artist and 0.25 for each already-selected song in the same genre. Each score is explained.

## Strengths
The logic is transparent, deterministic for a fixed catalog order, and easy to inspect. It recognizes familiar combinations such as happy pop and quiet lofi without training a model.

## Limitations and Bias
Genre has the largest default bonus and can hide songs with a closer mood or energy. The expanded dataset still gives some genres more candidates than others, creating unequal exposure. Synthetic popularity and language can reinforce biases if used as preferences. Diversity reduces repetition but can demote relevant tracks and is not a guarantee of fairness. The system has no actual listening history, lyrics or user satisfaction measurements.

## Evaluation
Actual Python execution confirmed the independently calculated first choices: High-Energy Pop — Sunrise City (4.390); Chill Lofi — Ocean Lanterns (4.390); Deep Intense Rock — Storm Runner (4.440); conflicting high-energy sad pop — Bittersweet Rush (4.380). Full top-five tables with reasons in the README were checked against captured Python output.

Sunrise City wins because it matches genre and happy mood, has energy only 0.02 away from the target, and adds 0.41 for low acousticness. Ocean Lanterns narrowly beats Library Rain because its energy is closer to the target despite being slightly less acoustic.

Pairwise comparisons:
- Pop vs lofi: the former rewards upbeat, less acoustic tracks; the latter promotes low-energy acoustic tracks. Their first choices differ because the profiles request different genre, mood and energy.
- Pop vs rock: Storm Runner wins for intense rock, while Sunrise City wins for happy pop. Gym Hero appears in both because its intensity and high energy fit rock and its genre fits pop.
- Lofi vs rock: Ocean Lanterns and Storm Runner sit at opposite energy targets and acoustic preferences, producing distinct lists.

The conflicting profile requests sad mood with 0.9 energy. Bittersweet Rush satisfies both; Quiet Letters matches sadness but loses points for energy and genre. A profile with a mood absent from the catalog receives no mood bonus, so other features decide.

Weight experiment: halve genre from 2 to 1 and double energy from 1 to 2. For pop, Sunrise City remains first (4.370), Accra Sunrise rises from fourth to second (3.340), Rooftop Lights from fifth to third (3.245), and Gym Hero drops from second to fifth (3.215). The change broadens exposure across genres, but without real feedback it cannot establish greater accuracy.

Regression tests cover data, scores, ranking, modes, optional features, diversity and the shared engine. All 14 pytest cases passed; 40 additional runtime scenarios passed across five profiles, four modes and both diversity settings. See VALIDATION.md.

## Intended Use and Non-Intended Use
Designed for classroom demonstrations of weighted ranking, explanations and bias. Not designed for production music services, commercial decisions, psychological profiling or predictions of actual listener satisfaction.

## Ideas for Improvement
1. Gather consented listener feedback and evaluate recommendations against it.
2. Expand and validate real metadata across languages and genres.
3. Measure relevance and exposure tradeoffs for different diversity settings.

## Personal Reflection
Reflection draft for the student to review and personalize: My biggest learning moment was understanding that scoring a song and ranking a list are separate tasks. AI helped draft and check the logic, but the sample explanations and expanded-catalog expectations needed independent arithmetic checks. It surprised me that a few weighted rules could produce a recognizable musical vibe. Next I would compare listener feedback against different ranking strategies.
