"""Implementation de QuickHull, analogue geometrie du QuickSort."""

import math as m
from utils import cross, area_signed


def enveloppe_quickhull(points):
    """1/pivots extremes 2/separation 3/recherche point le plus lointain 4/fusion."""

    def det(A, B, C):
        return (A[0] - B[0]) * (C[1] - B[1]) - (A[1] - B[1]) * (C[0] - B[0])

    def farthest(A, B, pts):
        # Cherche le point qui maximise la distance orientee a la droite AB.
        best, dmax = None, 0
        for p in pts:
            d = abs(det(A, B, p))
            if d > dmax:
                best, dmax = p, d
        return best

    def recurse(A, B, pts):
        # Portionne recursivement le demi-plan (AB) par le point le plus lointain.
        pmax = farthest(A, B, pts)
        if not pmax:
            return []
        left1 = [p for p in pts if det(A, pmax, p) > 0]
        left2 = [p for p in pts if det(pmax, B, p) > 0]
        return recurse(A, pmax, left1) + [pmax] + recurse(pmax, B, left2)

    if len(points) < 3:
        return points

    # Points les plus a gauche et a droite: base du partitionnement.
    A = min(points, key=lambda p: (p[0], p[1]))
    B = max(points, key=lambda p: (p[0], p[1]))
    left = [p for p in points if det(A, B, p) > 0]
    right = [p for p in points if det(A, B, p) < 0]

    enveloppe = [A] + recurse(A, B, left) + [B] + recurse(B, A, right)

    # Tri final pour eviter les croisements lors de l'affichage.
    cx, cy = sum(p[0] for p in enveloppe) / len(enveloppe), sum(p[1] for p in enveloppe) / len(enveloppe)
    enveloppe = sorted(enveloppe, key=lambda p: m.atan2(p[1] - cy, p[0] - cx))
    if area_signed(enveloppe) < 0:
        enveloppe.reverse()
    return enveloppe
