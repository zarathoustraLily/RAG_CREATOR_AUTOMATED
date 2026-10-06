"""Technique automatique : articles de Wikipédia via l'API officielle (MediaWiki).

Wikimedia limite les clients anonymes (10 requêtes par minute, partagées par l'adresse IP) et
accorde bien plus à un client qui donne un moyen de contact dans son agent utilisateur.
Réglages (registre.yaml) :
    contact : votre e-mail ou une URL ; mieux : variable d'environnement RAGC_CONTACT

Le robots.txt de Wikipédia interdit /w/ aux robots d'exploration ; l'API, elle, est faite pour
les programmes et suit ses propres règles (agent identifié, rythme modéré, maxlag) : cette
technique les applique et ne parcourt pas les pages du site.
"""

from __future__ import annotations

import html
import os
import re
from urllib.parse import quote

from .contrat import Candidat, CollecteurDeBase, Document, Politesse, Requete, SourceIndisponible
from .outils_http import agent_avec_contact

__manifeste__ = {
    "nom": "collecteur_wikipedia",
    "role": "Technique automatique : articles de Wikipédia via son API (contact conseillé).",
    "groupe": "methodo",
    "ordre": 10,
    "session": "S08",
    "entrees": {"requete": "une requête"},
    "sorties": {"candidats": "candidats trouvés", "document_collecte": "contenu de l'article"},
}

AVEC_CONTACT = Politesse(requetes_par_minute=30.0, delai_min_secondes=1.0, respecte_robots_txt=False)
SANS_CONTACT = Politesse(requetes_par_minute=5.0, delai_min_secondes=12.0, respecte_robots_txt=False)


def sans_balises(texte: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", texte or ""))


class CollecteurWikipedia(CollecteurDeBase):
    nom = "wikipedia"
    description = "Articles de Wikipédia (contexte, définitions, pistes de sources) via l'API MediaWiki."
    version = "1.0"
    voie = "automatique"
    sait_rechercher = True
    sait_recuperer = True
    politesse = SANS_CONTACT

    def __init__(self, reglages=None, **options):
        super().__init__(reglages, **options)
        self.contact = self.reglages.get("contact") or os.environ.get("RAGC_CONTACT", "")
        self.politesse = AVEC_CONTACT if self.contact else SANS_CONTACT

    def _appeler(self, langue: str, parametres: dict) -> dict:
        self.patienter()
        adresse = f"https://{langue}.wikipedia.org/w/api.php"
        communs = {"format": "json", "formatversion": "2", "utf8": "1", "maxlag": "5"}
        reponse = self.http(adresse, {**parametres, **communs},
                            {"User-Agent": agent_avec_contact(self.contact)}, 30.0)
        if reponse.statut != 200:
            raise SourceIndisponible(f"Wikipédia ({langue}) : HTTP {reponse.statut}")
        donnees = reponse.json()
        if "error" in donnees:
            raise SourceIndisponible(f"Wikipédia ({langue}) : {donnees['error'].get('info', donnees['error'])}")
        return donnees

    def rechercher(self, requete: Requete) -> list[Candidat]:
        langue = requete.langue or "fr"
        donnees = self._appeler(langue, {
            "action": "query", "list": "search", "srsearch": requete.texte,
            "srlimit": str(min(requete.limite, 50)),
        })
        candidats = []
        for page in donnees.get("query", {}).get("search", []):
            titre = page.get("title", "")
            candidats.append(Candidat(
                titre=titre,
                url=f"https://{langue}.wikipedia.org/wiki/{quote(titre.replace(' ', '_'))}",
                source=self.nom,
                extrait=sans_balises(page.get("snippet", "")),
                date=(page.get("timestamp") or "")[:10] or None,
                langue=langue,
                identifiant=f"wikipedia:{langue}:{page.get('pageid')}",
                metadonnees={"pageid": page.get("pageid"), "langue": langue, "mots": page.get("wordcount")},
            ))
        return candidats

    def recuperer(self, candidat: Candidat) -> Document | None:
        langue = candidat.metadonnees.get("langue") or candidat.langue or "fr"
        donnees = self._appeler(langue, {
            "action": "query", "prop": "extracts", "explaintext": "1",
            "pageids": str(candidat.metadonnees.get("pageid")),
        })
        pages = donnees.get("query", {}).get("pages", [])
        texte = pages[0].get("extract") if pages else None
        if not texte:
            return None
        document_collecte = Document(candidat=candidat, contenu=texte.encode("utf-8"),
                                     type_mime="text/plain; charset=utf-8")
        return document_collecte
