# S05 — Ingestion, bibliothèque, lecture (OCR, livres), datation, découpage

> Jalon J1 · Dépend de : S04 · Étapes : E2, E3, E5 (déterministe), E6 · Prompts : L01, L02, L03
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§3, §6, **§13**, §15),
`PLAN/001_but.md` (§7 cas E), `PLAN/002_strategie.md` (§4.2, §4.5, **§5.4**, §6),
`PLAN/004_decisions_techniques.md` (**outil de lecture retenu**),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Faire entrer **votre bibliothèque** et tout document dans le système : texte **fidèle** page par
page (natif ou OCR), figures décrites, structure des livres, rejets sans LLM de ce qui ne mérite
pas d'être lu, datation et versions déterministes, découpage selon **l'unité naturelle du
domaine**. Tout s'exécute comme tâches du **travail en fond** (phases P0, P1, P2), interruptibles.

## À réaliser

1. **Machine à états des documents** et transitions vérifiées ; motif obligatoire pour tout rejet.
2. **Import de bibliothèque** : dossiers surveillés et `inbox/` des thèmes ; Zotero / Calibre selon
   S01 (métadonnées reprises) ; `ragc ingest`, `ragc library add <dossier>`.
3. **Formats** : PDF, EPUB, DOCX, HTML, Markdown, texte, images.
4. **Lecture page par page** (`002_strategie.md` §5.4) : texte natif si la couche est bonne
   (diagnostic de qualité), sinon **OCR avec l'outil retenu en S01** (phase P1) ; couche dégradée
   refaite ; **L01** si l'OCR passe par un modèle ; contrôles automatiques (mots inconnus,
   répétitions, ordre de lecture, tableaux) ; second moteur sur échantillon ; **L03 arbitrage**
   par MiMo en vision (seulement le visible, sinon `[illisible]`) ; **L02 description de figures**
   (phase P2) ; tables `pages` et `figures`.
5. **Structure des livres** : table des matières, chapitres, notes rattachées, en-têtes et pieds de
   page retirés, **pagination imprimée**, métadonnées (auteur, titre, édition, année, ISBN) ;
   deux éditions = deux versions.
6. **Pré-contrôles E3** : longueur, langue, doublons exacts et quasi-doublons, bruit, domaines.
7. **Datation et versions déterministes** : métadonnées, motifs du texte, références juridiques
   (`unit_ref`, y compris articles du Code des impôts géorgien), **lignées de versions** sans
   écrasement.
8. **Découpage par profil** : article de loi ; section d'article scientifique ; chapitre et section
   d'un livre ; **blocs de code intacts** (cybersécurité) ; 300–450 tokens par défaut ; section
   parente ; page citée.
9. **Fixtures fictives** : extraits de codes fiscaux fictifs (deux versions d'un article), article
   scientifique, page de blog, **livre fictif de quelques dizaines de pages en version texte et
   en version scannée** (cas E), pages OCR de référence (deux colonnes, tableau, notes, figure,
   page dégradée), doublons.

## Bancs à ajouter

`ragc bench ocr` (erreurs, phrases inventées, temps par page, outil retenu vs autre option) et
`ragc bench book <pdf>` (lecture complète d'un livre scanné réel choisi par l'utilisateur :
durée, pages douteuses).

## Critères d'acceptation

- [ ] Un livre scanné devient du texte structuré, pages citées, figures décrites, alertes de
      qualité ; aucune phrase inventée sur les pages de référence.
- [ ] Pause au milieu d'un livre puis reprise exacte ; idempotence.
- [ ] Deux versions d'un article coexistent, reliées, avec des périodes de validité cohérentes.
- [ ] Procédure de clôture appliquée.
