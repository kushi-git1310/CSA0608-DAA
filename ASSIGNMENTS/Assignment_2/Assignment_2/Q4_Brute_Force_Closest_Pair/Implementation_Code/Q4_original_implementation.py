from math import sqrt
from time import perf_counter


def closest_pair(points):
    if len(points) < 2:
        return None, None, 0, 0.0
    best_pair = None
    best_d2 = float("inf")
    pairs_examined = 0
    distance_calculations = 0
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            pairs_examined += 1
            dx = points[i][0] - points[j][0]
            dy = points[i][1] - points[j][1]
            d2 = dx * dx + dy * dy
            distance_calculations += 1
            if d2 < best_d2:
                best_d2 = d2
                best_pair = (points[i], points[j])
    return best_pair, sqrt(best_d2), pairs_examined, distance_calculations


if __name__ == "__main__":
    for n in (10, 100, 500):
        points = [(i * 7 % 101, i * 13 % 97) for i in range(n)]
        start = perf_counter()
        pair, distance, pairs, calculations = closest_pair(points)
        elapsed = perf_counter() - start
        print(f"n={n}: expected pairs={n*(n-1)//2}, examined={pairs}, "
              f"distance calculations={calculations}, time={elapsed:.6f}s")
        print(f"closest pair={pair}, distance={distance:.4f}")
