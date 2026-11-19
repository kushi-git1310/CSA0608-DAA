# Task 10 – Theory vs Experiment

**Student:** S KUSHA LAKSHMI | **Reg. No.:** 192571074 | **Course:** CSA0608 DAA

## Comparison

| Algorithm | Theoretical (worst case) | Observed (n: 1,000 → 1,000,000) | Match? |
|---|---|---|---|
| Linear search | Θ(n); n comparisons | Comparisons exactly n (1,000 → 1,000,000); time 27.5 µs → 41.2 ms (≈1,500×) | Yes |
| Recursive binary search | Θ(log n) | Time 1.34 µs → 3.20 µs (≈2.4×); comparisons 20 → 40 | Yes |
| Hash table search | Expected Θ(1) | ≈0.1 µs at all sizes | Yes |
| Sorting (binary preprocessing) | O(n log n) | 8.8 µs → 22.5 ms | Roughly (input already sorted, so Timsort ≈ linear) |
| Dictionary build | Expected Θ(n) | 40.7 µs → 73.2 ms (≈1,800×) | Yes (slightly super-linear due to memory/cache effects) |

## Operation counts vs theory
- Linear: measured comparisons = n for an absent key – identical to the derivation.
- Binary: each level performs 2 explicit comparisons (equality, then less-than), so 40 comparisons for n = 10⁶ equals about 20 levels = ⌊log₂ 10⁶⌋+1, matching theory.

## Why measurements differ from theory
- Big-O ignores constants and hardware: interpreter overhead, cache effects, memory allocation, garbage collection and system load all affect timing.
- Linear time grew ~1,500× for a 1,000× larger n (slightly more than 1,000×), plausibly because a 1,000,000-element list no longer fits in CPU cache (not separately verified).
- Hash lookup times below ~1 µs are near timer resolution, so tiny differences are noise.
- Four input sizes support a trend discussion but do not prove an asymptotic bound.
- The hash worst case Θ(n) cannot appear with unique integers in Python's `dict`, so it was not observed.

## Conclusion
The experiments agree with the theory: linear search scales linearly, recursive binary search logarithmically and hash lookup in near-constant time. Hash search is fastest per lookup, binary search is a close second with lower memory use, and linear search becomes impractical at large n.
