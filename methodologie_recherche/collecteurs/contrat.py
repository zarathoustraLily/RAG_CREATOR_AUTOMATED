"""Contrat que toute technique de recherche (collecteur) doit respecter.

Le logiciel RAG Creator ne connaît que ce contrat : vous pouvez modifier ou ajouter des
techniques sans toucher au reste du code. Si vous changez ce contrat, incrémentez
VERSION_CONTRAT (le registre vérifie la compatibilité).
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

__manifeste__ = {
    "nom": "contrat_collecteur",
    "role": "Définit le contrat des techniques : requête, candidat, document, politesse, erreurs.",
    "groupe": "methodo",
    "ordre": 8,
    "session": "S08",
    "entrees": {},
    "sorties": {},
}

VERSION_CONTRAT = "1.0"
VOIES = ("locale", "automatique", "assistee")
NOM_VALIDE = re.compile(r"^[a-z][a-z0-9_]*$")


@dataclass(frozen=True)
class Requete:
    """Ce que le logiciel demande à une technique."""

    texte: str
    langue: str = "fr"
    theme: str | None = None
    sous_question: str | None = None
    filtres: dict[str, str] = field(default_factory=dict)
    limite: int = 20


@dataclass
class Candidat:
    """Un résultat trouvé, pas encore téléchargé."""

    titre: str
    url: str | None
    source: str
    extrait: str = ""
    date: str | None = None
    langue: str | None = None
    identifiant: str | None = None
    metadonnees: dict[str, Any] = field(default_factory=dict)

    def cle(self) -> str:
        """Clé de dédoublonnage : identifiant, sinon URL, sinon titre."""
        return (self.identifiant or self.url or self.titre).strip().lower()


@dataclass
class Document:
    """Contenu récupéré pour un candidat."""

    candidat: Candidat
    contenu: bytes
    type_mime: str
    chemin_local: str | None = None
    metadonnees: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Politesse:
    """Rythme que la technique s'engage à respecter envers sa source."""

    requetes_par_minute: float = 10.0
    delai_min_secondes: float = 1.0
    respecte_robots_txt: bool = True

    def delai(self) -> float:
        """Délai minimal entre deux appels, en secondes."""
        return max(self.delai_min_secondes, 60.0 / self.requetes_par_minute)


class ErreurCollecteur(Exception):
    """Erreur générique d'une technique."""


class SourceIndisponible(ErreurCollecteur):
    """La source ne répond pas (réseau, panne) : on réessaiera plus tard."""


class AccesRefuse(ErreurCollecteur):
    """La source refuse l'accès (401, 403…) : ne pas insister ; bascule vers la collecte assistée."""


class Ralentir(AccesRefuse):
    """La source demande de ralentir (HTTP 429) : attendre `reessayer_apres` secondes."""

    def __init__(self, message: str, reessayer_apres: float | None = None):
        super().__init__(message)
        self.reessayer_apres = reessayer_apres


@runtime_checkable
class Collecteur(Protocol):
    """Interface d'une technique de recherche."""

    nom: str
    description: str
    version: str
    voie: str
    sait_rechercher: bool
    sait_recuperer: bool
    politesse: Politesse

    def rechercher(self, requete: Requete) -> list[Candidat]: ...

    def recuperer(self, candidat: Candidat) -> Document | None: ...


class CollecteurDeBase:
    """Base pratique : réglages, client HTTP injectable (tests), robots.txt et respect du rythme."""

    nom = "a_definir"
    description = ""
    version = "0.1"
    voie = "automatique"
    sait_rechercher = True
    sait_recuperer = False
    politesse = Politesse()

    def __init__(self, reglages=None, http=None, horloge=time.monotonic, attendre=time.sleep):
        from .outils_http import VerificateurRobots, client_http_defaut  # évite un import circulaire

        self.reglages = dict(reglages or {})
        self.http = http or client_http_defaut
        self.robots = VerificateurRobots(self.http)
        self._horloge = horloge
        self._attendre = attendre
        self._dernier_appel: float | None = None

    def patienter(self) -> None:
        """Attend ce qu'il faut pour respecter la politesse déclarée."""
        if self._dernier_appel is not None:
            reste = self.politesse.delai() - (self._horloge() - self._dernier_appel)
            if reste > 0:
                self._attendre(reste)
        self._dernier_appel = self._horloge()

    def autorise(self, url: str) -> bool:
        """Vrai si robots.txt autorise l'URL (ou si la technique n'y est pas soumise)."""
        return not self.politesse.respecte_robots_txt or self.robots.autorise(url)

    def rechercher(self, requete: Requete) -> list[Candidat]:
        raise NotImplementedError

    def recuperer(self, candidat: Candidat) -> Document | None:
        return None


def verifier_conformite(collecteur: object) -> list[str]:
    """Liste les écarts au contrat (liste vide si la technique est conforme)."""
    problemes = []
    attendus = {"nom": str, "description": str, "version": str, "voie": str,
                "sait_rechercher": bool, "sait_recuperer": bool}
    for attribut, type_attendu in attendus.items():
        if not isinstance(getattr(collecteur, attribut, None), type_attendu):
            problemes.append(f"attribut « {attribut} » absent ou de mauvais type")
    nom = getattr(collecteur, "nom", "")
    if isinstance(nom, str) and not NOM_VALIDE.match(nom):
        problemes.append("« nom » : lettres minuscules, chiffres et _ uniquement")
    if not getattr(collecteur, "description", ""):
        problemes.append("« description » vide")
    if getattr(collecteur, "voie", None) not in VOIES:
        problemes.append(f"« voie » doit valoir l'une de : {', '.join(VOIES)}")
    politesse = getattr(collecteur, "politesse", None)
    if not isinstance(politesse, Politesse):
        problemes.append("« politesse » doit être une instance de Politesse")
    elif politesse.requetes_par_minute <= 0 or politesse.delai_min_secondes < 0:
        problemes.append("« politesse » : rythme invalide")
    if not callable(getattr(collecteur, "rechercher", None)):
        problemes.append("méthode « rechercher » absente")
    if getattr(collecteur, "sait_recuperer", False) and not callable(getattr(collecteur, "recuperer", None)):
        problemes.append("« sait_recuperer » est vrai mais « recuperer » est absente")
    return problemes
