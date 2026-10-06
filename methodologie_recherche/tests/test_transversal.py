"""Répertoire transversal : cohérence, exploration d'une question, ponts, fusion des plans."""

from __future__ import annotations

import pytest

from methodologie_recherche.outils_texte import contient, normaliser, similarite
from methodologie_recherche.transversal.couverture import couverture, fusionner_plans
from methodologie_recherche.transversal.exploration import explorer_transversal, rendre_menu
from methodologie_recherche.transversal.ponts import ponts_abc, voisins_transversaux
from methodologie_recherche.transversal.repertoire import RepertoireInvalide, charger_repertoire, verifier_repertoire

VEGANISME = "Comment convaincre quelqu'un d'abandonner le véganisme ?"


@pytest.fixture(scope="module")
def repertoire():
    return charger_repertoire(strict=True)


# ── Outils de texte ──────────────────────────────────────────────────────────

def test_normalisation_et_mots_cles():
    texte = normaliser(VEGANISME)
    assert texte == "comment convaincre quelqu un d abandonner le veganisme"
    assert contient(texte, "vegan") and contient(texte, "convain")
    assert not contient(texte, "ganisme")          # début de mot seulement
    assert contient(normaliser("Je veux créer une société"), "creer une societe")
    assert similarite("arnaque aux sentiments", "les arnaques aux sentiments") == 1.0
    assert similarite("arnaque aux sentiments", "fiscalité géorgienne") == 0.0


# ── Répertoire ───────────────────────────────────────────────────────────────

def test_repertoire_fourni_coherent(repertoire):
    assert repertoire["problemes"] == []
    assert {"situation", "presupposes", "tinbergen", "analogues", "contre_point"} <= {
        lentille["id"] for lentille in repertoire["lentilles"]}


def test_repertoire_incoherent_signale():
    problemes = " | ".join(verifier_repertoire({
        "types": {"persuasion": ["convain"]},
        "lentilles": [{"id": "x", "questions": []}, {"id": "x", "types": ["inconnu"], "questions": ["?"]}],
        "disciplines": [{"id": "d", "mots_cles": []}],
        "schemas": [{"id": "s", "indices": [[]], "disciplines": ["absente"], "analogues": []}],
    }))
    for attendu in ("sans questions", "en double", "type inconnu", "sans mots-clés", "indices vide",
                    "discipline inconnue", "sans analogues", "ni « toujours »"):
        assert attendu in problemes


def test_repertoire_strict(tmp_path):
    (tmp_path / "lentilles.yaml").write_text("types: {}\nlentilles: [{id: x, questions: []}]\n", encoding="utf-8")
    (tmp_path / "disciplines.yaml").write_text("disciplines: []\n", encoding="utf-8")
    (tmp_path / "analogues.yaml").write_text("schemas: []\n", encoding="utf-8")
    with pytest.raises(RepertoireInvalide):
        charger_repertoire(tmp_path, strict=True)


# ── Exploration ──────────────────────────────────────────────────────────────

def test_exploration_veganisme(repertoire):
    exploration = explorer_transversal(VEGANISME, repertoire)
    assert {"persuasion", "comportement", "croyance"} <= set(exploration["types"])
    assert [s["id"] for s in exploration["schemas"]] == ["changer_conviction_identitaire"]
    assert {"tinbergen", "communication", "leviers_obstacles", "ethique", "presupposes",
            "analogues", "contre_point"} <= set(exploration["lentilles"])
    assert "syllogisme" not in exploration["lentilles"]
    assert {"psychologie_morale", "neurosciences_decision", "sciences_communication", "nutrition",
            "ethologie", "biologie_evolutive", "philosophie_morale"} <= set(exploration["disciplines_suggerees"])
    assert "vegan" in exploration["concepts"]


def test_exploration_georgie(repertoire):
    exploration = explorer_transversal(
        "Conditions pour ne pas payer d'impôts en Géorgie si je crée une société là-bas", repertoire,
        situation={"acteurs": ["résident fiscal français"], "objectif": "réduire légalement l'imposition"})
    assert "droit" in exploration["types"]
    assert "arbitrer_juridictions" in [s["id"] for s in exploration["schemas"]]
    assert "syllogisme" in exploration["lentilles"] and "tinbergen" not in exploration["lentilles"]
    assert "droit_fiscal" in exploration["disciplines_suggerees"]


def test_menu_compact_et_ouvert(repertoire):
    exploration = explorer_transversal(VEGANISME, repertoire)
    menu = rendre_menu(exploration, repertoire)
    assert "Déconversion religieuse" in menu and "Tinbergen" in menu
    assert "Autres disciplines disponibles" in menu
    assert "absente de ce répertoire" in menu  # le modèle peut sortir du répertoire
    assert len(menu) < 6000


# ── Ponts (modèle ABC) ───────────────────────────────────────────────────────

CORPUS = [
    {"vegan", "identite"}, {"vegan", "identite", "communaute"}, {"vegan", "carence"},
    {"identite", "changement_attitude"}, {"identite", "changement_attitude", "dissonance"},
    {"changement_attitude", "dissonance"}, {"carence"}, {"meteo"},
]


def test_ponts_abc():
    ponts = ponts_abc(CORPUS, {"vegan"}, {"changement_attitude"}, documents_min=2)
    assert [p["concept"] for p in ponts] == ["identite"]
    assert ponts[0]["documents_ab"] == 2 and ponts[0]["documents_bc"] == 2 and ponts[0]["direct_ac"] == 0
    assert ponts_abc(CORPUS, {"absent"}, {"changement_attitude"}) == []


def test_voisins_transversaux():
    familles = {"carence": "vivant", "identite": "esprit_cerveau", "communaute": "societe"}
    voisins = voisins_transversaux(CORPUS, {"vegan"}, familles, familles_deja={"esprit_cerveau"}, documents_min=1)
    # « communaute » n'apparaît qu'avec « vegan » : association plus forte que « carence ».
    assert [v["concept"] for v in voisins] == ["communaute", "carence"]
    assert voisins[1]["famille"] == "vivant"


# ── Fusion des plans et couverture ───────────────────────────────────────────

def test_fusion_privilegie_les_angles_nouveaux(repertoire):
    exploration = explorer_transversal(VEGANISME, repertoire)
    plan_a = {"sous_questions": [
        {"id": "SQ1", "question": "Pourquoi les végans abandonnent-ils leur régime ?", "lentilles": ["presupposes"],
         "disciplines": ["nutrition"], "poids": 3},
        {"id": "SQ2", "question": "Quels arguments moraux touchent un végan ?", "lentilles": ["communication"],
         "disciplines": ["psychologie_morale"], "poids": 2},
    ]}
    plan_b = {"sous_questions": [
        {"id": "SQ1", "question": "Pourquoi les végans abandonnent leur régime ?", "lentilles": ["presupposes"],
         "disciplines": ["sociologie"], "poids": 2},
        {"id": "SQ2", "question": "Comment le cerveau représente-t-il une valeur sacrée ?", "lentilles": ["tinbergen"],
         "disciplines": ["neurosciences_decision"], "poids": 1},
        {"id": "CP1", "type": "contre_point", "question": "Quand tenter de convaincre se retourne-t-il contre soi ?",
         "lentilles": ["contre_point", "leviers_obstacles"], "disciplines": ["psychologie_sociale"], "poids": 2},
    ]}
    plan_fusionne, angles_manquants = fusionner_plans([plan_a, plan_b], exploration, max_sous_questions=10)
    questions = [sq["question"] for sq in plan_fusionne["sous_questions"]]
    assert len(questions) == 4                                   # le doublon est fusionné
    abandon = next(sq for sq in plan_fusionne["sous_questions"] if "abandonn" in sq["question"])
    assert abandon["proposee_par"] == 2 and abandon["poids"] == 3
    assert set(abandon["disciplines"]) == {"nutrition", "sociologie"}
    assert [sq["id"] for sq in plan_fusionne["sous_questions"]] == ["SQ1", "SQ2", "SQ3", "SQ4"]
    assert angles_manquants["contre_point"] is True
    assert "ethique" in angles_manquants["lentilles_manquantes"]
    assert "analogues" in angles_manquants["lentilles_manquantes"]
    assert 0 < angles_manquants["taux_lentilles"] < 1


def test_fusion_respecte_le_plafond(repertoire):
    exploration = explorer_transversal(VEGANISME, repertoire)
    plan = {"sous_questions": [{"id": f"S{i}", "question": f"question numero {i} sujet{i}", "lentilles": ["situation"],
                                "disciplines": [], "poids": 1} for i in range(20)]}
    plan_fusionne, _ = fusionner_plans([plan], exploration, max_sous_questions=5)
    assert len(plan_fusionne["sous_questions"]) == 5 and len(plan_fusionne["ecartees"]) == 15


def test_couverture_plan_vide(repertoire):
    exploration = explorer_transversal(VEGANISME, repertoire)
    resultat = couverture({"sous_questions": []}, exploration)
    assert resultat["taux_lentilles"] == 0 and resultat["contre_point"] is False
