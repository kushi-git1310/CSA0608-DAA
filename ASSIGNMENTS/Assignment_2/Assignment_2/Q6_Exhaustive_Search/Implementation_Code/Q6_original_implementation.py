from time import perf_counter


def exhaustive_packages(weights, values, capacity):
    n = len(weights)
    best_value = 0
    best_subset = []
    candidates = 0
    for mask in range(1 << n):
        candidates += 1
        total_weight = total_value = 0
        subset = []
        for i in range(n):
            if mask & (1 << i):
                total_weight += weights[i]
                total_value += values[i]
                subset.append(i)
        if total_weight <= capacity and total_value > best_value:
            best_value = total_value
            best_subset = subset
    return best_subset, best_value, candidates


if __name__ == "__main__":
    weights = [2, 3, 4, 5, 9, 7, 6, 3, 8, 1, 4, 2]
    values  = [3, 4, 5, 8, 10, 7, 6, 4, 9, 2, 5, 3]
    capacity = 15
    for n in (8, 10, 12):
        start = perf_counter()
        subset, value, candidates = exhaustive_packages(weights[:n], values[:n], capacity)
        elapsed = perf_counter() - start
        total_weight = sum(weights[i] for i in subset)
        print(f"n={n}: subsets={candidates} (expected {2**n}), "
              f"best package indices={subset}, weight={total_weight}, value={value}, "
              f"time={elapsed:.6f}s")
