"""Les techniques fournies : conformité et comportement, sans réseau (réponses simulées)."""

from __future__ import annotations

import pytest
from conftest import HttpSimule, jeu, reponse_json

from methodologie_recherche.collecteurs.api_openalex import CollecteurOpenAlex, resume_depuis_index
from methodologie_recherche.collecteurs.contrat import AccesRefuse, Ralentir, Requete, verifier_conformite
from methodologie_recherche.collecteurs.dossier_local import CollecteurDossierLocal
from methodologie_recherche.collecteurs.liste_lecture import CollecteurListeLecture, ecrire_liste_lecture
from methodologie_recherche.collecteurs.modele_collecteur import CollecteurModele
from methodologie_recherche.collecteurs.outils_http import ReponseHttp
from methodologie_recherche.collecteurs.wikipedia import CollecteurWikipedia

SANS_ATTENTE = {"attendre": lambda secondes: None}
ROBOTS_OUVERT = ReponseHttp(200, {}, b"User-agent: *\nAllow: /\n")


@pytest.mark.parametrize("classe", [
    CollecteurDossierLocal, CollecteurOpenAlex, CollecteurWikipedia, CollecteurListeLecture, CollecteurModele,
])
def test_techniques_fournies_conformes(classe):
    assert verifier_conformite(classe(http=HttpSimule())) == []


# ── Dossier local ────────────────────────────────────────────────────────────

def test_dossier_local_trouve_et_recupere(tmp_path):
    (tmp_path / "Arnaque_aux_sentiments_etude.pdf").write_bytes(b"%PDF-1.7 fictif")
    (tmp_path / "notes.md").write_text("Les escroqueries sentimentales en ligne", encoding="utf-8")
    (tmp_path / "recette.txt").write_text("Tarte aux pommes", encoding="utf-8")
    technique = CollecteurDossierLocal({"dossiers": [str(tmp_path)], "seuil": 0.5})
    candidats = technique.rechercher(Requete("arnaque sentiments"))
    assert [c.titre for c in candidats] == ["Arnaque aux sentiments etude"]
    document = technique.recuperer(candidats[0])
    assert document.contenu.startswith(b"%PDF") and document.type_mime == "application/pdf"
    assert technique.rechercher(Requete("escroqueries sentimentales"))[0].titre == "notes"


def test_dossier_local_ignore_accents_et_dossier_absent(tmp_path):
    (tmp_path / "Fiscalite_Georgie.txt").write_text("Impôt géorgien", encoding="utf-8")
    technique = CollecteurDossierLocal({"dossiers": [str(tmp_path), str(tmp_path / "absent")]})
    assert len(technique.rechercher(Requete("fiscalité géorgie"))) == 1
    assert technique.rechercher(Requete("de la")) == []


# ── OpenAlex ─────────────────────────────────────────────────────────────────

def test_openalex_resume_reconstitue():
    assert resume_depuis_index({"monde": [1], "Bonjour": [0]}) == "Bonjour monde"
    assert resume_depuis_index(None) == ""


def test_openalex_recherche(monkeypatch):
    monkeypatch.delenv("RAGC_OPENALEX_CLE", raising=False)
    http = HttpSimule({"https://api.openalex.org/works": reponse_json(jeu("openalex_recherche.json"))})
    technique = CollecteurOpenAlex({"cle_api": "cle-test"}, http=http, **SANS_ATTENTE)
    candidats = technique.rechercher(Requete("arnaque", langue="fr", filtres={"depuis": "2025-10-06"}))
    assert len(candidats) == 2
    premier = candidats[0]
    assert premier.extrait == "Cette étude fictive décrit les étapes"
    assert premier.identifiant == "https://doi.org/10.0000/fictif.1"
    assert premier.metadonnees["pdf"] == "https://editeur.exemple/article1.pdf"
    appel = http.appels[0]
    assert appel["parametres"]["filter"] == "language:fr,from_publication_date:2025-10-06"
    assert appel["entetes"] == {"Authorization": "Bearer cle-test"}
    assert "cle-test" not in str(appel["parametres"])  # la clé ne passe pas dans l'URL


def test_openalex_cle_par_variable_d_environnement(monkeypatch):
    monkeypatch.setenv("RAGC_OPENALEX_CLE", "cle-env")
    assert CollecteurOpenAlex(http=HttpSimule())._entetes() == {"Authorization": "Bearer cle-env"}


def test_openalex_ralentissement_remonte():
    http = HttpSimule({"https://api.openalex.org/works": Ralentir("429", 60)})
    with pytest.raises(Ralentir):
        CollecteurOpenAlex(http=http, **SANS_ATTENTE).rechercher(Requete("x"))


def test_openalex_recupere_pdf_si_robots_autorise():
    http = HttpSimule({
        "https://api.openalex.org/works": reponse_json(jeu("openalex_recherche.json")),
        "https://editeur.exemple/robots.txt": ROBOTS_OUVERT,
        "https://editeur.exemple/article1.pdf": ReponseHttp(200, {"Content-Type": "application/pdf"}, b"%PDF-1.7"),
    })
    technique = CollecteurOpenAlex(http=http, **SANS_ATTENTE)
    premier, second = technique.rechercher(Requete("x"))
    assert technique.recuperer(premier).contenu == b"%PDF-1.7"
    assert technique.recuperer(second) is None  # pas d'accès libre


def test_openalex_respecte_robots_txt():
    http = HttpSimule({
        "https://api.openalex.org/works": reponse_json(jeu("openalex_recherche.json")),
        "https://editeur.exemple/robots.txt": ReponseHttp(200, {}, b"User-agent: *\nDisallow: /\n"),
    })
    technique = CollecteurOpenAlex(http=http, **SANS_ATTENTE)
    premier = technique.rechercher(Requete("x"))[0]
    with pytest.raises(AccesRefuse):
        technique.recuperer(premier)
    assert not any(a["url"].endswith(".pdf") for a in http.appels)


def test_openalex_page_html_au_lieu_du_pdf():
    http = HttpSimule({
        "https://api.openalex.org/works": reponse_json(jeu("openalex_recherche.json")),
        "https://editeur.exemple/robots.txt": ROBOTS_OUVERT,
        "https://editeur.exemple/article1.pdf": ReponseHttp(200, {"Content-Type": "text/html"}, b"<html>"),
    })
    technique = CollecteurOpenAlex(http=http, **SANS_ATTENTE)
    assert technique.recuperer(technique.rechercher(Requete("x"))[0]) is None


# ── Wikipédia ────────────────────────────────────────────────────────────────

def test_wikipedia_recherche_et_extrait(monkeypatch):
    monkeypatch.delenv("RAGC_CONTACT", raising=False)
    http = HttpSimule({"https://fr.wikipedia.org/w/api.php": reponse_json(jeu("wikipedia_recherche.json"))})
    technique = CollecteurWikipedia({"contact": "vous@exemple.org"}, http=http, **SANS_ATTENTE)
    candidat = technique.rechercher(Requete("arnaque", langue="fr"))[0]
    assert candidat.extrait == "Une arnaque fictive & exemplaire"
    assert candidat.url == "https://fr.wikipedia.org/wiki/Arnaque_fictive"
    assert candidat.date == "2026-05-01"
    assert "vous@exemple.org" in http.appels[0]["entetes"]["User-Agent"]
    http.routes["https://fr.wikipedia.org/w/api.php"] = reponse_json(jeu("wikipedia_extrait.json"))
    assert technique.recuperer(candidat).contenu.decode() == "Texte fictif de l'article."


def test_wikipedia_plus_lent_sans_contact(monkeypatch):
    monkeypatch.delenv("RAGC_CONTACT", raising=False)
    lent = CollecteurWikipedia(http=HttpSimule()).politesse.delai()
    rapide = CollecteurWikipedia({"contact": "vous@exemple.org"}, http=HttpSimule()).politesse.delai()
    assert lent > rapide and lent >= 6  # 10 requêtes/minute partagées par l'adresse IP


# ── Liste de lecture ─────────────────────────────────────────────────────────

def test_liste_lecture_fabrique_des_liens_sans_reseau(tmp_path):
    http = HttpSimule()
    technique = CollecteurListeLecture({"sites_par_requete": 2}, http=http)
    requete = Requete("fraude & arnaque", filtres={"depuis": "2025-10-06", "sites": "a.gouv.fr,b.org,c.net"})
    candidats = technique.rechercher(requete)
    liens = [c.url for c in candidats]
    assert liens[0] == "https://search.brave.com/search?q=fraude+%26+arnaque"
    assert any("as_ylo=2025" in lien for lien in liens)
    assert sum("site%3A" in lien for lien in liens) == 2
    assert http.appels == []
    page = ecrire_liste_lecture(candidats, tmp_path / "lecture.html", titre="Test <b>")
    contenu = page.read_text(encoding="utf-8")
    assert "Test &lt;b&gt;" in contenu and "fraude &amp; arnaque" in contenu
    assert 'rel="noopener noreferrer"' in contenu


# ── Tests réels (réseau) : python -m pytest methodologie_recherche/tests --reseau ──

@pytest.mark.reseau
def test_reseau_openalex():
    candidats = CollecteurOpenAlex().rechercher(Requete("romance scam", langue="en", limite=3))
    assert candidats, "aucun résultat : clé RAGC_OPENALEX_CLE absente ou budget épuisé ?"


@pytest.mark.reseau
def test_reseau_wikipedia():
    candidats = CollecteurWikipedia().rechercher(Requete("escroquerie", langue="fr", limite=3))
    assert candidats
