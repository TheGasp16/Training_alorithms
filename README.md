# 🧭 Projet : Enveloppe convexe - comparaison d'algorithmes

Ce projet met en oeuvre plusieurs algorithmes classiques de geometrie computationnelle afin de calculer et comparer l'enveloppe convexe de nuages de points aleatoires. Les scripts mesurent le temps d'execution de chaque approche et tracent des visualisations pour faciliter la comparaison.

## ✨ Fonctionnalites principales
- 🌧️ Generation de nuages de points aleatoires dans un rectangle controle.
- ⚙️ Implementation de cinq algorithmes d'enveloppe convexe : Monotone Chain, QuickHull, Graham Scan, Merge Hull (Shamos) et Preparata-Hong.
- ⏱️ Mesure et comparaison des performances (medianes) sur des tailles de jeux de points croissantes.
- 📊 Visualisations matplotlib : courbes log-log des temps d'execution et superposition des enveloppes convexes sur un nuage commun.

## 🗂️ Apercu des fichiers
- `main.py` : point d'entree; orchestre la generation des nuages, le benchmark et les graphiques.
- `utils.py` : helpers (produit vectoriel, aire signee, generation de nuages, fonction de benchmark).
- `algorithms/` : implementations individuelles des algorithmes.
- `plots/compare.py` : fonctions de visualisation avec matplotlib.
- `jsp.py` : script de travail contenant des versions alternatives et des tests exploratoires.

## 📦 Prerequis
- Python 3.10 ou plus recent.
- Dependances : `matplotlib` (les autres importations font partie de la bibliotheque standard).

Installation rapide :
```bash
python -m venv .venv
source .venv/bin/activate  # sous Windows: .venv\Scripts\activate
pip install matplotlib
```

## 🚀 Lancer le benchmark
Depuis la racine du projet :
```bash
python main.py
```

Le script affiche dans le terminal le nombre de sommets et le temps median (en millisecondes) pour chaque algorithme, puis ouvre deux fenetres matplotlib :
1. Courbes log-log des temps en fonction du nombre de points.
2. Nuage de points avec les enveloppes convexes superposees.

## 🔧 Adapter les experiences
- Modifier la liste `tailles` dans `main.py` pour changer les tailles de nuages testes.
- Ajuster le parametre `repeat` de `benchmark` dans `utils.py` pour prendre davantage de mesures.
- Utiliser les fonctions de `plots/compare.py` dans vos propres scripts pour visualiser d'autres scenarios.

## 🗃️ Structure du depot
```
Training_alorithms/
├── algorithms/
│   ├── __init__.py
│   ├── graham.py
│   ├── mergehull.py
│   ├── monotone.py
│   ├── preparata_hong.py
│   └── quickhull.py
├── plots/
│   └── compare.py
├── utils.py
├── main.py
├── jsp.py
└── README.md
```

## 🚀 Aller plus loin
Quelques idees pour prolonger le projet :
1. Ajouter d'autres algorithmes (Jarvis March, Chan, Kirkpatrick-Seidel) pour comparer des approches lineaires ou hybrides.
2. Integrer une sauvegarde automatique des figures (PNG/SVG) et des tableaux de mesures (CSV).
3. Tester la robustesse face aux nuages contenant beaucoup de points alignes ou des duplicatas.
