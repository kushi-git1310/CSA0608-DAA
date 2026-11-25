"""
CSA06 - Assignment 5 (CO5) - Task B1
Graph Colouring (Cloud-Service Deployment) by instrumented backtracking.
Student : S KUSHA LAKSHMI   (CSA0608)

Counters recorded
  nodes      : search nodes visited (calls of SOLVE)
  attempts   : candidate (vertex, colour) assignments attempted
  rejected   : candidates rejected by the feasibility test
  backtracks : undo operations (a placed colour removed after its subtree failed)
  max_depth  : deepest level reached (= largest number of vertices coloured)
"""
import sys

sys.setrecursionlimit(10000)


def build_adj(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def input_order(n, adj):
    """Version 1 : vertices in the original / input order."""
    return list(range(n))


def conflict_first_order(n, adj):
    """
    Version 2 : 'Most-constrained-first' static ordering.
    Rule : start with the vertex of highest degree; then repeatedly choose the
    un-ordered vertex that has the MOST neighbours already in the order
    (ties -> higher degree, then smaller index).
    Reason : a vertex with many already-coloured neighbours has the fewest legal
    colours, so contradictions (dense sub-graphs such as cliques) are exposed
    near the root instead of after many irrelevant vertices have been coloured.
    """
    if n == 0:
        return []
    chosen, left = [], set(range(n))
    while left:
        in_order = set(chosen)
        v = max(left, key=lambda x: (len(adj[x] & in_order), len(adj[x]), -x))
        chosen.append(v)
        left.remove(v)
    return chosen


def colour_graph(n, edges, m, order_fn=input_order, verbose=False, names=None):
    """Backtracking m-colouring. Returns (colouring or None, stats dict)."""
    adj = build_adj(n, edges)
    order = order_fn(n, adj)
    colour = [-1] * n
    st = dict(nodes=0, attempts=0, rejected=0, backtracks=0, max_depth=0)
    nm = (lambda v: names[v]) if names else (lambda v: f"v{v}")

    def feasible(v, c):                      # feasibility test
        return all(colour[u] != c for u in adj[v])

    def solve(depth):
        st["nodes"] += 1
        st["max_depth"] = max(st["max_depth"], depth)
        if depth == n:                       # goal condition
            return True
        v = order[depth]                     # selection of next service
        pad = "  " * depth
        for c in range(m):                   # candidate server groups
            st["attempts"] += 1
            if verbose:
                print(f"{pad}CHOOSE {nm(v)} -> group {c}", end="  ")
            if feasible(v, c):               # CHECK
                colour[v] = c                # assign
                if verbose:
                    print("CHECK ok -> ACCEPT, EXPLORE deeper")
                if solve(depth + 1):         # recursive exploration
                    return True
                colour[v] = -1               # UNDO
                st["backtracks"] += 1
                if verbose:
                    print(f"{pad}  BACKTRACK: undo {nm(v)}={c}")
            else:
                st["rejected"] += 1
                if verbose:
                    clash = [nm(u) for u in adj[v] if colour[u] == c]
                    print(f"CHECK fail (clash with {', '.join(clash)}) -> REJECT")
        return False                         # all candidates failed

    ok = solve(0)
    return (colour[:] if ok else None), st


def valid_colouring(n, edges, m, col):
    if col is None:
        return False
    return (all(0 <= c < m for c in col) and all(col[u] != col[v] for u, v in edges))


# ------------------------------------------------------------------ graphs
CLOUD6 = (6, [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5)])  # m=3 colourable
K4 = (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])                       # chi=4
HIDDEN_K4 = (12, [(8, 9), (8, 10), (8, 11), (9, 10), (9, 11), (10, 11)])         # 8 free + K4 last
PETERSEN = (10, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
                 (5, 7), (7, 9), (9, 6), (6, 8), (8, 5)])                         # chi=3
_c5 = [(i, (i + 1) % 5) for i in range(5)]
_sh = [(5 + i, (i + 1) % 5) for i in range(5)] + [(5 + i, (i - 1) % 5) for i in range(5)]
_hub = [(10, 5 + i) for i in range(5)]
GROTZSCH = (11, _c5 + _sh + _hub)                                                 # chi=4


def scramble(g, perm):
    """Relabel vertices so that the INPUT order is unfavourable."""
    n, e = g
    return n, [(perm[u], perm[v]) for u, v in e]


# Petersen with interleaved labelling, Groetzsch with hub last, etc.
PETERSEN_S = scramble(PETERSEN, [0, 5, 1, 6, 2, 7, 3, 8, 4, 9])
TAIL_K5 = (13, [(a, b) for a in range(8, 13) for b in range(a + 1, 13)])          # K5 hidden at the end, m=4 -> impossible


def run_tests():
    print("=" * 78)
    print("B1.1  VALIDATION TESTS  (Version 1 - input order)")
    print("=" * 78)
    tests = [
        ("T1 colourable graph (6 services, m=3)", CLOUD6, 3, True,
         "normal case: a valid colouring must be found and be conflict-free"),
        ("T2 NOT colourable (K4, m=3)", K4, 3, False,
         "negative case: exhaustive search must report failure"),
        ("T3 boundary: empty graph n=0, m=1", (0, []), 1, True,
         "empty input: trivially colourable, zero search"),
        ("T4 boundary: single vertex, m=1", (1, []), 1, True,
         "smallest non-empty instance"),
        ("T5 boundary: edgeless graph n=5, m=1", (5, []), 1, True,
         "no conflicts: one group suffices"),
        ("T6 boundary: one edge, m=1", (2, [(0, 1)]), 1, False,
         "tight limit: 2 conflicting services cannot share 1 group"),
        ("T7 boundary: n=3 vertices, m=0", (3, []), 0, False,
         "no server groups available"),
        ("T8 Petersen graph, m=3", PETERSEN, 3, True, "chi=3 -> exactly tight m"),
        ("T9 Petersen graph, m=2", PETERSEN, 2, False, "contains odd cycle -> impossible"),
    ]
    allok = True
    for name, (n, e), m, expect, why in tests:
        col, st = colour_graph(n, e, m)
        found = col is not None
        sound = (not found) or valid_colouring(n, e, m, col)
        res = "PASS" if (found == expect and sound) else "FAIL"
        allok &= (res == "PASS")
        print(f"\n{name}\n  verifies : {why}\n  expected : {'colouring exists' if expect else 'no colouring'}"
              f"   actual : {'colouring found' if found else 'no colouring'}   -> {res}")
        print(f"  colouring: {col}")
        print(f"  stats    : {st}")
    print("\nALL TESTS PASSED" if allok else "\nSOME TESTS FAILED")


COMPARE = [
    ("G1 CLOUD6 (m=3)", CLOUD6, 3),
    ("G2 Petersen, interleaved labels (m=3)", PETERSEN_S, 3),
    ("G3 Hidden K4 after 8 free vertices (m=3)", HIDDEN_K4, 3),
    ("G4 Groetzsch graph (chi=4) (m=3)", GROTZSCH, 3),
    ("G5 Hidden K5 after 8 free vertices (m=4)", TAIL_K5, 4),
]


def run_comparison():
    print("\n" + "=" * 78)
    print("B1.3 / B1.4  VERSION 1 (input order)  vs  VERSION 2 (conflict-first order)")
    print("=" * 78)
    rows = []
    for name, (n, e), m in COMPARE:
        c1, s1 = colour_graph(n, e, m, input_order)
        c2, s2 = colour_graph(n, e, m, conflict_first_order)
        assert (c1 is None) == (c2 is None)
        rows.append((name, s1, s2, c1 is not None))
        print(f"\n{name}   result: {'colourable' if c1 else 'NOT colourable'}")
        print(f"  {'Measure':<22}{'Version 1':>12}{'Version 2':>12}{'V1/V2':>9}")
        for k, lab in [("nodes", "Search nodes"), ("attempts", "Candidate assignments"),
                       ("rejected", "Rejected branches"), ("backtracks", "Backtracks"),
                       ("max_depth", "Max depth")]:
            r = (s1[k] / s2[k]) if s2[k] else float("inf")
            print(f"  {lab:<22}{s1[k]:>12}{s2[k]:>12}{r:>9.1f}")
    return rows


if __name__ == "__main__":
    run_tests()
    run_comparison()
