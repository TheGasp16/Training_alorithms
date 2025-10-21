from utils import cross, area_signed

def enveloppe_monotone(points):
    """Algorithme Monotone Chain (Andrew, 1979)."""
    P = sorted(set(tuple(p) for p in points))
    if len(P) <= 1:
        return P

    # Chaîne inférieure
    lower = []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Chaîne supérieure
    upper = []
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    hull = lower[:-1] + upper[:-1]
    if area_signed(hull) < 0:
        hull.reverse()
    return hull