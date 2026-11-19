# CSA0608 – Design and Analysis of Algorithms (Assignment 2)

**Student Name:** S KUSHA LAKSHMI  
**Register Number:** 192571074  
**Course:** CSA0608 – Design and Analysis of Algorithms (DAA)  
**Assignment:** Assignment 2 (Questions 1 to 7)  
**Language:** Python 3  

---

## Repository Structure

```text
Assignment_2/
├── Q1_Sorting_Algorithms/
│   ├── Pseudocode/
│   │   └── Q1_pseudocode.txt
│   ├── Implementation_Code/
│   │   └── Q1_original_implementation.py
│   └── Output_Screenshots/
│       └── que 1.png
├── Q2_Sequential_Search/
│   ├── Pseudocode/
│   │   └── Q2_pseudocode.txt
│   ├── Implementation_Code/
│   │   └── Q2_original_implementation.py
│   └── Output_Screenshots/
│       └── que 2.png
├── Q3_Brute_Force_String_Matching/
│   ├── Pseudocode/
│   │   └── Q3_pseudocode.txt
│   ├── Implementation_Code/
│   │   └── Q3_original_implementation.py
│   └── Output_Screenshots/
│       └── que 3.png
├── Q4_Brute_Force_Closest_Pair/
│   ├── Pseudocode/
│   │   └── Q4_pseudocode.txt
│   ├── Implementation_Code/
│   │   └── Q4_original_implementation.py
│   └── Output_Screenshots/
│       └── que 4.png
├── Q5_Brute_Force_Convex_Hull/
│   ├── Pseudocode/
│   │   └── Q5_pseudocode.txt
│   ├── Implementation_Code/
│   │   └── Q5_original_implementation.py
│   └── Output_Screenshots/
│       └── que 5.png
├── Q6_Exhaustive_Search/
│   ├── Pseudocode/
│   │   └── Q6_pseudocode.txt
│   ├── Implementation_Code/
│   │   └── Q6_original_implementation.py
│   └── Output_Screenshots/
│       └── que 6.png
├── Q7_Day4_Design_Challenge/
│   ├── Pseudocode/
│   │   └── Q7_pseudocode.txt
│   ├── Implementation_Code/
│   │   └── Q7_original_implementation.py
│   └── Output_Screenshots/
│       └── que 7.png
├── Final_Report/
│   └── Assignment_2_Report.docx
└── README.md
```

## Overview of Questions
1. **Q1 – Sorting Algorithms:** Empirical comparison of Selection Sort, Bubble Sort, and Insertion Sort counting key comparisons and swaps/shifts across nearly sorted, reverse-ordered, empty, and duplicate datasets.
2. **Q2 – Sequential Search:** Linear search over tool records analyzing comparison counts across best, average, worst, and unsuccessful cases for $n = 10, 100, 1000$.
3. **Q3 – Brute-Force String Matching:** Naive sliding-window pattern search measuring exact character comparisons across early mismatch, repeated prefix, and end-match test cases.
4. **Q4 – Brute-Force Closest Pair:** Exhaustive 2D Euclidean distance comparison verifying the $\frac{n(n-1)}{2}$ pair-evaluation bound.
5. **Q5 – Brute-Force Convex Hull:** Cross-product orientation check identifying extreme boundary edges and ordering convex hull vertices.
6. **Q6 – Exhaustive Search (0/1 Knapsack):** Bitmask enumeration over all $2^n$ package subsets within weight capacity $15$.
7. **Q7 – Day 4 Design Challenge:** Redesigning repeated sequential tool lookups using an $O(n)$-preprocessed hash table (Python `dict`) for average $O(1)$ query time.

## How to Run
Execute any Python implementation from its directory using Python 3:
```bash
python Q1_original_implementation.py
```
