"""Banc de mesure : compteurs, arrêt sur refus, précision, comparaison, ligne de commande."""

from __future__ import annotations

import json
from datetime import date

from conftest import HttpSimule

from methodologie_recherche.bancs.banc_collecte import (
    comparer, evaluer, executer_banc, gabarit_etiquettes, principal, rendre_markdown,
)
from methodologie_recherche.collecteurs.contrat import Candidat, CollecteurDeBase, Ralentir

STRATEGIE = {
    "domaine": "test", "heritage": ["test", "commun"], "langues": ["fr"], "fraicheur_mois": 12,
    "filtrer_par_date": True, "gabarits": {"fr": ["{sujet}", "{sujet} étude"]},
    "techniques": ["premiere", "seconde", "bloquee"],
}


class Technique(CollecteurDeBase):
    voie = "automatique"
    description = "test"

    def __init__(self, nom, resultats=None, erreur=None):
        super().__init__(http=HttpSimule())
        self.nom, self.resultats, self.erreur, self.appels = nom, resultats or [], erreur, 0

    def rechercher(self, requete):
        self.appels += 1
        if self.erreur:
            raise self.erreur
        return [Candidat(t, f"https://x.org/{t}", self.nom, date=d) for t, d in self.resultats]


def _banc():
    premiere = Technique("premiere", [("a", "2026-01-01"), ("b", "2020-01-01")])
    seconde = Technique("seconde", [("b", None), ("c", "2026-02-01")])
    bloquee = Technique("bloquee", erreur=Ralentir("429", 60))
    hors_strategie = Technique("hors_strategie")
    horloge = iter(range(1000))
    rapport = executer_banc(STRATEGIE, [premiere, seconde, bloquee, hors_strategie], ["sujet"],
                            aujourd_hui=date(2026, 10, 6), horloge=lambda: next(horloge))
    return rapport, bloquee


def test_compteurs():
    rapport, bloquee = _banc()
    premiere, seconde = rapport["techniques"]["premiere"], rapport["techniques"]["seconde"]
    assert rapport["requetes"] == 2
    assert premiere["appels"] == 2 and premiere["candidats"] == 4
    assert premiere["nouveaux"] == 2 and premiere["doublons"] == 2
    assert premiere["recents"] == 2 and premiere["dates_connues"] == 4
    assert seconde["nouveaux"] == 1 and seconde["doublons"] == 3
    assert premiere["secondes_par_appel"] == 1.0
    assert rapport["ignorees"] == ["hors_strategie"]
    assert {c["cle"] for c in rapport["candidats"]} == {"https://x.org/a", "https://x.org/b", "https://x.org/c"}


def test_technique_qui_demande_de_ralentir_n_est_plus_sollicitee():
    rapport, bloquee = _banc()
    assert bloquee.appels == 1
    assert rapport["techniques"]["bloquee"]["ralentir"] == 1
    assert "ralentissement" in rapport["techniques"]["bloquee"]["arretee"]


def test_precision_et_comparaison():
    avant, _ = _banc()
    etiquettes = gabarit_etiquettes(avant)
    assert set(etiquettes.values()) == {None}
    etiquettes.update({"https://x.org/a": True, "https://x.org/b": False, "https://x.org/c": True})
    apres = evaluer(json.loads(json.dumps(avant)), etiquettes)
    assert apres["techniques"]["premiere"]["precision"] == 0.5
    assert apres["techniques"]["seconde"]["precision"] == 1.0
    lignes = comparer(avant, apres)
    assert {"technique": "seconde", "mesure": "precision", "avant": None, "apres": 1.0, "ecart": None} in lignes
    assert "| premiere | automatique | 2 | 4 | 2 | 2 | 2/4 |" in rendre_markdown(apres)


def test_ligne_de_commande_hors_ligne(tmp_path, capsys):
    (tmp_path / "doc_arnaque_sentiments.txt").write_text("arnaque aux sentiments", encoding="utf-8")
    registre = tmp_path / "registre.yaml"
    registre.write_text(f"""
version_contrat: "1.0"
techniques:
  - {{nom: dossier_local, module: dossier_local, classe: CollecteurDossierLocal,
     reglages: {{dossiers: ["{tmp_path.as_posix()}"]}}}}
  - {{nom: openalex, module: api_openalex, classe: CollecteurOpenAlex}}
  - {{nom: liste_lecture, module: liste_lecture, classe: CollecteurListeLecture}}
""", encoding="utf-8")
    sujets = tmp_path / "sujets.yaml"
    sujets.write_text("criminologie:\n  - {fr: arnaque aux sentiments, en: romance scam}\n", encoding="utf-8")
    http = HttpSimule()
    code = principal(["executer", "--domaine", "criminologie", "--sujets", str(sujets),
                      "--registre", str(registre), "--voies", "locale,assistee",
                      "--max-requetes", "3", "--sortie", str(tmp_path / "rapports")], http=http)
    assert code == 0
    assert http.appels == []  # hors ligne : aucune technique automatique
    rapports = sorted((tmp_path / "rapports").glob("*_criminologie.json"))
    assert len(rapports) == 1
    rapport = json.loads(rapports[0].read_text(encoding="utf-8"))
    assert set(rapport["techniques"]) == {"dossier_local", "liste_lecture"}
    assert rapport["techniques"]["dossier_local"]["nouveaux"] >= 1
    assert rapport["requetes"] == 3
    assert "Banc de collecte — criminologie" in capsys.readouterr().out
