"""
CSA0608 - Design and Analysis of Algorithms | Assignment 4B
Student : S KUSHA LAKSHMI   Reg.No : 192571074

TASK 2 - GREEDY vs DYNAMIC PROGRAMMING (Knapsack)

Solution A : Fractional Knapsack  - greedy by value/weight ratio
Solution B : 0/1 Knapsack         - dynamic programming over (item, capacity)
Extra      : the SAME greedy idea applied to 0/1 (to break it), plus statistics.
"""
import random
from dataclasses import dataclass
from functools import cmp_to_key


@dataclass(frozen=True)
class Item:
    item_id: str
    weight: int
    value: int

    @property
    def ratio(self):
        return self.value / self.weight


def validate(items, capacity):
    if capacity < 0:
        raise ValueError("capacity must be >= 0")
    for it in items:
        if it.weight <= 0 or it.value < 0:
            raise ValueError(f"invalid item {it}: weight must be > 0 and value >= 0")


# --------------------------------------------------------------------------- #
# SOLUTION A  - greedy (fractional)  and the same greedy applied to 0/1
# --------------------------------------------------------------------------- #
def sort_by_ratio(items, ops):
    """Sort by value/weight, highest first, counting every comparison made."""
    def cmp(a, b):
        ops["comparisons"] += 1
        return (b.ratio > a.ratio) - (b.ratio < a.ratio)
    return sorted(items, key=cmp_to_key(cmp))


def fractional_greedy(items, capacity):
    """Returns (total_value, picks, ops). picks = [(item, fraction, weight_taken, value_taken, note)]"""
    validate(items, capacity)
    ops = {"comparisons": 0, "item_steps": 0}
    ordered = sort_by_ratio(items, ops)
    remaining, total, picks = capacity, 0.0, []
    for it in ordered:
        ops["item_steps"] += 1
        if remaining <= 0:
            break
        if it.weight <= remaining:
            picks.append((it, 1.0, it.weight, float(it.value), "whole item"))
            remaining -= it.weight
            total += it.value
        else:
            frac = remaining / it.weight
            picks.append((it, frac, remaining, it.value * frac, f"fraction {remaining}/{it.weight}"))
            total += it.value * frac
            remaining = 0
    return total, picks, ops, remaining


def greedy_01(items, capacity):
    """The same ratio-first intuition, but an item can only be taken whole (skip if it does not fit)."""
    validate(items, capacity)
    ops = {"comparisons": 0, "item_steps": 0}
    ordered = sort_by_ratio(items, ops)
    remaining, total, log = capacity, 0, []
    for it in ordered:
        ops["item_steps"] += 1
        if it.weight <= remaining:
            remaining -= it.weight
            total += it.value
            log.append((it, "TAKE", remaining, total))
        else:
            log.append((it, "SKIP (does not fit)", remaining, total))
    return total, log, ops


def greedy_01_with_best_single(items, capacity):
    """Classic repair: max(greedy result, most valuable single item that fits)."""
    g, _, _ = greedy_01(items, capacity)
    singles = [it.value for it in items if it.weight <= capacity]
    return max([g] + singles)


# --------------------------------------------------------------------------- #
# SOLUTION B - 0/1 knapsack, dynamic programming
# --------------------------------------------------------------------------- #
def knapsack_dp(items, capacity):
    """table[i][c] = best value using the first i items with capacity c.
    Returns (best_value, chosen_items, table, ops)."""
    validate(items, capacity)
    n = len(items)
    ops = {"cell_evaluations": 0, "comparisons": 0}
    table = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        it = items[i - 1]
        for c in range(capacity + 1):
            ops["cell_evaluations"] += 1
            skip = table[i - 1][c]
            if it.weight <= c:
                take = table[i - 1][c - it.weight] + it.value
                ops["comparisons"] += 1
                table[i][c] = take if take > skip else skip
            else:
                table[i][c] = skip
    chosen, c = [], capacity
    for i in range(n, 0, -1):                       # trace back
        if table[i][c] != table[i - 1][c]:
            chosen.append(items[i - 1])
            c -= items[i - 1].weight
    chosen.reverse()
    return table[n][capacity], chosen, table, ops


def knapsack_dp_value_only(items, capacity):
    """Same DP with one rolling row: memory O(W) but the chosen items cannot be rebuilt."""
    row = [0] * (capacity + 1)
    for it in items:
        for c in range(capacity, it.weight - 1, -1):
            row[c] = max(row[c], row[c - it.weight] + it.value)
    return row[capacity]


# --------------------------------------------------------------------------- #
# PRINT HELPERS
# --------------------------------------------------------------------------- #
def show_items(items, capacity):
    print(f"Capacity = {capacity}")
    print(f"{'ID':<4}{'Weight':>7}{'Value':>7}{'Value/Wt':>10}")
    for it in items:
        print(f"{it.item_id:<4}{it.weight:>7}{it.value:>7}{it.ratio:>10.3f}")


def show_fractional(items, capacity):
    total, picks, ops, left = fractional_greedy(items, capacity)
    print("\nSolution A - Fractional greedy: decision sequence")
    print(f"{'step':>4} {'item':<4}{'ratio':>7}{'fraction':>10}{'weight used':>12}{'value gained':>14}  note")
    run_w = 0
    for k, (it, fr, wt, val, note) in enumerate(picks, 1):
        run_w += wt
        print(f"{k:>4} {it.item_id:<4}{it.ratio:>7.2f}{fr:>10.3f}{wt:>12}{val:>14.2f}  {note}  (cum. weight {run_w}/{capacity})")
    print(f"Fractional greedy value = {total:.2f}   unused capacity = {left}")
    print(f"Operations: {ops}")
    return total


def show_greedy01(items, capacity):
    total, log, ops = greedy_01(items, capacity)
    print("\nGreedy applied to 0/1 knapsack: decision sequence")
    print(f"{'step':>4} {'item':<4}{'w':>4}{'v':>5}{'ratio':>7}  {'decision':<22}{'cap left':>9}{'value so far':>14}")
    for k, (it, dec, left, tot) in enumerate(log, 1):
        print(f"{k:>4} {it.item_id:<4}{it.weight:>4}{it.value:>5}{it.ratio:>7.2f}  {dec:<22}{left:>9}{tot:>14}")
    print(f"Greedy 0/1 value = {total}")
    return total, log


def show_dp(items, capacity):
    best, chosen, table, ops = knapsack_dp(items, capacity)
    print("\nSolution B - 0/1 DP result")
    print("Chosen items :", [(c.item_id, c.weight, c.value) for c in chosen])
    print(f"Total weight = {sum(c.weight for c in chosen)}/{capacity}   Optimal value = {best}")
    print(f"Operations: {ops}   table cells = {(len(items) + 1) * (capacity + 1)}")
    return best, chosen, table


def show_table(items, capacity, table):
    print("\nDP table  (rows = items considered, columns = capacity 0..W)")
    print("     " + "".join(f"{c:>5}" for c in range(capacity + 1)))
    for i, row in enumerate(table):
        label = "none" if i == 0 else items[i - 1].item_id
        print(f"{label:>4} " + "".join(f"{v:>5}" for v in row))


# --------------------------------------------------------------------------- #
def random_instance(rng, n, max_w, cap_fraction):
    items = [Item(f"I{k + 1}", rng.randint(1, max_w), rng.randint(1, 100)) for k in range(n)]
    cap = max(1, int(sum(i.weight for i in items) * cap_fraction))
    return items, cap


def main():
    print("#" * 78)
    print("TASK 2.1  NORMAL CASE - ratio-greedy gives the optimum")
    print("#" * 78)
    normal = [Item("A", 5, 50), Item("B", 4, 36), Item("C", 6, 42), Item("D", 3, 18), Item("E", 2, 10)]
    cap = 17
    show_items(normal, cap)
    frac_val = show_fractional(normal, cap)
    g01_val, _ = show_greedy01(normal, cap)
    dp_val, chosen, table = show_dp(normal, cap)
    print(f"\nCHECK  fractional greedy = {frac_val:.2f} (provably optimal for the fractional problem, "
          f"and an upper bound for 0/1)")
    print(f"CHECK  greedy-0/1 = {g01_val}  DP optimum = {dp_val}  -> equal: {g01_val == dp_val}")
    show_table(normal, cap, table)

    print("\n" + "#" * 78)
    print("TASK 2.2  BREAK THE GREEDY INTUITION (student-designed counter-example)")
    print("#" * 78)
    trap = [Item("L1", 10, 60), Item("L2", 7, 40), Item("L3", 8, 45), Item("L4", 1, 2)]
    cap2 = 15
    show_items(trap, cap2)
    fr = show_fractional(trap, cap2)
    g, log = show_greedy01(trap, cap2)
    d, chosen, table2 = show_dp(trap, cap2)
    print(f"\nGreedyResult = {g}   DPOptimum = {d}   GreedyResult != DPOptimum : {g != d}")
    assert g != d
    first_commit = log[0][0]
    print(f"FIRST FATAL COMMITMENT: step 1 takes {first_commit.item_id} "
          f"(weight {first_commit.weight}, ratio {first_commit.ratio:.2f}) because it has the best ratio.")
    print(f"  After it only {cap2 - first_commit.weight} units remain, and neither L2 (7) nor L3 (8) can fit,")
    print("  yet L2 + L3 together fill exactly 15 units with value 85.  Greedy can never undo a commitment.")
    print(f"  Greedy reaches {g / d * 100:.1f}% of the optimum; the fractional bound would have been {fr:.2f}.")
    print(f"  Greedy + best-single-item repair = {greedy_01_with_best_single(trap, cap2)} (still < {d})")
    show_table(trap, cap2, table2)

    print("\n" + "#" * 78)
    print("TASK 2.3  ENGINEERING COMPARISON (operation counts, memory, quality, guarantee)")
    print("#" * 78)
    rng = random.Random(2026)
    print("(a) Work and memory as the problem grows (random items, capacity = 40% of total weight)")
    print(f"{'n':>5}{'W':>8} | {'greedy compares':>15}{'greedy steps':>13}{'greedy mem(items)':>19} | "
          f"{'DP cells':>10}{'DP compares':>12}{'DP mem full':>12}{'DP mem 1-row':>13}")
    for n, max_w in [(10, 10), (50, 20), (100, 50), (200, 50), (200, 500)]:
        its, c = random_instance(rng, n, max_w, 0.4)
        _, _, gops, _ = fractional_greedy(its, c)
        _, _, _, dops = knapsack_dp(its, c)
        print(f"{n:>5}{c:>8} | {gops['comparisons']:>15}{gops['item_steps']:>13}{n:>19} | "
              f"{dops['cell_evaluations']:>10}{dops['comparisons']:>12}{(n + 1) * (c + 1):>12}{c + 1:>13}")
    print("\n(b) Effect of the capacity VALUE on the same 100 items (capacity measured in kg vs g)")
    base_items, base_cap = random_instance(random.Random(7), 100, 50, 0.4)
    print(f"{'capacity':>10} | {'greedy compares':>15} | {'DP cell evaluations':>20}")
    for mult in (1, 10, 100):
        scaled = [Item(i.item_id, i.weight * mult, i.value) for i in base_items]
        _, _, gops, _ = fractional_greedy(scaled, base_cap * mult)
        _, _, _, dops = knapsack_dp(scaled, base_cap * mult)
        print(f"{base_cap * mult:>10} | {gops['comparisons']:>15} | {dops['cell_evaluations']:>20}")

    print("\n(c) Solution quality over 1000 random 0/1 instances (n=15, weights 1-30, capacity 35%)")
    rng = random.Random(42)
    optimal_hits = worst = 0
    worst = 1.0
    sum_ratio = sum_fix = 0.0
    fix_hits = 0
    for _ in range(1000):
        its, c = random_instance(rng, 15, 30, 0.35)
        g, _, _ = greedy_01(its, c)
        d = knapsack_dp_value_only(its, c)
        gf = greedy_01_with_best_single(its, c)
        optimal_hits += (g == d)
        fix_hits += (gf == d)
        r = g / d if d else 1.0
        sum_ratio += r
        sum_fix += gf / d if d else 1.0
        worst = min(worst, r)
    print(f"  greedy found the exact optimum in {optimal_hits}/1000 instances")
    print(f"  average quality = {sum_ratio / 1000 * 100:.2f}% of optimum, worst case = {worst * 100:.1f}%")
    print(f"  greedy + best-single repair optimal in {fix_hits}/1000, average {sum_fix / 1000 * 100:.2f}%")

    print("\n(d) Summary table")
    print(f"{'Criterion':<22}{'Greedy (fractional / 0-1 heuristic)':<42}{'DP 0/1'}")
    rows = [("Computational work", "O(n log n): sort + one pass", "O(n*W) cell evaluations"),
            ("Memory", "O(n) - just the item list", "O(n*W) table (O(W) value only)"),
            ("Solution quality", "optimal for fractional; heuristic for 0/1", "always the exact 0/1 optimum"),
            ("Guarantee", "none for 0/1 (can be far from optimum)", "optimal; pseudo-polynomial in W")]
    for a, b, c in rows:
        print(f"{a:<22}{b:<42}{c}")

    print("\n" + "#" * 78)
    print("TASK 2.4  CHANGED REQUIREMENT - 'answer extremely quickly, near-optimal is fine'")
    print("#" * 78)
    big_items, big_cap = random_instance(random.Random(99), 2000, 1000, 0.4)
    _, _, gops, _ = fractional_greedy(big_items, big_cap)
    print(f"Fleet-scale instance: n=2000 items, capacity={big_cap}")
    print(f"  greedy work       : {gops['comparisons']} comparisons")
    print(f"  DP work would be  : {2000 * (big_cap + 1)} cell evaluations "
          f"({2000 * (big_cap + 1) // max(1, gops['comparisons'])}x more), table memory {(2001) * (big_cap + 1)} cells")
    g, _, _ = greedy_01(big_items, big_cap)
    d = knapsack_dp_value_only(big_items, big_cap)
    print(f"  greedy 0/1 = {g}, DP optimum = {d}  ->  greedy is {g / d * 100:.3f}% of optimal")
    print("Conclusion: use ratio-greedy (+ best-single-item repair) when speed dominates; keep DP for audits.")

    print("\nBoundary tests:")
    print("  capacity 0         ->", fractional_greedy(normal, 0)[0], greedy_01(normal, 0)[0], knapsack_dp(normal, 0)[0])
    print("  empty item list    ->", fractional_greedy([], 10)[0], greedy_01([], 10)[0], knapsack_dp([], 10)[0])
    print("  item heavier than W->", fractional_greedy([Item('X', 50, 99)], 10)[0], greedy_01([Item('X', 50, 99)], 10)[0],
          knapsack_dp([Item('X', 50, 99)], 10)[0])
    try:
        knapsack_dp([Item("Z", 0, 5)], 10)
    except ValueError as e:
        print("  zero weight item   -> rejected:", e)


if __name__ == "__main__":
    main()
