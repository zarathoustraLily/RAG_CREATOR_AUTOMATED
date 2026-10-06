"""Outils de texte partagés : normalisation, mots significatifs, recherche de mots-clés, similarité."""

from __future__ import annotations

import re
import unicodedata

__manifeste__ = {
    "nom": "outils_texte",
    "role": "Normalise les textes (minuscules, sans accents), extrait les mots, repère les mots-clés, mesure la ressemblance.",
    "groupe": "methodo",
    "ordre": 8,
    "session": "S08",
    "entrees": {},
    "sorties": {},
}

MOTS_VIDES = {
    "les", "des", "une", "dans", "pour", "par", "sur", "avec", "aux", "est", "que", "qui", "quoi",
    "comment", "pourquoi", "quel", "quelle", "quels", "quelles", "son", "ses", "leur", "leurs",
    "the", "and", "for", "with", "from", "into", "how", "why", "what", "who",
}


def normaliser(texte: str) -> str:
    """Minuscules, sans accents, ponctuation remplacée par des espaces."""
    sans_accents = unicodedata.normalize("NFKD", texte or "").encode("ascii", "ignore").decode()
    return " ".join(re.split(r"[^a-z0-9]+", sans_accents.lower())).strip()


def _singulier(mot: str) -> str:
    """Retire un s ou un x final de pluriel (français, anglais) aux mots assez longs."""
    return mot[:-1] if len(mot) > 4 and mot[-1] in "sx" else mot


def mots(texte: str) -> set[str]:
    """Mots significatifs (plus de deux lettres, hors mots vides), normalisés, au singulier."""
    return {_singulier(m) for m in normaliser(texte).split() if len(m) > 2 and m not in MOTS_VIDES}


def contient(texte_normalise: str, mot_cle: str) -> bool:
    """Vrai si le mot-clé apparaît au début d'un mot (« vegan » trouve « veganisme »).

    Un mot-clé de plusieurs mots doit apparaître tel quel (« faire changer d'avis »).
    """
    cle = normaliser(mot_cle)
    if not cle:
        return False
    return re.search(r"(?:^|\s)" + re.escape(cle), texte_normalise) is not None


def similarite(a: str, b: str) -> float:
    """Ressemblance de deux textes (indice de Jaccard sur les mots significatifs)."""
    ma, mb = mots(a), mots(b)
    if not ma or not mb:
        return 0.0
    return len(ma & mb) / len(ma | mb)
