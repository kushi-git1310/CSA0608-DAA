"""
CSA06 - Assignment 5 - Task B2 : same size (n=12), same m (=3), very different search.
Student : S KUSHA LAKSHMI (CSA0608)
"""
from b1_graph_colouring import colour_graph, input_order, conflict_first_order, valid_colouring

N, M = 12, 3
# Graph A : a simple path 0-1-2-...-11 (sparse, every vertex only conflicts with its predecessor)
GRAPH_A = (N, [(i, i + 1) for i in range(N - 1)])
# Graph B : vertices 0..7 are completely free; the contradiction (K4 on 8..11) is hidden at the END
GRAPH_B = (N, [(a, b) for a in range(8, 12) for b in range(a + 1, 12)])

print("PREDICTION (written before running)")
print("  * Graph B needs far more search than Graph A.")
print("  * Unsuccessful branches arise only at depth 9-12 (when the K4 vertices are reached),")
print("    i.e. AFTER the 8 unconstrained vertices have been coloured in all 3^8 = 6561 ways.")
print("  * Pruning happens late in B (feasibility test cannot see the K4 contradiction early),")
print("    but immediately/never needed in A (every choice keeps a free colour).\n")

print("=" * 74)
for label, (n, e) in (("Graph A (path, easy)", GRAPH_A), ("Graph B (hidden K4, hard)", GRAPH_B)):
    col, st = colour_graph(n, e, M, input_order)
    print(f"{label}: n={n}, edges={len(e)}, m={M}  ->  {'colourable' if col else 'NOT colourable'}")
    print(f"   nodes={st['nodes']:,} attempts={st['attempts']:,} rejected={st['rejected']:,} "
          f"backtracks={st['backtracks']:,} max_depth={st['max_depth']}")
    if col:
        assert valid_colouring(n, e, M, col)
print("=" * 74)

print("\nSide-by-side table (Version 1 = input order)")
print(f"{'Measure':<18}{'Graph A':>12}{'Graph B':>14}")
a = colour_graph(*GRAPH_A, M, input_order)[1]
b = colour_graph(*GRAPH_B, M, input_order)[1]
for k, lab in [("nodes", "Search nodes"), ("backtracks", "Backtracks"), ("rejected", "Rejected branches")]:
    print(f"{lab:<18}{a[k]:>12,}{b[k]:>14,}")

print("\nSame Graph B, but with the conflict-first ordering (Version 2):")
b2 = colour_graph(*GRAPH_B, M, conflict_first_order)[1]
print(f"   nodes={b2['nodes']}, backtracks={b2['backtracks']}, rejected={b2['rejected']}")

print("\nGrowth experiment: k free vertices placed BEFORE a K4 (m=3, Version 1)")
print(f"{'k free':>7}{'n':>5}{'nodes':>12}{'backtracks':>13}")
for k in range(2, 10):
    n = k + 4
    e = [(a, b) for a in range(k, n) for b in range(a + 1, n)]
    _, s = colour_graph(n, e, 3, input_order)
    print(f"{k:>7}{n:>5}{s['nodes']:>12,}{s['backtracks']:>13,}")
