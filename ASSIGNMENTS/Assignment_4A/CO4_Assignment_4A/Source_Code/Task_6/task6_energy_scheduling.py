"""Task 6 - Energy-aware job scheduling = Weighted Interval Scheduling (Dynamic Programming).
Author: S KUSHA LAKSHMI | Reg No: 192571074 | Course: CSA0608"""
from itertools import combinations


def schedule_dp(jobs, verbose=True):
    jobs = sorted(jobs, key=lambda j: (j[2], j[1]))          # sort by finish time
    n = len(jobs)
    p = [0] * (n + 1)
    for k in range(1, n + 1):                                # p[k]: largest index i<k with finish_i <= start_k
        p[k] = 0
        for i in range(k - 1, 0, -1):
            if jobs[i - 1][2] <= jobs[k - 1][1]:
                p[k] = i
                break
    OPT = [0] * (n + 1)
    for k in range(1, n + 1):
        incl = jobs[k - 1][3] + OPT[p[k]]
        excl = OPT[k - 1]
        OPT[k] = incl if incl > excl else excl               # tie -> exclude
        if verbose:
            print(f"k={k} {jobs[k-1][0]} (s={jobs[k-1][1]},f={jobs[k-1][2]},v={jobs[k-1][3]}) p={p[k]} "
                  f"include={jobs[k-1][3]}+OPT[{p[k]}]={incl} exclude=OPT[{k-1}]={excl} -> OPT[{k}]={OPT[k]}")
    chosen, k = [], n
    while k > 0:
        if jobs[k - 1][3] + OPT[p[k]] > OPT[k - 1]:
            chosen.append(jobs[k - 1][0]); k = p[k]
        else:
            k -= 1
    chosen.reverse()
    return OPT[n], chosen, p, OPT


def brute(jobs):
    best, bs = 0, []
    for r in range(len(jobs) + 1):
        for c in combinations(jobs, r):
            ok = all(a[2] <= b[1] or b[2] <= a[1] for a, b in combinations(c, 2))
            v = sum(x[3] for x in c)
            if ok and v > best: best, bs = v, [x[0] for x in c]
    return best, bs


def greedy_earliest_finish(jobs):
    last, tot, ch = -1, 0, []
    for j in sorted(jobs, key=lambda j: j[2]):
        if j[1] >= last: ch.append(j[0]); tot += j[3]; last = j[2]
    return tot, ch


def greedy_highest_value(jobs):
    tot, ch = 0, []
    for j in sorted(jobs, key=lambda j: -j[3]):
        if all(j[2] <= c[1] or c[2] <= j[1] for c in ch): ch.append(j); tot += j[3]
    return tot, [c[0] for c in ch]


def greedy_shortest(jobs):
    tot, ch = 0, []
    for j in sorted(jobs, key=lambda j: j[2] - j[1]):
        if all(j[2] <= c[1] or c[2] <= j[1] for c in ch): ch.append(j); tot += j[3]
    return tot, [c[0] for c in ch]


if __name__ == "__main__":
    J = [("J1", 1, 3, 20), ("J2", 2, 5, 50), ("J3", 4, 6, 30), ("J4", 6, 8, 40),
         ("J5", 5, 9, 60), ("J6", 8, 10, 30), ("J7", 9, 11, 50), ("J8", 11, 13, 40)]
    print("===== GIVEN DATASET : DP =====")
    best, ch, p, OPT = schedule_dp(J)
    print("p[1..8] =", p[1:], "\nOPT[0..8] =", OPT)
    print("Selected jobs:", ch, "| Maximum energy saving:", best)
    print("Brute force  :", brute(J))
    print("\nStrategy comparison on the given data:")
    print("  earliest-finish greedy :", greedy_earliest_finish(J))
    print("  highest-value greedy   :", greedy_highest_value(J))
    print("  shortest-job greedy    :", greedy_shortest(J))

    print("\n===== ADVERSARIAL SET A (defeats earliest-finish & shortest-job greedy) =====")
    A = [("A1", 0, 10, 100), ("A2", 0, 3, 10), ("A3", 3, 6, 10), ("A4", 6, 9, 10), ("A5", 2, 7, 25)]
    best, ch, p, OPT = schedule_dp(A)
    print("DP:", best, ch, "| brute:", brute(A))
    print("earliest-finish:", greedy_earliest_finish(A), "| highest-value:", greedy_highest_value(A), "| shortest:", greedy_shortest(A))

    print("\n===== ADVERSARIAL SET B (defeats highest-value greedy) =====")
    B = [("B1", 0, 10, 100), ("B2", 0, 4, 60), ("B3", 4, 7, 60), ("B4", 7, 10, 60), ("B5", 3, 6, 20)]
    best, ch, p, OPT = schedule_dp(B)
    print("DP:", best, ch, "| brute:", brute(B))
    print("earliest-finish:", greedy_earliest_finish(B), "| highest-value:", greedy_highest_value(B), "| shortest:", greedy_shortest(B))

    print("\n===== RANDOMISED VALIDATION: DP vs brute force (300 instances) =====")
    import random
    random.seed(192571074)
    bad = 0
    for _ in range(300):
        n = random.randint(5, 9)
        jobs = []
        for i in range(n):
            s = random.randint(0, 12); f = s + random.randint(1, 5)
            jobs.append((f"R{i}", s, f, random.randint(1, 60)))
        if schedule_dp(jobs, False)[0] != brute(jobs)[0]: bad += 1
    print("mismatches:", bad)
