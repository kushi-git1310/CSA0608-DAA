# Task 9 – Experimental Performance

**Student:** S KUSHA LAKSHMI | **Reg. No.:** 192571074 | **Course:** CSA0608 DAA

## Environment
Python 3.12.3 · Linux 6.x · Intel Xeon 2.1 GHz (1 vCPU) · 3.9 GB RAM

## How to run
```bash
python Task_8_Implementation_Testing/Source_Code/search_experiments.py
```
Output: `Report/Tables_and_Graphs/performance_results.csv`, `execution_time.png`, `comparison_count.png`, `preprocessing_time.png`.

## Method
- Dataset sizes 1,000 / 10,000 / 100,000 / 1,000,000 unique integer registration numbers.
- Test cases: first, middle, last and absent target.
- `time.perf_counter()`, median of 5 repetitions per case.
- Preprocessing (sort / dictionary build) measured separately from search.
- Correctness verified for every case (48/48 rows correct).
- Python `dict` internal probes are not exposed, so no comparison count is reported for hashing (one lookup operation is recorded instead).

## Results – worst case (absent target)

| n | Linear time | Linear comparisons | Binary time | Binary comparisons | Hash time |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 27.5 µs | 1,000 | 1.34 µs | 20 | 0.094 µs |
| 10,000 | 325 µs | 10,000 | 1.87 µs | 28 | 0.114 µs |
| 100,000 | 3.50 ms | 100,000 | 2.00 µs | 34 | 0.108 µs |
| 1,000,000 | 41.2 ms | 1,000,000 | 3.20 µs | 40 | 0.139 µs |

## Preprocessing

| n | Linear | Sorting (binary) | Dictionary build (hash) |
|---:|---:|---:|---:|
| 1,000 | 0 | 8.8 µs | 40.7 µs |
| 10,000 | 0 | 126 µs | 392 µs |
| 100,000 | 0 | 1.46 ms | 6.79 ms |
| 1,000,000 | 0 | 22.5 ms | 73.2 ms |

## Mean search time over the four test cases

| n | Linear | Binary | Hash |
|---:|---:|---:|---:|
| 1,000 | 16.5 µs | 1.13 µs | 0.096 µs |
| 10,000 | 207 µs | 1.60 µs | 0.099 µs |
| 100,000 | 2.08 ms | 1.83 µs | 0.117 µs |
| 1,000,000 | 24.4 ms | 3.20 µs | 0.140 µs |

## Interpretation
1. **Linear search** grew almost exactly 10× for each 10× increase in n (27 µs → 325 µs → 3.5 ms → 41 ms) – linear growth.
2. **Binary search** grew very slowly: 1,000× more records increased the time only about 2.4× (1.34 µs → 3.20 µs). Comparisons rose by about 6 per 10× growth (2 per level × ~3.3 levels), i.e. logarithmic.
3. **Hash lookup** stayed essentially flat (≈0.1 µs) at every size.
4. **Preprocessing:** sorting and dictionary construction both grew roughly linearly with n (the sort was fast because the input was already ordered); the dictionary build cost more than the sort at every size.
5. **Noise:** timings below ~1 µs are near the resolution of the timer and vary between runs, so small differences (e.g. 0.094 vs 0.114 µs) are not meaningful.

Graphs: `Report/Tables_and_Graphs/execution_time.png`, `comparison_count.png`, `preprocessing_time.png`.
