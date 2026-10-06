"""Explore une question à travers le répertoire : types, problème général, grilles, disciplines.

Ce script ne remplace pas le modèle : il lui fournit un MENU systématique (toutes les grilles
qui s'appliquent, les problèmes analogues, les disciplines repérées et les familles absentes),
pour que le plan ne dépende pas seulement de ce qui vient spontanément au modèle.
"""

from __future__ import annotations

from ..outils_texte import contient, normaliser

__manifeste__ = {
    "nom": "explorer_transversal",
    "role": "Repère le type de question, le problème général et ses analogues, les grilles à appliquer et les disciplines concernées ; prépare le menu du plan.",
    "groupe": "transversal",
    "ordre": 32,
    "session": "S09",
    "entrees": {"question": "question", "situation": "situation (Q01)", "repertoire_transversal": "répertoire"},
    "sorties": {"exploration_transversale": "angles repérés", "menu_transversal": "menu injecté dans le prompt du plan"},
}


def _texte_situation(situation: dict | None) -> str:
    if not situation:
        return ""
    morceaux = []
    for valeur in situation.values():
        if isinstance(valeur, str):
            morceaux.append(valeur)
        elif isinstance(valeur, list):
            morceaux.extend(v for v in valeur if isinstance(v, str))
    return " ".join(morceaux)


def _trouves(texte: str, mots_cles: list[str]) -> list[str]:
    return [m for m in mots_cles if contient(texte, m)]


def explorer_transversal(question: str, repertoire_transversal: dict, situation: dict | None = None) -> dict:
    """Angles repérés pour une question (structure stable, testée)."""
    texte = normaliser(f"{question} {_texte_situation(situation)}")
    types = [t for t, mots_cles in repertoire_transversal["types"].items() if _trouves(texte, mots_cles)]
    concepts: list[str] = []

    schemas = []
    for schema in repertoire_transversal["schemas"]:
        indices = [_trouves(texte, groupe) for groupe in schema["indices"]]
        if all(indices):
            schemas.append(schema)
            concepts += [m for groupe in indices for m in groupe]
            types += [t for t in schema.get("types", []) if t not in types]

    lentilles = [lentille for lentille in repertoire_transversal["lentilles"]
                 if lentille.get("toujours") or set(lentille.get("types", [])) & set(types)]

    detectees = []
    for discipline in repertoire_transversal["disciplines"]:
        trouves = _trouves(texte, discipline["mots_cles"])
        if trouves:
            detectees.append(discipline["id"])
            concepts += trouves
    suggerees = []
    for ident in [d for s in schemas for d in s.get("disciplines", [])] + detectees:
        if ident not in suggerees:
            suggerees.append(ident)

    familles = {d["id"]: d.get("famille") for d in repertoire_transversal["disciplines"]}
    familles_presentes = {familles[i] for i in suggerees if i in familles}
    familles_absentes = sorted({f for f in familles.values() if f} - familles_presentes)

    exploration_transversale = {
        "question": question,
        "types": types,
        "schemas": [{"id": s["id"], "nom": s["nom"], "analogues": s.get("analogues", [])} for s in schemas],
        "lentilles": [lentille["id"] for lentille in lentilles],
        "disciplines_detectees": detectees,
        "disciplines_suggerees": suggerees,
        "familles_absentes": familles_absentes,
        "concepts": sorted({normaliser(c) for c in concepts}),
    }
    return exploration_transversale


def rendre_menu(exploration_transversale: dict, repertoire_transversal: dict) -> str:
    """Texte compact (Markdown) à placer dans le prompt du plan (Q02)."""
    lentilles = {lentille["id"]: lentille for lentille in repertoire_transversal["lentilles"]}
    disciplines = {d["id"]: d for d in repertoire_transversal["disciplines"]}
    lignes = ["## Grilles à appliquer (chacune doit produire au moins une sous-question, ou être écartée avec une raison)"]
    for ident in exploration_transversale["lentilles"]:
        lentille = lentilles[ident]
        lignes.append(f"- **{ident}** — {lentille['nom']} : " + " / ".join(lentille["questions"]))
        if lentille.get("niveaux"):
            lignes.append(f"  niveaux : {', '.join(lentille['niveaux'])}")
    if exploration_transversale["schemas"]:
        lignes.append("## Problème général et domaines analogues (chercher aussi dans ces littératures)")
        for schema in exploration_transversale["schemas"]:
            analogues = "; ".join(f"{a['domaine']} ({a['recherche_en']})" for a in schema["analogues"])
            lignes.append(f"- **{schema['nom']}** → {analogues}")
    lignes.append("## Disciplines repérées")
    for ident in exploration_transversale["disciplines_suggerees"]:
        discipline = disciplines.get(ident)
        if discipline:
            lignes.append(f"- **{ident}** — {discipline['nom']} : {discipline['apporte']}")
    autres = [d for d in repertoire_transversal["disciplines"]
              if d["id"] not in exploration_transversale["disciplines_suggerees"]]
    if autres:
        lignes.append("## Autres disciplines disponibles (à retenir si elles éclairent la question)")
        lignes.append(", ".join(d["id"] for d in autres))
    if exploration_transversale["familles_absentes"]:
        lignes.append("Familles non représentées : " + ", ".join(exploration_transversale["familles_absentes"])
                      + ". Vérifiez qu'aucune n'est nécessaire.")
    lignes.append("Vous pouvez proposer une discipline absente de ce répertoire : nommez-la et justifiez-la.")
    return "\n".join(lignes)
