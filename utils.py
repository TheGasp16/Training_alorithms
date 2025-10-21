import math as m
import random as rd
import time as t
import statistics as stats

def cross(o, a, b):
    """Produit vectoriel orienté : positif = virage gauche."""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def area_signed(poly):
    """Aire signée (utile pour vérifier si un polygone est orienté CCW)."""
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % len(poly)]
        s += x1*y2 - x2*y1
    return 0.5 * s

def nuage(n, xmin=-10, xmax=10, ymin=-10, ymax=10):
    """Génère un nuage de points aléatoires."""
    return [[rd.uniform(xmin, xmax), rd.uniform(ymin, ymax)] for _ in range(n)]

def benchmark(func, points, repeat=3):
    """Mesure le temps moyen d'exécution d'un algorithme."""
    times = []
    for _ in range(repeat):
        start = t.time()
        hull = func(points)
        times.append((t.time() - start) * 1000)
    elapsed = stats.median(times)
    return elapsed, len(hull)