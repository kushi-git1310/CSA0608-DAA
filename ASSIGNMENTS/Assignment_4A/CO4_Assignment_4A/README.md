# CO4 Assignment 4A – Algorithmic Design through Pseudocode

**Student:** S KUSHA LAKSHMI | **Reg. No.:** 192571074 | **Course:** CSA06 Design and Analysis of Algorithms (CSA0608)
**Faculty:** Dr. F. Mary Harin Fernandez | **Due:** 19 Nov 2026

## Structure
```
CO4_Assignment_4A/
├── Source_Code/
│   ├── Task_1/  task1_fractional_knapsack.py   + output.txt
│   ├── Task_2/  task2_job_sequencing.py        + output.txt
│   ├── Task_3/  task3_knapsack_01.py           + output.txt
│   ├── Task_4/  task4_wordbreak.py             + output.txt
│   ├── Task_5/  task5_shortest_paths.py        + output.txt
│   └── Task_6/  task6_energy_scheduling.py     + output.txt
├── Report/CO4_Assignment_4A_Report.pdf
└── README.md
```

## Tasks
| Task | Topic | Strategy | Result |
|---|---|---|---|
| 1 | Repair of LoadVehicle (fractional knapsack) | Greedy – value/weight ratio | 240 for C=50 sample |
| 2 | Job sequencing with deadlines | Greedy – profit order, latest free slot | 180 (C, A, D); modified case 135 |
| 3 | 0/1 knapsack, capacity 7 | DP + reconstruction | 45 (Q, R) |
| 4 | WordBreak forensics | Add `DP[j] = TRUE` test | catdog/{dog}: faulty TRUE, fixed FALSE |
| 5 | Dijkstra / Bellman-Ford / Floyd | Greedy, relaxation, DP | dist from A = 0,4,6,7,10 |
| 6 | Energy-aware job scheduling (Design Challenge) | DP – weighted interval scheduling | 200 (J2, J5, J7, J8) |

## Run
Python 3.8+, standard library only:
```
cd Source_Code/Task_1 && python3 task1_fractional_knapsack.py
```
(repeat for Task_2 … Task_6).

## Note
The assignment requires designs as pseudocode with manual traces (in the report). The programs only verify those traces and provide execution output.
