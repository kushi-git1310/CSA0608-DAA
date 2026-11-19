"""Task 1 - Repaired LoadVehicle (Fractional Knapsack, greedy by value/weight ratio).
Author: S KUSHA LAKSHMI | Reg No: 192571074 | Course: CSA0608
This program is a VERIFICATION of the pseudocode in the report."""

def load_vehicle(packages, capacity, verbose=True):
    # packages: list of (id, weight, value)
    ratio = [(pid, w, v, v / w) for pid, w, v in packages]
    ratio.sort(key=lambda t: (-t[3], t[1]))          # descending value/weight, tie -> lighter first
    remaining = capacity
    total = 0.0
    loaded = []
    if verbose:
        print("Sorted by ratio:", [(p, round(r, 2)) for p, _, _, r in ratio])
    for pid, w, v, r in ratio:
        if remaining <= 0:
            break
        if w <= remaining:                           # whole package fits
            fraction = 1.0
        else:                                        # partial package
            fraction = remaining / w
        gained = fraction * v
        loaded.append((pid, fraction, fraction * w, gained))
        remaining -= fraction * w
        total += gained
        if verbose:
            print(f"  take {pid}: fraction={fraction:.2f} weight={fraction*w:.1f} "
                  f"value={gained:.1f} remaining={remaining:.1f} total={total:.1f}")
    return total, loaded, remaining


if __name__ == "__main__":
    print("=== TEST 1: capacity 50 ===")
    data = [("P1", 10, 60), ("P2", 20, 100), ("P3", 30, 120)]
    t, l, r = load_vehicle(data, 50)
    print("TOTAL VALUE =", t, "| UNUSED CAPACITY =", r)

    print("\n=== TEST 2: capacity 0 (boundary) ===")
    t, l, r = load_vehicle(data, 0)
    print("TOTAL VALUE =", t)

    print("\n=== TEST 3: capacity larger than all packages ===")
    t, l, r = load_vehicle(data, 100)
    print("TOTAL VALUE =", t, "| UNUSED CAPACITY =", r)

    print("\n=== TEST 4: all same ratio ===")
    t, l, r = load_vehicle([("A", 4, 8), ("B", 2, 4), ("C", 6, 12)], 7)
    print("TOTAL VALUE =", t)
