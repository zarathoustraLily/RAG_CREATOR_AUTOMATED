"""Fusionne plusieurs plans candidats et mesure la couverture des angles.

Le modèle propose plusieurs plans (avec des grilles mises en avant différentes) ; ce script les
fusionne sans doublon, retient d'abord les sous-questions qui apportent des angles nouveaux,
puis signale les grilles et disciplines encore absentes pour la critique de complétude.

Format attendu d'une sous-question :
    {"id": "SQ1", "question": "...", "disciplines": [...], "lentilles": [...], "poids": 1-3,
     "type": "normale" | "contre_point" | "analogue"}
"""

from __future__ import annotations

from ..outils_texte import similarite

__manifeste__ = {
    "nom": "fusionner_plans",
    "role": "Fusionne les plans candidats sans doublon, privilégie les sous-questions qui ajoutent des angles, liste les angles manquants.",
    "groupe": "transversal",
    "ordre": 35,
    "session": "S09",
    "entrees": {"plans_candidats": "plans proposés par le modèle", "exploration_transversale": "angles repérés"},
    "sorties": {"plan_fusionne": "plan fusionné", "angles_manquants": "grilles et disciplines non couvertes"},
}

SEUIL_DOUBLON = 0.6


def _angles(sous_question: dict) -> set[str]:
    return {f"L:{x}" for x in sous_question.get("lentilles", [])} | {f"D:{x}" for x in sous_question.get("disciplines", [])}


def _gain(sous_question: dict, couverts) -> tuple:
    """Angles nouveaux d'abord, puis contre-point, poids, accord entre plans."""
    return (len(_angles(sous_question) - set(couverts)), sous_question.get("type") == "contre_point",
            sous_question.get("poids", 1), sous_question["proposee_par"])


def couverture(plan: dict, exploration_transversale: dict) -> dict:
    """Grilles et disciplines couvertes ou manquantes, et taux de couverture des grilles requises."""
    sous_questions = plan.get("sous_questions", [])
    lentilles = {x for sq in sous_questions for x in sq.get("lentilles", [])}
    disciplines = {x for sq in sous_questions for x in sq.get("disciplines", [])}
    requises = exploration_transversale.get("lentilles", [])
    suggerees = exploration_transversale.get("disciplines_suggerees", [])
    manquantes = [x for x in requises if x not in lentilles]
    return {
        "lentilles_couvertes": sorted(lentilles),
        "lentilles_manquantes": manquantes,
        "disciplines_couvertes": sorted(disciplines),
        "disciplines_suggerees_absentes": [x for x in suggerees if x not in disciplines],
        "disciplines_hors_repertoire": sorted(disciplines - set(suggerees)),
        "taux_lentilles": round(1 - len(manquantes) / len(requises), 3) if requises else 1.0,
        "contre_point": any(sq.get("type") == "contre_point" for sq in sous_questions),
    }


def fusionner_plans(plans_candidats: list[dict], exploration_transversale: dict,
                    max_sous_questions: int = 12) -> tuple[dict, dict]:
    """Renvoie (plan_fusionne, angles_manquants)."""
    groupes: list[dict] = []
    for plan in plans_candidats:
        for sous_question in plan.get("sous_questions", []):
            semblable = next((g for g in groupes
                              if similarite(g["question"], sous_question.get("question", "")) >= SEUIL_DOUBLON), None)
            if semblable is None:
                groupes.append({**sous_question, "lentilles": list(sous_question.get("lentilles", [])),
                                "disciplines": list(sous_question.get("disciplines", [])), "proposee_par": 1})
                continue
            semblable["proposee_par"] += 1
            semblable["poids"] = max(semblable.get("poids", 1), sous_question.get("poids", 1))
            for cle in ("lentilles", "disciplines"):
                semblable[cle] += [x for x in sous_question.get(cle, []) if x not in semblable[cle]]

    retenues, couverts = [], set()
    restantes = list(groupes)
    while restantes and len(retenues) < max_sous_questions:
        meilleure = max(restantes, key=lambda sq, deja=frozenset(couverts): _gain(sq, deja))
        if _gain(meilleure, couverts)[0] == 0 and any(sq.get("type") == "contre_point" for sq in retenues):
            # Plus d'angle nouveau : on complète par poids puis par accord entre plans.
            meilleure = max(restantes, key=lambda sq: (sq.get("poids", 1), sq["proposee_par"]))
        retenues.append(meilleure)
        couverts |= _angles(meilleure)
        restantes.remove(meilleure)

    for numero, sous_question in enumerate(retenues, 1):
        sous_question["id_origine"] = sous_question.get("id")
        sous_question["id"] = f"SQ{numero}"
    plan_fusionne = {"sous_questions": retenues, "plans_fusionnes": len(plans_candidats),
                     "ecartees": [sq.get("question") for sq in restantes]}
    angles_manquants = couverture(plan_fusionne, exploration_transversale)
    return plan_fusionne, angles_manquants
