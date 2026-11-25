"""
CSA06 - Assignment 5 - Task B4 : Bin packing (workloads -> servers) under a production constraint.
Student : S KUSHA LAKSHMI (CSA0608)
Placement rule : FIRST-FIT DECREASING (FFD)
   1. sort workloads by demand, largest first
   2. place each workload on the FIRST server whose remaining capacity >= demand
   3. if none fits, open a new server
"""
import itertools, math, random, time


def first_fit_decreasing(items, cap):
    order = sorted(range(len(items)), key=lambda i: -items[i])
    bins, rem = [], []
    for i in order:
        for b in range(len(bins)):
            if rem[b] >= items[i]:
                bins[b].append(i); rem[b] -= items[i]
                break
        else:
            bins.append([i]); rem.append(cap - items[i])
    return bins, rem


def first_fit(items, cap):             # no sorting (online)
    bins, rem = [], []
    for i, w in enumerate(items):
        for b in range(len(bins)):
            if rem[b] >= w:
                bins[b].append(i); rem[b] -= w
                break
        else:
            bins.append([i]); rem.append(cap - w)
    return bins, rem


def next_fit(items, cap):
    bins, rem = [[]], [cap]
    for i, w in enumerate(items):
        if rem[-1] < w:
            bins.append([]); rem.append(cap)
        bins[-1].append(i); rem[-1] -= w
    return bins, rem


def exact_min_bins(items, cap):
    """Small-n exact search (backtracking over bins); used only to judge heuristic quality."""
    items = sorted(items, reverse=True)
    best = [len(first_fit_decreasing(items, cap)[0])]
    rem = []

    def go(i):
        if len(rem) >= best[0]:
            return
        if i == len(items):
            best[0] = len(rem); return
        seen = set()
        for b in range(len(rem)):
            if rem[b] >= items[i] and rem[b] not in seen:
                seen.add(rem[b]); rem[b] -= items[i]; go(i + 1); rem[b] += items[i]
        rem.append(cap - items[i]); go(i + 1); rem.pop()
    go(0)
    return best[0]


def report(items, cap, bins, rem):
    print(f"  Servers used: {len(bins)}   (capacity per server = {cap})")
    for b, (content, r) in enumerate(zip(bins, rem), start=1):
        loads = [items[i] for i in content]
        print(f"   Server {b:>2}: workloads W{[i+1 for i in content]} demands={loads} used={sum(loads)} remaining={r}")


def main():
    C = 100
    demo = [45, 70, 30, 25, 55, 20, 60, 35, 15, 50, 10, 40]
    print("=" * 78 + "\nB4.1  FFD on a demonstration input\n" + "=" * 78)
    print("  workload demands W1..W12 =", demo)
    bins, rem = first_fit_decreasing(demo, C)
    report(demo, C, bins, rem)
    lb = math.ceil(sum(demo) / C)
    print(f"  total demand = {sum(demo)}  -> lower bound ceil(sum/C) = {lb} servers; exact optimum = {exact_min_bins(demo, C)}")

    print("\n" + "=" * 78 + "\nB4.2  CHALLENGING INPUT (FFD uses more servers than necessary)\n" + "=" * 78)
    rnd = random.Random(2024)
    found = None
    while found is None:
        cap = 20
        items = [rnd.randint(3, 10) for _ in range(rnd.randint(7, 10))]
        f = len(first_fit_decreasing(items, cap)[0])
        o = exact_min_bins(items, cap)
        if f > o:
            found = (items, cap, f, o)
    items, cap, f, o = found
    print(f"  capacity = {cap}, demands = {sorted(items, reverse=True)}")
    b, r = first_fit_decreasing(items, cap)
    report(items, cap, b, r)
    print(f"  FFD servers = {f},  exact optimum = {o}   -> FFD wastes {f-o} server(s)")
    # well-known FFD adversarial family
    k_items = [44, 44, 44, 44, 44, 44, 27, 27, 27, 27, 27, 27, 26, 26, 26, 26, 26, 26]
    print("\n  Known FFD-adversarial pattern (capacity 100): six 44s, six 27s, six 26s")
    print("  (optimal packs one of each per server = 97 units; FFD packs 44+44, 27+27+27, 26+26+26)")
    bb, rr = first_fit_decreasing(k_items, 100)
    print(f"  FFD servers = {len(bb)},  exact optimum = {exact_min_bins(k_items, 100)}")

    print("\n" + "=" * 78 + "\nB4.3  PRODUCTION-SCALE EVIDENCE (random workloads, C = 100)\n" + "=" * 78)
    print(f"{'workloads':>10}{'lower bound':>13}{'FFD':>7}{'FF':>7}{'NF':>7}{'FFD ms':>9}{'FF ms':>8}{'NF ms':>8}")
    for n in (100, 1000, 5000, 20000):
        r2 = random.Random(n)
        w = [r2.randint(1, 100) for _ in range(n)]
        lb = math.ceil(sum(w) / 100)
        out = []
        for fn in (first_fit_decreasing, first_fit, next_fit):
            t = time.perf_counter(); bn, _ = fn(w, 100); out.append((len(bn), (time.perf_counter() - t) * 1000))
        print(f"{n:>10}{lb:>13}{out[0][0]:>7}{out[1][0]:>7}{out[2][0]:>7}{out[0][1]:>9.1f}{out[1][1]:>8.1f}{out[2][1]:>8.1f}")


if __name__ == "__main__":
    main()
