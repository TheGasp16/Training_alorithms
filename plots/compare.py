"""Fonctions de visualisation des performances et des enveloppes convexes."""

import math
from pathlib import Path

import matplotlib.pyplot as plt

OUTPUT_DIR = Path("plots") / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_temps(tailles, temps, algos):
    """1/cree figure 2/trace courbes log-log 3/sauvegarde dans plots/output."""
    fig, ax = plt.subplots(figsize=(8, 6))
    for nom, _ in algos:
        ax.plot(tailles, temps[nom], marker="o", label=nom)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Comparaison des temps d'execution (log-log)")
    ax.set_xlabel("Nombre de points")
    ax.set_ylabel("Temps (ms)")
    ax.grid(True, which="both", linestyle="--", alpha=0.5)
    ax.legend()
    output = OUTPUT_DIR / "comparaison_temps.png"
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def plot_hulls(points, algos):
    """Trace un nuage par algorithme afin de comparer visuellement chaque enveloppe."""
    n = len(algos)
    if n == 0:
        return

    ncols = min(3, n)
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 4.5 * nrows))
    axes = [ax for ax in axes.flat] if hasattr(axes, "flat") else [axes]

    x, y = zip(*points)
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(y), max(y)
    span = max(xmax - xmin, ymax - ymin)
    padding = 0.05 * span if span else 1.0

    for idx, (nom, f) in enumerate(algos):
        ax = axes[idx]
        ax.scatter(x, y, s=8, color="gray", alpha=0.4)
        hull = f(points)
        if hull:
            hx, hy = zip(*(hull + [hull[0]]))
            ax.plot(hx, hy, color="tab:blue")
        ax.set_title(nom)
        ax.set_xlim(xmin - padding, xmax + padding)
        ax.set_ylim(ymin - padding, ymax + padding)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle="--", alpha=0.4)

    for ax in axes[n:]:
        ax.axis("off")

    fig.suptitle("Comparaison des enveloppes convexes")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    output = OUTPUT_DIR / "comparaison_enveloppes.png"
    fig.savefig(output, dpi=150)
    plt.close(fig)
