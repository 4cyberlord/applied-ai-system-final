# Runtime validation

## Scope and reproducibility

Validated source snapshot: [70ee38d](https://github.com/4cyberlord/ai110-module3show-musicrecommendersimulation-starter/commit/70ee38d53b668c99791db3929a99199aa1b46b5c).

The assistant retrieved these files through GitHub and verified the Git blob SHA-1 of each copied file before executing them in an isolated Python notebook:

| File | Verified blob SHA |
| --- | --- |
| src/recommender.py | 5fb93c50d1844c2e3439522a5496272d93807f9e |
| src/main.py | c36201beb2a61d7b45486f562de55cd09c3a49ff |
| tests/test_recommender.py | a27aa72cd3572838aaa04d9899408b0e6f06535e |
| data/songs.csv | c22bdec20053e70751dae3d954622976727ae4fc |

No GitHub CLI, GitHub Actions or separate hosted service was required. The Python interpreter was executed in a notebook; pytest was invoked through its Python API, and the application's main function was called with explicit argument lists while stdout was captured.

## Actual pytest result

```text
..............                                                           [100%]
14 passed in 0.10s
Exit: 0
```

## Extended runtime checks

40 of 40 scenarios passed: five profiles (four defaults plus Advanced) x four scoring modes x two diversity settings. Each scenario checked that the five recommendations were unique, their scores were finite and descending, explanations were nonempty, and the application printed its loaded-song count and table headers.

Default profile winners: Sunrise City (4.390), Ocean Lanterns (4.390), Storm Runner (4.440), Bittersweet Rush (4.380). The captured baseline and weight-shift tables matched the tables in README.md.

## Captured advanced profile output

```text
Loaded songs: 20

Advanced profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False, 'popularity': 80, 'release_decade': 2020, 'mood_tag': 'bright', 'duration_seconds': 210, 'language': 'tw'}
Mode: balanced; diversity: True
Rank | Song             | Artist        | Score | Reasons
-----+------------------+---------------+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1    | Sunrise City     | Neon Echo     | 6.380 | genre match (+2.000); mood match (+1.000); mood_tag match (+0.500); energy similarity (+0.980); popularity similarity (+0.490); release_decade similarity (+0.500); duration_seconds similarity (+0.500); acoustic preference (+0.410)
2    | Accra Sunrise    | Kora Wave     | 4.868 | mood match (+1.000); mood_tag match (+0.500); language match (+0.500); energy similarity (+0.950); popularity similarity (+0.495); release_decade similarity (+0.500); duration_seconds similarity (+0.483); acoustic preference (+0.440)
3    | Gym Hero         | Max Pulse     | 4.547 | genre match (+2.000); energy similarity (+0.870); popularity similarity (+0.460); release_decade similarity (+0.500); duration_seconds similarity (+0.492); acoustic preference (+0.475); diversity penalty (-0.250)
4    | Rooftop Lights   | Indigo Parade | 4.247 | mood match (+1.000); mood_tag match (+0.500); energy similarity (+0.960); popularity similarity (+0.470); release_decade similarity (+0.500); duration_seconds similarity (+0.492); acoustic preference (+0.325)
5    | Bittersweet Rush | Neon Echo     | 3.542 | genre match (+2.000); energy similarity (+0.920); popularity similarity (+0.485); release_decade similarity (+0.500); duration_seconds similarity (+0.487); acoustic preference (+0.400); diversity penalty (-1.250)
```

## Limits

This establishes the tested behavior in one Python environment, not universal correctness or real-world recommendation quality. Student-authored reflection and personal learning activities still need the student's own review. Documentation-only commits after the tested snapshot do not change the validated Python source, dataset, or tests.
