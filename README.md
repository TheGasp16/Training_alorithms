# 🧭 Projet : Enveloppe Convexe — Comparaison d'Algorithmes

> Projet d'analyse et d'implémentation d'algorithmes classiques de géométrie computationnelle.  
> Réalisé par **Gaspard MENOU** — Étudiant à Centrale Méditerranée.

---

## 🎯 Objectif

Ce projet vise à comparer plusieurs **algorithmes de calcul d’enveloppe convexe** sur des nuages de points aléatoires.  
L’objectif est d’évaluer :
- leur **vitesse d’exécution**,
- leur **robustesse**,
- et leur **complexité algorithmique**.

Le tout est accompagné d’une **visualisation graphique** (temps d’exécution et enveloppes superposées).

---

## 🧩 Algorithmes implémentés

| Algorithme | Type | Complexité moyenne | Année |
|-------------|------|--------------------|--------|
| **Monotone Chain** (Andrew) | Balayage gauche–droite | `O(n log n)` | 1979 |
| **QuickHull** | Divide & Conquer | `O(n log n)` | 1996 |
| **Graham Scan** | Tri angulaire + pile | `O(n log n)` | 1972 |
| **Merge Hull** (Shamos) | Divide & Conquer | `O(n log n)` | 1976 |
| **Preparata–Hong** | Divide & Conquer optimisé | `O(n log n)` | 1977 |

---

## 🧠 Rappels théoriques

L’**enveloppe convexe** d’un ensemble de points $S$ est le plus petit polygone convexe contenant tous les points de $S$.

\[
\text{det}(A,B,C) = (A_x - B_x)(C_y - B_y) - (A_y - B_y)(C_x - B_x)
\]

- `det > 0` → virage à gauche  
- `det < 0` → virage à droite  
- `det = 0` → points alignés

---

## 🗂️ Structure du projet

