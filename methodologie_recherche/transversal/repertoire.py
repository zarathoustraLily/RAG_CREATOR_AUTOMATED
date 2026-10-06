"""Charge et contrôle le répertoire transversal (lentilles, disciplines, problèmes analogues)."""

from __future__ import annotations

from pathlib import Path

import yaml

__manifeste__ = {
    "nom": "charger_repertoire",
    "role": "Charge le répertoire transversal (grilles d'analyse, disciplines, problèmes analogues) et vérifie sa cohérence.",
    "groupe": "transversal",
    "ordre": 30,
    "session": "S09",
    "entrees": {},
    "sorties": {"repertoire_transversal": "grilles, disciplines et analogues"},
    "lit": ["methodologie_recherche/transversal/*.yaml"],
}

DOSSIER_REPERTOIRE = Path(__file__).resolve().parent


class RepertoireInvalide(ValueError):
    """Répertoire incohérent (en mode strict)."""


def _lire(chemin: Path) -> dict:
    with chemin.open(encoding="utf-8") as fichier:
        return yaml.safe_load(fichier) or {}


def verifier_repertoire(repertoire: dict) -> list[str]:
    """Liste les incohérences (liste vide si tout va bien)."""
    problemes = []
    types = set(repertoire.get("types", {}))
    for nom, liste in (("lentille", repertoire["lentilles"]), ("discipline", repertoire["disciplines"]),
                       ("schéma", repertoire["schemas"])):
        vus = set()
        for element in liste:
            ident = element.get("id")
            if not ident:
                problemes.append(f"{nom} sans « id » : {element.get('nom')!r}")
            elif ident in vus:
                problemes.append(f"{nom} « {ident} » en double")
            vus.add(ident)
    for lentille in repertoire["lentilles"]:
        if not lentille.get("questions"):
            problemes.append(f"lentille « {lentille.get('id')} » sans questions")
        if not lentille.get("toujours") and not lentille.get("types"):
            problemes.append(f"lentille « {lentille.get('id')} » : ni « toujours » ni « types »")
        for type_ in lentille.get("types", []):
            if type_ not in types:
                problemes.append(f"lentille « {lentille.get('id')} » : type inconnu « {type_} »")
    ids_disciplines = {d.get("id") for d in repertoire["disciplines"]}
    for discipline in repertoire["disciplines"]:
        if not discipline.get("mots_cles"):
            problemes.append(f"discipline « {discipline.get('id')} » sans mots-clés")
    for schema in repertoire["schemas"]:
        if not schema.get("indices") or not all(schema["indices"]):
            problemes.append(f"schéma « {schema.get('id')} » : groupe d'indices vide")
        for ident in schema.get("disciplines", []):
            if ident not in ids_disciplines:
                problemes.append(f"schéma « {schema.get('id')} » : discipline inconnue « {ident} »")
        for type_ in schema.get("types", []):
            if type_ not in types:
                problemes.append(f"schéma « {schema.get('id')} » : type inconnu « {type_} »")
        if not schema.get("analogues"):
            problemes.append(f"schéma « {schema.get('id')} » sans analogues")
    return problemes


def charger_repertoire(dossier: Path = DOSSIER_REPERTOIRE, strict: bool = False) -> dict:
    """Assemble lentilles.yaml, disciplines.yaml et analogues.yaml."""
    dossier = Path(dossier)
    lentilles = _lire(dossier / "lentilles.yaml")
    repertoire_transversal = {
        "types": lentilles.get("types") or {},
        "lentilles": lentilles.get("lentilles") or [],
        "disciplines": _lire(dossier / "disciplines.yaml").get("disciplines") or [],
        "schemas": _lire(dossier / "analogues.yaml").get("schemas") or [],
    }
    problemes = verifier_repertoire(repertoire_transversal)
    if strict and problemes:
        raise RepertoireInvalide("\n".join(problemes))
    repertoire_transversal["problemes"] = problemes
    return repertoire_transversal
