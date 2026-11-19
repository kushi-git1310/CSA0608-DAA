from time import perf_counter


def sequential_search(records, target):
    comparisons = 0
    for record in records:
        comparisons += 1
        if record["tool_id"] == target:
            return record, comparisons
    return None, comparisons


def build_index(records):
    # Preprocessing: O(n) time and O(n) extra memory.
    return {record["tool_id"]: record for record in records}


if __name__ == "__main__":
    n = 5000
    records = [{"tool_id": f"T-{i:05d}", "work_bay": f"BAY-{i%30:02d}"} for i in range(n)]
    targets = [f"T-{i:05d}" for i in (4999, 2500, 100, 4500, 42, 3000, 4998, 17, 4200, 800)]

    start = perf_counter()
    sequential_total = 0
    for target in targets:
        _, comparisons = sequential_search(records, target)
        sequential_total += comparisons
    sequential_time = perf_counter() - start

    start = perf_counter()
    index = build_index(records)
    build_time = perf_counter() - start
    start = perf_counter()
    indexed_results = [index.get(target) for target in targets]
    indexed_time = perf_counter() - start

    print(f"records={n}, queries={len(targets)}")
    print(f"Sequential search: comparisons={sequential_total}, time={sequential_time:.6f}s")
    print(f"Dictionary redesign: build entries={len(index)}, successful results="
          f"{sum(item is not None for item in indexed_results)}, "
          f"build time={build_time:.6f}s, lookup time={indexed_time:.6f}s")
    print("Trade-off: indexing uses extra memory and preprocessing, but supports many repeated lookups.")
