"""Génère la carte du programme à partir de l'architecture prévue et des manifestes du code.

La carte (index.html) lit le fichier donnees.js produit ici. Elle montre les mini-scripts,
leur ordre chronologique, les flux entre eux et le nom des variables qui circulent.

Sources, par ordre de priorité :
1. les manifestes `__manifeste__` des scripts du code (lus sans exécuter le code) ;
2. architecture_prevue.yaml pour les scripts qui n'existent pas encore.

Usage :
    python carte_du_programme/generer_carte.py              # régénère donnees.js
    python carte_du_programme/generer_carte.py --verifier   # échoue si problème ou carte périmée
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

DOSSIER = Path(__file__).resolve().parent
RACINE = DOSSIER.parent
ARCHITECTURE = DOSSIER / "architecture_prevue.yaml"
SORTIE = DOSSIER / "donnees.js"

# Dossiers ignorés lors de la recherche des manifestes.
DOSSIERS_EXCLUS = {
    ".git", "carte_du_programme", "PLAN", "tests", "__pycache__", ".venv", "venv",
    "node_modules", "bench", "reports",
}
# Dossiers dont chaque script (hors __init__.py) doit avoir un manifeste.
DOSSIERS_DE_CODE = ("ragcreator", "methodologie_recherche")
CHAMPS_OBLIGATOIRES = ("id", "fichier", "groupe", "ordre", "role", "entrees", "sorties")
EN_TETE_JS = "// Fichier généré par generer_carte.py : ne pas modifier à la main.\n"


def lire_architecture(chemin: Path = ARCHITECTURE) -> dict:
    """Lit l'architecture prévue (YAML)."""
    with chemin.open(encoding="utf-8") as fichier:
        return yaml.safe_load(fichier)


def lire_manifeste(fichier: Path) -> dict | None:
    """Renvoie le dictionnaire `__manifeste__` d'un script, sans exécuter le script."""
    arbre = ast.parse(fichier.read_text(encoding="utf-8"), filename=str(fichier))
    for noeud in arbre.body:
        if isinstance(noeud, ast.Assign):
            cibles = [c.id for c in noeud.targets if isinstance(c, ast.Name)]
        elif isinstance(noeud, ast.AnnAssign) and isinstance(noeud.target, ast.Name):
            cibles = [noeud.target.id]
        else:
            continue
        if "__manifeste__" in cibles and noeud.value is not None:
            return ast.literal_eval(noeud.value)
    return None


def trouver_scripts(racine: Path = RACINE) -> list[Path]:
    """Liste les scripts Python du dépôt, hors dossiers exclus et fichiers de test."""
    scripts = []
    for chemin in sorted(racine.rglob("*.py")):
        relatif = chemin.relative_to(racine)
        if any(partie in DOSSIERS_EXCLUS for partie in relatif.parts[:-1]):
            continue
        if chemin.name.startswith("test_") or chemin.name == "conftest.py":
            continue
        scripts.append(chemin)
    return scripts


def manifeste_vers_script(manifeste: dict, fichier: Path, racine: Path) -> dict:
    """Convertit un manifeste de code en entrée de carte (statut « réalisé »)."""
    script = {cle: valeur for cle, valeur in manifeste.items() if cle != "nom"}
    script["id"] = manifeste.get("nom", fichier.stem)
    script["fichier"] = fichier.relative_to(racine).as_posix()
    script["entrees"] = dict(manifeste.get("entrees") or {})
    script["sorties"] = dict(manifeste.get("sorties") or {})
    script["statut"] = "realise"
    return script


def fusionner(prevus: list[dict], realises: list[dict]) -> list[dict]:
    """Les scripts réalisés remplacent leur version prévue ; les nouveaux sont ajoutés."""
    par_id = {s["id"]: {**s, "statut": "prevu"} for s in prevus}
    for script in realises:
        base = par_id.get(script["id"], {})
        par_id[script["id"]] = {**base, **{k: v for k, v in script.items() if v is not None}}
    return list(par_id.values())


def collecter_realises(racine: Path) -> tuple[list[dict], list[str]]:
    """Lit les manifestes du code ; signale les scripts de code sans manifeste."""
    realises, problemes = [], []
    for fichier in trouver_scripts(racine):
        relatif = fichier.relative_to(racine)
        try:
            manifeste = lire_manifeste(fichier)
        except (SyntaxError, ValueError) as erreur:
            problemes.append(f"{relatif.as_posix()} : manifeste illisible ({erreur})")
            continue
        if manifeste is None:
            if relatif.parts[0] in DOSSIERS_DE_CODE and fichier.name != "__init__.py":
                problemes.append(f"{relatif.as_posix()} : script sans manifeste")
            continue
        realises.append(manifeste_vers_script(manifeste, fichier, racine))
    return realises, problemes


def position_temporelle(script: dict, rang_moment: dict[str, int], groupes: dict) -> tuple:
    """Clé chronologique : moment du groupe, puis ordre."""
    moment = groupes.get(script.get("groupe"), {}).get("moment")
    return (rang_moment.get(moment, 99), script.get("ordre", 0))


def calculer_flux(scripts: list[dict], architecture: dict) -> tuple[list[dict], list[str]]:
    """Relie chaque entrée à ses producteurs ; détecte boucles et entrées orphelines."""
    externes = architecture.get("entrees_externes") or {}
    groupes = {g["id"]: g for g in architecture.get("groupes", [])}
    rang_moment = {m["id"]: i for i, m in enumerate(architecture.get("moments", []))}
    par_id = {s["id"]: s for s in scripts}
    producteurs: dict[str, list[str]] = defaultdict(list)
    for script in scripts:
        for variable in script.get("sorties", {}):
            producteurs[variable].append(script["id"])

    problemes: list[str] = []
    liens: dict[tuple[str, str], set[str]] = defaultdict(set)
    for script in scripts:
        for variable in script.get("entrees", {}):
            sources = [p for p in producteurs.get(variable, []) if p != script["id"]]
            if not sources and variable not in externes:
                problemes.append(
                    f"{script['id']} : l'entrée « {variable} » n'est produite par aucun script "
                    "et n'est pas déclarée externe"
                )
            for source in sources:
                liens[(source, script["id"])].add(variable)

    flux = []
    for (de, vers), variables in sorted(liens.items()):
        boucle = position_temporelle(par_id[vers], rang_moment, groupes) <= position_temporelle(
            par_id[de], rang_moment, groupes
        )
        flux.append({"de": de, "vers": vers, "variables": sorted(variables),
                     "type": "donnees", "boucle": boucle})
    for script in scripts:
        for appele in script.get("appelle", []) or []:
            if appele not in par_id:
                problemes.append(f"{script['id']} : appelle « {appele} », qui n'existe pas")
                continue
            flux.append({"de": script["id"], "vers": appele, "variables": [],
                         "type": "appel", "boucle": False})
    return flux, problemes


def verifier_structure(scripts: list[dict], architecture: dict) -> list[str]:
    """Contrôles de forme : champs, identifiants, groupes, moments, parcours."""
    problemes = []
    groupes = {g["id"]: g for g in architecture.get("groupes", [])}
    moments = {m["id"] for m in architecture.get("moments", [])}
    for groupe in groupes.values():
        if groupe.get("moment") not in moments:
            problemes.append(f"groupe {groupe['id']} : moment inconnu « {groupe.get('moment')} »")
    vus_id, vus_fichier = set(), set()
    for script in scripts:
        ident = script.get("id", "?")
        for champ in CHAMPS_OBLIGATOIRES:
            if champ not in script:
                problemes.append(f"{ident} : champ « {champ} » manquant")
        if ident in vus_id:
            problemes.append(f"{ident} : identifiant en double")
        vus_id.add(ident)
        fichier = script.get("fichier")
        if fichier in vus_fichier:
            problemes.append(f"{ident} : fichier « {fichier} » déjà utilisé")
        vus_fichier.add(fichier)
        if script.get("groupe") not in groupes:
            problemes.append(f"{ident} : groupe inconnu « {script.get('groupe')} »")
        if not isinstance(script.get("ordre"), int):
            problemes.append(f"{ident} : « ordre » doit être un entier")
    for parcours in architecture.get("parcours", []):
        for etape in parcours.get("etapes", []):
            if etape not in vus_id:
                problemes.append(f"parcours {parcours['id']} : étape inconnue « {etape} »")
    return problemes


def construire_donnees(racine: Path = RACINE, architecture: dict | None = None) -> dict:
    """Assemble toutes les données de la carte."""
    architecture = architecture or lire_architecture()
    realises, problemes = collecter_realises(racine)
    scripts = fusionner(architecture.get("scripts", []), realises)
    problemes += verifier_structure(scripts, architecture)
    flux, problemes_flux = calculer_flux(scripts, architecture)
    problemes += problemes_flux
    return {
        "titre": architecture.get("titre", "Carte du programme"),
        "version": architecture.get("version", ""),
        "moments": architecture.get("moments", []),
        "groupes": architecture.get("groupes", []),
        "entrees_externes": architecture.get("entrees_externes", {}),
        "parcours": architecture.get("parcours", []),
        "scripts": sorted(scripts, key=lambda s: (s.get("ordre", 0), s["id"])),
        "flux": flux,
        "problemes": problemes,
    }


def rendre_js(donnees: dict) -> str:
    """Texte de donnees.js."""
    return EN_TETE_JS + "window.CARTE = " + json.dumps(donnees, ensure_ascii=False, indent=1) + ";\n"


def main(arguments: list[str] | None = None) -> int:
    analyseur = argparse.ArgumentParser(description="Génère la carte du programme.")
    analyseur.add_argument("--verifier", action="store_true",
                           help="échoue si la carte a des problèmes ou si donnees.js est périmé")
    options = analyseur.parse_args(arguments)

    donnees = construire_donnees()
    texte = rendre_js(donnees)
    nb_realises = sum(1 for s in donnees["scripts"] if s.get("statut") == "realise")
    print(f"{len(donnees['scripts'])} scripts ({nb_realises} réalisés), "
          f"{len(donnees['flux'])} flux, {len(donnees['problemes'])} problème(s).")
    for probleme in donnees["problemes"]:
        print(f"  - {probleme}")

    if options.verifier:
        actuel = SORTIE.read_text(encoding="utf-8") if SORTIE.exists() else ""
        if actuel != texte:
            print("La carte n'est pas à jour : lancez « python carte_du_programme/generer_carte.py ».")
            return 1
        return 1 if donnees["problemes"] else 0

    SORTIE.write_text(texte, encoding="utf-8")
    print(f"Carte écrite : {SORTIE.relative_to(RACINE).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
