"""
CSA0608 - Design and Analysis of Algorithms | Assignment 4B
Student : S KUSHA LAKSHMI   Reg.No : 192571074

TASK 5 - THREE GREEDY ENGINEERS, ONE NETWORK : Kruskal + Prim + Boruvka

Common idea (cut property): for any cut of the vertices, the lightest edge crossing the cut is safe
(belongs to some MST).  The three algorithms only differ in WHICH cut they look at.
  Kruskal : the cut between the two components joined by the globally lightest remaining edge
  Prim    : the cut (tree so far, rest of the graph)
  Boruvka : for EVERY component simultaneously, the cut (component, rest)
"""
import heapq
import random
from functools import cmp_to_key
from itertools import combinations

NAMES = "ABCDEFGHI"
N = 9
# (u, v, weight) - undirected; weights all distinct
EDGES = [(0, 1, 4), (0, 2, 9), (1, 2, 7), (1, 3, 12), (2, 3, 5), (2, 4, 14), (3, 4, 2),
         (3, 5, 8), (4, 6, 6), (5, 6, 3), (5, 7, 11), (6, 7, 10), (6, 8, 13), (7, 8, 1)]
# modified graph with ties: A-C 9->7 (ties with B-C 7), F-H 11->10 (ties with G-H 10)
TIE_EDGES = [(0, 1, 4), (0, 2, 7), (1, 2, 7), (1, 3, 12), (2, 3, 5), (2, 4, 14), (3, 4, 2),
             (3, 5, 8), (4, 6, 6), (5, 6, 3), (5, 7, 10), (6, 7, 10), (6, 8, 13), (7, 8, 1)]


def vname(i):
    return NAMES[i] if i < len(NAMES) else str(i)


def lab(e):
    return f"{vname(e[0])}-{vname(e[1])}({e[2]})"


class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.find_calls = 0

    def find(self, x):
        self.find_calls += 1
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]       # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def check_connected(n, edges):
    ds = DisjointSet(n)
    for u, v, _ in edges:
        ds.union(u, v)
    return len({ds.find(i) for i in range(n)}) == 1


# --------------------------------------------------------------------------- #
def kruskal(n, edges, tie_order=None, trace=None, stats=None):
    """tie_order: list of edge indices giving the priority among equal weights (default: input order)."""
    if not check_connected(n, edges):
        raise ValueError("graph is not connected - no spanning tree exists")
    stats = stats if stats is not None else {}
    stats["comparisons"] = 0
    order = tie_order or list(range(len(edges)))
    rank = {idx: pos for pos, idx in enumerate(order)}

    def cmp(i, j):
        stats["comparisons"] += 1
        a, b = (edges[i][2], rank[i]), (edges[j][2], rank[j])
        return (a > b) - (a < b)

    sorted_idx = sorted(range(len(edges)), key=cmp_to_key(cmp))
    ds, mst, total = DisjointSet(n), [], 0
    for idx in sorted_idx:
        u, v, w = edges[idx]
        ru, rv = ds.find(u), ds.find(v)
        if ru != rv:
            ds.union(u, v)
            mst.append(edges[idx])
            total += w
            if trace is not None:
                trace.append(f"  ACCEPT {lab(edges[idx]):<9} joins components rooted {NAMES[ru]} and {NAMES[rv]}  (edges so far {len(mst)})")
        elif trace is not None:
            trace.append(f"  reject {lab(edges[idx]):<9} both ends already in the same component (would form a cycle)")
        if len(mst) == n - 1:
            break
    stats["find_calls"] = ds.find_calls
    return mst, total


def prim(n, edges, start=0, trace=None, stats=None):
    if not check_connected(n, edges):
        raise ValueError("graph is not connected - no spanning tree exists")
    stats = stats if stats is not None else {}
    stats.update(pushes=0, pops=0)
    adj = [[] for _ in range(n)]
    for k, (u, v, w) in enumerate(edges):
        adj[u].append((w, k, v))
        adj[v].append((w, k, u))
    in_tree = [False] * n
    heap, mst, total = [], [], 0
    in_tree[start] = True
    for item in adj[start]:
        heapq.heappush(heap, (item[0], item[1], start, item[2]))
        stats["pushes"] += 1
    if trace is not None:
        trace.append(f"  start at {NAMES[start]}; tree = {{{NAMES[start]}}}")
    while heap and len(mst) < n - 1:
        w, k, u, v = heapq.heappop(heap)
        stats["pops"] += 1
        if in_tree[v]:
            continue                                     # stale: both ends already in tree
        in_tree[v] = True
        mst.append(edges[k])
        total += w
        if trace is not None:
            tree = ",".join(NAMES[i] for i in range(n) if in_tree[i])
            trace.append(f"  ADD {lab(edges[k]):<9} (cheapest edge leaving tree) -> tree = {{{tree}}}")
        for item in adj[v]:
            if not in_tree[item[2]]:
                heapq.heappush(heap, (item[0], item[1], v, item[2]))
                stats["pushes"] += 1
    return mst, total


def prim_dense(n, edges, start=0, stats=None):
    """Array version, O(V^2): no heap, ideal for dense graphs."""
    stats = stats if stats is not None else {}
    stats["key_scans"] = 0
    INF = float("inf")
    mat = [[None] * n for _ in range(n)]
    for k, (u, v, w) in enumerate(edges):
        mat[u][v] = mat[v][u] = (w, k)
    key, via = [INF] * n, [None] * n
    done = [False] * n
    key[start] = 0
    mst, total = [], 0
    for _ in range(n):
        u, best = -1, INF
        for v in range(n):
            stats["key_scans"] += 1
            if not done[v] and key[v] < best:
                u, best = v, key[v]
        done[u] = True
        if via[u] is not None:
            mst.append(edges[via[u]])
            total += best
        for v in range(n):
            stats["key_scans"] += 1
            if mat[u][v] and not done[v] and mat[u][v][0] < key[v]:
                key[v], via[v] = mat[u][v][0], mat[u][v][1]
    return mst, total


def boruvka(n, edges, tie_reverse=False, trace=None, stats=None, tie_break=True):
    """Each round: every component picks its cheapest outgoing edge, all picks are merged together.
    tie_break=False reproduces the classic bug (equal weights may select a CYCLE)."""
    if not check_connected(n, edges):
        raise ValueError("graph is not connected - no spanning tree exists")
    stats = stats if stats is not None else {}
    stats.update(rounds=0, edge_scans=0, per_round_components=[])
    ds, mst, total = DisjointSet(n), [], 0
    comps = n
    sign = -1 if tie_reverse else 1
    while comps > 1:
        stats["rounds"] += 1
        stats["per_round_components"].append(comps)
        cheapest = {}
        for k, (u, v, w) in enumerate(edges):
            stats["edge_scans"] += 1
            ru, rv = ds.find(u), ds.find(v)
            if ru == rv:
                continue
            key = (w, sign * k) if tie_break else (w, 0)
            for r in (ru, rv):
                if r not in cheapest or key < cheapest[r][0]:
                    cheapest[r] = (key, k)
        chosen = sorted({k for _, k in cheapest.values()})
        if trace is not None:
            trace.append(f" Round {stats['rounds']}: {comps} components")
            for r in sorted(cheapest):
                trace.append(f"    component {NAMES[r]}* picks {lab(edges[cheapest[r][1]])}")
        added_now = []
        for k in chosen:
            u, v, w = edges[k]
            if ds.union(u, v):
                mst.append(edges[k])
                total += w
                comps -= 1
                if trace is not None:
                    added_now.append(lab(edges[k]))
            elif trace is not None:
                trace.append(f"    (skip {lab(edges[k])}: duplicate pick / cycle guard)")
        if trace is not None:
            trace.append(f"    merged: {added_now}  -> {comps} components left")
    return mst, total


def boruvka_naive_picks_form_cycle(n, edges):
    """Bug demonstration: ONE round of Boruvka where each vertex breaks weight ties with its OWN local rule
    (here: prefer the neighbour that comes next in cyclic order, as an adjacency-list order might).
    Without one GLOBAL tie order the chosen edges can form a cycle."""
    picks = {}
    for vtx in range(n):
        inc = [((edges[k][2], (edges[k][0] + edges[k][1] - vtx - vtx) % n), k)
               for k in range(len(edges)) if vtx in edges[k][:2]]
        picks[vtx] = min(inc)[1]
    chosen = set(picks.values())
    ds, cycle = DisjointSet(n), False
    for k in sorted(chosen):
        if not ds.union(edges[k][0], edges[k][1]):
            cycle = True
    return [edges[k] for k in sorted(chosen)], cycle


def edge_key(mst):
    return tuple(sorted(lab(e) for e in mst))


def all_msts(n, edges):
    """Brute force: enumerate every (n-1)-edge subset that is a spanning tree and has minimum cost."""
    best, found = float("inf"), []
    for combo in combinations(range(len(edges)), n - 1):
        ds, ok, cost = DisjointSet(n), True, 0
        for k in combo:
            u, v, w = edges[k]
            if not ds.union(u, v):
                ok = False
                break
            cost += w
        if ok:
            if cost < best:
                best, found = cost, [combo]
            elif cost == best:
                found.append(combo)
    return best, found


def random_graph(rng, n, m):
    """Connected random graph with distinct weights."""
    weights = rng.sample(range(1, 10 * m), m)
    edges, seen = [], set()
    for v in range(1, n):                              # random spanning tree guarantees connectivity
        u = rng.randrange(v)
        seen.add((u, v))
        edges.append((u, v, weights[len(edges)]))
    while len(edges) < m:
        u, v = rng.sample(range(n), 2)
        a, b = min(u, v), max(u, v)
        if (a, b) not in seen:
            seen.add((a, b))
            edges.append((a, b, weights[len(edges)]))
    return edges


def main():
    print("#" * 78)
    print("TASK 5  SAME GRAPH, THREE ALGORITHMS")
    print("#" * 78)
    print(f"Graph: {N} facilities A..I, {len(EDGES)} links:  " + ", ".join(lab(e) for e in EDGES))

    tk, tp, tb = [], [], []
    sk, sp, sb = {}, {}, {}
    mk, ck = kruskal(N, EDGES, trace=tk, stats=sk)
    mp, cp = prim(N, EDGES, 0, trace=tp, stats=sp)
    mb, cb = boruvka(N, EDGES, trace=tb, stats=sb)

    print("\n--- KRUSKAL (global edge list sorted by weight, union-find) ---")
    print("Next safe edge : lightest edge that joins two DIFFERENT components")
    print("State kept     : sorted edge list + disjoint-set (component id of every vertex)")
    print("Growth         : a forest of many fragments that coalesce")
    print("\n".join(tk))
    print(f"  MST = {[lab(e) for e in mk]}   total = {ck}   stats = {sk}")

    print("\n--- PRIM from A (one growing tree, priority queue) ---")
    print("Next safe edge : lightest edge with exactly one end inside the tree")
    print("State kept     : in-tree flags + priority queue of frontier edges")
    print("Growth         : ONE tree absorbs one vertex per step")
    print("\n".join(tp))
    print(f"  MST = {[lab(e) for e in mp]}   total = {cp}   stats = {sp}")

    print("\n--- BORUVKA (all components pick simultaneously) ---")
    print("Next safe edge : for every component, its lightest outgoing edge (ties broken by edge index)")
    print("State kept     : component id of every vertex + cheapest-edge slot per component")
    print("Growth         : number of components at least halves each round")
    print("\n".join(tb))
    print(f"  MST = {[lab(e) for e in mb]}   total = {cb}   stats = {sb}")

    print("\nFINAL COMPARISON")
    print(f"{'Algorithm':<10}{'Total':>7}  Edge set (sorted)")
    for nm, m, c in (("Kruskal", mk, ck), ("Prim", mp, cp), ("Boruvka", mb, cb)):
        print(f"{nm:<10}{c:>7}  {sorted(lab(e) for e in m)}")
    same = edge_key(mk) == edge_key(mp) == edge_key(mb)
    print(f"Identical edge sets: {same}   (distinct weights -> the MST is UNIQUE)")
    best, trees = all_msts(N, EDGES)
    print(f"Brute force over C({len(EDGES)},{N - 1}) = {len(list(combinations(range(len(EDGES)), N - 1)))} subsets: "
          f"minimum cost = {best}, number of MSTs = {len(trees)}")

    # ---------------- stress: ties -----------------
    print("\n" + "#" * 78)
    print("STRESS THE DESIGN - TIES (A-C changed 9->7, F-H changed 11->10)")
    print("#" * 78)
    print("Modified graph:", ", ".join(lab(e) for e in TIE_EDGES))
    best2, trees2 = all_msts(N, TIE_EDGES)
    print(f"Brute force: minimum cost = {best2}; number of distinct minimum spanning trees = {len(trees2)}")
    for t in trees2:
        print("   MST:", sorted(lab(TIE_EDGES[k]) for k in t))
    results = {}
    runs = [("Kruskal, input tie order", lambda: kruskal(N, TIE_EDGES)),
            ("Kruskal, reversed tie order", lambda: kruskal(N, TIE_EDGES, tie_order=list(range(len(TIE_EDGES)))[::-1])),
            ("Prim from A", lambda: prim(N, TIE_EDGES, 0)),
            ("Prim from I", lambda: prim(N, TIE_EDGES, 8)),
            ("Boruvka, low-index ties", lambda: boruvka(N, TIE_EDGES)),
            ("Boruvka, high-index ties", lambda: boruvka(N, TIE_EDGES, tie_reverse=True))]
    print(f"\n{'Run':<30}{'Total':>6}  {'Uses':<12}  Different tie-edges")
    for name, fn in runs:
        m, c = fn()
        keys = {lab(e) for e in m}
        which = [x for x in ("A-C(7)", "B-C(7)") if x in keys] + [x for x in ("F-H(10)", "G-H(10)") if x in keys]
        results[name] = (edge_key(m), c)
        print(f"{name:<30}{c:>6}  {'valid MST' if c == best2 else 'NOT optimal':<12}  {which}")
    distinct = {v[0] for v in results.values()}
    print(f"\nDistinct edge sets returned = {len(distinct)}; distinct totals = {sorted({v[1] for v in results.values()})}")
    print("=> different edge sets, same cost, ALL correct (each equals one of the brute-force MSTs):",
          all(any(sorted(lab(TIE_EDGES[k]) for k in t) == list(r[0]) for t in trees2) for r in results.values()))

    print("\nBoruvka tie-breaking defect demonstration (triangle A-B-C, all weights 1):")
    tri = [(0, 1, 1), (1, 2, 1), (2, 0, 1)]
    picks, cyc = boruvka_naive_picks_form_cycle(3, tri)
    print("   naive picks (no global tie order):", [f"{vname(u)}-{vname(v)}" for u, v, _ in picks], "-> forms a cycle:", cyc)
    m, c = boruvka(3, tri)
    print("   with (weight, edge-index) tie-break:", [f"{vname(u)}-{vname(v)}" for u, v, _ in m], "total", c, "-> tree, 2 edges")

    # ---------------- boundary tests -----------------
    print("\nBoundary / failure tests:")
    print("   disconnected graph ->", end=" ")
    try:
        kruskal(4, [(0, 1, 1), (2, 3, 1)])
    except ValueError as e:
        print("rejected:", e)
    print("   single vertex      ->", kruskal(1, [])[1], prim(1, [])[1], boruvka(1, [])[1])
    print("   two vertices       ->", kruskal(2, [(0, 1, 5)])[1], prim(2, [(0, 1, 5)])[1], boruvka(2, [(0, 1, 5)])[1])
    rng = random.Random(5)
    bad = 0
    for _ in range(300):
        n = rng.randint(2, 9)
        m = rng.randint(n - 1, min(n * (n - 1) // 2, 14))
        g = random_graph(rng, n, m)
        costs = {kruskal(n, g)[1], prim(n, g)[1], boruvka(n, g)[1]}
        bad += len(costs) != 1
    print(f"   300 random graphs: Kruskal = Prim = Boruvka total cost; disagreements = {bad}")

    # ---------------- deployment evidence -----------------
    print("\n" + "#" * 78)
    print("INDUSTRY DECISION - measured work on three environments")
    print("#" * 78)
    rng = random.Random(2026)
    envs = [("A  sparse  (V=2000, E=3000)", 2000, 3000),
            ("B  dense   (V=150,  E=10000)", 150, 10000),
            ("C  large   (V=20000,E=60000)", 20000, 60000)]
    print(f"{'Environment':<30}{'Kruskal cmp':>12}{'finds':>9} | {'Prim pushes':>12}{'pops':>8}{'array scans':>12} | "
          f"{'Boruvka rounds':>15}{'edge scans':>11}")
    for name, n, m in envs:
        g = random_graph(rng, n, m)
        s1, s2, s3, s4 = {}, {}, {}, {}
        _, c1 = kruskal(n, g, stats=s1)
        _, c2 = prim(n, g, 0, stats=s2)
        _, c3 = boruvka(n, g, stats=s3)
        scans = "-"
        if n <= 150:
            _, c4 = prim_dense(n, g, 0, stats=s4)
            scans = s4["key_scans"]
            assert c4 == c1
        assert c1 == c2 == c3
        print(f"{name:<30}{s1['comparisons']:>12}{s1['find_calls']:>9} | {s2['pushes']:>12}{s2['pops']:>8}{str(scans):>12} | "
              f"{s3['rounds']:>15}{s3['edge_scans']:>11}")
        if n == 20000:
            print(f"   Boruvka components per round: {s3['per_round_components']}")


if __name__ == "__main__":
    main()
