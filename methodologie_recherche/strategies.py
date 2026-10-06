"""Charge la méthodologie de recherche d'un domaine (fichiers YAML de strategies/).

Chaque domaine hérite d'un autre (`herite`, par défaut la méthodologie commune).
Fusion, du plus général au plus précis :
- valeurs simples : le domaine le plus précis l'emporte ;
- listes : celles du domaine passent en premier, puis celles dont il hérite, sans doublon ;
- dictionnaires : fusionnés clé par clé avec les mêmes règles ;
- `retirer` : enlève des éléments hérités, ex. `retirer: {techniques: [wikipedia]}`.
"""

from __future__ import annotations

from pathlib import Path

import yaml

__manifeste__ = {
    "nom": "charger_strategie",
    "role": "Charge la méthodologie d'un domaine (YAML) et la fusionne avec celles dont elle hérite.",
    "groupe": "methodo",
    "ordre": 8,
    "session": "S08",
    "entrees": {"domaine": "nom du domaine"},
    "sorties": {"strategie": "méthodologie du domaine"},
    "lit": ["methodologie_recherche/strategies/*.yaml"],
}

DOSSIER_STRATEGIES = Path(__file__).resolve().parent / "strategies"
COMMUN = "commun"
CLES_CONNUES = {
    "domaine", "description", "herite", "retirer", "langues", "fraicheur_mois",
    "filtrer_par_date", "techniques", "gabarits", "sources_preferees", "sources_exclues",
    "angles_obligatoires", "criteres_tri", "cadrage", "remarques",
}


class StrategieInvalide(ValueError):
    """Fichier de méthodologie illisible, introuvable ou incohérent."""


def domaines_disponibles(dossier: Path = DOSSIER_STRATEGIES) -> list[str]:
    """Noms des méthodologies présentes dans le dossier."""
    return sorted(chemin.stem for chemin in Path(dossier).glob("*.yaml"))


def _lire(nom: str, dossier: Path) -> dict:
    chemin = Path(dossier) / f"{nom}.yaml"
    if not chemin.exists():
        raise StrategieInvalide(f"méthodologie « {nom} » introuvable ({chemin})")
    with chemin.open(encoding="utf-8") as fichier:
        contenu = yaml.safe_load(fichier) or {}
    if not isinstance(contenu, dict):
        raise StrategieInvalide(f"{chemin.name} : le fichier doit contenir un dictionnaire")
    return contenu


def _fusionner(general, precis):
    """Fusionne deux valeurs : le plus précis l'emporte, les listes s'additionnent."""
    if isinstance(general, dict) and isinstance(precis, dict):
        resultat = dict(general)
        for cle, valeur in precis.items():
            resultat[cle] = _fusionner(general[cle], valeur) if cle in general else valeur
        return resultat
    if isinstance(general, list) and isinstance(precis, list):
        resultat = []
        for element in precis + general:
            if element not in resultat:
                resultat.append(element)
        return resultat
    return precis


def _retirer(strategie: dict, a_retirer: dict) -> dict:
    for cle, elements in (a_retirer or {}).items():
        valeur = strategie.get(cle)
        if isinstance(valeur, list):
            strategie[cle] = [e for e in valeur if e not in elements]
        elif isinstance(valeur, dict) and isinstance(elements, dict):
            _retirer(valeur, elements)
        elif isinstance(valeur, dict):
            for element in elements:
                valeur.pop(element, None)
    return strategie


def _chaine(domaine: str, dossier: Path) -> list[tuple[str, dict]]:
    """Liste [(nom, contenu)] du domaine jusqu'à la méthodologie commune."""
    chaine, nom = [], domaine
    while True:
        if nom in [n for n, _ in chaine]:
            raise StrategieInvalide(f"héritage circulaire : {' → '.join([n for n, _ in chaine] + [nom])}")
        contenu = _lire(nom, dossier)
        chaine.append((nom, contenu))
        if nom == COMMUN:
            return chaine
        nom = contenu.get("herite", COMMUN)


def charger_strategie(domaine: str, dossier: Path = DOSSIER_STRATEGIES, strict: bool = False) -> dict:
    """Méthodologie complète d'un domaine.

    Domaine inconnu : méthodologie commune (`repli_commun` vaut True), sauf si `strict`.
    """
    dossier = Path(dossier)
    if not (dossier / f"{domaine}.yaml").exists() and not strict:
        strategie = charger_strategie(COMMUN, dossier, strict=True)
        return {**strategie, "domaine": domaine, "repli_commun": True}
    chaine = _chaine(domaine, dossier)
    strategie: dict = {}
    for _nom, contenu in reversed(chaine):
        propre = {cle: valeur for cle, valeur in contenu.items() if cle not in ("retirer", "herite")}
        strategie = _fusionner(strategie, propre)
        strategie = _retirer(strategie, contenu.get("retirer"))
    strategie["domaine"] = domaine
    strategie["heritage"] = [nom for nom, _ in chaine]
    strategie["repli_commun"] = False
    return strategie


def verifier_strategie(strategie: dict) -> list[str]:
    """Liste les incohérences d'une méthodologie chargée (liste vide si tout va bien)."""
    problemes = []
    inconnues = set(strategie) - CLES_CONNUES - {"heritage", "repli_commun"}
    if inconnues:
        problemes.append(f"clés inconnues (faute de frappe ?) : {', '.join(sorted(inconnues))}")
    langues = strategie.get("langues") or []
    if not langues:
        problemes.append("« langues » est vide")
    gabarits = strategie.get("gabarits") or {}
    for langue in langues:
        if not gabarits.get(langue):
            problemes.append(f"aucun gabarit de requête pour la langue « {langue} »")
    for langue, liste in gabarits.items():
        for gabarit in liste or []:
            texte = gabarit.get("texte") if isinstance(gabarit, dict) else gabarit
            if not isinstance(texte, str) or "{sujet}" not in texte:
                problemes.append(f"gabarit {langue} sans « {{sujet}} » : {gabarit!r}")
    fraicheur = strategie.get("fraicheur_mois")
    if fraicheur is not None and (not isinstance(fraicheur, int) or fraicheur <= 0):
        problemes.append("« fraicheur_mois » doit être un entier positif")
    if not strategie.get("techniques"):
        problemes.append("« techniques » est vide : aucune technique de recherche")
    return problemes
