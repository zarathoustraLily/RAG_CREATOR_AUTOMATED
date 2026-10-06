"""Le contrat des techniques, le rythme de politesse et la lecture de robots.txt."""

from __future__ import annotations

import pytest
from conftest import HttpSimule

from methodologie_recherche.collecteurs.contrat import (
    AccesRefuse, Candidat, CollecteurDeBase, Politesse, Ralentir, SourceIndisponible, verifier_conformite,
)
from methodologie_recherche.collecteurs.outils_http import ReponseHttp, VerificateurRobots, agent_avec_contact


class TechniqueCorrecte(CollecteurDeBase):
    nom = "correcte"
    description = "Technique de test."
    voie = "automatique"

    def rechercher(self, requete):
        return []


def test_technique_correcte_conforme():
    assert verifier_conformite(TechniqueCorrecte(http=HttpSimule())) == []


def test_ecarts_au_contrat_signales():
    class Mauvaise:
        nom = "Mauvais Nom"
        description = ""
        version = "1"
        voie = "furtive"
        sait_rechercher = True
        sait_recuperer = True
        politesse = "lente"

    problemes = " | ".join(verifier_conformite(Mauvaise()))
    for attendu in ("nom", "description", "voie", "politesse", "rechercher", "recuperer"):
        assert attendu in problemes


def test_ralentir_est_un_refus():
    erreur = Ralentir("trop vite", reessayer_apres=30)
    assert isinstance(erreur, AccesRefuse) and erreur.reessayer_apres == 30


def test_delai_de_politesse():
    assert Politesse(requetes_par_minute=30, delai_min_secondes=1).delai() == 2
    assert Politesse(requetes_par_minute=600, delai_min_secondes=1).delai() == 1


def test_patienter_respecte_le_rythme():
    temps, attentes = [100.0], []
    technique = TechniqueCorrecte(http=HttpSimule(), horloge=lambda: temps[0], attendre=attentes.append)
    technique.politesse = Politesse(requetes_par_minute=6, delai_min_secondes=0)  # 10 s entre deux appels
    technique.patienter()
    temps[0] = 103.0
    technique.patienter()
    assert attentes == [7.0]


def test_cle_de_dedoublonnage():
    assert Candidat("Titre", "https://A.org/x", "s", identifiant="DOI:1").cle() == "doi:1"
    assert Candidat("Titre", "https://A.org/x", "s").cle() == "https://a.org/x"
    assert Candidat(" Titre ", None, "s").cle() == "titre"


def test_agent_utilisateur_avec_contact():
    assert "vous@exemple.org" in agent_avec_contact("vous@exemple.org")
    assert agent_avec_contact("") == agent_avec_contact(None)


@pytest.mark.parametrize("reponse, autorise", [
    (ReponseHttp(200, {}, b"User-agent: *\nDisallow: /prive/\n"), False),
    (ReponseHttp(404, {}, b""), True),
    (ReponseHttp(503, {}, b""), False),
    (SourceIndisponible("injoignable"), False),
    (AccesRefuse("403"), True),
])
def test_robots_txt(reponse, autorise):
    http = HttpSimule({"https://site.exemple/robots.txt": reponse})
    robots = VerificateurRobots(http)
    assert robots.autorise("https://site.exemple/prive/page") is autorise
    assert robots.autorise("https://site.exemple/prive/autre") is autorise
    assert len(http.appels) == 1  # robots.txt lu une seule fois par site


def test_robots_txt_autorise_le_reste():
    http = HttpSimule({"https://site.exemple/robots.txt": ReponseHttp(200, {}, b"User-agent: *\nDisallow: /prive/\n")})
    assert VerificateurRobots(http).autorise("https://site.exemple/public/page")
