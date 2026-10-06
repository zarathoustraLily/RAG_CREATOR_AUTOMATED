# S08 — Agent de recherche : situation, plan, recherche, contrôles, hiérarchisation, dossier

> Jalon J2 · Dépend de : S07 · Étapes : R1–R8 · Prompts d'exécution : Q01, Q02, Q03, Q04, Q06
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§1, §2, §8, §11, §12**),
`PLAN/001_but.md` (**§4, §5, §7**), `PLAN/002_strategie.md` (**§6 en entier**, §7),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

C'est le cœur du projet : un RAG qui **raisonne**. Face à une question, l'agent comprend la
situation, repère les ambiguïtés, tient compte de l'angle de l'utilisateur, bâtit un **plan**
de sous-questions pondérées à travers les thèmes, fait exécuter les recherches par le moteur de
S07, **contrôle** et **hiérarchise** les preuves, puis remet un **dossier** à partir duquel le
modèle consommateur répond. Principe : *l'agent planifie, le moteur exécute* (EdA §2).

## À réaliser

1. **Cas de référence** `tests/cas_reference/{A,B,C,D}.yaml` (`001_but.md` §7 ; le cas E existe
   depuis S05) : question,
   date de référence, angle éventuel, **sous-questions attendues** (projet à faire valider par
   l'utilisateur — le signaler dans le message final), étiquettes attendues, pièges. Pour
   chaque cas, un **mini-corpus fictif** rédigé pour le projet (marqué fictif), ingéré par le
   pipeline existant, couvrant aussi des pièges : version abrogée (A), résultat fragile
   (B, C), espèce voisine (D).
2. **Profils utilisateurs** (`profils_utilisateurs/<nom>.yaml`) : vision en clair, thèmes
   privilégiés et poids, contre-point actif ou non, mode ambiguïté (`demander` / `supposer`) ;
   `ragc user-profile init|show|edit`.
3. **Q01 `situation_analysis`** (réflexion activée) : acteurs, objectif, contraintes,
   juridictions, **date de référence** (extraite, sinon aujourd'hui), **ambiguïtés** avec leurs
   interprétations, hypothèses, **angle détecté** dans la formulation.
4. **Q02 `research_plan`** (réflexion activée) : à partir de la situation, de l'angle résolu
   (priorité : validation du plan > `--focus` > formulation > profil utilisateur > défaut) et de
   la **carte** (pour l'instant : chartes résumées des thèmes ; les fiches de nœud viendront en
   S12) → plan au format de `002_strategie.md` §6.2 : sous-questions, thèmes, filtres, **poids**,
   dépendances, **contre-point**, budget. Un angle **reconstruit le plan** (tronc + ponts vers
   l'action), il ne change pas les échelles de solidité.
5. **Validation du plan par le code** : thèmes existants, filtres valides pour le profil de
   chaque thème, identifiants uniques, dépendances sans cycle, budget respecté ; plan invalide →
   réparation par le modèle puis repli sur un plan minimal.
6. **Exécuteur** (`ragcreator/research/`) :
   - **premier coup** : toutes les sous-questions sans dépendance en parallèle ; recherche avec
     `query` = question complète + sous-question, `rerank_query` = sous-question, filtres et
     `valid_at` = date de référence ; consolidation ;
   - **approfondissement** : effort réparti selon le **rendement** de chaque sous-question
     (exploration / exploitation simple, EdA §12), sous-questions dépendantes ensuite ;
     **escalade** extrait → section parente → document ; 2 tours maximum ; budget global.
7. **Q03 `evidence_selection`** (sans réflexion), par sous-question et par lots : garder ou non,
   **fidélité** (l'extrait dit-il vraiment cela ?), applicabilité à la situation, raison ;
   contrôles du code : version en vigueur à la date de référence (filtre dur selon profil),
   **adéquation de la source** au type de sous-question, identifiants valides.
8. **Hiérarchisation** : `importance = P × S × A × F × R` (`002_strategie.md` §6.4), poids dans
   la configuration ; S tiré des étiquettes (niveau de preuve, réplication, crédibilité).
9. **Q04 `evidence_dossier`** : dossier Markdown compact et JSON (`002_strategie.md` §6.5),
   classé par poids de sous-question puis importance, étiquettes visibles, conflits présentés,
   **lacunes** → table `gaps` ; budget de tokens par modèle consommateur respecté.
10. **Q06 `consumer_answer`** : prompt système pour Qwen3.8 — s'appuyer **uniquement** sur le
    dossier, citer `[S#]`, distinguer solide / fragile, signaler conflits et lacunes, rappeler
    les limites (pas de conseil juridique, fiscal, médical).
11. **Traçabilité** : table `research_runs` (question, situation, plan, angle, trajectoire,
    dossier, réponse, métriques, durée, tokens) — elle servira à l'évaluation (S15) et à
    l'entraînement éventuel (S16).
12. **CLI** : `ragc ask "<question>" [--focus <thème>…] [--date AAAA-MM-JJ]
    [--user-profile <nom>] [--show-plan] [--validate-plan] [--dossier-only]` ; avec
    `--validate-plan`, l'utilisateur modifie poids et sous-questions avant l'exécution ; en cas
    d'ambiguïté forte, question posée (mode `demander`) ou hypothèse affichée (mode `supposer`).
13. **Métrique de qualité du plan** : couverture des sous-questions attendues des cas de
    référence (appariement par similarité + vérification), respect de l'angle (part des preuves
    de tête issues du thème demandé), présence du contre-point.

## Expériences en conditions réelles (si disponibles)

Les 5 cas de référence (A–E) : qualité du plan, bonne version (A), étiquettes fragiles signalées
(B, C), espèce voisine signalée (D), respect de l'angle (C), temps total, tokens par étape.
Comparer Q01/Q02 avec et sans réflexion. Tout dans le journal.

## Critères d'acceptation

- [ ] `ragc ask "Comment vendre une voiture à un vendeur de voitures ?" --show-plan` signale
      l'ambiguïté, affiche un plan pondéré multi-thèmes avec contre-point.
- [ ] La même question avec `--focus neurosciences` reconstruit le plan ; la solidité reste
      affichée (résultat fragile signalé).
- [ ] Le cas A ne retient que la version en vigueur à la date de référence ; avec
      `--date` antérieure, l'ancienne version est retenue.
- [ ] Tests hors ligne des cinq cas avec le faux serveur ; validation du plan ; filtre dur ;
      calcul d'importance ; budget du dossier ; lacunes enregistrées.
- [ ] Message final : demander à l'utilisateur de valider les sous-questions attendues des cas
      de référence.
- [ ] Procédure de clôture appliquée.
