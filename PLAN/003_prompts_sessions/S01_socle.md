# S01 — Socle : projet, configuration, base de données, arbre des thèmes

> Jalon J1 · Dépend de : — · Étapes : — · Prompts d'exécution : —
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md`, `PLAN/001_but.md`,
`PLAN/002_strategie.md` (en particulier §3 et §4), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction entre ce prompt et ces documents,
arrête-toi et pose la question.

## Objectif

Poser des fondations solides : paquet installable, configuration complète et validée, base
SQLite avec migrations, **arbre des thèmes** et son reflet sur disque, emplacement des
**profils de domaine** et des **profils utilisateurs**, premières commandes `ragc`.

## À réaliser

1. **Projet** : `pyproject.toml` (paquet `ragcreator`, script `ragc`, extras des règles §3),
   configuration `ruff` et `pytest` (option `--live`, marqueur `live`), `README.md` minimal en
   français, `docs/architecture.md` décrivant la carte des modules prévue (`config`, `db`,
   `themes`, `profiles`, `llm`, `prompts`, `schemas`, `sources`, `ingest`, `verify`, `enrich`,
   `index`, `graph`, `temporal`, `synth`, `research` (agent), `pipeline`, `daemon`, `serve`,
   `eval`) — ne crée que les modules nécessaires à cette session.
2. **Configuration** (`ragcreator/config.py`) : modèles Pydantic couvrant **toute** la
   configuration de `002_strategie.md` (espace de travail, profils de modèles avec repli,
   affectation par étape et réflexion, embeddings, re-classement, consommateurs et budgets de
   contexte, connecteurs, seuils de vérification, poids de hiérarchisation, découpage, démon,
   agent de recherche). Chargement YAML + surcharges `RAGC_*`. `ragc init` écrit un
   `config.yaml` **commenté en français** (profils `mimo-9b` et `qwen38-27b`).
3. **Base de données** (`ragcreator/db/`) : SQLite (WAL, clés étrangères, `busy_timeout`),
   migrations par `PRAGMA user_version` et fichiers SQL numérotés. Schéma initial : `themes`
   (avec `profile`), `theme_aliases`, `documents` (**avec dès maintenant** les colonnes
   temporelles et de version de `002_strategie.md` §3.6), `document_themes`, `chunks` (avec
   `unit_ref`, `facets`, `evidence_level`, `valid_from`, `valid_to`, `flags`), `cycles`,
   `llm_calls`, `jobs` (avec bail). Les sessions suivantes ajouteront leurs tables.
4. **Thèmes** (`ragcreator/themes/`) : analyse de `"Droit > Fiscalité > Géorgie"` et de
   `droit/fiscalite/georgie` ; *slug* sans accents ; nom d'affichage conservé ; nœuds
   intermédiaires créés ; ajout idempotent ; alias ; statut ; renommage ; suppression logique ;
   requête **sous-arbre** efficace ; reflet sur disque `themes/<chemin>/` avec `charte.yaml`
   (squelette), `inbox/`, `prompts/`, `fiches/`.
5. **Emplacements** : `profils/` (profils de domaine, remplis en S03) et
   `profils_utilisateurs/` (remplis en S08) créés par `ragc init`, avec un README court.
6. **CLI** : `ragc init [chemin]`, `ragc config show|validate`,
   `ragc theme add|tree|show|alias|pause|resume|rm`.
7. **Journalisation** : fichier tournant dans `logs/`, niveau via `-v/-q`.

## Hors de cette session

Aucun appel LLM, aucune collecte, aucun traitement de document, aucun contenu de profil.

## Critères d'acceptation

- [ ] `pip install -e ".[dev]"` fonctionne ; `ragc --help` en français.
- [ ] `ragc init ~/rag-test` crée l'arborescence et un `config.yaml` commenté qui passe
      `ragc config validate`.
- [ ] `ragc theme add "Droit > Fiscalité > Géorgie"` puis `"Droit > Fiscalité > France"` donnent
      un arbre à 4 nœuds sans doublon ; `ragc theme tree` l'affiche.
- [ ] `"Mycologie > Amanite tue-mouches"` donne le slug `mycologie/amanite-tue-mouches`.
- [ ] Migrations rejouables sur une base existante.
- [ ] Au moins 15 tests (chemins, slugs, idempotence, sous-arbre, migrations, configuration
      invalide rejetée avec un message clair).
- [ ] Procédure de clôture appliquée.
