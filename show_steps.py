"""Visualisation iterative des etapes des enveloppes convexes."""

import math
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt

from algorithms import enveloppe_monotone, enveloppe_quickhull
from utils import area_signed, cross, nuage

Point = Tuple[float, float]
Step = dict

STEPS_DIR = Path("plots") / "steps"
STEPS_DIR.mkdir(parents=True, exist_ok=True)


def _unique(points: Sequence[Sequence[float]]) -> List[Point]:
    """Convertit en tuples dedoupes pour faciliter les copies."""
    return sorted({(float(p[0]), float(p[1])) for p in points})


def _close_coords(poly: Sequence[Point], close: bool) -> Tuple[List[float], List[float]]:
    """Retourne les coordonnees x/y (ferme la chaine si demande)."""
    if not poly:
        return [], []
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    if close and len(poly) >= 2:
        xs.append(poly[0][0])
        ys.append(poly[0][1])
    return xs, ys


def _partial_monotone(lower: Sequence[Point], upper: Sequence[Point]) -> List[Point]:
    """Assemble les chaines courantes de l'algorithme monotone."""
    chain = list(lower)
    if upper:
        rev = list(reversed(upper))
        if chain:
            chain += rev[:-1]  # Ajoute la chaine haute sans repeter l'extremite droite.
        else:
            chain = rev
    return chain


def monotone_steps(points: Sequence[Sequence[float]]) -> Iterator[Step]:
    pts = _unique(points)
    if len(pts) <= 1:
        yield {"hull": pts, "active": None, "label": "Cas trivial", "close": False}
        return

    lower: List[Point] = []
    upper: List[Point] = []
    yield {"hull": [], "active": None, "label": "Tri des points", "close": False}

    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            removed = lower.pop()
            yield {
                "hull": _partial_monotone(lower, upper),
                "active": removed,
                "label": f"Lower pop {removed}",
                "close": False,
            }
        lower.append(p)
        yield {
            "hull": _partial_monotone(lower, upper),
            "active": p,
            "label": f"Lower push {p}",
            "close": False,
        }

    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            removed = upper.pop()
            yield {
                "hull": _partial_monotone(lower, upper),
                "active": removed,
                "label": f"Upper pop {removed}",
                "close": True,
            }
        upper.append(p)
        yield {
            "hull": _partial_monotone(lower, upper),
            "active": p,
            "label": f"Upper push {p}",
            "close": True,
        }

    hull = lower[:-1] + upper[:-1]
    if area_signed(hull) < 0:
        hull.reverse()
    yield {"hull": hull, "active": None, "label": "Enveloppe complete", "close": True}


def graham_steps(points: Sequence[Sequence[float]]) -> Iterator[Step]:
    pts = _unique(points)
    if len(pts) <= 2:
        yield {"hull": pts, "active": None, "label": "Moins de 3 points", "close": False}
        return

    pivot = min(pts, key=lambda p: (p[1], p[0]))
    sorted_pts = sorted(
        [p for p in pts if p != pivot],
        key=lambda p: math.atan2(p[1] - pivot[1], p[0] - pivot[0]),
    )
    if not sorted_pts:
        yield {"hull": [pivot], "active": None, "label": "Points colineaires", "close": False}
        return

    stack: List[Point] = [pivot, sorted_pts[0]]
    yield {"hull": stack.copy(), "active": sorted_pts[0], "label": "Initialisation", "close": False}

    for p in sorted_pts[1:]:
        while len(stack) >= 2 and cross(stack[-2], stack[-1], p) <= 0:
            removed = stack.pop()
            yield {
                "hull": stack.copy(),
                "active": removed,
                "label": f"Pop {removed}",
                "close": False,
            }
        stack.append(p)
        yield {
            "hull": stack.copy(),
            "active": p,
            "label": f"Push {p}",
            "close": False,
        }

    hull = stack.copy()
    yield {"hull": hull, "active": None, "label": "Enveloppe complete", "close": True}


def quickhull_steps(points: Sequence[Sequence[float]]) -> Iterator[Step]:
    pts = _unique(points)
    if len(pts) <= 2:
        yield {"hull": pts, "active": None, "label": "Moins de 3 points", "close": False}
        return

    def det(A: Point, B: Point, C: Point) -> float:
        return (A[0] - B[0]) * (C[1] - B[1]) - (A[1] - B[1]) * (C[0] - B[0])

    def farthest(A: Point, B: Point, subset: Iterable[Point]) -> Optional[Point]:
        best, dmax = None, 0.0
        for p in subset:
            d = abs(det(A, B, p))
            if d > dmax:
                best, dmax = p, d
        return best

    A = min(pts, key=lambda p: (p[0], p[1]))
    B = max(pts, key=lambda p: (p[0], p[1]))
    selected = {A, B}
    yield {
        "hull": list(selected),
        "active": None,
        "label": f"Points extremes {A} et {B}",
        "close": False,
    }

    def recurse(P: Point, Q: Point, subset: List[Point]) -> Iterator[Step]:
        if not subset:
            yield {
                "hull": enveloppe_monotone(list(selected)),
                "active": None,
                "label": f"Aucun point a gauche de {P}->{Q}",
                "close": True,
            }
            return
        pmax = farthest(P, Q, subset)
        if pmax is None:
            yield {
                "hull": enveloppe_monotone(list(selected)),
                "active": None,
                "label": f"Aucun point a gauche de {P}->{Q}",
                "close": True,
            }
            return
        selected.add(pmax)
        yield {
            "hull": enveloppe_monotone(list(selected)),
            "active": pmax,
            "label": f"Point le plus eloigne {pmax}",
            "close": True,
        }
        left1 = [p for p in subset if det(P, pmax, p) > 0]
        left2 = [p for p in subset if det(pmax, Q, p) > 0]
        yield from recurse(P, pmax, left1)
        yield from recurse(pmax, Q, left2)

    left = [p for p in pts if det(A, B, p) > 0]
    right = [p for p in pts if det(A, B, p) < 0]
    yield from recurse(A, B, left)
    yield from recurse(B, A, right)

    hull = enveloppe_quickhull(pts)
    yield {"hull": hull, "active": None, "label": "Enveloppe complete", "close": True}


def merge_steps(points: Sequence[Sequence[float]], seuil: int) -> Iterator[Step]:
    pts = _unique(points)

    def recurse(subset: List[Point], depth: int) -> Iterator[Step]:
        if len(subset) <= seuil:
            hull = enveloppe_monotone(subset)
            yield {
                "hull": hull,
                "active": None,
                "label": f"Monotone (taille {len(subset)})",
                "close": True,
            }
            return hull

        mid = len(subset) // 2
        left = subset[:mid]
        right = subset[mid:]
        hull_left = yield from recurse(left, depth + 1)
        hull_right = yield from recurse(right, depth + 1)
        merged = enveloppe_monotone(hull_left + hull_right)
        yield {
            "hull": merged,
            "active": None,
            "label": f"Fusion niveau {depth}",
            "close": True,
        }
        return merged

    yield {"hull": [], "active": None, "label": "Tri et division rec", "close": False}
    final = yield from recurse(pts, 0)
    yield {"hull": final, "active": None, "label": "Enveloppe complete", "close": True}


def merge_hull_steps(points: Sequence[Sequence[float]]) -> Iterator[Step]:
    yield from merge_steps(points, seuil=64)


def preparata_hong_steps(points: Sequence[Sequence[float]]) -> Iterator[Step]:
    yield from merge_steps(points, seuil=32)


def animate_algorithms(points: Sequence[Sequence[float]], pause: float = 0.7) -> None:
    pts = _unique(points)
    if not pts:
        print("Aucun point a afficher.")
        return
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    span_x = max(xs) - min(xs)
    span_y = max(ys) - min(ys)
    span = max(span_x, span_y)
    padding = 0.08 * span if span else 1.0

    step_funcs = [
        ("Monotone Chain", monotone_steps),
        ("Graham Scan", graham_steps),
        ("QuickHull", quickhull_steps),
        ("Merge Hull", merge_hull_steps),
        ("Preparata-Hong", preparata_hong_steps),
    ]

    for name, generator in step_funcs:
        algo_dir = STEPS_DIR / name.lower().replace(" ", "_")
        algo_dir.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(6.5, 6.5))
        ax.scatter(xs, ys, s=18, color="gray", alpha=0.45)
        (hull_line,) = ax.plot([], [], color="tab:blue", linewidth=2)
        highlight = ax.scatter([], [], s=60, color="tab:red", zorder=5)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(name)
        ax.set_xlim(min(xs) - padding, max(xs) + padding)
        ax.set_ylim(min(ys) - padding, max(ys) + padding)
        ax.grid(True, linestyle="--", alpha=0.35)

        highlight.set_offsets([[math.nan, math.nan]])
        frame_idx = 0
        saved_frame = False

        for step in generator(pts):
            hx, hy = _close_coords(step.get("hull", []), step.get("close", False))
            hull_line.set_data(hx, hy)
            active = step.get("active")
            if active is not None:
                highlight.set_offsets([active])
            else:
                highlight.set_offsets([[math.nan, math.nan]])
            fig.canvas.draw()
            frame_path = algo_dir / f"{frame_idx:03d}.png"
            fig.savefig(frame_path, dpi=150)
            frame_idx += 1
            saved_frame = True

        if not saved_frame:
            fig.canvas.draw()
            frame_path = algo_dir / "000.png"
            fig.savefig(frame_path, dpi=150)

        plt.close(fig)


def main() -> None:
    points = nuage(120)
    animate_algorithms(points)


if __name__ == "__main__":
    main()
