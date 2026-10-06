"""Technique automatique : publications scientifiques via l'API OpenAlex.

Sans clé, OpenAlex accorde un petit budget quotidien PARTAGÉ par toutes les machines de la
même adresse IP ; une fois épuisé, il répond 429. Une clé gratuite (compte sur openalex.org,
puis openalex.org/settings/api) donne un budget dix fois plus grand, réservé à vous.

Réglages (registre.yaml) :
    cle_api  : votre clé ; mieux : variable d'environnement RAGC_OPENALEX_CLE (hors du dépôt)
    par_page : nombre de résultats par requête (100 au plus)

La recherche passe par l'API ; le téléchargement d'un PDF en accès libre, sur le site de
l'éditeur, respecte le robots.txt de ce site.
"""

from __future__ import annotations

import os

from .contrat import AccesRefuse, Candidat, CollecteurDeBase, Document, Politesse, Requete, SourceIndisponible

__manifeste__ = {
    "nom": "collecteur_openalex",
    "role": "Technique automatique : publications scientifiques via l'API OpenAlex (clé gratuite conseillée).",
    "groupe": "methodo",
    "ordre": 10,
    "session": "S08",
    "entrees": {"requete": "une requête"},
    "sorties": {"candidats": "candidats trouvés", "document_collecte": "PDF en accès libre"},
}

ADRESSE = "https://api.openalex.org/works"
CHAMPS = ("id,display_name,publication_date,doi,language,type,cited_by_count,"
          "abstract_inverted_index,open_access,best_oa_location,primary_location")


def resume_depuis_index(index: dict | None) -> str:
    """Reconstitue le résumé à partir de l'index inversé d'OpenAlex ({mot: [positions]})."""
    if not index:
        return ""
    positions = {position: mot for mot, liste in index.items() for position in liste}
    return " ".join(positions[i] for i in sorted(positions))


class CollecteurOpenAlex(CollecteurDeBase):
    nom = "openalex"
    description = "Publications scientifiques (métadonnées, résumés, PDF en accès libre) via OpenAlex."
    version = "1.0"
    voie = "automatique"
    sait_rechercher = True
    sait_recuperer = True
    politesse = Politesse(requetes_par_minute=30.0, delai_min_secondes=1.0, respecte_robots_txt=True)

    def _entetes(self) -> dict[str, str]:
        cle = self.reglages.get("cle_api") or os.environ.get("RAGC_OPENALEX_CLE", "")
        return {"Authorization": f"Bearer {cle}"} if cle else {}

    def parametres(self, requete: Requete) -> dict[str, str]:
        """Paramètres de l'appel à l'API (séparés pour être testés)."""
        filtres = [f"language:{requete.langue}"] if requete.langue else []
        if requete.filtres.get("depuis"):
            filtres.append(f"from_publication_date:{requete.filtres['depuis']}")
        parametres = {
            "search": requete.texte,
            "per-page": str(min(int(self.reglages.get("par_page", requete.limite)), 100)),
            "select": CHAMPS,
        }
        if filtres:
            parametres["filter"] = ",".join(filtres)
        return parametres

    def rechercher(self, requete: Requete) -> list[Candidat]:
        self.patienter()
        reponse = self.http(ADRESSE, self.parametres(requete), self._entetes(), 30.0)
        if reponse.statut != 200:
            raise SourceIndisponible(f"OpenAlex : HTTP {reponse.statut}")
        candidats = []
        for oeuvre in reponse.json().get("results", [])[: requete.limite]:
            lieu_libre = oeuvre.get("best_oa_location") or {}
            source = ((oeuvre.get("primary_location") or {}).get("source") or {}).get("display_name")
            candidats.append(Candidat(
                titre=oeuvre.get("display_name") or "(sans titre)",
                url=oeuvre.get("doi") or lieu_libre.get("landing_page_url") or oeuvre.get("id"),
                source=self.nom,
                extrait=resume_depuis_index(oeuvre.get("abstract_inverted_index"))[:2000],
                date=oeuvre.get("publication_date"),
                langue=oeuvre.get("language"),
                identifiant=oeuvre.get("doi") or oeuvre.get("id"),
                metadonnees={
                    "openalex": oeuvre.get("id"),
                    "type": oeuvre.get("type"),
                    "citations": oeuvre.get("cited_by_count"),
                    "revue": source,
                    "acces_libre": (oeuvre.get("open_access") or {}).get("is_oa", False),
                    "pdf": lieu_libre.get("pdf_url"),
                },
            ))
        return candidats

    def recuperer(self, candidat: Candidat) -> Document | None:
        adresse_pdf = candidat.metadonnees.get("pdf")
        if not adresse_pdf:
            return None
        if not self.autorise(adresse_pdf):
            raise AccesRefuse(f"robots.txt interdit {adresse_pdf} : à récupérer vous-même (collecte assistée)")
        self.patienter()
        reponse = self.http(adresse_pdf, None, None, 60.0)
        if reponse.statut == 404:
            return None
        if reponse.statut != 200:
            raise SourceIndisponible(f"{adresse_pdf} : HTTP {reponse.statut}")
        type_mime = next((v for k, v in reponse.entetes.items() if k.lower() == "content-type"), "")
        if "pdf" not in type_mime.lower() and not reponse.corps.startswith(b"%PDF"):
            return None  # page d'accueil de l'éditeur plutôt qu'un PDF
        document_collecte = Document(candidat=candidat, contenu=reponse.corps, type_mime="application/pdf")
        return document_collecte
