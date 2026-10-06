"""Tests de la carte du programme : cohérence de l'architecture et du générateur."""

import sys
from pathlib import Path

DOSSIER_CARTE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DOSSIER_CARTE))

import generer_carte as gc  # noqa: E402


def test_architecture_prevue_sans_probleme():
    donnees = gc.construire_donnees()
    assert donnees["problemes"] == []
    assert len(donnees["scripts"]) >= 60


def test_donnees_js_a_jour():
    """La carte enregistrée doit correspondre au code et à l'architecture actuels."""
    attendu = gc.rendre_js(gc.construire_donnees())
    assert gc.SORTIE.read_text(encoding="utf-8") == attendu, (
        "Carte périmée : lancez « python carte_du_programme/generer_carte.py »"
    )


def test_manifeste_lu_sans_executer_le_script(tmp_path):
    script = tmp_path / "exemple.py"
    script.write_text(
        '__manifeste__ = {"nom": "exemple", "entrees": {"a": "x"}, "sorties": {"b": "y"}}\n'
        'raise SystemExit("ce code ne doit pas être exécuté")\n',
        encoding="utf-8",
    )
    assert gc.lire_manifeste(script)["nom"] == "exemple"


def test_script_realise_remplace_le_prevu():
    prevus = [{"id": "x", "fichier": "a.py", "groupe": "g", "ordre": 1, "role": "prévu",
               "entrees": {}, "sorties": {"v": "d"}}]
    realises = [{"id": "x", "fichier": "b.py", "role": "réalisé", "entrees": {},
                 "sorties": {"v": "d"}, "statut": "realise"}]
    (script,) = gc.fusionner(prevus, realises)
    assert script["statut"] == "realise"
    assert script["fichier"] == "b.py"
    assert script["ordre"] == 1  # conservé depuis la version prévue


def _architecture(scripts, externes=None):
    return {
        "moments": [{"id": "m", "nom": "M"}],
        "groupes": [{"id": "g", "nom": "G", "moment": "m"}],
        "entrees_externes": externes or {},
        "parcours": [],
        "scripts": scripts,
    }


def _script(ident, ordre, entrees=None, sorties=None):
    return {"id": ident, "fichier": f"{ident}.py", "groupe": "g", "ordre": ordre, "role": ident,
            "entrees": entrees or {}, "sorties": sorties or {}}


def test_entree_orpheline_signalee():
    scripts = [_script("a", 1, entrees={"inconnue": "?"})]
    _, problemes = gc.calculer_flux(scripts, _architecture(scripts))
    assert any("inconnue" in p for p in problemes)


def test_entree_externe_acceptee():
    scripts = [_script("a", 1, entrees={"question": "?"})]
    _, problemes = gc.calculer_flux(scripts, _architecture(scripts, {"question": "vous"}))
    assert problemes == []


def test_flux_et_boucle():
    scripts = [
        _script("a", 1, entrees={"retour": "r"}, sorties={"v": "d"}),
        _script("b", 2, entrees={"v": "d"}, sorties={"retour": "r"}),
    ]
    flux, problemes = gc.calculer_flux(scripts, _architecture(scripts))
    assert problemes == []
    par_sens = {(f["de"], f["vers"]): f for f in flux}
    assert par_sens[("a", "b")]["variables"] == ["v"]
    assert par_sens[("a", "b")]["boucle"] is False
    assert par_sens[("b", "a")]["boucle"] is True


def test_parcours_avec_etape_inconnue():
    architecture = _architecture([_script("a", 1)])
    architecture["parcours"] = [{"id": "p", "etapes": ["a", "fantome"]}]
    problemes = gc.verifier_structure(architecture["scripts"], architecture)
    assert any("fantome" in p for p in problemes)
