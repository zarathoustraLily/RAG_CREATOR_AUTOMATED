# S04 — Ingestion locale, extraction, pré-contrôles, découpage

> Jalon J1 · Dépend de : S01 · Étapes du pipeline : E2 (fichiers), E3, E5 · Prompts : —
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md`, `PLAN/002_strategie.md` (en particulier
§3.4, §5.1, §5.2, §6), `PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`.
Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Faire entrer des documents locaux dans le système, en extraire un texte **propre et
structuré**, écarter sans LLM ce qui ne mérite pas d'être lu, et produire des **extraits de
qualité** (la qualité du découpage conditionne celle de tout le RAG).

## À réaliser

1. **Machine à états** (`ragcreator/pipeline/states.py`) : états des documents de
   `002_strategie.md` §5.1, transitions autorisées vérifiées, motif obligatoire pour tout rejet
   ou échec. **Exécuteur minimal** `ragc run --once [--theme <chemin>] [--until <état>]` qui fait
   avancer les documents d'étape en étape (le démon de S10 s'appuiera dessus).
2. **Boîtes d'entrée** : scan de `themes/<chemin>/inbox/` (TXT, MD, HTML, PDF, DOCX), empreinte
   de fichier stable, pas de double ingestion, `ragc ingest <chemin-theme> <fichiers…>`.
3. **Extraction** (`ragcreator/ingest/extract.py`) : HTML via `trafilatura` (titre, date, auteur,
   texte principal) avec repli `html.parser` ; PDF via `pypdf` ou `pymupdf` (numéros de page,
   recollage des mots coupés, suppression des en-têtes/pieds de page répétés) ; DOCX via
   `python-docx`. **Structure préservée** en Markdown : titres, listes, tableaux. Normalisation
   Unicode NFC et espaces.
4. **Pré-contrôles E3** (`ragcreator/ingest/precheck.py`) : longueur minimale, détection de
   langue (bibliothèque légère optionnelle, repli heuristique), doublon exact (SHA-256 du texte
   normalisé), **quasi-doublon** (MinHash sur bardeaux de mots, seuil configurable), ratio de
   bruit (navigation, mentions légales), listes de domaines. Chaque rejet a un motif lisible.
5. **Découpage E5** (`ragcreator/ingest/chunking.py`) :
   - découpage **par la structure** : titres → sections → paragraphes, puis phrases si besoin ;
   - cible 300–450 tokens (configurable), chevauchement d'une phrase, jamais de coupure au
     milieu d'un tableau ou d'une liste courte ;
   - chaque extrait garde : `section_path` (« Titre > Sous-titre »), page, positions de
     caractères, nombre de tokens, identifiant de la **section parente** (stratégie
     petit-vers-grand de `002_strategie.md` §6).
6. **Commandes** : `ragc docs list [--theme] [--status]`, `ragc docs show <id>` (métadonnées,
   motif, extraits).
7. **Fixtures** rédigées pour le projet (FR et EN, sur la pharmacologie des champignons) :
   HTML d'article, PDF de 3 pages, Markdown, doublon exact, quasi-doublon, page trop courte,
   page de navigation.

## Hors de cette session

Aucun appel LLM (la vérification arrive en S05), aucune collecte web.

## Critères d'acceptation

- [ ] Déposer les fixtures dans `inbox/` puis `ragc run --once --until decoupe` donne des
      extraits avec `section_path`, page et positions ; doublons et pages pauvres rejetés avec
      motif.
- [ ] Relancer la commande ne crée aucun doublon (idempotence).
- [ ] Tests : extraction par format, détection des quasi-doublons, respect des tailles, aucune
      coupure de tableau, transitions d'état interdites refusées.
- [ ] Procédure de clôture appliquée.
