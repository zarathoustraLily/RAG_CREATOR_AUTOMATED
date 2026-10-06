"""Outils réseau partagés : client HTTP identifié et lecture de robots.txt."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

from .contrat import AccesRefuse, Ralentir, SourceIndisponible

__manifeste__ = {
    "nom": "outils_http",
    "role": "Client HTTP identifié (agent utilisateur honnête), refus convertis en AccesRefuse ou Ralentir, lecture de robots.txt.",
    "groupe": "methodo",
    "ordre": 9,
    "session": "S08",
    "entrees": {},
    "sorties": {},
}

AGENT_UTILISATEUR = "RAGCreator/0.1 (outil de recherche personnel)"
CODES_REFUS = (401, 403, 429)


def agent_avec_contact(contact: str | None) -> str:
    """Agent utilisateur avec un moyen de contact (e-mail ou URL), demandé par certaines API."""
    contact = (contact or "").strip()
    return f"RAGCreator/0.1 (outil de recherche personnel; {contact})" if contact else AGENT_UTILISATEUR


def _secondes(valeur: str | None) -> float | None:
    """Lit un en-tête Retry-After exprimé en secondes (la forme date est ignorée)."""
    try:
        return float(valeur) if valeur is not None else None
    except ValueError:
        return None


@dataclass
class ReponseHttp:
    """Réponse simplifiée, facile à simuler dans les tests."""

    statut: int
    entetes: dict[str, str]
    corps: bytes

    def texte(self, encodage: str = "utf-8") -> str:
        return self.corps.decode(encodage, errors="replace")

    def json(self):
        return json.loads(self.texte())


def client_http_defaut(url, parametres=None, entetes=None, delai=30.0) -> ReponseHttp:
    """GET identifié. Lève Ralentir (429), AccesRefuse (401, 403) ou SourceIndisponible (réseau)."""
    if parametres:
        url = f"{url}?{urlencode(parametres)}"
    demande = Request(url, headers={"User-Agent": AGENT_UTILISATEUR, **(entetes or {})})
    try:
        with urlopen(demande, timeout=delai) as reponse:
            return ReponseHttp(reponse.status, dict(reponse.headers), reponse.read())
    except HTTPError as erreur:
        if erreur.code == 429:
            attente = _secondes((erreur.headers or {}).get("Retry-After"))
            raise Ralentir(f"{url} : HTTP 429 (trop de requêtes)", attente) from erreur
        if erreur.code in CODES_REFUS:
            raise AccesRefuse(f"{url} : HTTP {erreur.code}") from erreur
        return ReponseHttp(erreur.code, dict(erreur.headers or {}), erreur.read() or b"")
    except (URLError, TimeoutError, OSError) as erreur:
        raise SourceIndisponible(f"{url} : {erreur}") from erreur


def _tout_interdit() -> RobotFileParser:
    analyseur = RobotFileParser()
    analyseur.parse(["User-agent: *", "Disallow: /"])
    return analyseur


class VerificateurRobots:
    """Lit et met en cache les robots.txt (règles de la RFC 9309)."""

    def __init__(self, http, agent: str = AGENT_UTILISATEUR):
        self.http = http
        self.agent = agent
        self._cache: dict[str, RobotFileParser | None] = {}

    def autorise(self, url: str) -> bool:
        parties = urlparse(url)
        if parties.scheme not in ("http", "https"):
            return True
        base = f"{parties.scheme}://{parties.netloc}"
        if base not in self._cache:
            self._cache[base] = self._charger(base)
        analyseur = self._cache[base]
        return True if analyseur is None else analyseur.can_fetch(self.agent, url)

    def _charger(self, base: str) -> RobotFileParser | None:
        """None = aucune règle (fichier absent) ; tout interdit si le serveur est injoignable."""
        try:
            reponse = self.http(base + "/robots.txt", None, None, 15.0)
        except AccesRefuse:
            return None
        except SourceIndisponible:
            return _tout_interdit()
        if 400 <= reponse.statut < 500:
            return None
        if reponse.statut >= 500:
            return _tout_interdit()
        analyseur = RobotFileParser()
        analyseur.parse(reponse.texte().splitlines())
        return analyseur
