"""Outils communs des tests : client HTTP simulé, option --reseau pour les tests réels."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[2]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from methodologie_recherche.collecteurs.outils_http import ReponseHttp  # noqa: E402

JEUX = Path(__file__).resolve().parent / "jeux"


def pytest_addoption(parser):
    parser.addoption("--reseau", action="store_true", default=False,
                     help="lance aussi les tests qui interrogent les vraies sources")


def pytest_configure(config):
    config.addinivalue_line("markers", "reseau: test qui interroge une vraie source (lent, réseau)")


def pytest_collection_modifyitems(config, items):
    reseau = config.getoption("--reseau", default=False) or os.environ.get("RAGC_TESTS_RESEAU") == "1"
    if reseau:
        return
    passer = pytest.mark.skip(reason="test réseau : ajoutez --reseau (ou RAGC_TESTS_RESEAU=1)")
    for item in items:
        if "reseau" in item.keywords:
            item.add_marker(passer)


class HttpSimule:
    """Remplace le réseau : associe un début d'URL à une réponse ou à une exception."""

    def __init__(self, routes=None):
        self.routes = dict(routes or {})
        self.appels = []

    def __call__(self, url, parametres=None, entetes=None, delai=30.0):
        self.appels.append({"url": url, "parametres": parametres or {}, "entetes": entetes or {}})
        for prefixe in sorted(self.routes, key=len, reverse=True):
            if url.startswith(prefixe):
                reponse = self.routes[prefixe]
                if isinstance(reponse, Exception):
                    raise reponse
                return reponse
        return ReponseHttp(404, {}, b"")


def reponse_json(donnees, statut=200):
    return ReponseHttp(statut, {"Content-Type": "application/json"}, json.dumps(donnees).encode())


def jeu(nom):
    """Lit un jeu de données fictif de tests/jeux/."""
    return json.loads((JEUX / nom).read_text(encoding="utf-8"))


@pytest.fixture
def http_simule():
    return HttpSimule()
