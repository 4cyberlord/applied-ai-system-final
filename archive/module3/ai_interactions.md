# AI Interactions Log

## Agentic Workflow (SF8)
Actual user requests: audit the repository against the assignment without CLI validation; then complete all required and optional work directly on main, keep a TODO, and commit completed changes.

The assistant inspected the repository and identified a missing dataset expansion, duplicated scoring, incorrect explanations, missing evaluation evidence and unimplemented stretch challenges. It added ten synthetic tracks and five advanced fields (popularity, release decade, mood tag, duration, language), updated scoring, added strategy modes, diversity and formatted tables, expanded tests and rewrote documentation.

Manual verification by the assistant: read the CSV and source through GitHub; independently recalculated all four baseline top-five lists and the weight experiment using arithmetic outside the Python CLI. The expanded catalog changed the expected lofi winner from Library Rain to Ocean Lanterns, so the regression assertion was corrected. The assistant subsequently executed the hash-verified Python files in an isolated notebook: 14 pytest cases and 40 runtime scenarios passed. No student manual verification is claimed.

## Design Pattern (SF10)
A lightweight Strategy pattern uses a mapping of mode names to genre, mood and energy weights. A single score_song function selects those weights; both the functional and object interfaces delegate to it. This avoids maintaining separate formulas. The AI proposed this design while implementing the requested extensions; no separate brainstorming chat is claimed.

## Diversity and presentation
The assistant implemented greedy artist and genre penalties and an aligned text table with score explanations. A regression test specifies that a different artist should rank ahead of a repeated artist when base relevance is equal.

## Validation scope
Independent calculations and source review were followed by actual Python execution and captured output. See VALIDATION.md. The student should review and personalize the reflection and confirm personal learning activities.
