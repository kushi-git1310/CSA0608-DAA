"""
CSA0608 - Design and Analysis of Algorithms | Assignment 4B
Student : S KUSHA LAKSHMI   Reg.No : 192571074

TASK 3 - ROUTING ENGINE UNDER CHANGING NETWORK CONDITIONS
Dijkstra (A) -> Bellman-Ford (B, C) -> Floyd + Warshall (D)

Network: 9 logistics hubs A..I, 14 directed weighted edges (cost = hours).
"""
import heapq

INF = float("inf")
VERTICES = list("ABCDEFGHI")

# (from, to, weight)
BASE_EDGES = [
    ("A", "B", 4), ("A", "C", 2), ("B", "D", 3), ("C", "B", 1), ("C", "D", 8),
    ("C", "E", 10), ("D", "E", 2), ("D", "F", 6), ("E", "G", 3), ("F", "G", 1),
    ("F", "H", 5), ("G", "H", 2), ("G", "I", 7), ("H", "I", 1),
]
NEGATIVE_EDGE = ("F", "E", -5)        # Stage B : F->E is a 'rebate' lane
NEGATIVE_CYCLE_EDGE = ("E", "D", -3)  # Stage C : creates cycle D->E->D of weight 2-3 = -1


def build_adjacency(vertices, edges):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def path_to(pred, source, target):
    """Rebuild the route from the predecessor map. Returns None if unreachable."""
    if target != source and pred.get(target) is None:
        return None
    route, cur = [], target
    while cur is not None:
        route.append(cur)
        cur = pred.get(cur)
    return route[::-1]


# --------------------------------------------------------------------------- #
# STAGE A  Dijkstra (finalise-once version, valid for NON-NEGATIVE weights only)
# --------------------------------------------------------------------------- #
def dijkstra(vertices, edges, source):
    adj = build_adjacency(vertices, edges)
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    finalised, order = set(), []
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in finalised:                 # stale queue entry
            continue
        finalised.add(u)                   # distance of u is now declared FINAL
        order.append((u, d))
        for v, w in adj[u]:
            if v not in finalised and d + w < dist[v]:
                dist[v] = d + w
                pred[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, pred, order


# --------------------------------------------------------------------------- #
# STAGE B/C  Bellman-Ford with negative-cycle detection
# --------------------------------------------------------------------------- #
def bellman_ford(vertices, edges, source):
    """Returns (dist, pred, passes_used, negative_cycle or None)."""
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    passes_used = 0
    for _ in range(len(vertices) - 1):            # |V|-1 relaxation passes
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                changed = True
        passes_used += 1
        if not changed:                            # early exit - already stable
            break
    # |V|-th pass: if ANY edge can still be relaxed, a reachable negative cycle exists
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return dist, pred, passes_used, extract_cycle(vertices, pred, v)
    return dist, pred, passes_used, None


def extract_cycle(vertices, pred, start):
    """Walk |V| predecessor steps to be sure we are INSIDE the cycle, then collect it."""
    x = start
    for _ in range(len(vertices)):
        x = pred[x]
    cycle, cur = [x], pred[x]
    while cur != x:
        cycle.append(cur)
        cur = pred[cur]
    cycle.append(x)
    return cycle[::-1]


# --------------------------------------------------------------------------- #
# STAGE D  Floyd (all-pairs cost) and Warshall (reachability)
# --------------------------------------------------------------------------- #
def floyd(vertices, edges):
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    d = [[INF] * n for _ in range(n)]
    nxt = [[None] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
        nxt[i][i] = i
    for u, v, w in edges:
        if w < d[idx[u]][idx[v]]:
            d[idx[u]][idx[v]] = w
            nxt[idx[u]][idx[v]] = idx[v]
    for k in range(n):
        for i in range(n):
            if d[i][k] == INF:
                continue
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
                    nxt[i][j] = nxt[i][k]
    negative_cycle = any(d[i][i] < 0 for i in range(n))
    return d, nxt, negative_cycle


def floyd_path(vertices, nxt, a, b):
    idx = {v: i for i, v in enumerate(vertices)}
    i, j = idx[a], idx[b]
    if nxt[i][j] is None:
        return None
    route = [a]
    while i != j:
        i = nxt[i][j]
        route.append(vertices[i])
    return route


def warshall(vertices, edges):
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    r = [[False] * n for _ in range(n)]
    for i in range(n):
        r[i][i] = True
    for u, v, _ in edges:
        r[idx[u]][idx[v]] = True
    for k in range(n):
        for i in range(n):
            if r[i][k]:
                for j in range(n):
                    r[i][j] = r[i][j] or r[k][j]
    return r


# --------------------------------------------------------------------------- #
# PRINT HELPERS
# --------------------------------------------------------------------------- #
def fmt(x):
    return "INF" if x == INF else str(x)


def show_graph(edges, title, full=True):
    head = f": |V|={len(VERTICES)}, |E|={len(edges)}" if full else ""
    print(f"\n{title}{head}")
    for u, v, w in edges:
        print(f"   {u} -> {v}  weight {w:>3}")


def show_sssp(dist, pred, source, title):
    print(f"\n{title}  (source = {source})")
    print(f"{'Vertex':<7}{'Dist':>6}  {'Pred':<5} Route")
    for v in VERTICES:
        r = path_to(pred, source, v)
        print(f"{v:<7}{fmt(dist[v]):>6}  {str(pred[v]):<5} {' -> '.join(r) if r else 'unreachable'}")


def show_matrix(m, title, cell=lambda x: fmt(x)):
    print(f"\n{title}")
    print("     " + "".join(f"{v:>5}" for v in VERTICES))
    for i, v in enumerate(VERTICES):
        print(f"{v:>3}  " + "".join(f"{cell(m[i][j]):>5}" for j in range(len(VERTICES))))


def main():
    src = "A"
    print("#" * 78)
    print("STAGE A  NORMAL ROUTING - DIJKSTRA")
    print("#" * 78)
    show_graph(BASE_EDGES, "Base network (all weights positive)")
    dist, pred, order = dijkstra(VERTICES, BASE_EDGES, src)
    print("\nOrder in which vertices become FINALISED (vertex, final distance):")
    print("   " + " , ".join(f"{v}({d})" for v, d in order))
    show_sssp(dist, pred, src, "Dijkstra result on base network")
    bf_dist, _, passes, cyc = bellman_ford(VERTICES, BASE_EDGES, src)
    print(f"\nCross-check with Bellman-Ford: identical distances = {bf_dist == dist}, passes used = {passes}")

    print("\n" + "#" * 78)
    print("STAGE B  INTRODUCE A NEGATIVE EDGE  F -> E  (weight -5)")
    print("#" * 78)
    print("PREDICTION (recorded before running):")
    print("  * Dijkstra will NOT remain valid. E is finalised at distance 8 (via D) BEFORE F (distance 12)")
    print("    is processed. When F is processed, the edge F->E (-5) would give E = 12-5 = 7, but E is")
    print("    already 'final', so Dijkstra will never look at it again.")
    print("  * Affected decisions: the route to E (should become ...D -> F -> E), and everything that is")
    print("    reached through E: G, H and I (each should be 1 hour cheaper than Dijkstra reports).")
    neg_edges = BASE_EDGES + [NEGATIVE_EDGE]
    show_graph([NEGATIVE_EDGE], "Added edge", full=False)
    d2, p2, order2 = dijkstra(VERTICES, neg_edges, src)
    print("\nDijkstra finalisation order on modified graph:", " , ".join(f"{v}({d})" for v, d in order2))
    show_sssp(d2, p2, src, "Dijkstra on modified graph (WRONG for negative edges)")
    bd, bp, bpasses, bcyc = bellman_ford(VERTICES, neg_edges, src)
    show_sssp(bd, bp, src, "Bellman-Ford on modified graph (CORRECT)")
    print(f"\nBellman-Ford passes used = {bpasses}, negative cycle found = {bcyc}")
    print("\nCOMPARISON  Dijkstra vs Bellman-Ford")
    print(f"{'Vertex':<7}{'Dijkstra':>9}{'B-Ford':>8}{'Error':>7}   Dijkstra route  |  true route")
    wrong = []
    for v in VERTICES:
        err = d2[v] - bd[v]
        if err:
            wrong.append(v)
        print(f"{v:<7}{d2[v]:>9}{bd[v]:>8}{err:>7}   {' '.join(path_to(p2, src, v)):<15} |  {' '.join(path_to(bp, src, v))}")
    print(f"Vertices with wrong Dijkstra answer: {wrong}")
    print("PREDICTION CHECK: affected set predicted = {E, G, H, I}; actual =", set(wrong),
          "->", "MATCH" if set(wrong) == {"E", "G", "H", "I"} else "MISMATCH")
    print("Why an irrelevant negative edge would not do: a negative edge that points to a vertex finalised")
    print("AFTER its tail (e.g. G->H as -1) changes nothing for Dijkstra; F->E was chosen because E is")
    print("finalised before F, which breaks Dijkstra's 'a finalised distance never improves' invariant.")

    print("\n" + "#" * 78)
    print("STAGE C  PRODUCTION FAILURE - REACHABLE NEGATIVE CYCLE")
    print("#" * 78)
    cyc_edges = neg_edges + [NEGATIVE_CYCLE_EDGE]
    show_graph([NEGATIVE_CYCLE_EDGE], "Added edge", full=False)
    print("Two negative cycles now exist: D->E->D (2-3 = -1) and E->D->F->E (-3+6-5 = -2).")
    print("Every lap round either cycle lowers the cost, so distances can fall forever.")
    cd, cp, cpasses, ccyc = bellman_ford(VERTICES, cyc_edges, src)
    print(f"Bellman-Ford: passes = {cpasses}  ->  NEGATIVE CYCLE DETECTED: {' -> '.join(ccyc) if ccyc else None}")
    if ccyc:
        total = 0
        edge_w = {(u, v): w for u, v, w in cyc_edges}
        for a, b in zip(ccyc, ccyc[1:]):
            total += edge_w[(a, b)]
        print(f"Cycle weight re-computed independently = {total} (< 0)  -> shortest paths are UNDEFINED, "
              "no distances returned.")
    print("Detection mechanism: after |V|-1 passes every shortest path (at most |V|-1 edges) is final.")
    print("If the |V|-th pass can still relax an edge, some path uses >= |V| edges, i.e. repeats a vertex,")
    print("and only a negative cycle makes repetition profitable. Walking pred[] |V| times lands inside it.")
    print("\nFor comparison, the finalise-once Dijkstra silently returns numbers on this graph:")
    dd, _, _ = dijkstra(VERTICES, cyc_edges, src)
    print("   Dijkstra distances:", {k: fmt(v) for k, v in dd.items()}, " <-- misleading")
    print("\nBoundary tests for failure handling:")
    iso = VERTICES + ["X", "Y"]
    iso_edges = BASE_EDGES + [("X", "Y", -3), ("Y", "X", 1)]
    _, _, _, c1 = bellman_ford(iso, iso_edges, src)
    print(f"  negative cycle X<->Y NOT reachable from {src}: reported = {c1}   (correct: only reachable cycles matter)")
    _, _, _, c2 = bellman_ford(iso, iso_edges, "X")
    print(f"  same graph, source X                          : reported = {c2}")
    _, _, _, c3 = bellman_ford(["P"], [], "P")
    print(f"  single-vertex graph                           : reported = {c3}")
    _, _, _, c4 = bellman_ford(["P", "Q"], [("P", "P", -1)], "P")
    print(f"  negative self-loop P->P (-1)                  : reported = {c4}")

    print("\n" + "#" * 78)
    print("STAGE D  ALL-PAIRS COST (FLOYD) AND REACHABILITY (WARSHALL)")
    print("#" * 78)
    fd, nxt, neg = floyd(VERTICES, neg_edges)
    show_matrix(fd, "Floyd distance matrix (graph WITH the F->E negative edge)")
    print(f"Negative cycle (diagonal < 0)? {neg}")
    print("Sample reconstructed routes:")
    for a, b in [("A", "I"), ("A", "E"), ("C", "H"), ("F", "I"), ("I", "A")]:
        r = floyd_path(VERTICES, nxt, a, b)
        print(f"   {a} -> {b}: cost {fmt(fd[VERTICES.index(a)][VERTICES.index(b)])}  route {' -> '.join(r) if r else 'unreachable'}")
    print("Row A of Floyd equals Bellman-Ford distances from A:",
          all(fd[0][j] == bd[v] for j, v in enumerate(VERTICES)))
    reach = warshall(VERTICES, neg_edges)
    show_matrix(reach, "Warshall reachability matrix (1 = reachable)", cell=lambda x: "1" if x else "0")
    print("\nQuestions answered by the matrices:")
    for a, b in [("A", "I"), ("I", "A"), ("D", "C"), ("F", "G"), ("E", "F")]:
        print(f"   Can {a} reach {b}? {reach[VERTICES.index(a)][VERTICES.index(b)]}")
    fdc, _, negc = floyd(VERTICES, cyc_edges)
    print(f"\nFloyd on the negative-cycle graph: diagonal entries < 0 for {[v for i, v in enumerate(VERTICES) if fdc[i][i] < 0]}"
          f" -> negative cycle flagged = {negc}")
    reach_cyc = warshall(VERTICES, cyc_edges)
    new_pairs = [(a, b) for i, a in enumerate(VERTICES) for j, b in enumerate(VERTICES)
                 if reach_cyc[i][j] and not reach[i][j]]
    print("Warshall ignores weights, so it still works on the cyclic graph. Pairs that became reachable only")
    print("because of the new edge E->D:", new_pairs)


if __name__ == "__main__":
    main()
