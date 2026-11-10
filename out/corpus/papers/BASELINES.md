# Paper ground truth: baseline scores

Written by `python3 bench/paper_truth.py --baselines`. Each cell is **exact / near**: the number of paper items with a mapped declaration in the first k listed declarations, and the number with a mapped declaration in the first k or one dependency step from one of them. Random rows are means over 200 seeded random orders (seed 20261110).

## ns: 86 paper items, 36,203 declarations, 7,671 with a docstring

### all mapped items (any confidence): 85 items

| list | size | k=10 | k=20 | k=50 | k=100 | k=200 | k=500 | k=1000 | k=2000 | k=5000 | all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dominator outline `ns_r3` | 69 | 5 / 12 | 6 / 20 | 8 / 49 |  |  |  |  |  |  | 8 / 56 |
| dominator outline `ns_periodic` | 69 | 6 / 11 | 7 / 19 | 9 / 49 |  |  |  |  |  |  | 9 / 56 |
| largest proof beneath it (proof mass reachable through dependencies) | 36,203 | 3 / 3 | 5 / 8 | 7 / 15 | 8 / 16 | 10 / 19 | 10 / 19 | 10 / 20 | 11 / 21 | 17 / 27 | 85 / 85 |
| own proof size | 36,203 | 0 / 0 | 0 / 0 | 4 / 11 | 10 / 24 | 13 / 37 | 19 / 45 | 30 / 55 | 43 / 68 | 56 / 80 | 85 / 85 |
| has a docstring, ordered by proof mass beneath | 7,671 | 3 / 3 | 7 / 11 | 8 / 16 | 9 / 19 | 9 / 19 | 12 / 23 | 32 / 50 | 57 / 69 | 75 / 85 | 83 / 85 |
| has a docstring, random order (mean) | 7,671 | 0.26 / 4.47 | 0.54 / 8.43 | 1.43 / 16.51 | 2.71 / 25.77 | 5.34 / 38.94 | 13.04 / 60.85 | 24.41 / 74.33 | 42.73 / 81.67 | 73.95 / 84.58 | |
| any declaration, random order (mean) | 36,203 | 0.06 / 3.64 | 0.1 / 6.14 | 0.34 / 11.57 | 0.63 / 17.36 | 1.27 / 27.0 | 3.19 / 44.25 | 6.2 / 59.76 | 12.19 / 73.36 | 28.7 / 82.67 | |

Dominator outline by level (cumulative exact / near): `ns_r3`: root + spine (5) 1/6, level 1 (chapters) (18) 6/19, level 2 (32) 7/22, level 3 (45) 8/22, toolkit (69) 8/56; `ns_periodic`: root + spine (5) 2/5, level 1 (chapters) (18) 7/18, level 2 (32) 8/21, level 3 (45) 9/21, toolkit (69) 9/56

### items mapped at probable or certain: 79 items

| list | size | k=10 | k=20 | k=50 | k=100 | k=200 | k=500 | k=1000 | k=2000 | k=5000 | all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dominator outline `ns_r3` | 69 | 5 / 12 | 6 / 20 | 8 / 46 |  |  |  |  |  |  | 8 / 53 |
| dominator outline `ns_periodic` | 69 | 6 / 11 | 7 / 19 | 9 / 46 |  |  |  |  |  |  | 9 / 53 |
| largest proof beneath it (proof mass reachable through dependencies) | 36,203 | 3 / 3 | 5 / 8 | 7 / 15 | 8 / 16 | 10 / 19 | 10 / 19 | 10 / 20 | 11 / 21 | 17 / 27 | 79 / 79 |
| own proof size | 36,203 | 0 / 0 | 0 / 0 | 4 / 11 | 9 / 22 | 12 / 35 | 18 / 43 | 27 / 52 | 39 / 64 | 52 / 74 | 79 / 79 |
| has a docstring, ordered by proof mass beneath | 7,671 | 3 / 3 | 7 / 11 | 8 / 16 | 9 / 19 | 9 / 19 | 12 / 23 | 31 / 47 | 53 / 63 | 69 / 79 | 77 / 79 |
| has a docstring, random order (mean) | 7,671 | 0.26 / 4.4 | 0.54 / 8.24 | 1.38 / 15.97 | 2.6 / 24.68 | 5.12 / 37.01 | 12.53 / 57.66 | 23.38 / 70.2 | 40.71 / 76.78 | 69.63 / 78.94 | |
| any declaration, random order (mean) | 36,203 | 0.06 / 3.58 | 0.1 / 6.04 | 0.34 / 11.16 | 0.61 / 16.63 | 1.23 / 25.58 | 3.06 / 41.72 | 5.92 / 55.95 | 11.52 / 68.42 | 26.96 / 76.79 | |

Dominator outline by level (cumulative exact / near): `ns_r3`: root + spine (5) 1/6, level 1 (chapters) (18) 6/19, level 2 (32) 7/22, level 3 (45) 8/22, toolkit (69) 8/53; `ns_periodic`: root + spine (5) 2/5, level 1 (chapters) (18) 7/18, level 2 (32) 8/21, level 3 (45) 9/21, toolkit (69) 9/53

### items mapped at certain: 20 items

| list | size | k=10 | k=20 | k=50 | k=100 | k=200 | k=500 | k=1000 | k=2000 | k=5000 | all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dominator outline `ns_r3` | 69 | 1 / 6 | 1 / 6 | 1 / 10 |  |  |  |  |  |  | 1 / 10 |
| dominator outline `ns_periodic` | 69 | 2 / 5 | 2 / 5 | 2 / 10 |  |  |  |  |  |  | 2 / 10 |
| largest proof beneath it (proof mass reachable through dependencies) | 36,203 | 3 / 3 | 4 / 5 | 7 / 8 | 7 / 8 | 7 / 8 | 7 / 8 | 7 / 8 | 7 / 9 | 7 / 9 | 20 / 20 |
| own proof size | 36,203 | 0 / 0 | 0 / 0 | 0 / 1 | 0 / 1 | 0 / 3 | 1 / 4 | 4 / 9 | 5 / 10 | 10 / 16 | 20 / 20 |
| has a docstring, ordered by proof mass beneath | 7,671 | 3 / 3 | 7 / 8 | 7 / 8 | 7 / 8 | 7 / 8 | 7 / 9 | 9 / 11 | 12 / 14 | 17 / 20 | 20 / 20 |
| has a docstring, random order (mean) | 7,671 | 0.03 / 0.57 | 0.07 / 1.1 | 0.2 / 2.46 | 0.39 / 4.05 | 0.8 / 6.57 | 2.14 / 11.46 | 4.18 / 15.52 | 7.71 / 18.43 | 15.37 / 19.91 | |
| any declaration, random order (mean) | 36,203 | 0.01 / 0.25 | 0.01 / 0.43 | 0.06 / 1.2 | 0.12 / 2.05 | 0.24 / 3.83 | 0.55 / 6.98 | 1.08 / 10.44 | 1.99 / 14.29 | 4.68 / 18.04 | |

Dominator outline by level (cumulative exact / near): `ns_r3`: root + spine (5) 1/3, level 1 (chapters) (18) 1/6, level 2 (32) 1/7, level 3 (45) 1/7, toolkit (69) 1/10; `ns_periodic`: root + spine (5) 2/2, level 1 (chapters) (18) 2/5, level 2 (32) 2/6, level 3 (45) 2/6, toolkit (69) 2/10

## euler: 31 paper items, 16,302 declarations, 4,839 with a docstring

### all mapped items (any confidence): 31 items

| list | size | k=10 | k=20 | k=50 | k=100 | k=200 | k=500 | k=1000 | k=2000 | k=5000 | all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dominator outline `euler_compact` | 65 | 1 / 12 | 1 / 14 | 4 / 27 |  |  |  |  |  |  | 4 / 27 |
| dominator outline `euler_r3` | 65 | 1 / 13 | 1 / 13 | 4 / 27 |  |  |  |  |  |  | 4 / 27 |
| largest proof beneath it (proof mass reachable through dependencies) | 16,302 | 2 / 4 | 2 / 4 | 4 / 11 | 6 / 14 | 8 / 17 | 9 / 19 | 10 / 20 | 14 / 24 | 25 / 29 | 31 / 31 |
| own proof size | 16,302 | 1 / 8 | 1 / 8 | 2 / 13 | 4 / 18 | 6 / 21 | 9 / 24 | 13 / 27 | 18 / 28 | 24 / 30 | 31 / 31 |
| has a docstring, ordered by proof mass beneath | 4,839 | 1 / 6 | 1 / 10 | 2 / 13 | 3 / 15 | 3 / 15 | 8 / 19 | 11 / 23 | 13 / 27 |  | 22 / 31 |
| has a docstring, random order (mean) | 4,839 | 0.05 / 2.23 | 0.14 / 4.14 | 0.35 / 8.05 | 0.75 / 11.96 | 1.53 / 16.96 | 3.6 / 23.66 | 6.72 / 27.67 | 11.92 / 30.0 | 22.0 / 31.0 | |
| any declaration, random order (mean) | 16,302 | 0.07 / 3.57 | 0.12 / 5.83 | 0.3 / 10.16 | 0.59 / 14.33 | 1.08 / 19.05 | 2.69 / 25.22 | 5.12 / 28.16 | 9.85 / 29.75 | 20.09 / 30.65 | |

Dominator outline by level (cumulative exact / near): `euler_compact`: root + spine (1) 1/3, level 1 (chapters) (22) 1/14, level 2 (34) 3/16, level 3 (41) 3/16, toolkit (65) 4/27; `euler_r3`: root + spine (1) 1/3, level 1 (chapters) (20) 1/13, level 2 (32) 3/15, level 3 (41) 3/15, toolkit (65) 4/27

### items mapped at probable or certain: 31 items

| list | size | k=10 | k=20 | k=50 | k=100 | k=200 | k=500 | k=1000 | k=2000 | k=5000 | all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dominator outline `euler_compact` | 65 | 1 / 12 | 1 / 14 | 4 / 27 |  |  |  |  |  |  | 4 / 27 |
| dominator outline `euler_r3` | 65 | 1 / 13 | 1 / 13 | 4 / 27 |  |  |  |  |  |  | 4 / 27 |
| largest proof beneath it (proof mass reachable through dependencies) | 16,302 | 2 / 4 | 2 / 4 | 4 / 10 | 6 / 14 | 8 / 17 | 9 / 19 | 10 / 20 | 14 / 24 | 24 / 29 | 31 / 31 |
| own proof size | 16,302 | 1 / 8 | 1 / 8 | 2 / 13 | 4 / 18 | 6 / 21 | 8 / 24 | 12 / 27 | 17 / 28 | 24 / 30 | 31 / 31 |
| has a docstring, ordered by proof mass beneath | 4,839 | 1 / 6 | 1 / 10 | 2 / 13 | 3 / 15 | 3 / 15 | 8 / 19 | 11 / 23 | 13 / 27 |  | 22 / 31 |
| has a docstring, random order (mean) | 4,839 | 0.05 / 2.17 | 0.12 / 4.05 | 0.34 / 7.85 | 0.72 / 11.67 | 1.46 / 16.58 | 3.48 / 23.11 | 6.53 / 27.23 | 11.65 / 29.8 | 22.0 / 31.0 | |
| any declaration, random order (mean) | 16,302 | 0.06 / 3.5 | 0.1 / 5.71 | 0.28 / 9.96 | 0.55 / 14.14 | 1.03 / 18.85 | 2.57 / 24.93 | 4.87 / 27.98 | 9.4 / 29.7 | 19.41 / 30.65 | |

Dominator outline by level (cumulative exact / near): `euler_compact`: root + spine (1) 1/3, level 1 (chapters) (22) 1/14, level 2 (34) 3/16, level 3 (41) 3/16, toolkit (65) 4/27; `euler_r3`: root + spine (1) 1/3, level 1 (chapters) (20) 1/13, level 2 (32) 3/15, level 3 (41) 3/15, toolkit (65) 4/27

### items mapped at certain: 4 items

| list | size | k=10 | k=20 | k=50 | k=100 | k=200 | k=500 | k=1000 | k=2000 | k=5000 | all |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dominator outline `euler_compact` | 65 | 1 / 1 | 1 / 2 | 1 / 3 |  |  |  |  |  |  | 1 / 3 |
| dominator outline `euler_r3` | 65 | 1 / 1 | 1 / 1 | 1 / 3 |  |  |  |  |  |  | 1 / 3 |
| largest proof beneath it (proof mass reachable through dependencies) | 16,302 | 1 / 2 | 1 / 2 | 1 / 2 | 1 / 2 | 1 / 2 | 1 / 2 | 1 / 2 | 2 / 2 | 3 / 3 | 4 / 4 |
| own proof size | 16,302 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 1 | 1 / 2 | 1 / 2 | 2 / 3 | 4 / 4 |
| has a docstring, ordered by proof mass beneath | 4,839 | 1 / 2 | 1 / 2 | 1 / 2 | 1 / 2 | 1 / 2 | 2 / 2 | 3 / 3 | 3 / 3 |  | 4 / 4 |
| has a docstring, random order (mean) | 4,839 | 0.0 / 0.09 | 0.01 / 0.15 | 0.03 / 0.34 | 0.06 / 0.63 | 0.14 / 1.23 | 0.39 / 2.4 | 0.81 / 3.42 | 1.66 / 3.87 | 4.0 / 4.0 | |
| any declaration, random order (mean) | 16,302 | 0.0 / 0.04 | 0.01 / 0.11 | 0.02 / 0.31 | 0.04 / 0.59 | 0.09 / 0.93 | 0.16 / 1.61 | 0.32 / 2.21 | 0.71 / 2.93 | 1.72 / 3.75 | |

Dominator outline by level (cumulative exact / near): `euler_compact`: root + spine (1) 1/1, level 1 (chapters) (22) 1/2, level 2 (34) 1/2, level 3 (41) 1/2, toolkit (65) 1/3; `euler_r3`: root + spine (1) 1/1, level 1 (chapters) (20) 1/1, level 2 (32) 1/1, level 3 (41) 1/1, toolkit (65) 1/3

