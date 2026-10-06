"""Gabarit à copier pour écrire VOTRE technique de recherche.

1. Copiez ce fichier sous un nouveau nom, ex. `collecteurs/ma_source.py`.
2. Changez le manifeste (« nom » unique, « role »), puis la classe : nom, description, voie,
   politesse, et les méthodes `rechercher` (et `recuperer` si la source fournit le contenu).
3. Déclarez-la dans `registre.yaml` (module, classe, actif: true, réglages).
4. Vérifiez : `python -m pytest methodologie_recherche/tests`
   puis mesurez : `python -m methodologie_recherche.bancs.banc_collecte executer --domaine ...`

Règles : utilisez `self.http` (jamais un autre client réseau) pour que les tests puissent le
simuler ; appelez `self.patienter()` avant chaque appel ; vérifiez `self.autorise(url)` avant de
télécharger une page ; en cas de refus, levez `AccesRefuse` : le logiciel bascule alors vers
la collecte assistée au lieu d'insister.
"""

from __future__ import annotations

from .contrat import AccesRefuse, Candidat, CollecteurDeBase, Document, Politesse, Requete

__manifeste__ = {
    "nom": "modele_collecteur",
    "role": "Gabarit à copier pour écrire votre propre technique (inactif, absent du registre).",
    "groupe": "methodo",
    "ordre": 10,
    "session": "S08",
    "entrees": {},
    "sorties": {},
}


class CollecteurModele(CollecteurDeBase):
    nom = "modele"
    description = "Exemple de technique : remplacez ce texte par ce que fait la vôtre."
    version = "0.1"
    voie = "automatique"  # « locale », « automatique » ou « assistee »
    sait_rechercher = True
    sait_recuperer = False
    politesse = Politesse(requetes_par_minute=10.0, delai_min_secondes=2.0, respecte_robots_txt=True)

    def rechercher(self, requete: Requete) -> list[Candidat]:
        adresse = self.reglages.get("adresse", "https://exemple.org/recherche")
        if not self.autorise(adresse):
            raise AccesRefuse(f"robots.txt interdit {adresse}")
        self.patienter()
        reponse = self.http(adresse, {"q": requete.texte}, None, 30.0)
        candidats = []
        for element in reponse.json().get("resultats", []):
            candidats.append(Candidat(
                titre=element.get("titre", ""),
                url=element.get("url"),
                source=self.nom,
                extrait=element.get("resume", ""),
                date=element.get("date"),
            ))
        return candidats

    def recuperer(self, candidat: Candidat) -> Document | None:
        return None
