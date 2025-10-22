"""Enveloppe convexes de Preparata-Hong via la variante Merge Hull."""

from algorithms.mergehull import merge_hull


def preparata_hong(points):
    """Suit Merge Hull mais abaisse le seuil pour equilibrer profondeur et cout."""
    return merge_hull(points, seuil=32)
