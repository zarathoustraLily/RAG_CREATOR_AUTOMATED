"""Charge les techniques actives du registre et vérifie qu'elles respectent le contrat.

Une technique défectueuse (introuvable, non conforme, nom en double) est écartée et signalée
dans `problemes_registre` : le travail en fond continue avec les autres.
"""

from __future__ import annotations

import importlib
from pathlib import Path

import yaml

from .collecteurs.contrat import VERSION_CONTRAT, verifier_conformite

__manifeste__ = {
    "nom": "charger_registre",
    "role": "Charge les techniques actives du registre et vérifie qu'elles respectent le contrat.",
    "groupe": "methodo",
    "ordre": 9,
    "session": "S08",
    "entrees": {"registre": "registre.yaml"},
    "sorties": {"collecteurs": "techniques actives", "problemes_registre": "techniques écartées et pourquoi"},
}

REGISTRE = Path(__file__).resolve().parent / "registre.yaml"
PAQUET_COLLECTEURS = "methodologie_recherche.collecteurs"


class RegistreInvalide(ValueError):
    """Registre inutilisable (en mode strict)."""


def lire_registre(registre=REGISTRE) -> dict:
    """Accepte un chemin de fichier YAML ou un dictionnaire déjà lu."""
    if isinstance(registre, dict):
        return registre
    with Path(registre).open(encoding="utf-8") as fichier:
        return yaml.safe_load(fichier) or {}


def _majeure(version: str) -> str:
    return str(version).split(".")[0]


def charger_registre(registre=REGISTRE, http=None, actives_seulement: bool = True,
                     strict: bool = False) -> tuple[list, list[str]]:
    """Renvoie (collecteurs, problemes_registre). En mode strict, tout problème lève une erreur."""
    contenu = lire_registre(registre)
    collecteurs, problemes_registre = [], []
    if _majeure(contenu.get("version_contrat", "")) != _majeure(VERSION_CONTRAT):
        problemes_registre.append(
            f"registre écrit pour le contrat {contenu.get('version_contrat')!r}, contrat actuel {VERSION_CONTRAT}"
        )
    noms = set()
    for entree in contenu.get("techniques") or []:
        nom = entree.get("nom", "?")
        if actives_seulement and not entree.get("actif", True):
            continue
        if nom in noms:
            problemes_registre.append(f"{nom} : nom en double dans le registre")
            continue
        module = entree.get("module", nom)
        chemin_module = module if "." in module else f"{PAQUET_COLLECTEURS}.{module}"
        try:
            classe = getattr(importlib.import_module(chemin_module), entree["classe"])
            collecteur = classe(reglages=entree.get("reglages") or {}, http=http)
        except Exception as erreur:  # noqa: BLE001 — une technique cassée ne doit pas arrêter les autres
            problemes_registre.append(f"{nom} : chargement impossible ({type(erreur).__name__} : {erreur})")
            continue
        ecarts = verifier_conformite(collecteur)
        if getattr(collecteur, "nom", None) != nom:
            ecarts.append(f"le registre l'appelle « {nom} » mais la classe dit « {getattr(collecteur, 'nom', None)} »")
        if ecarts:
            problemes_registre.append(f"{nom} : non conforme au contrat — " + " ; ".join(ecarts))
            continue
        noms.add(nom)
        collecteurs.append(collecteur)
    if strict and problemes_registre:
        raise RegistreInvalide("\n".join(problemes_registre))
    return collecteurs, problemes_registre
