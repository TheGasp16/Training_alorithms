from utils import cross
from algorithms.monotone import enveloppe_monotone

def merge_hull(points, seuil=64):
    """Algorithme Merge Hull (Divide & Conquer)."""
    pts = sorted({(p[0], p[1]) for p in points})
    if len(pts) <= seuil:
        return enveloppe_monotone(pts)

    mid = len(pts)//2
    left = merge_hull(pts[:mid])
    right = merge_hull(pts[mid:])
    return _fusion(left, right)

def _fusion(left, right):
    """Fusionne deux enveloppes convexes via tangentes."""
    def next_idx(i, n): return (i + 1) % n
    def prev_idx(i, n): return (i - 1) % n
    nL, nR = len(left), len(right)
    iL, iR = nL - 1, 0

    # Tangente supérieure
    changed = True
    while changed:
        changed = False
        while cross(right[iR], left[iL], left[prev_idx(iL, nL)]) > 0:
            iL = prev_idx(iL, nL); changed = True
        while cross(left[iL], right[iR], right[next_idx(iR, nR)]) < 0:
            iR = next_idx(iR, nR); changed = True
    topL, topR = iL, iR

    # Tangente inférieure
    iL, iR = nL - 1, 0
    changed = True
    while changed:
        changed = False
        while cross(right[iR], left[iL], left[next_idx(iL, nL)]) < 0:
            iL = next_idx(iL, nL); changed = True
        while cross(left[iL], right[iR], right[prev_idx(iR, nR)]) > 0:
            iR = prev_idx(iR, nR); changed = True
    botL, botR = iL, iR

    hull = []
    i = topL
    while i != botL:
        hull.append(left[i])
        i = next_idx(i, nL)
    hull.append(left[botL])

    i = botR
    while i != topR:
        hull.append(right[i])
        i = next_idx(i, nR)
    hull.append(right[topR])
    return hull
