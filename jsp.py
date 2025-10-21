from collections import deque
import math as m
import random as rd
import time as t
import matplotlib.pyplot as plt
import statistics as stats


# -------------------------------
# Fonctions utilitaires
# -------------------------------
def cross(o, a, b):
    """Calcule le produit vectoriel oriente pour savoir si le virage est a gauche ou a droite."""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def area_signed(poly):
    """Retourne l'aire signee pour connaitre le sens de parcours (positive = antihoraire)."""
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % len(poly)]
        s += x1*y2 - x2*y1
    return 0.5 * s

def nuage(n, xmin=-10, xmax=10, ymin=-10, ymax=10):
    """Cree un nuage de points tires uniformement dans le rectangle fourni."""
    return [[rd.uniform(xmin, xmax), rd.uniform(ymin, ymax)] for _ in range(n)]

def benchmark(func, points, label=None):
    """Lance un algorithme sur un jeu de points et affiche un resume convivial."""
    start = t.time()
    hull = func(points)
    elapsed = (t.time() - start) * 1000
    nom = label or func.__name__.replace("_", " ").title()
    print(f"- {nom:<28} : {len(points):5d} points -> {len(hull):3d} sommets en {elapsed:7.2f} ms")
    return hull


# -------------------------------
# Algorithmes d’enveloppe convexe
# -------------------------------

def enveloppe_monotone(points):
    """Assemble l'enveloppe convexe en deux parcours monotones (methode Andrew)."""
    P = sorted(set(tuple(p) for p in points))
    if len(P) <= 1: return P

    lower = []
    for p in P:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(P):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    hull = lower[:-1] + upper[:-1]
    if area_signed(hull) < 0: hull.reverse()
    return hull


def enveloppe_quickhull(points):
    """Cherche les points extremes puis scinde recursivement pour reconstruire la coque."""
    def det(A, B, C): 
        return (A[0]-B[0])*(C[1]-B[1]) - (A[1]-B[1])*(C[0]-B[0])
    def farthest(A, B, pts):
        best, dmax = None, 0
        for p in pts:
            d = abs(det(A, B, p))
            if d > dmax: best, dmax = p, d
        return best
    def recurse(A, B, pts):
        pmax = farthest(A, B, pts)
        if not pmax: return []
        left1 = [p for p in pts if det(A, pmax, p) > 0]
        left2 = [p for p in pts if det(pmax, B, p) > 0]
        return recurse(A, pmax, left1) + [pmax] + recurse(pmax, B, left2)

    if len(points) < 3: return points
    A = min(points, key=lambda p: (p[0], p[1]))
    B = max(points, key=lambda p: (p[0], p[1]))
    left = [p for p in points if det(A, B, p) > 0]
    right = [p for p in points if det(A, B, p) < 0]
    hull = [A] + recurse(A, B, left) + [B] + recurse(B, A, right)

    # Tri final pour éviter les croisements
    cx, cy = sum(p[0] for p in hull)/len(hull), sum(p[1] for p in hull)/len(hull)
    hull = sorted(hull, key=lambda p: m.atan2(p[1]-cy, p[0]-cx))
    if area_signed(hull) < 0: hull.reverse()
    return hull


def enveloppe_graham(points):
    """Trie les points par angle autour d'un pivot puis empile seulement les virages a gauche."""
    P = sorted(points, key=lambda p: (p[1], p[0]))
    pivot = P[0]
    tri = sorted(P[1:], key=lambda p: m.atan2(p[1]-pivot[1], p[0]-pivot[0]))
    hull = [pivot, tri[0]]
    for p in tri[1:]:
        while len(hull) >= 2 and cross(hull[-2], hull[-1], p) <= 0:
            hull.pop()
        hull.append(p)
    return hull


# --- Merge Hull (Shamos) ---
# ---------- Divide & Conquer robuste ----------

def _to_unique_sorted(points):
    pts = sorted({(p[0], p[1]) for p in points})
    return [list(p) for p in pts]

def _ensure_ccw(hull):
    if len(hull) >= 3:
        s = 0.0
        for i in range(len(hull)):
            x1, y1 = hull[i]
            x2, y2 = hull[(i+1) % len(hull)]
            s += x1*y2 - x2*y1
        if s < 0:
            hull.reverse()
    return hull

def _rightmost_index(hull):
    xmax = max(hull, key=lambda p: (p[0], p[1]))[0]
    # en cas d’égalité sur x, on prend le plus haut y
    idx = max((i for i, p in enumerate(hull) if p[0] == xmax), key=lambda i: (hull[i][1], i))
    return idx

def _leftmost_index(hull):
    xmin = min(hull, key=lambda p: (p[0], p[1]))[0]
    idx = min((i for i, p in enumerate(hull) if p[0] == xmin), key=lambda i: (hull[i][1], i))
    return idx

def merge_hulls(left, right):
    # suppose left et right convexes CCW, sans répétition du premier point
    nL, nR = len(left), len(right)
    if nL == 0: return right[:]
    if nR == 0: return left[:]
    if nL == 1 and nR == 1:
        return [min(left[0], right[0]), max(left[0], right[0])] if left[0] != right[0] else [left[0]]

    i = _rightmost_index(left)
    j = _leftmost_index(right)

    # tangente supérieure
    max_iter = 2 * (nL + nR) + 10
    cnt = 0
    changed = True
    while changed and cnt < max_iter:
        changed = False; cnt += 1
        # avance i tant que (left[i]->right[j]->left[i+1]) fait un virage gauche
        while True:
            i_next = (i + 1) % nL
            if (left[i+1 if i+1 < nL else 0] == left[i]): break
            if ( (right[j][0]-left[i][0])*(left[i_next][1]-left[i][1]) - (right[j][1]-left[i][1])*(left[i_next][0]-left[i][0]) ) > 0:
                i = i_next; changed = True
            else:
                break
        # recule j tant que (right[j-1]->left[i]->right[j]) fait un virage droite (donc on monte)
        while True:
            j_prev = (j - 1) % nR
            if ( (left[i][0]-right[j][0])*(right[j_prev][1]-right[j][1]) - (left[i][1]-right[j][1])*(right[j_prev][0]-right[j][0]) ) < 0:
                j = j_prev; changed = True
            else:
                break
    upper_i, upper_j = i, j

    # tangente inférieure
    i = _rightmost_index(left)
    j = _leftmost_index(right)
    cnt = 0
    changed = True
    while changed and cnt < max_iter:
        changed = False; cnt += 1
        # recule i tant que (left[i-1]->right[j]->left[i]) fait un virage droite
        while True:
            i_prev = (i - 1) % nL
            if ( (right[j][0]-left[i][0])*(left[i_prev][1]-left[i][1]) - (right[j][1]-left[i][1])*(left[i_prev][0]-left[i][0]) ) < 0:
                i = i_prev; changed = True
            else:
                break
        # avance j tant que (right[j]->left[i]->right[j+1]) fait un virage gauche
        while True:
            j_next = (j + 1) % nR
            if ( (left[i][0]-right[j][0])*(right[j_next][1]-right[j][1]) - (left[i][1]-right[j][1])*(right[j_next][0]-right[j][0]) ) > 0:
                j = j_next; changed = True
            else:
                break
    lower_i, lower_j = i, j

    # construire la nouvelle enveloppe : left[upper_i -> lower_i] + right[lower_j -> upper_j]
    hull = []
    k = upper_i
    hull.append(left[k])
    while k != lower_i:
        k = (k + 1) % nL
        hull.append(left[k])

    k = lower_j
    hull.append(right[k])
    while k != upper_j:
        k = (k + 1) % nR
        hull.append(right[k])

    # éliminer d’éventuels doublons consécutifs
    clean = []
    for p in hull:
        if not clean or p != clean[-1]:
            clean.append(p)
    if len(clean) >= 2 and clean[0] == clean[-1]:
        clean.pop()

    return _ensure_ccw(clean)

def _divide_by_x(points):
    pts = _to_unique_sorted(points)
    if not pts: return [], []
    xs = [p[0] for p in pts]
    midx = (min(xs) + max(xs)) / 2.0
    left = [p for p in pts if p[0] <= midx]
    right = [p for p in pts if p[0] >  midx]
    if not right:  # tous égaux à midx
        mid = len(pts)//2
        left, right = pts[:mid], pts[mid:]
    return left, right

def merge_hull(points, threshold=64):
    """Divise les points en deux sous-ensembles puis fusionne leurs enveloppes."""
    pts = _to_unique_sorted(points)
    n = len(pts)
    if n <= threshold:
        return enveloppe_monotone(pts)
    left_pts, right_pts = _divide_by_x(pts)
    left_hull  = merge_hull(left_pts, threshold)
    right_hull = merge_hull(right_pts, threshold)
    return merge_hulls(left_hull, right_hull)

def preparata_hong(points):
    """Version pratique de Preparata-Hong basee sur le meme coeur divide and conquer."""
    # meme coeur que merge_hull ici (version pratique et sure)
    return merge_hull(points, threshold=64)



# -------------------------------
# Programme principal
# -------------------------------
if __name__ == "__main__":
    tailles = [100, 500, 1000, 2000, 5000, 10000]
    algos = [
        ("Monotone Chain", enveloppe_monotone),
        ("QuickHull", enveloppe_quickhull),
        ("Graham Scan", enveloppe_graham),
        ("Merge Hull", merge_hull),
        ("Preparata-Hong", preparata_hong)
    ]

    print("=== Tour d'horizon des enveloppes convexes ===")
    for n in tailles:
        print(f"\nNuage de {n} points aleatoires")
        E = nuage(n)
        for nom, f in algos:
            benchmark(f, E, label=nom)

    # Trace comparative : cinq sous-graphiques pour visualiser chaque algorithme
    E = nuage(1000)
    x, y = zip(*E)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    for idx, (nom, f) in enumerate(algos):
        ax = axes[idx]
        H = f(E)
        hx, hy = zip(*(H + [H[0]]))
        ax.scatter(x, y, s=8, alpha=0.3, color="gray")
        ax.plot(hx, hy, linewidth=2, label="Enveloppe")
        ax.set_title(nom)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle="--", alpha=0.5)
    # Désactive les axes inutilisés
    for ax in axes[len(algos):]:
        ax.axis("off")

    fig.suptitle("Comparaison visuelle des enveloppes convexes", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()




