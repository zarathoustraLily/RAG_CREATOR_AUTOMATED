"""Ponts entre littératures, calculés sur VOTRE corpus (modèle « ABC » de Swanson).

Idée : si le concept A (la question) est souvent associé à B dans certains documents, et B à C
(le but recherché) dans d'autres, alors B relie A et C même si aucun document ne relie A et C
directement. Ces ponts viennent des données, pas de l'intuition du modèle : ils font apparaître
des angles qu'on n'aurait pas pensé à explorer. Ils restent des PISTES, à vérifier.

Entrée : les concepts de chaque document ou extrait (étiquettes, entités, sujets), fournis par
l'index du RAG (session S14).
"""

from __future__ import annotations

from collections import Counter
from math import sqrt

__manifeste__ = {
    "nom": "ponts_corpus",
    "role": "Calcule sur le corpus les concepts qui relient la question à son but (modèle ABC) et les voisins venus d'autres familles de disciplines.",
    "groupe": "transversal",
    "ordre": 33,
    "session": "S14",
    "entrees": {"exploration_transversale": "angles repérés", "concepts_par_document": "concepts de chaque document (index)"},
    "sorties": {"ponts": "concepts-ponts et voisins transversaux"},
}


def _contient(document: set[str], concepts: set[str]) -> bool:
    return bool(document & concepts)


def ponts_abc(concepts_par_document: list[set[str]], concepts_a, concepts_c, top: int = 10,
              documents_min: int = 2) -> list[dict]:
    """Concepts B associés à A et à C ; score = min(association A–B, association B–C).

    Association de Ochiai : n(X et B) / racine(n(X) × n(B)). `direct_ac` indique combien de
    documents relient déjà A et C : un pont est d'autant plus intéressant que ce nombre est faible.
    """
    a, c = set(concepts_a), set(concepts_c)
    n_a = sum(_contient(doc, a) for doc in concepts_par_document)
    n_c = sum(_contient(doc, c) for doc in concepts_par_document)
    if not n_a or not n_c:
        return []
    n_b, n_ab, n_bc = Counter(), Counter(), Counter()
    direct_ac = 0
    for doc in concepts_par_document:
        avec_a, avec_c = _contient(doc, a), _contient(doc, c)
        direct_ac += avec_a and avec_c
        for concept in doc - a - c:
            n_b[concept] += 1
            n_ab[concept] += avec_a
            n_bc[concept] += avec_c
    ponts = []
    for concept, total in n_b.items():
        if n_ab[concept] < documents_min or n_bc[concept] < documents_min:
            continue
        score = min(n_ab[concept] / sqrt(n_a * total), n_bc[concept] / sqrt(n_c * total))
        ponts.append({"concept": concept, "score": round(score, 4), "documents_ab": n_ab[concept],
                      "documents_bc": n_bc[concept], "direct_ac": direct_ac})
    ponts.sort(key=lambda p: (-p["score"], p["concept"]))
    return ponts[:top]


def voisins_transversaux(concepts_par_document: list[set[str]], concepts_a, famille_de: dict[str, str],
                         familles_deja: set[str], top: int = 10, documents_min: int = 2) -> list[dict]:
    """Concepts souvent associés à A mais rangés dans une famille de disciplines encore absente du plan."""
    a = set(concepts_a)
    n_a = sum(_contient(doc, a) for doc in concepts_par_document)
    if not n_a:
        return []
    n_b, n_ab = Counter(), Counter()
    for doc in concepts_par_document:
        avec_a = _contient(doc, a)
        for concept in doc - a:
            n_b[concept] += 1
            n_ab[concept] += avec_a
    voisins = []
    for concept, total in n_b.items():
        famille = famille_de.get(concept)
        if not famille or famille in familles_deja or n_ab[concept] < documents_min:
            continue
        voisins.append({"concept": concept, "famille": famille,
                        "score": round(n_ab[concept] / sqrt(n_a * total), 4), "documents": n_ab[concept]})
    voisins.sort(key=lambda v: (-v["score"], v["concept"]))
    return voisins[:top]
