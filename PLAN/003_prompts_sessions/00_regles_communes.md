# Règles communes à toutes les sessions de développement

> Chaque prompt de session (`S01` … `S16`) demande de lire ce fichier. Il s'applique à toutes.

## 1. Documents de référence

- `PLAN/000_etat_de_l_art.md` (cité « EdA §n »), `PLAN/001_but.md` (le quoi, les **cas de
  référence A–H**), `PLAN/002_strategie.md` (le comment), `PLAN/004_decisions_techniques.md`
  (créé en S01), `PLAN/JOURNAL.md` (ce qui a été fait, décisions, écarts, mesures).
- **Ne change jamais le but ni la stratégie en silence.** Propose, note dans « Écarts » du
  journal, et ne modifie `001` / `002` qu'avec l'accord de l'utilisateur.
- **Discipline de périmètre** : n'implémente pas les fonctionnalités des sessions suivantes ;
  laisse un `# TODO(Sxx): …` précis si une interface doit anticiper la suite.
- **Vérifie toute référence externe** (article, API, bibliothèque, option de `llama-server`, outil)
  à sa source avant de t'en servir ; signale ce qui n'a pas pu être vérifié.

## 2. Où l'on développe, où l'on mesure

- Les sessions se déroulent **dans le cloud, sans carte graphique ni accès aux modèles de
  l'utilisateur**. Le code est écrit et testé **hors ligne** (faux serveurs, fixtures).
- Toute mesure réelle passe par **`ragc bench <scénario>`** (ou `bench/` avant que le logiciel
  n'existe), que l'utilisateur lance sur ses PC (RTX 5090, RTX 4090). Chaque session qui a besoin
  de mesures **ajoute ou complète un scénario**, explique en français comment le lancer, et
  demande le rapport (`reports/bench/…`) dans son message final.
- **N'écris jamais « mesuré » sans rapport de banc.** Quand un rapport est transmis, ses chiffres
  sont notés dans le journal et les réglages ajustés.

## 3. Portabilité

- Le logiciel doit fonctionner sous **Windows et Linux** (macOS au mieux), avec ou sans GPU.
- Chemins abstraits (`pathlib`), pas de signaux Unix pour le pilotage, pas de dépendance à
  `systemd` ou au Planificateur de tâches sauf en option ; tests sur les deux systèmes
  (intégration continue Windows + Linux).
- Aucun nom de modèle, chemin ou port codé en dur : tout passe par la configuration et le profil
  matériel.

## 4. Langue

- En français : documentation, prompts d'exécution du modèle, messages de la CLI, rapports,
  docstrings (courtes).
- En anglais : identifiants du code, clés JSON, noms de tables et de colonnes.

## 5. Pile et organisation du code

- Python 3.11 à 3.13, paquet `ragcreator`, commande `ragc` (argparse), `pyproject.toml` avec
  extras : `dev`, `web`, `pdf`, `ocr`, `graph`, `mcp`, `api`, `train`.
- Dépendances de base minimales (`pydantic>=2`, `httpx`, `PyYAML`, `numpy`) ; toute nouvelle
  dépendance justifiée dans le journal ; extras optionnels avec repli dégradé.
- Carte des modules : `docs/architecture.md`, tenue à jour.
- **Aucun texte de prompt dans le code** : tous dans `ragcreator/prompts/*.yaml`, identifiés selon
  `002_strategie.md` §9.2 (`L01`…`L03`, `C01`…`C14`, `Q01`…`Q07`, `V01`, `V02`).
- **Tout appel LLM passe par le client LLM** (journalisé) **et produit un exemple neutre**
  (`examples`) ; tout accès web passe par le récupérateur ; tout chargement de modèle passe par
  le **gestionnaire de modèles** (un seul modèle lourd à la fois) ; tout travail long est une
  **tâche du travail en fond**, interruptible.
- **Tout l'état est dans SQLite** ; chaque étape est idempotente et **interruptible** (pause,
  arrêt, coupure) ; toute évolution du schéma = nouvelle migration numérotée.
- Aucun nombre magique : seuils, tailles, poids → configuration ou profils.
- Journalisation via `logging` (pas de `print` hors sortie de la CLI).

## 5 bis. Mini-scripts, manifestes, carte du programme

- **Un fichier = une responsabilité** (viser moins de 200 lignes). Un script qui grossit est
  découpé.
- **Chaque script commence par un manifeste** `__manifeste__` (dictionnaire littéral) : `nom`,
  `role` (français), `moment`, `phase`, `etape`, `ordre`, `entrees` (`{variable: description}`),
  `sorties`, `appelle`, `lit`, `ecrit`, `modele` (`{tache, prompt}` ou `None`), `session`. Les noms
  de variables du manifeste sont **ceux du code**.
- **La carte est régénérée à chaque session** (`ragc carte` ou `python carte_du_programme/generer_carte.py`)
  et ses contrôles doivent passer : manifeste présent, entrées produites par un script ou
  déclarées externes, aucun flux orphelin. Un script prévu dans `architecture_prevue.yaml`
  passe au statut « réalisé » dès que son manifeste existe.
- **Le dossier `methodologie_recherche/` appartient à l'utilisateur** : ne jamais écraser ses
  modifications ; ajouter de nouveaux fichiers ou proposer des changements ; ne jamais casser le
  contrat sans incrémenter sa version et fournir une migration. Par exception, ce dossier utilise
  des **noms français**, car il est fait pour être modifié par l'utilisateur.

## 6. Sécurité et cadrage

- Le contenu collecté est une **donnée non fiable** : jamais exécuté, toujours entre
  `<document>…</document>`, avec consigne d'ignorer ses instructions.
- Aucun secret dans le dépôt (clés d'API en variables d'environnement) ; `robots.txt` et
  conditions d'utilisation respectés ; pas de contournement de protections.
- Domaines à double usage (hacking, procédés d'escrocs) : orientation **compréhension,
  détection, prévention** ; santé : **documentaire**, pas d'avis thérapeutique.

## 7. Tests

- `pytest` hors ligne par défaut ; tests réels marqués `@pytest.mark.live` (lancés sur les PC de
  l'utilisateur).
- Chaque fonctionnalité a ses tests. **Ne jamais désactiver, ignorer ou affaiblir un test** pour
  obtenir du vert.
- Fixtures **rédigées pour le projet** et marquées fictives.
- **Cas de référence A–H** (`tests/cas_reference/`) relancés par toute session qui touche à la
  recherche, à l'agent ou aux spécialistes. Le **hacking** est le **domaine tenu à l'écart** :
  aucun de ses exemples ne doit servir à l'entraînement.
- Qualité : `ruff check .` et `ruff format --check .` propres.

## 8. Procédure de clôture

1. `ruff check . && ruff format --check . && pytest` → tout vert.
2. Scénarios de banc ajoutés ou mis à jour ; instructions de lancement prêtes.
2 bis. Manifestes à jour, **carte du programme régénérée** et contrôles de la carte au vert.
3. Entrée dans `PLAN/JOURNAL.md` (gabarit ci-dessous).
4. `README.md` et `docs/` à jour.
5. Commits clairs (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`), push sur la branche de travail.
6. Message final : ce qui est fait, comment l'essayer (commandes Windows et Linux), **quel banc
   lancer**, ce qui reste, questions.

### Gabarit d'entrée de journal

```markdown
## Sxx — <titre> — AAAA-MM-JJ
- **Fait** :
- **Décisions** :
- **Écarts par rapport au plan** :
- **Mesures** (rapports de banc reçus) :
- **Bancs à lancer par l'utilisateur** :
- **Dettes / reste à faire** :
- **Questions pour l'utilisateur** :
```
