"""Task 5 - Dijkstra (greedy), Bellman-Ford (repeated relaxation), Floyd-Warshall (all pairs).
Author: S KUSHA LAKSHMI | Reg No: 192571074 | Course: CSA0608"""
INF = float("inf")
V = ["A", "B", "C", "D", "E"]
E = [("A", "B", 4), ("A", "C", 7), ("B", "C", 2), ("B", "D", 6), ("C", "D", 1), ("D", "E", 3), ("C", "E", 8)]


def dijkstra(vertices, edges, src, verbose=True):
    dist = {v: INF for v in vertices}; pred = {v: None for v in vertices}
    done = set(); dist[src] = 0
    while len(done) < len(vertices):
        cand = [v for v in vertices if v not in done and dist[v] < INF]
        if not cand: break
        u = min(cand, key=lambda v: dist[v])          # greedy choice: smallest tentative distance
        done.add(u)
        if verbose: print(f"SELECT {u} (dist={dist[u]}) | finalised={sorted(done)}")
        for a, b, w in edges:
            if a == u and b not in done and dist[u] + w < dist[b]:
                if verbose: print(f"   relax {a}->{b}: {dist[u]}+{w}={dist[u]+w} < {dist[b]} => update, pred[{b}]={a}")
                dist[b] = dist[u] + w; pred[b] = a
            elif a == u and verbose:
                print(f"   relax {a}->{b}: {dist[u]}+{w}={dist[u]+w} not better than {dist[b]}")
    return dist, pred


def path(pred, t):
    p = []
    while t is not None: p.append(t); t = pred[t]
    return "->".join(reversed(p))


def bellman_ford(vertices, edges, src, verbose=True):
    dist = {v: INF for v in vertices}; pred = {v: None for v in vertices}; dist[src] = 0
    for k in range(1, len(vertices)):
        changed = False
        for a, b, w in edges:
            if dist[a] < INF and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w; pred[b] = a; changed = True
        if verbose: print(f"pass {k}: {dist}")
        if not changed: break
    neg = any(dist[a] < INF and dist[a] + w < dist[b] for a, b, w in edges)
    return dist, pred, neg


def floyd(vertices, edges, verbose=True):
    n = len(vertices); idx = {v: i for i, v in enumerate(vertices)}
    D = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, w in edges: D[idx[a]][idx[b]] = min(D[idx[a]][idx[b]], w)
    def show(M, title):
        print(title); print("     " + "".join(f"{v:>5}" for v in vertices))
        for i in range(n): print(f"  {vertices[i]}: " + "".join(f"{('INF' if x == INF else x):>5}" for x in M[i]))
    if verbose: show(D, "D(0) (direct edges only)")
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]: D[i][j] = D[i][k] + D[k][j]
        if verbose: show(D, f"D({k+1}) (intermediates allowed: {vertices[:k+1]})")
    return D


if __name__ == "__main__":
    print("===== 5.1 DIJKSTRA from A =====")
    d, p = dijkstra(V, E, "A")
    for v in V: print(f"dist[{v}]={d[v]}  path={path(p, v)}")
    print("\n===== 5.2 BELLMAN-FORD from A (same graph) =====")
    d2, p2, neg = bellman_ford(V, E, "A")
    print("Final:", d2, "| negative cycle reachable:", neg)
    print("\n--- Dijkstra FAILS with a negative edge: A->B 2, A->C 3, C->B -2 ---")
    V2 = ["A", "B", "C"]; E2 = [("A", "B", 2), ("A", "C", 3), ("C", "B", -2)]
    print("Dijkstra :", dijkstra(V2, E2, "A", False)[0])
    print("BellmanFd:", bellman_ford(V2, E2, "A", False)[0], " (true dist[B] = 1)")
    print("\n--- Negative cycle: A->B 1, B->C -3, C->B 1 ---")
    V3 = ["A", "B", "C"]; E3 = [("A", "B", 1), ("B", "C", -3), ("C", "B", 1)]
    r = bellman_ford(V3, E3, "A", True)
    print("negative cycle detected:", r[2])
    print("\n===== 5.3 FLOYD-WARSHALL all pairs =====")
    D = floyd(V, E)
    print("\nCross-check with Dijkstra from every source:")
    ok = True
    for i, s in enumerate(V):
        ds, _ = dijkstra(V, E, s, False)
        for j, t in enumerate(V):
            if ds[t] != D[i][j]: ok = False
    print("Floyd == repeated Dijkstra:", ok)
