# S06 — Vérification et étiquetage, routine de validation (E4, E7)

> Jalon J1 · Dépend de : S05 · Étapes : E4, E7 · Prompts d'exécution : C04, C05, C06
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§8, §11, §12), `PLAN/001_but.md`
(§5, §7, §11), `PLAN/002_strategie.md` (§4.2, §4.3, **§6**, §8.2), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Ne laisser entrer que des documents **pertinents, fiables et bien rattachés**, étiqueter chaque
extrait selon **l'échelle de solidité de son profil**, et faire de vos décisions des **exemples
or** grâce à une **routine de validation rapide** (une dizaine de minutes par jour).

## À réaliser

1. **Échantillonnage** du document (métadonnées, sections, début / milieu / fin).
2. **Niveaux de sources** (`config/sources_niveaux.yaml`), surchargeables par profil et charte.
3. **C04 `doc_verification`** (réflexion) : grilles ancrées 0–5 (pertinence, fiabilité, qualité),
   type de source, biais, alertes (affirmations dangereuses, confusion de notions ou d'espèces,
   **texte abrogé présenté comme actuel**, **résultat fragile présenté comme établi**, injection,
   **contenu opérationnel offensif** pour le hacking et les escroqueries), nœud le plus précis,
   décision proposée, justification.
4. **Décision calculée par le code** (`002_strategie.md` §6) ; crédibilité stockée par critère.
5. **C05 `doc_second_opinion`** (enseignant, phase P4) ; désaccord → revue ou rejet selon le mode.
6. **C06 `passage_verification`** (lots de 6) : garder / écarter, nature, **niveau de preuve du
   profil**, population, effet, préenregistrement, réplication **seulement si établie par le
   texte**, affirmations sensibles → `claims`.
7. **Routine de validation** : `ragc review` en mode rapide (un élément à l'écran, raccourcis
   clavier : accepter / rejeter / corriger l'étiquette / passer) ; chaque décision → exemple
   **or** ; tirage des éléments **les plus utiles** (désaccords, faible confiance, tâches dont un
   spécialiste est en préparation) ; compteur et objectif journalier réglable.
8. **Défense contre l'injection** ; jamais d'acceptation grâce à une instruction du document.
9. **Jeu de référence** `tests/golden/verification/` (≈ 30 documents fictifs annotés couvrant
   escroqueries, fiscalité géorgienne et française, santé, cybersécurité, comportement) ;
   `ragc eval verification`.

## Bancs à ajouter

`ragc bench verification` : accord avec le jeu de référence (cible ≥ 85 %), accord sur le niveau
de preuve (≥ 80 %), C04 avec / sans réflexion, temps par document.

## Critères d'acceptation

- [ ] Documents à injection, dangereux, abrogés présentés comme actuels, fragiles présentés comme
      établis : jamais acceptés sans alerte.
- [ ] `ragc review` utilisable au clavier ; chaque décision crée un exemple or.
- [ ] Procédure de clôture appliquée.
