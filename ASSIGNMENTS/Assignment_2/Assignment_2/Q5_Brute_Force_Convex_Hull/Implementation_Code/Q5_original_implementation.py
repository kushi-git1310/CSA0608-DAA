def orientation(a, b, p):
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def brute_force_hull_edges(points):
    edges = set()
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            positive = negative = False
            a, b = points[i], points[j]
            for k, p in enumerate(points):
                if k == i or k == j:
                    continue
                cross = orientation(a, b, p)
                if cross > 0:
                    positive = True
                elif cross < 0:
                    negative = True
            if not (positive and negative):
                edges.add(tuple(sorted((a, b))))
    return edges


def convex_hull_vertices(points):
    # Monotonic-chain ordering of the vertices detected by the brute-force edge test.
    edges = brute_force_hull_edges(points)
    vertices = sorted({p for edge in edges for p in edge})
    if len(vertices) <= 1:
        return vertices

    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    lower = []
    for p in vertices:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(vertices):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    tests = {
        "boundary and interior": [(0, 0), (4, 0), (4, 4), (0, 4), (2, 2), (1, 2)],
        "challenging triangle/collinear": [(0, 0), (2, 0), (4, 0), (2, 3), (2, 1), (1, 1)],
    }
    for name, points in tests.items():
        print(f"\n{name}: points={points}")
        print("accepted candidate edges:", sorted(brute_force_hull_edges(points)))
        print("ordered hull vertices:", convex_hull_vertices(points))
