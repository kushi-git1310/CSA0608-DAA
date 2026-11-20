# CSA0608 – Design and Analysis of Algorithms | CO4 Assignment 4B

**Student:** S KUSHA LAKSHMI  **Reg. No:** 192571074  **Course:** CSA0608
**Topic:** Algorithm Engineering – Implement, Test, Debug & Optimise (Dynamic Programming and Greedy strategies)

## Files
| File | Task | Algorithms |
|---|---|---|
| `task1_word_wrap.py` | 1 – Word wrap | suffix DP, brute-force oracle, greedy baseline, fault injection |
| `task2_greedy_vs_dp.py` | 2 – Greedy vs DP | fractional greedy, 0/1 greedy, 0/1 DP, statistics |
| `task3_routing.py` | 3 – Routing | Dijkstra, Bellman-Ford (+ negative-cycle extraction), Floyd, Warshall |
| `task4_assembly_line.py` | 4 – Assembly line | two-line DP, brute-force oracle, experiments |
| `task5_mst.py` | 5 – MST | Kruskal, Prim (heap + array), Borůvka, multiple-MST enumeration |
| `task6_tsp.py` | 6 – TSP | Held-Karp bit-mask DP, brute force, growth study, heuristic trial |
| `make_screenshots.py` | – | renders `outputs/*.txt` as terminal screenshots |
| `run_all.sh` | – | runs everything |
| `outputs/` | – | captured console output of each task |
| `screenshots/` | – | terminal screenshots used in the report |
| `CSA0608_Assignment4B_Report.docx / .pdf` | – | full report |

## How to run
```
python task1_word_wrap.py
python task2_greedy_vs_dp.py
python task3_routing.py
python task4_assembly_line.py
python task5_mst.py
python task6_tsp.py
```
No packages are required for the tasks (standard library only). All random experiments use fixed seeds, so the numbers are reproducible.

## Key results
* **Task 1** – W=40: minimum penalty 52 (greedy 76). W=30 → 54, W=50 → 49, W=60 → 69 (prediction of a decrease at W=60 was wrong – penalty is not monotonic in W).
* **Task 2** – counter-example: greedy 62 ≠ DP optimum 85 (first fatal commitment: item L1). Greedy optimal on 517/1000 random instances, 99.997 % of optimum at n=2000.
* **Task 3** – Dijkstra wrong on E, G, H, I after adding F→E (−5); Bellman-Ford correct; negative cycle E→D→F→E detected; Floyd and Warshall matrices printed.
* **Task 4** – minimum production time 38, route L1,L2,L1,L2,L2,L1; transfer 20 → 39; slow machine at station 3 → route moves to Line 2, time 39.
* **Task 5** – Kruskal = Prim = Borůvka = 38; with ties there are 4 MSTs, different tie rules return different (equally correct) edge sets.
* **Task 6** – Hub → F → B → E → A → C → D → Hub, cost 80; validated against exhaustive search; states = n·2^(n-1) (245,760 at n=15).
