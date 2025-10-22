"""Script principal: compare graphiquement plusieurs enveloppes convexes.

Etapes clefs de l'experience:
1. Construire une liste de tailles de jeux de points de test.
2. Associer chaque taille aux differentes implementations d'enveloppe convexe.
3. Chronometrer chaque algorithme sur les nuages generes et collecter les stats.
4. Tracer les courbes de performances puis visualiser les enveloppes resultantes.
"""

from utils import nuage, benchmark
from algorithms import *
from plots.compare import plot_temps, plot_hulls


def main():
    tailles = [100, 500, 1000, 2000, 5000]
    algos = [
        ("Monotone Chain", enveloppe_monotone),
        ("QuickHull", enveloppe_quickhull),
        ("Graham Scan", enveloppe_graham),
        ("Merge Hull", merge_hull),
        ("Preparata-Hong", preparata_hong)
    ]

    print("=== COMPARAISON DES ALGORITHMES D'ENVELOPPE CONVEXE ===")
    # Stocke les temps median calcules pour chaque algorithme (par taille).
    temps = {nom: [] for nom, _ in algos}

    for n in tailles:
        # Genere un nouveau nuage pour chaque taille afin de limiter les biais.
        E = nuage(n)
        print(f"\n--- {n} points ---")
        for nom, f in algos:
            tps, nsom = benchmark(f, E)
            temps[nom].append(tps)
            print(f"{nom:<20} | {nsom:3d} sommets | {tps:7.2f} ms")

    plot_temps(tailles, temps, algos)

    # Visualisation finale: toutes les enveloppes d'un meme nuage pour comparer.
    E = nuage(800)
    plot_hulls(E, algos)


if __name__ == "__main__":
    main()
