# Reproducible evaluation

Run from the repository root:

```bash
python -m pytest -q
python -m src.applied "happy pop high energy" --k 1
python -m src.applied "chill lofi acoustic" --k 1
python -m src.applied "pop rock"
```

| Test input | Criteria | Status |
| --- | --- | --- |
| Happy pop, high energy | Best candidate and grounded score | Expected; runtime pending |
| Chill lofi acoustic | Acoustic and mood preference | Expected; runtime pending |
| Pop rock | Safe ambiguity error | Expected; runtime pending |
| Reversed ranking | Evaluator rejects and retries | Test implemented; runtime pending |
| Incorrect but plausible ranking | Evaluator detects ranking error | Test implemented; runtime pending |
| Altered score or reason | Evaluator rejects | Test implemented; runtime pending |

The test source is committed. No actual execution has yet been verified for this repository. The original project validation records are archived separately and do not establish that the new application passes.
