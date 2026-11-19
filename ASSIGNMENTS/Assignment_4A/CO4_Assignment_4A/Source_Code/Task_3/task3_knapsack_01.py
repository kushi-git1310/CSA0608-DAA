"""Task 3 - 0/1 Knapsack by Dynamic Programming with item reconstruction.
Author: S KUSHA LAKSHMI | Reg No: 192571074 | Course: CSA0608"""

def knapsack01(items, W):
    n = len(items)
    DP = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, wt, val = items[i - 1]
        for w in range(0, W + 1):
            if wt > w:
                DP[i][w] = DP[i - 1][w]
            else:
                DP[i][w] = max(DP[i - 1][w], val + DP[i - 1][w - wt])
    # reconstruction
    chosen, w = [], W
    for i in range(n, 0, -1):
        if DP[i][w] != DP[i - 1][w]:
            chosen.append(items[i - 1][0])
            w -= items[i - 1][1]
    chosen.reverse()
    return DP, DP[n][W], chosen


if __name__ == "__main__":
    items = [("P", 2, 12), ("Q", 3, 20), ("R", 4, 25), ("S", 5, 30)]
    W = 7
    DP, best, chosen = knapsack01(items, W)
    print("DP TABLE (rows i=0..4, columns w=0..%d)" % W)
    print("       " + " ".join(f"w={w:<2}" for w in range(W + 1)))
    for i, row in enumerate(DP):
        label = "i=0 --" if i == 0 else f"i={i} {items[i-1][0]}"
        print(f"{label:<7}" + " ".join(f"{v:<4}" for v in row))
    print("\nOptimum value :", best)
    print("Items selected:", chosen)
    print("Total weight  :", sum(w for n, w, v in items if n in chosen))

    print("\n=== Brute-force verification ===")
    from itertools import combinations
    bf = 0; bfset = None
    for r in range(len(items) + 1):
        for c in combinations(items, r):
            if sum(x[1] for x in c) <= W and sum(x[2] for x in c) > bf:
                bf = sum(x[2] for x in c); bfset = [x[0] for x in c]
    print("Brute force best:", bf, bfset)

    print("\n=== Boundary tests ===")
    print("W=0  ->", knapsack01(items, 0)[1:])
    print("W=1  ->", knapsack01(items, 1)[1:])
    print("W=14 ->", knapsack01(items, 14)[1:])
