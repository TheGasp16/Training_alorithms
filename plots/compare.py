import matplotlib.pyplot as plt

def plot_temps(tailles, temps, algos):
    """Trace les temps d'exécution en échelle log-log."""
    plt.figure(figsize=(8,6))
    for nom, _ in algos:
        plt.plot(tailles, temps[nom], marker='o', label=nom)
    plt.xscale("log"); plt.yscale("log")
    plt.title("Comparaison des temps d'exécution (log-log)")
    plt.xlabel("Nombre de points"); plt.ylabel("Temps (ms)")
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend(); plt.show()

def plot_hulls(points, algos):
    """Affiche les enveloppes convexes sur un même nuage."""
    plt.figure(figsize=(7,7))
    x, y = zip(*points)
    plt.scatter(x, y, s=8, color="gray", alpha=0.4)
    for nom, f in algos:
        H = f(points)
        hx, hy = zip(*(H + [H[0]]))
        plt.plot(hx, hy, label=nom)
    plt.legend(); plt.title("Comparaison des enveloppes convexes")
    plt.gca().set_aspect("equal"); plt.grid(True, linestyle="--", alpha=0.5)
    plt.show()
