"""A1.5 - verbose search trace on a 5-service graph (printed by the real implementation)."""
from b1_graph_colouring import colour_graph

names = ["S1", "S2", "S3", "S4", "S5"]
edges = [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 4)]   # S3,S4,S5 form a triangle
print("Graph: services S1..S5, conflicts:", [(names[a], names[b]) for a, b in edges])
for m in (2, 3):
    print("\n" + "-" * 70 + f"\nTRACE with m = {m} server groups\n" + "-" * 70)
    col, st = colour_graph(5, edges, m, verbose=True, names=names)
    print("RESULT:", "no valid assignment" if col is None else dict(zip(names, col)))
    print("STATS :", st)
