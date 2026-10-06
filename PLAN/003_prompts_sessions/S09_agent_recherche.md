# S09 — Agent de recherche, modes sans rechargement, journal des questions, cas A–I

> Jalon J2 · Dépend de : S08 · Étapes : R1–R8 · Prompts d'exécution : Q01, Q02, Q03, Q04, Q06
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§1, §2, §8, §11, §12, §17**),
`PLAN/001_but.md` (**§4, §5, §7**), `PLAN/002_strategie.md` (**§3.3, §7, dont §7.6**),
`methodologie_recherche/transversal/` (répertoire transversal, à l'utilisateur),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Le cœur du projet : un RAG qui **raisonne**. L'agent comprend la situation, repère les
ambiguïtés, tient compte de votre angle, bâtit un **plan** pondéré à travers les thèmes, fait
exécuter les recherches par le moteur de S07, **contrôle** et **hiérarchise** les preuves, et
remet un **dossier** puis une réponse — **sans jamais recharger de modèle pendant une question**.

## À réaliser

1. **Cas de référence** `tests/cas_reference/{A,B,C,D,F,G,H,I}.yaml` (E existe depuis S05) :
   question, date de référence, angle, **sous-questions attendues** (projet à faire valider par
   l'utilisateur), étiquettes attendues, pièges ; un **mini-corpus fictif** par cas (marqué
   fictif), dont : version abrogée (A), résultat fragile (B, C), espèce voisine (D), « manuel »
   d'escroquerie et rapport officiel (F), recommandation clinique et approche récente
   incertaine (G), documents d'ingénierie sociale marqués **domaine tenu à l'écart** (H),
   documents de disciplines différentes dont un seul relie directement la question à son but (I).
2. **Profils utilisateurs** (`profils_utilisateurs/<nom>.yaml`) et `ragc user-profile`.
3. **Q01 `situation_analysis`**, puis la **décomposition transversale** (`002_strategie.md` §7.6) :
   brancher `charger_repertoire` et `explorer_transversal` (déjà écrits dans
   `methodologie_recherche/transversal/`, ne pas les réécrire) ; **Q02 `research_plan`** appelé
   **K fois** (3 par défaut), chaque fois avec une grille mise en avant différente, sur le
   **menu transversal** (carte = chartes résumées en attendant S15) ; `fusionner_plans` ;
   **Q08 `completeness_critique`** (une passe : chaque grille ou discipline manquante devient une
   sous-question ou reçoit une raison écrite ; sous-questions « analogue ») ; **validation du
   plan par le code** (thèmes, filtres, dépendances, budget). `ponts_corpus` reste inactif
   jusqu'à S14 (pas encore de concepts par document).
4. **Exécuteur** : premier coup parallèle (question entière + sous-question, re-classement par
   sous-question, `valid_at`), approfondissement selon le rendement, escalade, 2 tours au plus.
5. **Q03 `evidence_selection`** + contrôles du code (version, adéquation, identifiants) ;
   **hiérarchisation** `P × S × A × F × R` ; **Q04 `evidence_dossier`** ; **Q06
   `consumer_answer`** ; lacunes → `gaps`.
6. **Modes sans rechargement** (`002_strategie.md` §3.3) : le code choisit le mode selon le
   modèle chargé (RAG direct, Qwen3.8 + adaptateur quand il existera, Qwen3.8 seul) ; le travail
   en fond se **met en pause** le temps d'une question (réglable).
7. **Journal de vos questions** (`questions`) : chaque question, le mode, la durée ; `ragc rate
   <id> <1-5> [--correction "…"]` ; une note et une correction → **exemples or** pour les
   spécialistes de l'agent.
8. **Traçabilité** : `research_runs` (situation, plan, trajectoire, dossier, réponse, métriques).
9. **CLI** : `ragc ask "<question>" [--focus …] [--date …] [--mode …] [--show-plan]
   [--validate-plan] [--dossier-only]`.
10. **Métriques** : couverture des sous-questions attendues, **couverture transversale** (grilles
    traitées, disciplines distinctes, analogues exploités, apport de la critique), respect de
    l'angle, contre-point, bonne version, rechargements (doit être 0).

## Bancs à ajouter

`ragc bench agent` : les cas de référence en conditions réelles avec MiMo (qualité du plan, durée,
tokens par étape, réflexion on / off pour Q01–Q02).

## Critères d'acceptation

- [ ] Le cas B signale l'ambiguïté et produit un plan pondéré multi-thèmes avec contre-point ; le
      cas C reconstruit le plan autour des neurosciences en gardant les étiquettes de solidité.
- [ ] Le cas A ne retient que la version en vigueur ; avec `--date` antérieure, l'ancienne.
- [ ] Le cas H traverse criminologie, cybersécurité et sciences comportementales.
- [ ] Le cas I atteint la cible « couverture transversale » de `001_but.md` §9 ; les branches
      absentes du corpus sont inscrites dans `gaps`.
- [ ] Aucun rechargement de modèle pendant une question (test).
- [ ] Message final : demander la validation des sous-questions attendues.
- [ ] Procédure de clôture appliquée.
