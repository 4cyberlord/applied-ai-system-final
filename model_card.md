# Model card — VibeFinder AI 2.0

## Purpose and intended use
Educational music discovery and explainable ranking for a small synthetic catalog. Not a production streaming service, psychological profiler or trained language model.

## Data and method
Twenty synthetic songs across fifteen genres. Metadata includes genre, mood, energy, acousticness and optional advanced fields. The bounded parser supports explicit positive preferences; it rejects ambiguity and negation. Weighted scoring ranks retrieved candidates, and an integrated evaluator checks identities, scores, reasons, ordering and count. One retry is permitted.

## AI collaboration and design reflection
The following is an assistant-prepared record and reflection draft for the student to review and personalize. The user requested an evolution of the original project, direct commits to a separate public repo and reproducible validation. AI assisted with design, code, tests and documentation.

Accepted design suggestion: add a runtime evaluator, rather than only standalone tests, so incorrect recommendations are withheld before reaching the listener. Revised design suggestion: instead of claiming that local retrieval and fixed text explanations constitute LLM RAG, identify the system accurately as a deterministic reliability-enhanced recommender. This avoids unsupported claims and API dependencies.

## Bias, safety and limitations
The dataset is synthetic and cannot establish real music relevance. Genre weighting can produce filter bubbles; some genres have more tracks than others. Language and popularity attributes could amplify representation bias. Diversity can sacrifice relevance and does not establish fairness. The parser is limited to explicit English terms and cannot reliably interpret nuanced or multilingual requests. The evaluator checks algorithmic consistency, not actual human satisfaction, and shares the scoring function with the ranker. Logs omit the raw query, but users should not enter private information.

## Testing and evaluation
Automated tests cover the inherited engine, supported and unsupported preferences, strategies, diversity, invalid outputs and retry behavior. All 44 automated tests passed in Python 3.13.5 with pytest 9.0.2. Fault injection confirmed that incorrect rankings and altered evidence are rejected, a successful retry recovers, and repeated failure releases no results. The initial predicted pop score was corrected using actual runtime output. See evaluation/test_results.md. Human relevance evaluation has not been conducted.

## Future improvements
Add consented listener feedback, independently implement the reference scoring oracle, improve multilingual parsing, and evaluate exposure and relevance on a larger catalog.

## Personal reflection
Draft for student review: I learned that a recommendation is not reliable merely because it looks plausible. Separating candidate ranking from verification helped me understand how guardrails and tests can make AI systems easier to debug. I would next evaluate the recommendations with real listener feedback and revise the preference parser. The student should confirm or revise this account to reflect their own experience.
