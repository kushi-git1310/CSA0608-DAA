def sequential_search(records, target):
    comparisons = 0
    for index, record in enumerate(records):
        comparisons += 1
        if record["tool_id"] == target:
            return index, comparisons
    return -1, comparisons


if __name__ == "__main__":
    for n in (10, 100, 1000):
        records = [{"tool_id": f"T-{i:04d}", "technician": f"TECH-{i%20:02d}"} for i in range(n)]
        cases = {
            "first item": "T-0000",
            "middle item": f"T-{n//2:04d}",
            "last item": f"T-{n-1:04d}",
            "missing item": "T-MISSING",
        }
        print(f"\nList size n={n}")
        for label, target in cases.items():
            index, comparisons = sequential_search(records, target)
            print(f"{label}: index={index}, comparisons={comparisons}")
