"""
CSA0608 - Design and Analysis of Algorithms | Assignment 4B
Student : S KUSHA LAKSHMI   Reg.No : 192571074

TASK 6 - LAST-MILE DELIVERY ROUTE OPTIMISATION (TSP with Dynamic Programming, Held-Karp)

Model
  Input   : cost matrix c[i][j] for hub (index 0) and n delivery locations (indices 1..n)
  Output  : a closed tour hub -> every location exactly once -> hub, and its cost
  Objective: minimise the sum of the n+1 legs
  State   : DP[S][j]  S = SET of locations already visited (bitmask over 1..n), j = current location (j in S)
            DP[S][j] = cheapest cost of starting at the hub, visiting exactly the locations in S, ending at j
  Base    : DP[{j}][j] = c[hub][j]
  Recurrence : DP[S][j] = min over k in S\\{j} of  DP[S\\{j}][k] + c[k][j]
  Answer  : min over j of  DP[ALL][j] + c[j][hub]
"""
import math
import random
import time
import tracemalloc
from itertools import permutations

INF = float("inf")
LABELS = ["Hub", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]


def validate_matrix(cost):
    n1 = len(cost)
    if n1 == 0 or any(len(r) != n1 for r in cost):
        raise ValueError("cost matrix must be square and non-empty")
    for i in range(n1):
        for j in range(n1):
            if cost[i][j] < 0:
                raise ValueError("travel costs must be non-negative")


def held_karp(cost, stats=None):
    """Returns (best_cost, tour_as_index_list). tour starts and ends at 0. (INF, None) if no tour exists."""
    validate_matrix(cost)
    n = len(cost) - 1                                   # number of delivery locations
    stats = stats if stats is not None else {}
    stats.update(states=0, transitions=0, table_entries=0)
    if n == 0:
        return 0, [0, 0]
    full = (1 << n) - 1
    size = 1 << n
    dp = [[INF] * n for _ in range(size)]               # dp[mask][j-1]
    parent = [[-1] * n for _ in range(size)]
    stats["table_entries"] = size * n
    for j in range(n):                                  # base states
        dp[1 << j][j] = cost[0][j + 1]
        stats["states"] += 1
    for mask in range(1, size):
        for j in range(n):
            if not (mask >> j) & 1 or mask == (1 << j):
                continue
            stats["states"] += 1
            prev = mask ^ (1 << j)
            best, arg = INF, -1
            for k in range(n):
                if (prev >> k) & 1:
                    stats["transitions"] += 1
                    cand = dp[prev][k] + cost[k + 1][j + 1]
                    if cand < best:
                        best, arg = cand, k
            dp[mask][j], parent[mask][j] = best, arg
    best, last = INF, -1
    for j in range(n):                                  # close the tour
        total = dp[full][j] + cost[j + 1][0]
        if total < best:
            best, last = total, j
    if best == INF:
        return INF, None
    tour, mask, j = [0], full, last
    while j != -1:                                      # rebuild backwards
        tour.append(j + 1)
        pj = parent[mask][j]
        mask ^= (1 << j)
        j = pj
    tour.append(0)
    tour = [0] + tour[1:-1][::-1] + [0]
    return best, tour


def tour_cost(cost, tour):
    return sum(cost[a][b] for a, b in zip(tour, tour[1:]))


def brute_force(cost):
    """Independent oracle: evaluate every permutation of the locations. Returns (best, best_tour, all_results)."""
    n = len(cost) - 1
    results = []
    for perm in permutations(range(1, n + 1)):
        tour = [0] + list(perm) + [0]
        results.append((tour_cost(cost, tour), tour))
    best = min(results, key=lambda r: r[0])
    return best[0], best[1], results


def fmt_tour(tour):
    return " -> ".join(LABELS[i] for i in tour)


# ---------------- supporting heuristics for Task 6.6 (NOT the required deliverable) --------------- #
def nearest_neighbour(cost):
    n1 = len(cost)
    tour, seen = [0], {0}
    while len(tour) < n1:
        cur = tour[-1]
        nxt = min((j for j in range(n1) if j not in seen), key=lambda j: cost[cur][j])
        tour.append(nxt)
        seen.add(nxt)
    return tour + [0]


def two_opt(cost, tour):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):
                delta = (cost[tour[i - 1]][tour[j]] + cost[tour[i]][tour[j + 1]]
                         - cost[tour[i - 1]][tour[i]] - cost[tour[j]][tour[j + 1]])
                if delta < -1e-9:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
    return tour


def euclid_matrix(points):
    return [[math.dist(p, q) for q in points] for p in points]


def random_matrix(rng, n, lo=5, hi=60):
    m = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(n + 1):
            if i != j:
                m[i][j] = rng.randint(lo, hi)
    return m


def print_matrix(cost, names):
    print("      " + "".join(f"{nm:>5}" for nm in names))
    for i, row in enumerate(cost):
        print(f"{names[i]:>5} " + "".join(f"{'INF' if v == INF else v:>5}" for v in row))


def main():
    # ----- 6.1 / 6.2 are explained in the report; the program prints the model for the record -----
    print("#" * 78)
    print("TASK 6.1 / 6.2  MODEL AND DP STATE")
    print("#" * 78)
    print("Input     : (n+1)x(n+1) cost matrix, hub = index 0")
    print("Output    : closed tour Hub -> all n locations once -> Hub, and its total cost")
    print("Objective : minimise total travel cost")
    print("Constraints: each location exactly once; start and end at the hub; costs non-negative")
    print("State     : DP[S][j] = cheapest way to leave the hub, visit exactly the set S, finish at j (j in S)")
    print("Base      : DP[{j}][j] = cost[Hub][j]")
    print("Recurrence: DP[S][j] = min_{k in S-{j}} ( DP[S-{j}][k] + cost[k][j] )")
    print("Final     : OPT = min_j ( DP[ALL][j] + cost[j][Hub] )")
    print("Why 'current location' alone is not enough: Hub->A->B->C and Hub->B->A->C both end at C but")
    print("have visited the same SET in different orders with different costs; two partial routes are")
    print("comparable only if they have the same visited set AND the same current location.")

    # ----- 6.3 -----
    names = LABELS[:7]
    cost = [
        [0, 12, 29, 22, 13, 24, 19],
        [12, 0, 19, 3, 25, 6, 33],
        [29, 19, 0, 21, 23, 20, 15],
        [22, 3, 21, 0, 4, 12, 17],
        [13, 25, 23, 4, 0, 9, 14],
        [24, 6, 20, 12, 9, 0, 11],
        [19, 33, 15, 17, 14, 11, 0],
    ]
    print("\n" + "#" * 78)
    print("TASK 6.3  ROUTE OPTIMISATION ENGINE  (hub + 6 locations)")
    print("#" * 78)
    print("Cost matrix:")
    print_matrix(cost, names)
    stats = {}
    best, tour = held_karp(cost, stats)
    print("\nOptimal route (order of visits):")
    for step, idx in enumerate(tour[1:-1], 1):
        print(f"   stop {step}: {LABELS[idx]}   (leg cost {cost[tour[step - 1]][idx]})")
    print(f"   return : {LABELS[tour[-1]]}   (leg cost {cost[tour[-2]][tour[-1]]})")
    print("\nRoute :", fmt_tour(tour))
    print(f"Minimum Travel Cost = {best}")
    print(f"Independent re-addition of legs = {tour_cost(cost, tour)}")
    print("DP statistics:", stats)

    # ----- 6.4 -----
    print("\n" + "#" * 78)
    print("TASK 6.4  VALIDATION (hub + 4 locations, exhaustive enumeration of 4! = 24 routes)")
    print("#" * 78)
    small = [[row[j] for j in (0, 1, 2, 3, 4)] for row in cost[:5]]
    print("Cost matrix (Hub, A, B, C, D):")
    print_matrix(small, LABELS[:5])
    bf_best, bf_tour, allr = brute_force(small)
    print(f"\n{'#':>3}  {'Route':<32}{'Cost':>5}")
    for k, (c, t) in enumerate(sorted(allr, key=lambda r: r[0]), 1):
        flag = "  <-- minimum" if c == bf_best else ""
        print(f"{k:>3}  {fmt_tour(t):<32}{c:>5}{flag}")
    d_best, d_tour = held_karp(small)
    print(f"\nExhaustive optimum = {bf_best}   DP optimum = {d_best}   -> {'MATCH' if bf_best == d_best else 'MISMATCH'}")
    print(f"Exhaustive tour(s) with that cost: {[fmt_tour(t) for c, t in allr if c == bf_best]}")
    print(f"DP tour: {fmt_tour(d_tour)}  (a reversed tour has the same cost for a symmetric matrix)")
    rng = random.Random(11)
    bad = 0
    for _ in range(300):
        n = rng.randint(1, 7)
        m = random_matrix(rng, n)                       # ASYMMETRIC random costs
        if held_karp(m)[0] != brute_force(m)[0]:
            bad += 1
    print(f"Randomised validation: 300 asymmetric instances (n=1..7), DP vs exhaustive, mismatches = {bad}")
    print("Boundary / failure tests:")
    print("   hub only (n=0)            ->", held_karp([[0]]))
    print("   one location (n=1)        ->", held_karp([[0, 7], [9, 0]]), "(7 + 9)")
    blocked = [[0, INF, 5], [3, 0, INF], [4, INF, 0]]
    print("   no road into B (INF)      ->", held_karp(blocked), "(no feasible tour reported, not a wrong number)")
    try:
        held_karp([[0, 1], [1]])
    except ValueError as e:
        print("   ragged matrix             -> rejected:", e)
    try:
        held_karp([[0, -1], [1, 0]])
    except ValueError as e:
        print("   negative cost             -> rejected:", e)

    # ----- 6.5 -----
    print("\n" + "#" * 78)
    print("TASK 6.5  STATE-SPACE GROWTH (random asymmetric instances, seed 2026)")
    print("#" * 78)
    rng = random.Random(2026)
    print(f"{'n':>3} {'DP states':>10} {'transitions':>12} {'table entries':>14} {'time (s)':>9} {'time ratio':>11} "
          f"{'tracemalloc peak (MB)':>22} {'theory n*2^(n-1)':>17}")
    prev_t = None
    for n in range(4, 16):
        m = random_matrix(rng, n)
        st = {}
        t0 = time.perf_counter()
        held_karp(m, st)
        el = time.perf_counter() - t0
        tracemalloc.start()
        held_karp(m)
        peak = tracemalloc.get_traced_memory()[1] / 1e6
        tracemalloc.stop()
        ratio = f"{el / prev_t:.2f}x" if prev_t else "-"
        prev_t = el
        print(f"{n:>3} {st['states']:>10} {st['transitions']:>12} {st['table_entries']:>14} {el:>9.4f} {ratio:>11} "
              f"{peak:>22.2f} {n * 2 ** (n - 1):>17}")
    print("\nProjection from the formulas (states = n*2^(n-1), table = n*2^n entries x 8 bytes):")
    print(f"{'n':>4} {'states':>22} {'table memory':>22}")
    for n in (20, 25, 30, 40):
        print(f"{n:>4} {n * 2 ** (n - 1):>22,} {n * 2 ** n * 8 / 2 ** 30:>19,.1f} GiB")
    print(f"{200:>4} {'about 10^' + str(round(math.log10(200) + 199 * math.log10(2), 1)):>22} {'impossible':>22}")
    print("(number of subsets of 200 locations = 2^200 ~ 1.6e60; the Earth contains only about 1e50 atoms)")
    print("Plain enumeration needs n! routes: n=10 -> %s,  n=15 -> %s,  n=20 -> %s" %
          (f"{math.factorial(10):,}", f"{math.factorial(15):,}", f"{math.factorial(20):,}"))
    print("DP vs enumeration at n=15: %s states vs %s routes (%.0fx fewer)" %
          (f"{15 * 2 ** 14:,}", f"{math.factorial(15):,}", math.factorial(15) / (15 * 2 ** 14)))

    # ----- 6.6 supporting evidence -----
    print("\n" + "#" * 78)
    print("TASK 6.6  SUPPORTING EVIDENCE FOR THE BUSINESS CHANGE (heuristic trial, not required)")
    print("#" * 78)
    rng = random.Random(77)
    gaps = []
    for _ in range(20):
        pts = [(rng.random() * 100, rng.random() * 100) for _ in range(13)]       # hub + 12
        m = euclid_matrix(pts)
        opt, _ = held_karp(m)
        h = two_opt(m, nearest_neighbour(m))
        gaps.append((tour_cost(m, h) - opt) / opt * 100)
    print(f"12 locations x 20 random maps: nearest-neighbour + 2-opt is on average {sum(gaps) / 20:.2f}% above the DP "
          f"optimum (worst {max(gaps):.2f}%, exact optimum in {sum(1 for g in gaps if g < 1e-9)}/20 maps)")
    pts = [(rng.random() * 1000, rng.random() * 1000) for _ in range(201)]        # hub + 200
    m = euclid_matrix(pts)
    t0 = time.perf_counter()
    nn = nearest_neighbour(m)
    t1 = time.perf_counter()
    imp = two_opt(m, nn[:])
    t2 = time.perf_counter()
    print(f"200 locations: nearest-neighbour length {tour_cost(m, nn):.1f} in {t1 - t0:.4f}s;"
          f" after 2-opt {tour_cost(m, imp):.1f} in {t2 - t1:.3f}s  (valid tour: {sorted(imp[:-1]) == list(range(201))})")
    print("The exact DP was NOT run for 200 locations: it would need ~10^62 states.")


if __name__ == "__main__":
    main()
