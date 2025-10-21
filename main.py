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
        ("Preparata–Hong", preparata_hong)
    ]

    print("=== COMPARAISON DES ALGORITHMES D’ENVELOPPE CONVEXE ===")
    temps = {nom: [] for nom, _ in algos}

    for n in tailles:
        E = nuage(n)
        print(f"\n--- {n} points ---")
        for nom, f in algos:
            tps, nsom = benchmark(f, E)
            temps[nom].append(tps)
            print(f"{nom:<20} | {nsom:3d} sommets | {tps:7.2f} ms")

    plot_temps(tailles, temps, algos)

    # Visualisation finale d’un nuage de points
    E = nuage(800)
    plot_hulls(E, algos)

if __name__ == "__main__":
    main()
