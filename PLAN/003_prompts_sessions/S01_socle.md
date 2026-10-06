# S01 — Socle : projet, configuration, base de données, arbre des thèmes

> Jalon J1 · Dépend de : — · Étapes du pipeline : — · Prompts d'exécution : —
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md`, `PLAN/002_strategie.md`,
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction entre ce prompt et ces documents, arrête-toi et pose la question.

## Objectif

Poser des fondations solides : paquet Python installable, configuration complète et validée,
base SQLite avec migrations, **arbre des thèmes hiérarchiques** et son reflet sur disque,
premières commandes `ragc`.

## À réaliser

1. **Projet** : `pyproject.toml` (paquet `ragcreator`, script `ragc`, extras du §3 des règles),
   configuration `ruff` et `pytest` (option `--live` et marqueur `live` dans `conftest.py`),
   `README.md` minimal en français, `docs/architecture.md` décrivant la carte des modules
   prévue (sous-paquets `config`, `db`, `themes`, `llm`, `prompts`, `schemas`, `sources`,
   `ingest`, `verify`, `enrich`, `index`, `graph`, `synth`, `pipeline`, `daemon`, `serve`, `eval`)
   — ne crée que les modules nécessaires à cette session.
2. **Configuration** (`ragcreator/config.py`) : modèles Pydantic couvrant **toute** la
   configuration décrite dans `002_strategie.md` (espace de travail, profils de modèles avec
   repli, affectation par étape et réflexion, embeddings, re-classement, sources, seuils de
   vérification, découpage, démon, budgets de contexte par modèle consommateur). Chargement
   YAML + surcharges par variables `RAGC_*`. `ragc init` écrit un `config.yaml` **commenté en
   français** avec des valeurs par défaut raisonnables (profils `mimo-9b` et `qwen38-27b`).
3. **Base de données** (`ragcreator/db/`) : connexion SQLite (WAL, clés étrangères,
   `busy_timeout`), système de migrations par `PRAGMA user_version` et fichiers SQL numérotés.
   Schéma initial : `themes`, `theme_aliases`, `documents`, `document_themes`, `chunks`,
   `cycles`, `llm_calls`, `jobs` (avec bail : `lease_owner`, `lease_expires_at`). Les sessions
   suivantes ajouteront leurs tables par de nouvelles migrations.
4. **Thèmes** (`ragcreator/themes/`) :
   - analyse de `"Pharmacologie > Champignons > Amanita muscaria"` et de
     `pharmacologie/champignons/amanita-muscaria` ; *slug* sans accents ni espaces ; nom
     d'affichage conservé ; création des nœuds intermédiaires ; ajout idempotent ;
   - alias (`--alias "amanite tue-mouches" --alias "fly agaric"`), statut
     (`nouveau`, `actif`, `pause`, `stable`), profondeur, renommage, suppression logique ;
   - reflet sur disque : `themes/<chemin>/` avec `charte.yaml` (squelette vide), `inbox/`,
     `prompts/`, `fiches/` ;
   - requête « sous-arbre » efficace (préfixe de chemin) — elle servira à toute la recherche.
5. **CLI** : `ragc init [chemin]`, `ragc config show|validate`,
   `ragc theme add|tree|show|alias|pause|resume|rm`. Affichage de l'arbre lisible avec
   statuts et nombre de documents.
6. **Journalisation** : fichier tournant dans `logs/`, niveau via `-v/-q`.

## Hors de cette session

Aucun appel LLM, aucune collecte, aucun traitement de document.

## Critères d'acceptation

- [ ] `pip install -e ".[dev]"` fonctionne ; `ragc --help` en français.
- [ ] `ragc init ~/rag-test` crée l'arborescence de `002_strategie.md` §4.3 et un `config.yaml`
      commenté qui passe `ragc config validate`.
- [ ] `ragc theme add "Pharmacologie > Champignons > Amanita muscaria" --alias "fly agaric"`
      crée 3 nœuds ; le relancer ne crée aucun doublon ; `ragc theme tree` affiche l'arbre.
- [ ] `"Mycologie > Amanite tue-mouches"` donne le slug `mycologie/amanite-tue-mouches`.
- [ ] Les migrations sont rejouables sans erreur sur une base existante.
- [ ] Au moins 15 tests (analyse de chemins, slugs, idempotence, sous-arbre, migrations,
      configuration invalide rejetée avec un message clair).
- [ ] Procédure de clôture de `00_regles_communes.md` appliquée.
