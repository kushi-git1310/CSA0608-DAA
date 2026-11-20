"""
CSA0608 - Design and Analysis of Algorithms | Assignment 4B
Student : S KUSHA LAKSHMI   Reg.No : 192571074

TASK 4 - SMART MANUFACTURING OPTIMISATION (Assembly-Line Scheduling, DP)

Notation (stations are numbered 1..n in the report, 0..n-1 in code)
    a[L][j]   processing time of station j on line L
    t[L][j]   time to transfer from line L (after station j) to the OTHER line (before station j+1)
    e[L]      entry time onto line L          x[L]  exit time from line L
DP
    f[L][j] = fastest time to finish station j on line L
    f[L][0] = e[L] + a[L][0]
    f[L][j] = a[L][j] + min( f[L][j-1]                  (stay on L),
                             f[O][j-1] + t[O][j-1] )    (transfer from other line O)
    answer  = min( f[0][n-1] + x[0], f[1][n-1] + x[1] )
    choice[L][j] remembers which predecessor line was used  -> route reconstruction
"""
from itertools import product

LINE_NAME = ["Line 1", "Line 2"]


def validate(a, t, e, x):
    n = len(a[0])
    if n == 0:
        raise ValueError("at least one station is required")
    if len(a[1]) != n:
        raise ValueError("both lines must have the same number of stations")
    if len(t[0]) != n - 1 or len(t[1]) != n - 1:
        raise ValueError("each transfer list needs exactly n-1 values")
    if any(v < 0 for row in (a[0], a[1], t[0], t[1], e, x) for v in (row if isinstance(row, list) else [row])):
        raise ValueError("times must be non-negative")


def assembly_line_dp(a, t, e, x):
    """Returns dict(total, f, choice, trace, route, transfers, exit_line)."""
    validate(a, t, e, x)
    n = len(a[0])
    f = [[0] * n for _ in range(2)]
    choice = [[None] * n for _ in range(2)]          # line used at station j-1
    trace = []                                        # one dict per station j >= 1
    for L in (0, 1):
        f[L][0] = e[L] + a[L][0]
    for j in range(1, n):
        row = {"station": j + 1}
        for L in (0, 1):
            O = 1 - L
            stay = f[L][j - 1] + a[L][j]
            move = f[O][j - 1] + t[O][j - 1] + a[L][j]
            if stay <= move:                          # tie -> prefer staying (fewer transfers)
                f[L][j], choice[L][j] = stay, L
                row[L] = (stay, move, "stay")
            else:
                f[L][j], choice[L][j] = move, O
                row[L] = (stay, move, "transfer")
        trace.append(row)
    finish = [f[0][n - 1] + x[0], f[1][n - 1] + x[1]]
    exit_line = 0 if finish[0] <= finish[1] else 1
    total = finish[exit_line]
    lines = [0] * n                                   # reconstruct backwards
    lines[n - 1] = exit_line
    for j in range(n - 1, 0, -1):
        lines[j - 1] = choice[lines[j]][j]
    transfers = [(j + 1, lines[j], lines[j + 1]) for j in range(n - 1) if lines[j] != lines[j + 1]]
    return {"total": total, "f": f, "choice": choice, "trace": trace, "route": lines,
            "transfers": transfers, "exit_line": exit_line, "finish": finish}


def brute_force(a, t, e, x):
    """Independent oracle: try all 2^n line assignments."""
    n = len(a[0])
    best, best_route = float("inf"), None
    for assign in product((0, 1), repeat=n):
        cost = e[assign[0]] + a[assign[0]][0]
        for j in range(1, n):
            if assign[j] != assign[j - 1]:
                cost += t[assign[j - 1]][j - 1]
            cost += a[assign[j]][j]
        cost += x[assign[-1]]
        if cost < best:
            best, best_route = cost, list(assign)
    return best, best_route


# ------------------------------- OUTPUT ------------------------------------ #
def print_route(res):
    lines, n = res["route"], len(res["route"])
    print("Entry")
    for j in range(n):
        print("  |")
        if j > 0 and lines[j] != lines[j - 1]:
            print(f"  v  Transfer (cost {TRANSFER_LOOKUP[(lines[j - 1], j - 1)]})")
        else:
            print("  v")
        print(f"{LINE_NAME[lines[j]]} - Station {j + 1}")
    print("  |\n  v\nExit")


def print_trace(res, a, e):
    f = res["f"]
    print(f"\nDP decision trace (f = fastest finishing time at that station)")
    print(f"Station 1 : reach Line 1 by entry = {e[0]}+{a[0][0]} = {f[0][0]};   reach Line 2 by entry = {e[1]}+{a[1][0]} = {f[1][0]}")
    hdr = (f"{'Stn':>3} | {'L1 stay':>8}{'L1 transfer':>12}{'L1 chosen':>11}{'f1':>5} | "
           f"{'L2 stay':>8}{'L2 transfer':>12}{'L2 chosen':>11}{'f2':>5}")
    print(hdr)
    print("-" * len(hdr))
    for row in res["trace"]:
        j = row["station"] - 1
        s1, m1, c1 = row[0]
        s2, m2, c2 = row[1]
        print(f"{row['station']:>3} | {s1:>8}{m1:>12}{c1:>11}{f[0][j]:>5} | {s2:>8}{m2:>12}{c2:>11}{f[1][j]:>5}")


def report(title, a, t, e, x, show_trace=True, show_route=True):
    global TRANSFER_LOOKUP
    TRANSFER_LOOKUP = {(L, j): t[L][j] for L in (0, 1) for j in range(len(t[L]))}
    res = assembly_line_dp(a, t, e, x)
    print(f"\n=== {title} ===")
    if show_trace:
        print_trace(res, a, e)
    print(f"Exit: via Line 1 = {res['finish'][0]}, via Line 2 = {res['finish'][1]} -> leave from {LINE_NAME[res['exit_line']]}")
    seq = " | ".join(f"S{j + 1}:L{l + 1}" for j, l in enumerate(res["route"]))
    print("Line chosen at each station :", seq)
    print("Transfer points             :", [f"after station {s}: Line {p + 1} -> Line {q + 1}" for s, p, q in res["transfers"]] or "none")
    if show_route:
        print_route(res)
    print(f"MINIMUM PRODUCTION TIME = {res['total']}")
    return res


def main():
    # -------- base data (6 stations) --------
    a = [[7, 9, 3, 4, 8, 4], [8, 5, 6, 4, 5, 7]]
    t = [[2, 3, 1, 3, 4], [2, 1, 2, 2, 1]]
    e, x = [2, 4], [3, 2]
    print("#" * 78)
    print("TASK 4.1 / 4.2  BASE CASE")
    print("#" * 78)
    print("Line 1 processing :", a[0], "\nLine 2 processing :", a[1])
    print("Transfer L1->L2 (after stn 1..5):", t[0], "\nTransfer L2->L1 (after stn 1..5):", t[1])
    print("Entry times       :", e, "  Exit times:", x)
    base = report("Base production line", a, t, e, x)
    bf, bf_route = brute_force(a, t, e, x)
    print(f"Validation by exhaustive search of 2^6 = 64 routes: optimum = {bf}, route = {bf_route}  ->  "
          f"{'MATCH' if bf == base['total'] and bf_route == base['route'] else 'MISMATCH'}")

    # Show the arithmetic of one decision (optimal substructure made visible)
    print("\nOptimal-substructure check: the best route to the LAST station contains the best route to the")
    print("previous station on its line:  f[line][j] uses f[line'][j-1], never a worse earlier schedule.")

    # -------- 4.3 predict-before-execute --------
    print("\n" + "#" * 78)
    print("TASK 4.3  PREDICT BEFORE YOU EXECUTE")
    print("#" * 78)
    print("Experiment: raise transfer time t[L1->L2] after station 1 from 2 to 20")
    print("            (the base route uses exactly this transfer: Line 1 stn 1 -> Line 2 stn 2).")
    print("PREDICTION (recorded before running):")
    print("  * The optimal route WILL change - an 18-unit rise on a 38-unit route is far larger than the few units this transfer saves.")
    print("  * The decision at station 2 (Line 2 'transfer from Line 1') is the one most affected; the route")
    print("    should enter Line 1 and stay on it for stations 1-2, or start on Line 2 from the entry.")
    print("  * Total production time WILL increase, but by LESS than 18 (the transfer increase), because the")
    print("    DP can re-route around the expensive transfer.")
    t_mod = [row[:] for row in t]
    t_mod[0][0] = 20
    mod = report("Modified: t[L1->L2][1] = 20", a, t_mod, e, x)
    d_total = mod["total"] - base["total"]
    print(f"\nOBSERVED: route changed = {mod['route'] != base['route']}, base route {[l + 1 for l in base['route']]} "
          f"-> new route {[l + 1 for l in mod['route']]}")
    print(f"          total {base['total']} -> {mod['total']} (increase of {d_total}, less than 18 = {d_total < 18})")
    print(f"          brute-force check: {brute_force(a, t_mod, e, x)[0]}")

    # -------- 4.4 production disruption --------
    print("\n" + "#" * 78)
    print("TASK 4.4  PRODUCTION DISRUPTION")
    print("#" * 78)
    broken_station = 3                       # station 3 (index 2)
    # find the line used at that station in the base route
    used = base["route"][broken_station - 1]
    print(f"Base route uses Line {used + 1} at station {broken_station}. The machine there slows from "
          f"{a[used][broken_station - 1]} to 30.")
    a_slow = [row[:] for row in a]
    a_slow[used][broken_station - 1] = 30
    slow = report(f"Disrupted: Line {used + 1}, station {broken_station} = 30", a_slow, t, e, x)
    print(f"\nRoute changed? {slow['route'] != base['route']}")
    print(f"Base route  : {[l + 1 for l in base['route']]}")
    print(f"New route   : {[l + 1 for l in slow['route']]}")
    print(f"Transfers   : {slow['transfers']}")
    print(f"Time {base['total']} -> {slow['total']}  (increase {slow['total'] - base['total']}; the slowdown itself was "
          f"{30 - a[used][broken_station - 1]}, so the DP absorbed {30 - a[used][broken_station - 1] - (slow['total'] - base['total'])})")
    print(f"Brute force confirms: {brute_force(a, t, e, x)[0]} -> {brute_force(a_slow, t, e, x)[0]}")

    # -------- boundary and failure tests --------
    print("\n" + "#" * 78)
    print("BOUNDARY / FAILURE TESTS")
    print("#" * 78)
    r1 = assembly_line_dp([[5], [3]], [[], []], [1, 1], [1, 1])
    print("single station (no transfers possible):", r1["total"], r1["route"])
    r2 = assembly_line_dp([[4, 4, 4], [4, 4, 4]], [[0, 0], [0, 0]], [0, 0], [0, 0])
    print("identical lines, free transfers (ties): total", r2["total"], "route", r2["route"],
          "(tie rule 'prefer stay' keeps the plan stable)")
    r3 = assembly_line_dp([[1, 1, 1], [9, 9, 9]], [[1, 1], [1, 1]], [0, 0], [0, 0])
    print("Line 1 always faster -> never leaves it:", r3["route"], r3["total"])
    r4 = assembly_line_dp([[9, 9, 9], [1, 1, 1]], [[100, 100], [100, 100]], [50, 0], [0, 0])
    print("huge transfer cost, cheap entry for Line 2 -> stays on Line 2:", r4["route"], r4["total"])
    for bad in [([[1, 2], [1]], [[1], [1]], [0, 0], [0, 0]),
                ([[1, 2], [1, 2]], [[1, 1], [1]], [0, 0], [0, 0]),
                ([[1, -2], [1, 2]], [[1], [1]], [0, 0], [0, 0]),
                ([[], []], [[], []], [0, 0], [0, 0])]:
        try:
            assembly_line_dp(*bad)
            print("  invalid input accepted <-- defect")
        except ValueError as err:
            print("  invalid input rejected ->", err)
    import random
    rng = random.Random(1)
    mism = 0
    for _ in range(500):
        n = rng.randint(1, 9)
        aa = [[rng.randint(1, 9) for _ in range(n)] for _ in range(2)]
        tt = [[rng.randint(0, 6) for _ in range(n - 1)] for _ in range(2)]
        ee, xx = [rng.randint(0, 5), rng.randint(0, 5)], [rng.randint(0, 5), rng.randint(0, 5)]
        if assembly_line_dp(aa, tt, ee, xx)["total"] != brute_force(aa, tt, ee, xx)[0]:
            mism += 1
    print(f"Randomised regression: 500 random lines (n=1..9) DP vs brute force -> mismatches = {mism}")


if __name__ == "__main__":
    main()
