from algorithms.mergehull import merge_hull

def preparata_hong(points):
    """Algorithme Preparata–Hong (1977)."""
    return merge_hull(points, seuil=32)
