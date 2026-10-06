"""VOS tests : exemples à adapter. Écrivez ici ce que VOUS attendez de vos méthodologies.

Après chaque modification d'une méthodologie ou d'une technique :
    python -m pytest methodologie_recherche/tests
Un test qui échoue vous dit précisément quelle attente n'est plus respectée.
"""

from datetime import date

from methodologie_recherche.requetes import generer_requetes_strategie
from methodologie_recherche.strategies import charger_strategie


def test_georgie_cherche_aussi_en_georgien():
    strategie = charger_strategie("fiscalite_georgie")
    requetes = generer_requetes_strategie(
        strategie, {"fr": "impôt sur les sociétés", "en": "corporate tax", "ka": "მოგების გადასახადი"},
        aujourd_hui=date(2026, 10, 6),
    )
    assert any(r.langue == "ka" for r in requetes)
    assert any("convention fiscale France Géorgie" in r.texte for r in requetes)


def test_criminologie_reste_preventive():
    strategie = charger_strategie("criminologie")
    assert "prévention" in strategie["cadrage"]
    assert any("mode d'emploi" in critere for critere in strategie["criteres_tri"]["ecarter"])


def test_sante_cherche_des_essais_controles():
    strategie = charger_strategie("sante_clinique")
    requetes = generer_requetes_strategie(strategie, {"en": "specific phobia exposure therapy"},
                                          aujourd_hui=date(2026, 10, 6))
    assert any("randomized controlled trial" in r.texte for r in requetes)
