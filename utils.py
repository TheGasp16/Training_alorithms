"""Fonctions utilitaires communement partagees par les enveloppes convexes."""

import math as m
import random as rd
import time as t
import statistics as stats


def cross(o, a, b):
    """Calcule le determinant 2D: > 0 signifie que o->a->b tourne a gauche."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def area_signed(poly):
    """Retourne l'aire signee d'un polygone; le signe indique l'orientation."""
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return 0.5 * s


def nuage(n, xmin=-10, xmax=10, ymin=-10, ymax=10):
    """Genere n points uniformes dans un rectangle axis-aligne."""
    return [[rd.uniform(xmin, xmax), rd.uniform(ymin, ymax)] for _ in range(n)]


def benchmark(func, points, repeat=5):
    """Evalue un algorithme: moyenne du temps sur repeat executions."""
    times = []
    for _ in range(repeat):
        start = t.time()
        enveloppe = func(points)
        times.append((t.time() - start) * 1000)
    elapsed = stats.mean(times)
    return elapsed, len(enveloppe)
