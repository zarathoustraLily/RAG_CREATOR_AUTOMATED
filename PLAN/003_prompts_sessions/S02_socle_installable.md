# S02 — Socle installable, gestionnaire de modèles, travail en fond pilotable

> Jalon J1 · Dépend de : S01 · Étapes : — · Prompts d'exécution : —
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md`, `PLAN/001_but.md` (§2, §8, §10),
`PLAN/002_strategie.md` (**§3**, §4.1, §4.6, **§5.6**), `PLAN/004_decisions_techniques.md`,
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md` (dont les rapports de banc
s'ils existent). Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Des fondations qui s'installent **sur n'importe quel PC** (Windows, Linux), connaissent leur
matériel, ne chargent **qu'un modèle lourd à la fois**, et font tourner un **travail en fond que
l'utilisateur démarre, suspend, arrête et reprend à volonté** — sans perte.

## À réaliser

1. **Projet** : `pyproject.toml` (paquet `ragcreator`, commande `ragc`, extras des règles §5),
   `ruff`, `pytest` (option `--live`), intégration continue Windows + Linux, `README.md` en
   français, `docs/architecture.md`.
2. **Installation** : scripts `install.ps1` (Windows) et `install.sh` (Linux) selon S01 ;
   `ragc init [dossier]` : arborescence de l'espace de travail, **détection du matériel** →
   `profils_materiels/<machine>.yaml`, `config.yaml` commenté en français, téléchargement (avec
   confirmation) de la bonne version de `llama-server` ; `ragc doctor` (premier niveau).
3. **Configuration** Pydantic complète (`002_strategie.md`), surcharges `RAGC_*`, validation avec
   messages clairs.
4. **Base de données** : SQLite (WAL), migrations ; tables `themes`, `theme_aliases`, `documents`
   (avec colonnes temporelles et de version), `document_themes`, `pages`, `chunks`, `jobs` (avec
   **modèle et adaptateur requis**, bail), `cycles`, `llm_calls`, `worker_state`.
5. **Thèmes** : chemins `A > B > C` ou `a/b/c`, slugs sans accents, alias, sous-arbre, reflet sur
   disque (`charte.yaml`, `inbox/`, `prompts/`, `fiches/`) ; `ragc theme add|tree|show|alias|rm`.
6. **Gestionnaire de modèles** (mécanisme retenu en S01) : un seul modèle lourd chargé ; petits
   modèles d'aide sur CPU ou GPU selon le profil ; `ragc models status|load|unload` ; refus de
   toute bascule pendant une question ; arrêt propre des processus `llama-server` sous Windows et
   Linux.
7. **Travailleur de fond** (`ragcreator/worker/`) :
   - processus détaché ; `ragc start|pause|resume|stop|status` ;
   - **canal de contrôle local** commun à Windows et Linux (pas de signaux Unix), protégé ;
   - file de tâches avec baux ; **regroupement par modèle puis par adaptateur** ; phases
     P0…P5 (squelette, avec une tâche factice pour les tests) ;
   - `pause` : termine ou met de côté l'élément en cours, **décharge le modèle**, carte graphique
     libre en ≤ 30 s ; `resume` : recharge et continue ; reprise exacte après coupure ;
   - plages horaires optionnelles ; démarrage automatique optionnel (Planificateur de tâches /
     `systemd --user`), documentés ;
   - étude d'une **pause automatique** quand un autre programme occupe la VRAM (au moins la
     détection).
8. **Journalisation** : fichiers tournants dans `logs/`, `ragc logs`.
9. **Mini-scripts et carte** : chaque script créé a son `__manifeste__` ; brancher le générateur
   existant (`carte_du_programme/generer_carte.py`) sur le code (`ragc carte`), et ses contrôles
   dans l'intégration continue ; les scripts réalisés remplacent leurs équivalents « prévus ».

## Bancs à ajouter

`ragc bench install` (installation propre, diagnostic), `ragc bench worker` (démarrage, pause
→ temps jusqu'à libération de la VRAM, reprise, arrêt brutal puis reprise).

## Critères d'acceptation

- [ ] Installation et `ragc doctor` fonctionnent dans l'intégration continue Windows et Linux.
- [ ] Le travailleur passe les tests : pause et reprise au milieu d'une tâche factice, arrêt brutal
      (processus tué) puis reprise sans perte ni double traitement.
- [ ] Le gestionnaire refuse de charger un second modèle lourd.
- [ ] Au moins 30 tests ; procédure de clôture appliquée.
