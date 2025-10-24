"""Script principal: compare graphiquement plusieurs enveloppes convexes.

Etapes clefs de l'experience:
1. Construire une liste de tailles de jeux de points de test.
2. Associer chaque taille aux differentes implementations d'enveloppe convexe.
3. Chronometrer chaque algorithme sur les nuages generes et collecter les stats.
4. Tracer les courbes de performances puis visualiser les enveloppes resultantes.
"""

from functools import partial

from utils import nuage, benchmark
from algorithms import (
    enveloppe_monotone,
    enveloppe_quickhull,
    enveloppe_graham,
    merge_hull as merge_enveloppe,
    preparata_hong,
)
from plots.compare import plot_temps, plot_hulls as plot_enveloppes, plot_merge_thresholds


def main():
    
    tailles = [10 + i*200 for i in range(100)]  
    algos = [
        ("Monotone Chain", enveloppe_monotone),
        ("QuickHull", enveloppe_quickhull),
        ("Graham Scan", enveloppe_graham),
        ("Merge enveloppe", merge_enveloppe),
        ("Preparata-Hong", preparata_hong)
    ]

    print("=== COMPARAISON DES ALGORITHMES D'ENVELOPPE CONVEXE ===")
    # Stocke les temps median calcules pour chaque algorithme (par taille).
    temps = {nom: [] for nom, _ in algos}

    for n in tailles:
        # Genere un nouveau nuage pour chaque taille afin de limiter les biais.
        E = nuage(n)
        #print(f"\n--- {n} points ---")
        for nom, f in algos:
            tps, nsom = benchmark(f, E)
            temps[nom].append(tps)
            #print(f"{nom:<20} | {nsom:3d} sommets | {tps:7.2f} ms")

    plot_temps(tailles, temps, algos)
    
    #Analyse specifique de Merge enveloppe: impact du seuil de division sur un nuage fixe.
    seuils = [i for i in range(1, 101, 2)]
    E_merge = nuage(6000)
    temps_merge = []
    print("\n=== IMPACT DU SEUIL SUR MERGE enveloppe (nuage fixe) ===")
    for seuil in seuils:
        f_merge = partial(merge_enveloppe, seuil=seuil)
        tps, nsom = benchmark(f_merge, E_merge)
        temps_merge.append(tps)
        #print(f"seuil={seuil:<3d} | sommets={nsom:3d} | temps={tps:7.2f} ms")
    plot_merge_thresholds(seuils, temps_merge, len(E_merge))

    # Visualisation finale: toutes les enveloppes d'un meme nuage pour comparer.
    E = nuage(800)
    plot_enveloppes(E, algos)


if __name__ == "__main__":
    main()
