# Task 12 – Day-4 Design Challenge

**Student:** S KUSHA LAKSHMI | **Reg. No.:** 192571074 | **Course:** CSA0608 DAA

## Changed requirement
The university now processes **50,000 search requests per hour** on a database of **1,000,000 student records**. New records are added **only once per day**.

## Task 12A – Impact Analysis

| Original requirement | Changed requirement |
|---|---|
| Dataset size varies | Fixed database of 1,000,000 records |
| Search frequency unspecified | 50,000 searches per hour (≈14 per second) |
| Update frequency unspecified | New records added once daily |
| General searching efficiency | High repeated-search performance |

**Impact.** Search efficiency now matters much more because of the volume of requests. Since updates happen once a day, the index does not need to be maintained continuously, so preprocessing cost can be spread across a very large number of searches.

**Conclusion:** prioritise fast repeated lookups and a reusable index.

## Task 12B – Evaluation of the Original Design

| Algorithm | Complexity | Suitability |
|---|---|---|
| Linear search | Θ(n) | Not suitable as primary strategy |
| Recursive binary search | Θ(log n) | Suitable |
| Hash table search | Expected Θ(1) | Most suitable for frequent lookups |

**Linear search.** Worst case 1,000,000 comparisons per search, so 50,000 × 1,000,000 = 50,000,000,000 (50 billion) comparisons per hour. Measured: 41.2 ms per absent-key search × 50,000 = about 2,060 s (≈34 minutes) of CPU time every hour – too much of the hour spent on searching alone.

**Binary search.** About 20 midpoint levels for 10⁶ records: 50,000 × 20 = 1,000,000 levels per hour. Measured 3.2 µs per search × 50,000 ≈ 0.16 s per hour. Needs sorted data (sorted once per day).

**Hash table.** Expected constant time. Measured 0.139 µs per search × 50,000 ≈ 0.007 s per hour. Built once (73 ms measured), then reused.

## Task 12C – Adaptation or Redesign

**Decision: MODIFY.** Keep hash-table search but turn it into a persistent, reusable index that is loaded once and refreshed when the daily batch of records arrives. A full redesign is unnecessary because the core algorithm already fits the new workload.

### Revised algorithm
1. Load student records from the database.
2. Create a hash table with registration numbers as keys and student records as values.
3. Keep the table in memory for repeated searches.
4. For each request, look up the registration number and return the record or "Student Not Found".
5. After the daily update, insert the new records (or rebuild the table, ≈73 ms for 10⁶ records).
6. Optionally keep a sorted copy for binary-search fallback / range queries.

### Revised pseudocode
```text
ALGORITHM OPTIMIZED_STUDENT_SEARCH
1.  LOAD student records
2.  CREATE HASH_TABLE
3.  FOR each student record
4.      HASH_TABLE[registration_number] = student_record
5.  END FOR
6.  WHILE system is running
7.      READ target_registration_number
8.      IF target_registration_number EXISTS IN HASH_TABLE THEN
9.          DISPLAY student record
10.     ELSE
11.         DISPLAY "Student Not Found"
12.     END IF
13.     IF daily update available THEN
14.         INSERT new records into HASH_TABLE
15.     END IF
16. END WHILE
17. STOP
```

### Trade-offs
- Extra memory (Θ(n)) for the table; acceptable for 10⁶ records.
- The in-memory table is lost on restart, so it must be rebuilt from the database (≈73 ms) or backed by a persistent database index.
