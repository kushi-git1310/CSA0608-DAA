# CO1 Assignment – Student Registration Number Search

| | |
|---|---|
| **Name** | S KUSHA LAKSHMI |
| **Registration Number** | 192571074 |
| **Course** | CSA0608 – Design and Analysis of Algorithms (DAA) |

## Objective
Design, implement, test and compare three algorithms for locating a student registration number:
1. Iterative Linear Search
2. Recursive Binary Search
3. Hash Table Search (Python `dict`)

Dataset sizes: 1,000; 10,000; 100,000; 1,000,000 records.

## Folder structure
```
CO1_Assignment
├── Task_1_Algorithm_Design/
├── Task_2_Basic_Operation/
├── Task_3_Mathematical_Complexity/
├── Task_4_Case_Analysis/
├── Task_5_Asymptotic_Analysis/
├── Task_6_Recurrence_Formulation/
├── Task_7_Recurrence_Solution/
├── Task_8_Implementation_Testing/
│   └── Source_Code/          (search_experiments.py, test_cases.py)
├── Task_9_Experimental_Performance/
├── Task_10_Theory_vs_Experiment/
├── Task_11_Final_Recommendation/
├── Task_12_Design_Challenge/
├── Report/
│   ├── Source_Code_Screenshots/
│   ├── Output_Screenshots/
│   ├── Analysis/
│   ├── Tables_and_Graphs/
│   └── Documentation/        (final report: DOCX + PDF)
└── README.md
```

## Requirements
Python 3.10+ and matplotlib:
```bash
python -m pip install -r requirements.txt
```

## How to run (from the CO1_Assignment folder)
```bash
python Task_8_Implementation_Testing/Source_Code/test_cases.py          # 10 unit tests
python Task_8_Implementation_Testing/Source_Code/search_experiments.py  # benchmark + graphs
```
The benchmark writes `performance_results.csv` and three PNG graphs to `Report/Tables_and_Graphs/`.

## Note on results
Timings are machine-dependent. The results in this submission were produced by the included program (Python 3.12.3, Linux, 1 vCPU Intel Xeon 2.1 GHz). Re-running on another computer will give different absolute times but the same growth trends.
