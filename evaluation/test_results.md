# Reproducible evaluation

Tested snapshot: [aed0c1c](https://github.com/4cyberlord/applied-ai-system-final/commit/aed0c1cc5d0c297dc51b2ac4478b09b401eaf263). All source files, tests, dataset and dependency manifest were matched against GitHub blob hashes before execution in an isolated Python 3.13.5 notebook environment using pytest 9.0.2. No GitHub CLI or Actions used. The first collection attempt encountered a cached test module from an earlier project in the notebook; clearing that cache and using importlib collection resolved the environment issue.

Reproduce from the repository root:

```bash
python -m pip install -r requirements.txt
python -m pytest -q --import-mode=importlib
```

Actual captured test result:

```text
............................................                             [100%]
44 passed in 0.06s
Exit: 0
```

| Test input | Criteria | Result |
| --- | --- | --- |
| Four ranking modes, diversity on/off | Five valid ranked results per scenario | Pass |
| Happy pop high energy | Grounded recommendation and validation | Pass |
| Chill lofi acoustic | Grounded acoustic and mood preference | Pass |
| Pop rock | Safe ambiguity error | Pass |
| Reversed ranking | Reject and retry | Pass |
| Incorrect but plausible ranking | Detect ranking error | Pass |
| Altered score or reason | Reject invalid output | Pass |
| Ranker mutates trusted data | Isolate evidence and recover | Pass |
| Duplicate or nonfinite results | Reject | Pass |
| Both attempts fail | Release no results | Pass |
| Contradictory acoustic preference | Reject ambiguity | Pass |

## Actual application stdout

Captured by calling the same main function used by the documented module commands with explicit argument lists. Diagnostic logging is emitted separately. Successful examples returned exit code 0.

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

```text
Input: python -m src.applied "intense rock non-acoustic" --mode energy-focused --diversity --k 3
Loaded songs: 20
Preferences: {'genre': 'rock', 'mood': 'intense', 'likes_acoustic': False}
Rank | Song           | Artist     | Score | Reasons
-----+----------------+------------+-------+------------------------------------------------------------------------
1    | Storm Runner   | Voltline   | 2.450 | genre match (+1.000); mood match (+1.000); acoustic preference (+0.450)
2    | Gym Hero       | Max Pulse  | 1.475 | mood match (+1.000); acoustic preference (+0.475)
3    | Velvet Thunder | Iron Coast | 0.490 | acoustic preference (+0.490)
Reliability: PASS (3 checked; attempts: 1)
```

Observed diagnostic messages for successful requests:

```text
INFO Retrieved 20 candidates
INFO Evaluation attempt 1: pass
```

The initial expected pop score was revised from 4.330 to 3.920: unspecified acoustic preferences correctly contribute no points. Tests establish algorithmic consistency and recovery, not actual listener satisfaction. Human relevance evaluation remains future work.
