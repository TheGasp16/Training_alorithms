"""Algorithme de Preparata-Hong avec fusion par tangentes."""

from math import fsum

from algorithms.monotone import enveloppe_monotone
from utils import area_signed

_EPS = 1e-12


def preparata_hong(points, seuil=32):
    """
    Calcule l'enveloppe convexe par l'algorithme Preparata-Hong.

    Complexite temporelle: T(n) = 2T(n/2) + O(n) => O(n log n) avec seuil constant.
    Complexite spatiale: O(n) pour stocker les sous-coques et pour la recursion.
    """
    pts = sorted({(float(p[0]), float(p[1])) for p in points})
    if len(pts) <= 1:
        return pts
    if len(pts) <= seuil:
        return enveloppe_monotone(pts)

    hull = _divide(pts, seuil)
    if len(hull) > 2 and area_signed(hull) < 0:
        # Assure une sortie en sens anti-horaire quel que soit le chemin recursif.
        hull.reverse()
    return hull


def _divide(pts, seuil):
    if len(pts) <= seuil:
        return enveloppe_monotone(pts)  # Cas de base: traitement lineaire par Monotone.

    mid = len(pts) // 2
    left = _divide(pts[:mid], seuil)
    right = _divide(pts[mid:], seuil)
    return _merge(left, right)  # Fusion des deux enveloppes partielles.


def _merge(left, right):
    """Fusionne deux enveloppes locales en une coque globale via tangentes communes."""
    if not left:
        return right[:]
    if not right:
        return left[:]
    if len(left) <= 2 or len(right) <= 2:
        return enveloppe_monotone(left + right)
    if abs(area_signed(left)) <= _EPS or abs(area_signed(right)) <= _EPS:
        return enveloppe_monotone(left + right)

    if len(left) > 2 and area_signed(left) < 0:
        # Garantit une orientation anti-horaire avant de chercher les tangentes.
        left = list(reversed(left))
    if len(right) > 2 and area_signed(right) < 0:
        right = list(reversed(right))

    ui, uj = _upper_tangent(left, right)
    li, lj = _lower_tangent(left, right)

    merged = []

    # Ajoute les sommets de la coque gauche entre les tangentes (sens direct CCW).
    idx = ui
    merged.append(left[idx])
    while idx != li:
        idx = (idx + 1) % len(left)
        merged.append(left[idx])

    # Ajoute la coque droite de la tangente basse vers la tangente haute.
    idx = lj
    if not merged or right[idx] != merged[-1]:
        merged.append(right[idx])
    while idx != uj:
        idx = (idx + 1) % len(right)
        if right[idx] != merged[-1]:
            merged.append(right[idx])

    if len(merged) > 2 and area_signed(merged) < 0:
        merged.reverse()
    return merged


def _orient(a, b, c):
    """Determinant signe de (a,b,c); >0 pour virage gauche, <0 pour virage droit."""
    ax = b[0] - a[0]
    ay = b[1] - a[1]
    bx = c[0] - a[0]
    by = c[1] - a[1]
    return fsum((ax * by, -ay * bx))


def _upper_tangent(left, right):
    """Calcule la tangente superieure commune aux deux polygones convexes."""
    return _tangent(left, right, upper=True)


def _lower_tangent(left, right):
    """Calcule la tangente inferieure commune aux deux polygones convexes."""
    return _tangent(left, right, upper=False)


def _tangent(left, right, upper):
    """Balaye circulairement chaque coque jusqu'a stabilisation des tangentes."""
    i = _rightmost_index(left)
    j = _leftmost_index(right)
    n = len(left)
    m = len(right)

    step_left = 1 if upper else -1
    step_right = -1 if upper else 1
    target_left = -1 if upper else 1
    target_right = 1 if upper else -1

    while True:
        settled = True  # Retient si un ajustement reste necessaire sur l'une des coques.
        while True:
            nxt = (i + step_left) % n
            # Si l'orientation indique que gauche[nxt] est encore "hors" de la tangente,
            # on deplace i pour le reintegrer dans la chaine finale.
            if _orient_sign(right[j], left[i], left[nxt]) == target_left:
                i = nxt
            else:
                break
        while True:
            nxt = (j + step_right) % m
            # Meme idee cote droit: tant que droite[nxt] reste du mauvais cote,
            # on fait tourner j pour tendre la tangente.
            if _orient_sign(left[i], right[j], right[nxt]) == target_right:
                j = nxt
                settled = False
            else:
                break
        if settled:
            break
    return i, j


def _orient_sign(a, b, c):
    """Renvoie -1, 0 ou 1 selon l'orientation avec tolerance numerique."""
    val = _orient(a, b, c)
    if abs(val) <= _EPS:
        return 0
    return 1 if val > 0 else -1


def _rightmost_index(hull):
    """Renvoie l'indice du point le plus a droite (x max, puis y max)."""
    return max(range(len(hull)), key=lambda k: (hull[k][0], hull[k][1]))


def _leftmost_index(hull):
    """Renvoie l'indice du point le plus a gauche (x min, puis y min)."""
    return min(range(len(hull)), key=lambda k: (hull[k][0], hull[k][1]))
