"""
CSA06 - Assignment 5 - Task B3 : Emergency-service Set Cover, exact vs greedy.
Student : S KUSHA LAKSHMI (CSA0608)
Sets are stored as bit-masks (bit i = zone Z(i+1)).
Operation counts
  exact  : number of k-subsets of centres (combinations) tested
  greedy : number of 'uncovered-zones-covered' evaluations (one per remaining centre per round)
"""
import itertools, random, time


def to_mask(zs):
    m = 0
    for z in zs:
        m |= 1 << (z - 1)
    return m


def popcount(x):
    return bin(x).count("1")


def exact_cover(n, sets):
    """Smallest k such that some k centres cover all zones (iterative deepening on k)."""
    full = (1 << n) - 1
    tested = 0
    for k in range(1, len(sets) + 1):
        for combo in itertools.combinations(range(len(sets)), k):
            tested += 1
            cov = 0
            for i in combo:
                cov |= sets[i]
            if cov == full:
                return list(combo), tested
    return None, tested


def greedy_cover(n, sets, trace=False):
    uncovered = (1 << n) - 1          # state: uncovered zones
    chosen, evals = [], 0             # state: selected centres
    while uncovered:                  # termination: nothing uncovered
        best, best_gain = -1, 0
        for i, s in enumerate(sets):  # selection criterion: max newly covered zones
            evals += 1
            g = popcount(s & uncovered)
            if g > best_gain:
                best, best_gain = i, g
        if best == -1:
            return None, evals        # some zone belongs to no centre
        if trace:
            print(f"    pick C{best+1} (covers {best_gain} new zones), uncovered before = {popcount(uncovered)}")
        chosen.append(best)
        uncovered &= ~sets[best]      # state update
    return chosen, evals


def random_instance(n, m, seed):
    rnd = random.Random(seed)
    sets = []
    for _ in range(m):
        size = rnd.randint(max(2, n // 6), max(3, n // 3))
        sets.append(to_mask(rnd.sample(range(1, n + 1), size)))
    cov = 0
    for s in sets:
        cov |= s
    for z in range(n):                # guarantee feasibility
        if not (cov >> z) & 1:
            sets[rnd.randrange(m)] |= 1 << z
    return sets


def show(sets):
    return "  ".join(f"C{i+1}={{{','.join(str(z+1) for z in range(64) if (s>>z)&1)}}}" for i, s in enumerate(sets))


def main():
    print("=" * 78 + "\nB3.1  CORRECTNESS ON SMALL INSTANCES\n" + "=" * 78)
    inst = []
    # Instance 1 - hand made
    inst.append(("1 (hand-made, n=6)", 6, [to_mask(s) for s in
                 [[1, 2, 3], [4, 5, 6], [1, 4], [2, 5], [3, 6]]]))
    # Instance 2 - hand made, overlapping
    inst.append(("2 (hand-made, n=7)", 7, [to_mask(s) for s in
                 [[1, 2, 3, 4], [3, 4, 5, 6], [5, 6, 7], [1, 7], [2, 6]]]))
    # Instances 3-5 : random, seeds fixed in advance (NOT picked to favour greedy)
    for idx, seed in enumerate((11, 22, 33), start=3):
        inst.append((f"{idx} (random seed {seed}, n=12)", 12, random_instance(12, 9, seed)))
    print(f"{'Instance':<28}{'Exact':>7}{'Greedy':>8}{'Same?':>7}")
    for name, n, sets in inst:
        ex, _ = exact_cover(n, sets)
        gr, _ = greedy_cover(n, sets)
        print(f"{name:<28}{len(ex):>7}{len(gr):>8}{'Yes' if len(ex)==len(gr) else 'NO':>7}")

    print("\n" + "=" * 78 + "\nB3.2  COUNTEREXAMPLE  (greedy > optimal)\n" + "=" * 78)
    U = 9
    cex = [to_mask(s) for s in [[1, 2, 3, 4, 5], [6, 7, 8, 9], [3, 4, 5, 6, 7, 8]]]
    print("Zones Z1..Z9;", show(cex))
    ex, _ = exact_cover(U, cex)
    print("  Optimal cover :", [f"C{i+1}" for i in ex], "-> size", len(ex))
    print("  Greedy trace  :")
    gr, _ = greedy_cover(U, cex, trace=True)
    print("  Greedy cover  :", [f"C{i+1}" for i in gr], "-> size", len(gr))
    print(f"  GreedyCoverSize ({len(gr)}) > OptimalCoverSize ({len(ex)})")

    print("\n" + "=" * 78 + "\nB3.3  SCALING  (random instances, zones n, centres m)\n" + "=" * 78)
    print(f"{'n':>4}{'m':>4} | {'Exact combos tested':>20}{'Exact':>7}{'ms':>9} | "
          f"{'Greedy evals':>13}{'Greedy':>8}{'ms':>8} | ratio")
    for n, m, seed in [(10, 8, 1), (14, 12, 2), (18, 16, 3), (22, 20, 4), (26, 24, 5),
                       (30, 28, 6), (34, 32, 7), (38, 34, 8)]:
        sets = random_instance(n, m, seed)
        t0 = time.perf_counter(); ex, tested = exact_cover(n, sets); t1 = time.perf_counter()
        gr, evals = greedy_cover(n, sets); t2 = time.perf_counter()
        print(f"{n:>4}{m:>4} | {tested:>20,}{len(ex):>7}{(t1-t0)*1000:>9.1f} | "
              f"{evals:>13,}{len(gr):>8}{(t2-t1)*1000:>8.2f} | {len(gr)/len(ex):.2f}")

    from math import comb
    print("\nProjection: combinations an exact enumerator must examine up to size k (m centres)")
    print(f"{'m':>6}{'k':>4}{'sum C(m,1..k)':>34}{'greedy evals (<= m*k)':>24}")
    for m, k in [(30, 6), (50, 8), (100, 10), (200, 15)]:
        print(f"{m:>6}{k:>4}{sum(comb(m, j) for j in range(1, k + 1)):>34,}{m*k:>24,}")


if __name__ == "__main__":
    main()
