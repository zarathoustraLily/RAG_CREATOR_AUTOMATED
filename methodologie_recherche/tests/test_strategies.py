"""Méthodologies (YAML), génération des requêtes et registre des techniques."""

from __future__ import annotations

from datetime import date

import pytest
import yaml
from conftest import HttpSimule

from methodologie_recherche.registre import RegistreInvalide, charger_registre
from methodologie_recherche.requetes import date_limite, generer_requetes_strategie
from methodologie_recherche.strategies import (
    StrategieInvalide, charger_strategie, domaines_disponibles, verifier_strategie,
)

AUJOURD_HUI = date(2026, 10, 6)


# ── Méthodologies fournies ───────────────────────────────────────────────────

@pytest.mark.parametrize("domaine", domaines_disponibles())
def test_chaque_methodologie_est_valide(domaine):
    strategie = charger_strategie(domaine, strict=True)
    assert verifier_strategie(strategie) == []
    assert generer_requetes_strategie(strategie, "sujet de test", aujourd_hui=AUJOURD_HUI)


def test_heritage_fiscalite_georgie():
    strategie = charger_strategie("fiscalite_georgie")
    assert strategie["heritage"] == ["fiscalite_georgie", "juridique_fiscal", "commun"]
    assert strategie["langues"][:3] == ["fr", "en", "ka"]
    assert strategie["sources_preferees"][0] == "matsne.gov.ge"
    assert "legifrance.gouv.fr" in strategie["sources_preferees"]  # hérité du juridique
    assert strategie["filtrer_par_date"] is False  # le texte en vigueur compte plus que la date
    assert strategie["techniques"] == ["dossier_local", "openalex", "wikipedia", "liste_lecture"]


def test_domaine_inconnu():
    strategie = charger_strategie("domaine_qui_n_existe_pas")
    assert strategie["repli_commun"] is True and strategie["domaine"] == "domaine_qui_n_existe_pas"
    with pytest.raises(StrategieInvalide):
        charger_strategie("domaine_qui_n_existe_pas", strict=True)


def _ecrire(dossier, nom, contenu):
    (dossier / f"{nom}.yaml").write_text(yaml.safe_dump(contenu, allow_unicode=True), encoding="utf-8")


def test_fusion_et_retrait(tmp_path):
    _ecrire(tmp_path, "commun", {"langues": ["fr", "en"], "techniques": ["a", "b", "c"],
                                 "gabarits": {"fr": ["{sujet}"], "en": ["{sujet}"]}, "fraicheur_mois": 12})
    _ecrire(tmp_path, "parent", {"techniques": ["d"], "fraicheur_mois": 24, "retirer": {"techniques": ["b"]}})
    _ecrire(tmp_path, "enfant", {"herite": "parent", "gabarits": {"fr": ["{sujet} loi"]}})
    strategie = charger_strategie("enfant", dossier=tmp_path)
    assert strategie["techniques"] == ["d", "a", "c"]
    assert strategie["fraicheur_mois"] == 24
    assert strategie["gabarits"]["fr"] == ["{sujet} loi", "{sujet}"]


def test_heritage_circulaire(tmp_path):
    _ecrire(tmp_path, "commun", {"langues": ["fr"]})
    _ecrire(tmp_path, "a", {"herite": "b"})
    _ecrire(tmp_path, "b", {"herite": "a"})
    with pytest.raises(StrategieInvalide, match="circulaire"):
        charger_strategie("a", dossier=tmp_path)


def test_verification_signale_les_erreurs():
    problemes = " | ".join(verifier_strategie({
        "langues": ["fr", "de"], "gabarits": {"fr": ["sans variable"]}, "fraicheur_mois": 0,
        "techniques": [], "gabarit": {},
    }))
    for attendu in ("clés inconnues", "« de »", "sans « {sujet} »", "fraicheur_mois", "techniques"):
        assert attendu in problemes


# ── Requêtes ─────────────────────────────────────────────────────────────────

def test_date_limite():
    assert date_limite(date(2026, 10, 6), 12) == date(2025, 10, 6)
    assert date_limite(date(2026, 3, 31), 1) == date(2026, 2, 28)
    assert date_limite(date(2026, 1, 15), 13) == date(2024, 12, 15)


def test_requetes_par_langue_avec_filtre_de_date():
    strategie = {
        "langues": ["fr", "en"], "fraicheur_mois": 12, "filtrer_par_date": True,
        "gabarits": {"fr": ["{sujet}", "{sujet}  réforme {annee}"],
                     "en": [{"texte": "{sujet} meta-analysis", "sans_date": True}, "{sujet}"]},
        "sources_preferees": ["a.fr", "b.org"],
    }
    requetes = generer_requetes_strategie(strategie, {"fr": "arnaque", "en": "scam"}, aujourd_hui=AUJOURD_HUI)
    assert [(r.langue, r.texte) for r in requetes] == [
        ("fr", "arnaque"), ("fr", "arnaque réforme 2026"), ("en", "scam meta-analysis"), ("en", "scam"),
    ]
    assert requetes[0].filtres == {"depuis": "2025-10-06", "sites": "a.fr,b.org"}
    assert "depuis" not in requetes[2].filtres


def test_requetes_sans_doublon_et_langue_absente_ignoree():
    strategie = {"langues": ["fr", "ka"], "gabarits": {"fr": ["{sujet}", "{sujet} "], "ka": ["{sujet}"]}}
    requetes = generer_requetes_strategie(strategie, {"fr": "impôt"}, aujourd_hui=AUJOURD_HUI)
    assert [(r.langue, r.texte) for r in requetes] == [("fr", "impôt")]


# ── Registre ─────────────────────────────────────────────────────────────────

def test_registre_fourni_charge_toutes_les_techniques():
    collecteurs, problemes = charger_registre(http=HttpSimule(), strict=True)
    assert problemes == []
    assert [c.nom for c in collecteurs] == ["dossier_local", "openalex", "wikipedia", "liste_lecture"]
    voies = {c.voie for c in collecteurs}
    assert voies == {"locale", "automatique", "assistee"}


def test_registre_ecarte_les_techniques_defectueuses():
    registre = {"version_contrat": "1.0", "techniques": [
        {"nom": "liste_lecture", "module": "liste_lecture", "classe": "CollecteurListeLecture"},
        {"nom": "liste_lecture", "module": "liste_lecture", "classe": "CollecteurListeLecture"},
        {"nom": "absente", "module": "n_existe_pas", "classe": "X"},
        {"nom": "mal_nommee", "module": "liste_lecture", "classe": "CollecteurListeLecture"},
        {"nom": "coupee", "module": "n_existe_pas", "classe": "X", "actif": False},
    ]}
    collecteurs, problemes = charger_registre(registre, http=HttpSimule())
    assert [c.nom for c in collecteurs] == ["liste_lecture"]
    texte = " | ".join(problemes)
    assert "en double" in texte and "absente" in texte and "mal_nommee" in texte
    assert "coupee" not in texte
    with pytest.raises(RegistreInvalide):
        charger_registre(registre, http=HttpSimule(), strict=True)


def test_registre_version_de_contrat_incompatible():
    _, problemes = charger_registre({"version_contrat": "2.0", "techniques": []})
    assert problemes and "contrat" in problemes[0]
