# Task 11 – Final Design Recommendation

## Candidate recommendation
For repeated exact-match lookup by a unique registration number, a hash-based index is a strong candidate because lookup is expected Θ(1) after expected Θ(n) construction. A database's persistent unique index is generally more suitable for a real university service than rebuilding an in-memory Python dictionary for every application start.

## Alternatives and trade-offs
- Linear search: minimal setup, but Θ(n) per lookup; appropriate mainly for tiny collections or rare queries.
- Binary search: Θ(log n) lookup after sorting; good when sorted order and range queries matter, but sorting is O(n log n) if needed.
- Hash table: expected Θ(1) exact lookup and expected Θ(n) construction, but requires memory and has Θ(n) pathological worst-case lookup.

## Measured evidence (Python 3.12.3, Linux, 1 vCPU Intel Xeon 2.1 GHz)

| n | Linear (absent) | Binary (absent) | Hash (absent) | Sort time | Dict build time |
|---:|---:|---:|---:|---:|---:|
| 1,000 | 27.5 µs | 1.34 µs | 0.094 µs | 8.8 µs | 40.7 µs |
| 10,000 | 325 µs | 1.87 µs | 0.114 µs | 126 µs | 392 µs |
| 100,000 | 3.50 ms | 2.00 µs | 0.108 µs | 1.46 ms | 6.79 ms |
| 1,000,000 | 41.2 ms | 3.20 µs | 0.139 µs | 22.5 ms | 73.2 ms |

At n = 1,000,000 the dictionary build (73 ms) is repaid after only 2 linear searches (2 × 41 ms), so preprocessing is cheap relative to repeated use.

##  Recommended Algorithm

The recommended approach for repeated student-record retrieval is Hash Table Search.

### Reasons for Selection

1. Hash Table Search provides expected constant-time lookup.
2. It does not require sorting student records.
3. It supports frequent registration-number searches.
4. The hash table can be constructed once and reused.
5. It is suitable for large student databases.

###  Theoretical Efficiency

| Operation | Complexity |
|---|---|
| Hash table construction | Θ(n) expected |
| Successful lookup | Θ(1) expected |
| Unsuccessful lookup | Θ(1) expected |
| Worst-case lookup | Θ(n) |

### Trade-offs

- Hash tables require additional memory.
- Hash table construction takes time.
- Collisions may reduce lookup efficiency.
- Updates must be reflected in the hash table.

###  Final Recommendation
Hash Table Search is recommended because the university requires efficient retrieval of student information using unique registration numbers. Its expected constant-time lookup provides an advantage for repeated searches on large datasets. Although the hash table requires additional memory and preprocessing, these costs can be justified when the index is reused for many search operations.
