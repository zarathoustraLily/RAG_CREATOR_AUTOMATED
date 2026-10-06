"""Banc de mesure : compare vos techniques et vos méthodologies sur des sujets de test.

Mesures par technique : appels, candidats, nouveaux (absents des techniques précédentes),
doublons, candidats récents, refus, ralentissements, pannes, temps. Avec vos étiquettes
(pertinent : oui / non), la précision de chaque technique.

Usage :
    python -m methodologie_recherche.bancs.banc_collecte executer --domaine criminologie \\
        --sujets methodologie_recherche/bancs/sujets_exemple.yaml [--voies locale,assistee]
    python -m methodologie_recherche.bancs.banc_collecte evaluer RAPPORT.json ETIQUETTES.json
    python -m methodologie_recherche.bancs.banc_collecte comparer AVANT.json APRES.json

Une technique qui refuse l'accès ou demande de ralentir n'est plus sollicitée pendant le banc.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date, datetime
from pathlib import Path

import yaml

from ..collecteurs.contrat import AccesRefuse, Ralentir, SourceIndisponible
from ..registre import REGISTRE, charger_registre
from ..requetes import date_limite, generer_requetes_strategie
from ..strategies import charger_strategie

__manifeste__ = {
    "nom": "banc_collecte",
    "role": "Mesure vos techniques et méthodologies : rendement, nouveauté, doublons, fraîcheur, refus, temps ; précision avec vos étiquettes.",
    "groupe": "methodo",
    "ordre": 11,
    "session": "S08",
    "entrees": {"strategie": "méthodologie", "collecteurs": "techniques", "sujets_banc": "sujets de test"},
    "sorties": {"rapport_banc": "rapport de mesure (JSON et Markdown)"},
    "appelle": ["generer_requetes_strategie"],
}

DOSSIER_RAPPORTS = Path(__file__).resolve().parent.parent / "rapports"
COMPTEURS = ("appels", "candidats", "nouveaux", "doublons", "recents", "dates_connues",
             "refus", "ralentir", "indisponible", "erreurs")


def lire_sujets(chemin, domaine: str | None = None) -> list:
    """Sujets d'un fichier YAML : une liste, ou un dictionnaire {domaine: liste}."""
    with Path(chemin).open(encoding="utf-8") as fichier:
        contenu = yaml.safe_load(fichier) or []
    if isinstance(contenu, dict):
        return list(contenu.get(domaine) or [])
    return list(contenu)


def _nouvelle_mesure(collecteur) -> dict:
    return {"voie": collecteur.voie, **{c: 0 for c in COMPTEURS}, "secondes": 0.0, "arretee": None}


def executer_banc(strategie: dict, collecteurs: list, sujets_banc: list, aujourd_hui: date | None = None,
                  max_requetes: int | None = None, horloge=time.perf_counter) -> dict:
    """Interroge chaque technique (dans l'ordre de la méthodologie) sur chaque sujet."""
    aujourd_hui = aujourd_hui or date.today()
    limite_recent = date_limite(aujourd_hui, strategie.get("fraicheur_mois") or 12).isoformat()
    par_nom = {c.nom: c for c in collecteurs}
    ordre = [nom for nom in strategie.get("techniques", []) if nom in par_nom]
    mesures = {nom: _nouvelle_mesure(par_nom[nom]) for nom in ordre}
    vus: set[str] = set()
    candidats_vus, messages, nombre_requetes = [], [], 0

    for sujet in sujets_banc:
        requetes = generer_requetes_strategie(strategie, sujet, aujourd_hui=aujourd_hui)
        if max_requetes is not None:
            requetes = requetes[: max(0, max_requetes - nombre_requetes)]
        nombre_requetes += len(requetes)
        for requete in requetes:
            for nom in ordre:
                mesure, collecteur = mesures[nom], par_nom[nom]
                if mesure["arretee"]:
                    continue
                debut = horloge()
                try:
                    trouves = collecteur.rechercher(requete)
                except Ralentir as erreur:
                    mesure["ralentir"] += 1
                    mesure["arretee"] = f"ralentissement demandé : {erreur}"
                    trouves = []
                except AccesRefuse as erreur:
                    mesure["refus"] += 1
                    mesure["arretee"] = f"accès refusé : {erreur}"
                    trouves = []
                except SourceIndisponible as erreur:
                    mesure["indisponible"] += 1
                    messages.append(f"{nom} : {erreur}")
                    trouves = []
                except Exception as erreur:  # noqa: BLE001 — le banc mesure aussi les pannes
                    mesure["erreurs"] += 1
                    messages.append(f"{nom} : {type(erreur).__name__} : {erreur}")
                    trouves = []
                mesure["secondes"] += horloge() - debut
                mesure["appels"] += 1
                mesure["candidats"] += len(trouves)
                for candidat in trouves:
                    if candidat.date:
                        mesure["dates_connues"] += 1
                        mesure["recents"] += candidat.date >= limite_recent
                    cle = candidat.cle()
                    if cle in vus:
                        mesure["doublons"] += 1
                        continue
                    vus.add(cle)
                    mesure["nouveaux"] += 1
                    candidats_vus.append({
                        "cle": cle, "technique": nom, "titre": candidat.titre, "url": candidat.url,
                        "date": candidat.date, "requete": requete.texte, "langue": requete.langue,
                    })
    for mesure in mesures.values():
        mesure["secondes"] = round(mesure["secondes"], 3)
        mesure["secondes_par_appel"] = round(mesure["secondes"] / mesure["appels"], 3) if mesure["appels"] else None
    rapport_banc = {
        "date": datetime.now().isoformat(timespec="seconds"),
        "domaine": strategie.get("domaine"),
        "heritage": strategie.get("heritage", []),
        "sujets": len(sujets_banc),
        "requetes": nombre_requetes,
        "recent_depuis": limite_recent,
        "techniques": mesures,
        "ignorees": sorted(set(par_nom) - set(ordre)),
        "candidats": candidats_vus,
        "messages": messages,
    }
    return rapport_banc


def evaluer(rapport_banc: dict, etiquettes: dict) -> dict:
    """Ajoute la précision de chaque technique d'après vos étiquettes {cle: true/false}."""
    for nom, mesure in rapport_banc["techniques"].items():
        jugees = [etiquettes[c["cle"]] for c in rapport_banc["candidats"]
                  if c["technique"] == nom and etiquettes.get(c["cle"]) is not None]
        mesure["etiquetes"] = len(jugees)
        mesure["pertinents"] = sum(bool(j) for j in jugees)
        mesure["precision"] = round(mesure["pertinents"] / len(jugees), 3) if jugees else None
    return rapport_banc


def gabarit_etiquettes(rapport_banc: dict) -> dict:
    """Fichier à remplir : chaque candidat avec « pertinent » à null (mettez true ou false)."""
    return {c["cle"]: None for c in rapport_banc["candidats"]}


MESURES_COMPAREES = ("candidats", "nouveaux", "doublons", "recents", "refus", "ralentir",
                     "secondes_par_appel", "precision")


def comparer(avant: dict, apres: dict) -> list[dict]:
    """Une ligne par technique et par mesure : valeur avant, après, écart."""
    lignes = []
    for nom in sorted(set(avant["techniques"]) | set(apres["techniques"])):
        a, b = avant["techniques"].get(nom, {}), apres["techniques"].get(nom, {})
        for mesure in MESURES_COMPAREES:
            va, vb = a.get(mesure), b.get(mesure)
            if va is None and vb is None:
                continue
            ecart = round(vb - va, 3) if isinstance(va, (int, float)) and isinstance(vb, (int, float)) else None
            lignes.append({"technique": nom, "mesure": mesure, "avant": va, "apres": vb, "ecart": ecart})
    return lignes


def rendre_markdown(rapport_banc: dict) -> str:
    entete = ["technique", "voie", "appels", "candidats", "nouveaux", "doublons", "récents",
              "refus", "ralentir", "pannes", "s/appel", "précision"]
    lignes = [
        f"# Banc de collecte — {rapport_banc['domaine']} ({rapport_banc['date']})",
        "",
        f"Méthodologie : {' ← '.join(rapport_banc['heritage']) or rapport_banc['domaine']} ; "
        f"{rapport_banc['sujets']} sujets, {rapport_banc['requetes']} requêtes ; "
        f"récent = publié depuis le {rapport_banc['recent_depuis']}.",
        "",
        "| " + " | ".join(entete) + " |",
        "|" + "---|" * len(entete),
    ]
    for nom, m in rapport_banc["techniques"].items():
        valeurs = [nom, m["voie"], m["appels"], m["candidats"], m["nouveaux"], m["doublons"],
                   f"{m['recents']}/{m['dates_connues']}", m["refus"], m["ralentir"],
                   m["indisponible"] + m["erreurs"], m["secondes_par_appel"], m.get("precision")]
        lignes.append("| " + " | ".join("—" if v is None else str(v) for v in valeurs) + " |")
    arretees = [f"- {nom} : {m['arretee']}" for nom, m in rapport_banc["techniques"].items() if m["arretee"]]
    if arretees:
        lignes += ["", "Techniques arrêtées pendant le banc :", *arretees]
    if rapport_banc["messages"]:
        lignes += ["", "Messages :", *[f"- {m}" for m in rapport_banc["messages"][:20]]]
    return "\n".join(lignes) + "\n"


def rendre_comparaison(lignes: list[dict]) -> str:
    sortie = ["| technique | mesure | avant | après | écart |", "|---|---|---|---|---|"]
    for ligne in lignes:
        valeurs = [ligne[c] for c in ("technique", "mesure", "avant", "apres", "ecart")]
        sortie.append("| " + " | ".join("—" if v is None else str(v) for v in valeurs) + " |")
    return "\n".join(sortie) + "\n"


def _ecrire_json(chemin: Path, donnees) -> None:
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8")


def principal(arguments=None, http=None) -> int:
    analyseur = argparse.ArgumentParser(description="Banc de mesure de la collecte.")
    commandes = analyseur.add_subparsers(dest="commande", required=True)
    executer = commandes.add_parser("executer", help="mesurer une méthodologie et ses techniques")
    executer.add_argument("--domaine", required=True)
    executer.add_argument("--sujets", required=True, help="fichier YAML des sujets")
    executer.add_argument("--registre", default=str(REGISTRE))
    executer.add_argument("--voies", default="", help="ex. locale,assistee (toutes par défaut)")
    executer.add_argument("--max-requetes", type=int, default=None)
    executer.add_argument("--sortie", default=str(DOSSIER_RAPPORTS))
    evaluation = commandes.add_parser("evaluer", help="ajouter la précision d'après vos étiquettes")
    evaluation.add_argument("rapport")
    evaluation.add_argument("etiquettes")
    comparaison = commandes.add_parser("comparer", help="comparer deux rapports")
    comparaison.add_argument("avant")
    comparaison.add_argument("apres")
    options = analyseur.parse_args(arguments)

    if options.commande == "executer":
        strategie = charger_strategie(options.domaine)
        collecteurs, problemes_registre = charger_registre(options.registre, http=http)
        voies = {v for v in options.voies.split(",") if v}
        if voies:
            collecteurs = [c for c in collecteurs if c.voie in voies]
        sujets_banc = lire_sujets(options.sujets, options.domaine)
        if not sujets_banc:
            print(f"Aucun sujet pour le domaine « {options.domaine} » dans {options.sujets}.", file=sys.stderr)
            return 2
        rapport_banc = executer_banc(strategie, collecteurs, sujets_banc, max_requetes=options.max_requetes)
        rapport_banc["problemes_registre"] = problemes_registre
        base = Path(options.sortie) / f"{datetime.now():%Y%m%d_%H%M%S}_{options.domaine}"
        _ecrire_json(base.with_suffix(".json"), rapport_banc)
        base.with_suffix(".md").write_text(rendre_markdown(rapport_banc), encoding="utf-8")
        _ecrire_json(base.parent / f"{base.name}_etiquettes.json", gabarit_etiquettes(rapport_banc))
        print(rendre_markdown(rapport_banc))
        print(f"Rapport : {base.with_suffix('.json')}")
        print(f"Étiquettes à remplir (true/false) : {base.parent / (base.name + '_etiquettes.json')}")
        return 0
    if options.commande == "evaluer":
        chemin = Path(options.rapport)
        rapport_banc = evaluer(json.loads(chemin.read_text(encoding="utf-8")),
                               json.loads(Path(options.etiquettes).read_text(encoding="utf-8")))
        _ecrire_json(chemin, rapport_banc)
        chemin.with_suffix(".md").write_text(rendre_markdown(rapport_banc), encoding="utf-8")
        print(rendre_markdown(rapport_banc))
        return 0
    avant = json.loads(Path(options.avant).read_text(encoding="utf-8"))
    apres = json.loads(Path(options.apres).read_text(encoding="utf-8"))
    print(rendre_comparaison(comparer(avant, apres)))
    return 0


if __name__ == "__main__":
    sys.exit(principal())
