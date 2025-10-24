"""Implementation de Graham Scan pour l'enveloppe convexe plane."""

import math as m
from utils import cross


def enveloppe_graham(points):
    """1/trouver pivot 2/trier par angle 3/empiler en supprimant les retours."""
    P = sorted(points, key=lambda p: (p[1], p[0]))
    pivot = P[0]
    # Trie les points restants par angle polaire autour du pivot choisi.
    sorted_pts = sorted(P[1:], key=lambda p: m.atan2(p[1] - pivot[1], p[0] - pivot[0]))

    enveloppe = [pivot, sorted_pts[0]]
    for p in sorted_pts[1:]:
        # Tant que l'on forme un virage a droite, on depile le sommet courant.
        while len(enveloppe) >= 2 and cross(enveloppe[-2], enveloppe[-1], p) <= 0:
            enveloppe.pop()
        enveloppe.append(p)
    return enveloppe
