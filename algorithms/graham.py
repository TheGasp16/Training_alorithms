import math as m
from utils import cross

def enveloppe_graham(points):
    """Algorithme de Graham Scan (1972)."""
    P = sorted(points, key=lambda p: (p[1], p[0]))
    pivot = P[0]
    sorted_pts = sorted(P[1:], key=lambda p: m.atan2(p[1]-pivot[1], p[0]-pivot[0]))

    hull = [pivot, sorted_pts[0]]
    for p in sorted_pts[1:]:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull
