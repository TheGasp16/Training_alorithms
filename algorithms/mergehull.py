"""Implementation diviser-pour-regner de Merge Hull (Preparata et Shamos)."""

from utils import area_signed
from algorithms.monotone import enveloppe_monotone


def merge_hull(points, seuil=64):
    """1/tri 2/division rec 3/stop monotone 4/fusion par union de coques."""
    pts = sorted({(p[0], p[1]) for p in points})
    if len(pts) <= seuil:
        # Cas de base: retour a l'algorithme monotone plus efficace sur petits ensembles.
        return enveloppe_monotone(pts)

    mid = len(pts) // 2
    left = merge_hull(pts[:mid])
    right = merge_hull(pts[mid:])
    return _fusion(left, right)


def _fusion(left, right):
    """Recalcule l'enveloppe monotone sur la reunion des sommets partiels."""
    merged = {tuple(p) for p in left + right}
    enveloppe = enveloppe_monotone(list(merged))
    if len(enveloppe) > 2 and area_signed(enveloppe) < 0:
        enveloppe.reverse()
    return enveloppe
