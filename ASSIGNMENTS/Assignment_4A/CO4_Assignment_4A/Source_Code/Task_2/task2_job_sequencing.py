"""Task 2 - Job Sequencing with Deadlines (greedy: highest profit first, latest free slot).
Author: S KUSHA LAKSHMI | Reg No: 192571074 | Course: CSA0608"""

def job_sequencing(jobs, verbose=True):
    jobs = sorted(jobs, key=lambda j: -j[2])          # profit descending
    maxd = max(j[1] for j in jobs)
    slot = [None] * (maxd + 1)                        # slot[1..maxd]
    total = 0
    if verbose:
        print("Order of consideration:", [j[0] for j in jobs], "| slots 1..%d" % maxd)
    for jid, d, p in jobs:
        placed = False
        for t in range(min(d, maxd), 0, -1):          # latest free slot <= deadline
            if slot[t] is None:
                slot[t] = jid
                total += p
                placed = True
                if verbose:
                    print(f"  {jid}(d={d},p={p}) -> slot {t}   slots={slot[1:]} profit={total}")
                break
        if not placed and verbose:
            print(f"  {jid}(d={d},p={p}) -> REJECTED (no free slot <= {d})   slots={slot[1:]} profit={total}")
    return slot[1:], total


if __name__ == "__main__":
    base = [("A", 2, 80), ("B", 1, 35), ("C", 2, 60), ("D", 3, 40), ("E", 1, 25)]
    print("=== GIVEN INSTANCE ===")
    s, t = job_sequencing(base)
    print("Schedule:", s, "Total profit:", t)

    print("\n=== MODIFIED INSTANCE (A profit 80 -> 30) ===")
    mod = [("A", 2, 30), ("B", 1, 35), ("C", 2, 60), ("D", 3, 40), ("E", 1, 25)]
    s, t = job_sequencing(mod)
    print("Schedule:", s, "Total profit:", t)

    print("\n=== BRUTE-FORCE CHECK (all subsets, all orders) ===")
    from itertools import permutations
    def brute(jobs):
        best = 0
        n = len(jobs)
        for r in range(n + 1):
            for perm in permutations(jobs, r):
                if all(i + 1 <= perm[i][1] for i in range(r)):
                    best = max(best, sum(j[2] for j in perm))
        return best
    print("Greedy base =", job_sequencing(base, False)[1], "| brute force =", brute(base))
    print("Greedy mod  =", job_sequencing(mod, False)[1], "| brute force =", brute(mod))
