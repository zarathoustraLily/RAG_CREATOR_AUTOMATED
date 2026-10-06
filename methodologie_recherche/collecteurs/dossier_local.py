"""Technique locale : cherche dans vos dossiers de documents (aucun accès réseau).

Réglages (registre.yaml) :
    dossiers   : liste de dossiers à parcourir (le ~ est accepté)
    extensions : extensions retenues
    seuil      : part des mots de la requête qui doit apparaître (0 à 1)
"""

from __future__ import annotations

import mimetypes
import re
import unicodedata
from pathlib import Path

from .contrat import Candidat, CollecteurDeBase, Document, Politesse, Requete

__manifeste__ = {
    "nom": "collecteur_dossier_local",
    "role": "Technique locale : vos documents déposés dans des dossiers.",
    "groupe": "methodo",
    "ordre": 10,
    "session": "S08",
    "entrees": {"requete": "une requête"},
    "sorties": {"candidats": "candidats trouvés", "document_collecte": "contenu récupéré"},
}

EXTENSIONS = [".pdf", ".epub", ".txt", ".md", ".html", ".htm", ".docx", ".odt"]
TEXTE_LISIBLE = {".txt", ".md", ".html", ".htm"}
TAILLE_LUE = 200_000  # octets lus au début des fichiers texte pour chercher les mots
MOTS_VIDES = {
    "les", "des", "une", "dans", "pour", "par", "sur", "avec", "aux", "du", "de", "la", "le",
    "the", "and", "for", "with", "from", "into", "of", "in", "on",
}


def mots(texte: str) -> set[str]:
    """Mots significatifs, en minuscules et sans accents."""
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    return {m for m in re.split(r"[^a-z0-9]+", sans_accents.lower()) if len(m) > 2 and m not in MOTS_VIDES}


class CollecteurDossierLocal(CollecteurDeBase):
    nom = "dossier_local"
    description = "Vos documents déposés dans des dossiers (PDF, livres, articles, notes)."
    version = "1.0"
    voie = "locale"
    sait_rechercher = True
    sait_recuperer = True
    politesse = Politesse(requetes_par_minute=600.0, delai_min_secondes=0.0, respecte_robots_txt=False)

    def _fichiers(self):
        extensions = {e.lower() for e in self.reglages.get("extensions", EXTENSIONS)}
        for dossier in self.reglages.get("dossiers", []):
            racine = Path(dossier).expanduser()
            if not racine.is_dir():
                continue
            for chemin in sorted(racine.rglob("*")):
                if chemin.is_file() and chemin.suffix.lower() in extensions:
                    yield chemin

    def _mots_du_fichier(self, chemin: Path) -> set[str]:
        trouves = mots(chemin.stem)
        if chemin.suffix.lower() in TEXTE_LISIBLE:
            with chemin.open("rb") as fichier:
                trouves |= mots(fichier.read(TAILLE_LUE).decode("utf-8", errors="ignore"))
        return trouves

    def rechercher(self, requete: Requete) -> list[Candidat]:
        cherches = mots(requete.texte)
        if not cherches:
            return []
        seuil = float(self.reglages.get("seuil", 0.5))
        resultats = []
        for chemin in self._fichiers():
            score = len(cherches & self._mots_du_fichier(chemin)) / len(cherches)
            if score >= seuil:
                resultats.append((score, chemin))
        resultats.sort(key=lambda r: (-r[0], str(r[1])))
        candidats = []
        for score, chemin in resultats[: requete.limite]:
            candidats.append(Candidat(
                titre=chemin.stem.replace("_", " "),
                url=chemin.resolve().as_uri(),
                source=self.nom,
                identifiant=str(chemin.resolve()),
                metadonnees={"score": round(score, 3), "chemin": str(chemin)},
            ))
        return candidats

    def recuperer(self, candidat: Candidat) -> Document | None:
        chemin = Path(candidat.metadonnees.get("chemin") or candidat.identifiant or "")
        if not chemin.is_file():
            return None
        type_mime = mimetypes.guess_type(chemin.name)[0] or "application/octet-stream"
        document_collecte = Document(candidat=candidat, contenu=chemin.read_bytes(),
                                     type_mime=type_mime, chemin_local=str(chemin))
        return document_collecte
