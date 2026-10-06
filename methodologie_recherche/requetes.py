"""Applique les gabarits de requêtes d'une méthodologie à un sujet, dans chaque langue.

Le sujet est soit un texte (utilisé tel quel dans toutes les langues), soit un dictionnaire
{langue: texte} ; les langues absentes du dictionnaire sont ignorées. La traduction du sujet
est faite en amont, par le modèle (prompt C02).

Variables utilisables dans un gabarit : {sujet}, {annee}.
"""

from __future__ import annotations

from datetime import date

from .collecteurs.contrat import Requete

__manifeste__ = {
    "nom": "generer_requetes_strategie",
    "role": "Applique les gabarits de requêtes de la méthodologie à un sujet, dans chaque langue.",
    "groupe": "methodo",
    "ordre": 9,
    "session": "S08",
    "entrees": {"strategie": "méthodologie", "sujet": "sujet"},
    "sorties": {"requetes_strategie": "formulations de requêtes"},
}

NOMBRE_SITES = 5  # sites préférés transmis à la liste de lecture


def date_limite(aujourd_hui: date, mois: int) -> date:
    """Date située `mois` mois avant `aujourd_hui` (jour ramené à 28 au besoin)."""
    total = aujourd_hui.year * 12 + aujourd_hui.month - 1 - mois
    return date(total // 12, total % 12 + 1, min(aujourd_hui.day, 28))


def _textes_du_sujet(sujet, langues: list[str]) -> dict[str, str]:
    if isinstance(sujet, dict):
        return {langue: sujet[langue] for langue in langues if sujet.get(langue)}
    return {langue: sujet for langue in langues}


def generer_requetes_strategie(strategie: dict, sujet, aujourd_hui: date | None = None,
                               theme: str | None = None, limite: int = 20) -> list[Requete]:
    """Liste des requêtes (sans doublon) à confier aux techniques de recherche."""
    aujourd_hui = aujourd_hui or date.today()
    langues = strategie.get("langues") or ["fr"]
    textes = _textes_du_sujet(sujet, langues)
    depuis = None
    if strategie.get("filtrer_par_date") and strategie.get("fraicheur_mois"):
        depuis = date_limite(aujourd_hui, strategie["fraicheur_mois"]).isoformat()
    sites = ",".join((strategie.get("sources_preferees") or [])[:NOMBRE_SITES])
    sous_question = sujet if isinstance(sujet, str) else next(iter(textes.values()), None)

    requetes_strategie: list[Requete] = []
    vues = set()
    for langue, texte_sujet in textes.items():
        for gabarit in (strategie.get("gabarits") or {}).get(langue) or []:
            modele = gabarit["texte"] if isinstance(gabarit, dict) else gabarit
            sans_date = isinstance(gabarit, dict) and gabarit.get("sans_date", False)
            texte = " ".join(
                modele.replace("{sujet}", texte_sujet).replace("{annee}", str(aujourd_hui.year)).split()
            )
            filtres = {}
            if depuis and not sans_date:
                filtres["depuis"] = depuis
            if sites:
                filtres["sites"] = sites
            cle = (langue, texte.lower(), filtres.get("depuis"))
            if cle in vues:
                continue
            vues.add(cle)
            requetes_strategie.append(Requete(
                texte=texte, langue=langue, theme=theme, sous_question=sous_question,
                filtres=filtres, limite=limite,
            ))
    return requetes_strategie
