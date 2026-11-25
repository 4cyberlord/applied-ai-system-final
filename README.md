# VibeFinder AI 2.0

An explainable music recommendation system with an integrated reliability gate. It translates a limited natural-language request into preferences, retrieves catalog candidates, ranks them, verifies the results and retries a failed ranking once.

## Original project (Modules 1–3)

[Music Recommender Simulation](https://github.com/4cyberlord/ai110-module3show-musicrecommendersimulation-starter) used weighted content-based scoring to rank songs by genre, mood, energy and acoustic preferences. It supported four scoring modes, advanced attributes and optional diversity reranking. This final project reuses that engine and adds bounded language input and runtime verification before results are released.

The source snapshot is [e7860b7](https://github.com/4cyberlord/ai110-module3show-musicrecommendersimulation-starter/commit/e7860b7a84bbc50bf397d35c5d12173153480066). Original documentation is archived in archive/module3. The independent repository contains a copied snapshot; original Git ancestry could not be transferred through the connector.

## Architecture

See [Mermaid source](diagrams/architecture.mmd). The parser extracts supported preferences, the retriever reads trusted catalog evidence, and the ranker scores and optionally diversifies results. The evaluator independently checks the best remaining candidate, score, identity, explanation and completeness. A failed result triggers one retry with the trusted ranker; a second failure releases no recommendations. Logs record candidate counts and verification outcomes, not raw requests. Automated tests inject faults; human review is needed to judge musical relevance.

## Setup

Use Python 3.10+ from the repository root. No API keys or network services are needed.

```bash
python -m venv .venv
# Activate: source .venv/bin/activate (Windows: .venv\Scripts\activate)
python -m pip install -r requirements.txt
python -m src.applied "happy pop high energy" --k 3
python -m pytest
```

Use --mode balanced, genre-first, mood-first or energy-focused; add --diversity to reduce repetition. The original module remains available via python -m src.main.

## Sample interactions

Actual captured Python application output (successful examples exit 0):

```text
Input: python -m src.applied "happy pop high energy" --k 1
Loaded songs: 20
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
Rank | Song         | Artist    | Score | Reasons
-----+--------------+-----------+-------+----------------------------------------------------------------------
1    | Sunrise City | Neon Echo | 3.920 | genre match (+2.000); mood match (+1.000); energy similarity (+0.920)
Reliability: PASS (1 checked; attempts: 1)
```

```text
Input: python -m src.applied "chill lofi acoustic" --k 1
Loaded songs: 20
Preferences: {'genre': 'lofi', 'mood': 'chill', 'likes_acoustic': True}
Rank | Song         | Artist         | Score | Reasons
-----+--------------+----------------+-------+------------------------------------------------------------------------
1    | Library Rain | Paper Lanterns | 3.430 | genre match (+2.000); mood match (+1.000); acoustic preference (+0.430)
Reliability: PASS (1 checked; attempts: 1)
```

```text
Input: python -m src.applied "pop rock"
Loaded songs: 20
Error: Choose one genre and one mood per request.
Exit status: 1
```

## Design decisions

The advanced feature required by the assignment is the integrated reliability/testing system. The workflow also follows a bounded plan-act-check-retry pattern. Catalog retrieval and deterministic template explanations are not claimed to be LLM-based RAG; no trained model or external LLM is used. This trades flexible interpretation for reproducibility, low cost and transparent evidence. The full catalog is retrieved to avoid excluding the actual best candidate. The verifier shares the scoring formula, so it detects ranking and output errors but cannot detect every shared scoring-design defect.

## Testing summary

The inherited tests and new parameterized tests cover preference extraction, invalid requests, four modes with and without diversity, fault recovery, wrong rankings, altered scores and explanations, and command entry behavior. All 44 automated tests passed. Fault injection confirmed recovery and fail-closed behavior. See [evaluation notes](evaluation/test_results.md) for actual execution evidence. Do not interpret a reliability PASS as a probability of listener satisfaction.

## Reflection

Reliable AI needs a way to detect incorrect output before it reaches a user. Separating ranking from evaluation makes errors observable and enables bounded recovery. The responsible-AI reflection and limitations are in [model_card.md](model_card.md).

## Repository layout

- src/: original and applied recommendation logic
- data/: synthetic music catalog
- tests/: regression and integration tests
- diagrams/: editable Mermaid architecture
- assets/: supplementary architecture media
- evaluation/: reproducible evidence and validation notes
- archive/module3/: original project documentation
