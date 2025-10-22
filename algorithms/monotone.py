"""Implementation de l'algorithme Monotone Chain (Andrew, 1979)."""

from utils import cross, area_signed


def enveloppe_monotone(points):
    """Etapes: 1/tri unique 2/chaine basse 3/chaine haute 4/fusion."""
    P = sorted(set(tuple(p) for p in points))
    if len(P) <= 1:
        return P

    # Construction de la chaine inferieure (balaye gauche -> droite).
    lower = []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            # Supprime les virages a droite pour conserver la convexite.
            lower.pop()
        lower.append(p)

    # Construction de la chaine superieure (balaye droite -> gauche).
    upper = []
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    hull = lower[:-1] + upper[:-1]
    # Reoriente le polygone en sens anti-horaire si besoin.
    if area_signed(hull) < 0:
        hull.reverse()
    return hull
