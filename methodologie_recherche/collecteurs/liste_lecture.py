"""Technique assistée : prépare des recherches que VOUS ouvrez dans votre navigateur.

Le logiciel ne navigue pas à votre place : il fabrique des liens de recherche (Brave Search,
Google Scholar, Europe PMC… et recherches « site: » sur les sources préférées du domaine),
rassemblés dans une page HTML de lecture. Vous ouvrez ce qui vous intéresse, puis envoyez
les pages ou PDF utiles au RAG (bouton « Envoyer au RAG » ou dossier de téléchargements surveillé).

Réglages (registre.yaml) :
    moteurs           : {nom: adresse avec {q}} ; par défaut brave, scholar, europepmc
    sites_par_requete : nombre de recherches « site: » par requête
"""

from __future__ import annotations

import html
from datetime import datetime
from pathlib import Path
from urllib.parse import quote_plus

from .contrat import Candidat, CollecteurDeBase, Politesse, Requete

__manifeste__ = {
    "nom": "collecteur_liste_lecture",
    "role": "Technique assistée : prépare des recherches et des liens que VOUS ouvrez dans votre navigateur.",
    "groupe": "methodo",
    "ordre": 10,
    "session": "S08",
    "entrees": {"requete": "une requête"},
    "sorties": {"candidats": "liens de recherche à ouvrir"},
}

MOTEURS = {
    "brave": "https://search.brave.com/search?q={q}",
    "scholar": "https://scholar.google.com/scholar?q={q}",
    "europepmc": "https://europepmc.org/search?query={q}",
}


class CollecteurListeLecture(CollecteurDeBase):
    nom = "liste_lecture"
    description = "Liens de recherche à ouvrir vous-même dans votre navigateur (collecte assistée)."
    version = "1.0"
    voie = "assistee"
    sait_rechercher = True
    sait_recuperer = False
    politesse = Politesse(requetes_par_minute=600.0, delai_min_secondes=0.0, respecte_robots_txt=False)

    def _lien(self, moteur: str, texte: str, requete: Requete) -> str:
        adresse = self.reglages.get("moteurs", MOTEURS)[moteur].replace("{q}", quote_plus(texte))
        if moteur == "scholar" and requete.filtres.get("depuis"):
            adresse += f"&as_ylo={requete.filtres['depuis'][:4]}"
        return adresse

    def rechercher(self, requete: Requete) -> list[Candidat]:
        moteurs = self.reglages.get("moteurs", MOTEURS)
        candidats = []
        for moteur in moteurs:
            candidats.append(self._candidat(moteur, requete.texte, requete))
        premier = next(iter(moteurs), None)
        sites = [s for s in requete.filtres.get("sites", "").split(",") if s]
        for site in sites[: int(self.reglages.get("sites_par_requete", 3))]:
            if premier:
                candidats.append(self._candidat(premier, f"{requete.texte} site:{site}", requete))
        return candidats[: max(requete.limite, len(moteurs))]

    def _candidat(self, moteur: str, texte: str, requete: Requete) -> Candidat:
        lien = self._lien(moteur, texte, requete)
        return Candidat(
            titre=f"{moteur} : {texte}",
            url=lien,
            source=self.nom,
            langue=requete.langue,
            identifiant=lien,
            metadonnees={"moteur": moteur, "requete": requete.texte, "a_ouvrir_par": "vous"},
        )


def ecrire_liste_lecture(candidats: list[Candidat], chemin, titre: str = "Liste de lecture") -> Path:
    """Écrit une page HTML autonome regroupant les liens par requête."""
    groupes: dict[str, list[Candidat]] = {}
    for candidat in candidats:
        groupes.setdefault(candidat.metadonnees.get("requete", candidat.titre), []).append(candidat)
    blocs = []
    for requete, liste in groupes.items():
        liens = "\n".join(
            f'      <li><a href="{html.escape(c.url or "", quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{html.escape(c.titre)}</a></li>'
            for c in liste
        )
        blocs.append(f"    <section>\n      <h2>{html.escape(requete)}</h2>\n      <ul>\n{liens}\n      </ul>\n    </section>")
    page = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titre)}</title>
  <style>
    :root {{ --fond: #ffffff; --texte: #1f2937; --lien: #1d4ed8; --bord: #e5e7eb; }}
    @media (prefers-color-scheme: dark) {{ :root {{ --fond: #111827; --texte: #e5e7eb; --lien: #93c5fd; --bord: #374151; }} }}
    body {{ background: var(--fond); color: var(--texte); font: 16px/1.5 system-ui, sans-serif;
           max-width: 52rem; margin: 0 auto; padding: 1rem; }}
    section {{ border-top: 1px solid var(--bord); padding: .5rem 0; }}
    h2 {{ font-size: 1.05rem; margin: .5rem 0; }}
    a {{ color: var(--lien); overflow-wrap: anywhere; }}
  </style>
</head>
<body>
  <h1>{html.escape(titre)}</h1>
  <p>Préparée le {datetime.now():%d/%m/%Y à %H:%M}. Ouvrez les liens qui vous intéressent, puis
  envoyez les pages ou PDF utiles au RAG (bouton « Envoyer au RAG » ou dossier surveillé).</p>
{chr(10).join(blocs)}
</body>
</html>
"""
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text(page, encoding="utf-8")
    return chemin
