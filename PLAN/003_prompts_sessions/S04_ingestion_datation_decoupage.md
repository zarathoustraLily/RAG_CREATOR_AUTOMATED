# S04 — Ingestion locale, pré-contrôles, datation, versions, découpage par profil

> Jalon J1 · Dépend de : S03 · Étapes : E2 (fichiers), E3, E5 (partie déterministe), E6 · Prompts : —
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§3, §6), `PLAN/001_but.md`,
`PLAN/002_strategie.md` (§3.2, **§3.5**, §3.6, §5), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Faire entrer des documents locaux, en extraire un texte propre et structuré, écarter sans LLM
ce qui ne mérite pas d'être lu, **dater et versionner** ce qui peut l'être de façon
déterministe, et découper selon **l'unité naturelle du domaine** (un article de loi, une
section d'article scientifique).

## À réaliser

1. **Machine à états** (`ragcreator/pipeline/states.py`) : états des documents (ajouter l'état
   `date` entre `verifie` et `decoupe`), transitions vérifiées, motif obligatoire pour tout rejet.
   **Exécuteur minimal** `ragc run --once [--theme] [--until <état>]` (le démon de S13 s'appuiera
   dessus).
2. **Boîtes d'entrée** : `themes/<chemin>/inbox/` (TXT, MD, HTML, PDF, DOCX, EPUB, images), empreinte stable,
   pas de double ingestion ; `ragc ingest <chemin-theme> <fichiers…>`.
3. **Extraction** : HTML (`trafilatura` + repli), PDF **à couche texte** page par page (`pymupdf` :
   numéros de page, mots coupés, en-têtes répétés), DOCX, EPUB ; structure préservée en Markdown
   (titres, listes, tableaux). Table `pages` (migration) avec un **diagnostic de qualité** par page ;
   les pages sans texte exploitable (scans, couche texte dégradée) et les images sont marquées
   `a_lire` : leur lecture par OCR et vision est l'objet de **S05**.
4. **Pré-contrôles E3** : longueur, langue, doublon exact (SHA-256 normalisé), **quasi-doublon**
   (MinHash), ratio de bruit, listes de domaines ; motifs lisibles.
5. **Datation et versions (partie déterministe de E5)** (`ragcreator/temporal/`) :
   - dates depuis les métadonnées (HTML `meta`, PDF, en-têtes HTTP plus tard) et motifs du
     texte (« en vigueur à compter du… », « version du… ») ;
   - références d'unités juridiques (« Article 209 B », « art. L. 64 LPF ») → `unit_ref` ;
   - **lignées de versions** : même source (identifiant officiel ou URL canonique) avec un
     contenu différent → nouvelle version, `supersedes_id`, `valid_to` de l'ancienne quand la
     date d'effet est connue ; rien n'est écrasé ;
   - la partie LLM (documents sans métadonnées exploitables) viendra en S07 (C07).
6. **Découpage E6 par profil** (`ragcreator/ingest/chunking.py`) :
   - `juridique_fiscal` : **un article = une unité** (alinéas si trop long), avec code, numéro,
     version ; décisions découpées par motifs ;
   - `pharmaco_medical` / `sciences_comportementales` : sections de l'article scientifique
     (résumé, méthode, résultats, discussion) ;
   - `generique` / `mycologie` : structure (titres → sections → paragraphes) ;
   - tailles du profil (300–450 tokens par défaut), chevauchement d'une phrase, jamais de
     tableau coupé, `section_path`, page, positions, **section parente**.
7. **Commandes** : `ragc docs list|show`, `ragc docs versions <id>`.
8. **Fixtures** rédigées pour le projet et marquées fictives : extrait de code fiscal fictif
   avec **deux versions d'un même article** (dates d'effet différentes), décision de justice
   fictive, article scientifique fictif (IMRaD), page HTML de blog, PDF de 3 pages, doublon,
   quasi-doublon, page trop courte.

## Critères d'acceptation

- [ ] `ragc run --once --until decoupe` sur les fixtures : unités correctes par profil, dates et
      `unit_ref` renseignés quand c'est possible, doublons rejetés avec motif.
- [ ] Les deux versions de l'article fictif coexistent, reliées, avec des périodes de validité
      cohérentes.
- [ ] Idempotence : relancer ne crée rien de nouveau.
- [ ] Tests : extraction par format, quasi-doublons, unités juridiques, lignées de versions,
      tailles, aucune coupure de tableau, transitions interdites refusées.
- [ ] Procédure de clôture appliquée.
