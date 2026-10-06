# S03 — Charte de thème (E0) et sous-thèmes

> Jalon J1 · Dépend de : S02 · Étape du pipeline : E0 · Prompts d'exécution : P01, P02
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md`, `PLAN/002_strategie.md` (en particulier
§4 et §7), `PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md` (notamment les
résultats des expériences de S02 sur le mode JSON). Respecte-les. En cas de contradiction,
arrête-toi et pose la question.

## Objectif

Transformer un simple nom de thème en une **charte** précise qui guidera toute la suite :
recherche, vérification, rattachement, couverture. C'est la première étape où MiMo travaille
vraiment : elle sert aussi à valider notre façon d'écrire les prompts.

## À réaliser

1. **Schéma Pydantic `ThemeCharter`** reprenant les champs de `002_strategie.md` §4.1 (clés en
   anglais dans le JSON, rendu YAML en français dans `charte.yaml`) : définition, périmètre
   inclus / exclu, sous-thèmes proposés (avec justification), mots-clés FR/EN, synonymes et
   noms scientifiques, **confusions à éviter**, sources prioritaires, types d'**affirmations
   sensibles**, niveau de sensibilité, langues.
2. **Prompt P01 `theme_charter`** (réflexion activée) — entrées : nom, chemin, charte du parent,
   noms et définitions des thèmes frères, alias connus, langues. Exigences de rédaction :
   - un enfant est **strictement plus étroit** que son parent et ne chevauche pas ses frères ;
   - pour un organisme : nom scientifique, noms vernaculaires FR/EN, **espèces confondables** ;
   - pour un domaine médical ou toxicologique : sensibilité haute et affirmations sensibles
     (dose, toxicité, comestibilité, interactions, contre-indications, traitement) ;
   - `null` plutôt qu'une invention ; un exemple court (*few-shot*) en fin de prompt système.
3. **Prompt P02 `search_queries`** (sans réflexion) — à partir de la charte : requêtes par source
   (`web`, `wikipedia`, `europepmc`) et par langue, variées (synonymes, sous-thèmes,
   mécanismes, revues de littérature), en excluant les requêtes déjà exécutées. Table `queries`
   (thème, source, langue, texte, cycle, statut) créée par migration — elle servira à S07.
4. **Synchronisation charte ↔ fichier** : la charte est en base et dans `charte.yaml` ; une
   modification manuelle du fichier est détectée (empreinte) et **prime** ; `verrouille: true`
   empêche toute réécriture automatique. Les synonymes alimentent `theme_aliases`.
5. **Sous-thèmes proposés** : stockés comme suggestions ; politique `auto` (création jusqu'à
   `max_depth`) ou `validation` selon `config.yaml` ; commandes `ragc theme suggestions` et
   `ragc theme accept <suggestion>`.
6. **Commandes** : `ragc theme plan <chemin>` (une fois), `ragc theme plan --pending` (tous les
   thèmes sans charte, **parents d'abord**), `ragc theme charter <chemin>` (affiche la charte).
7. **Tests** : faux serveur avec chartes de référence pour l'exemple
   `Pharmacologie > Champignons > Amanita muscaria` ; ordre parent → enfant ; priorité des
   modifications manuelles ; verrouillage ; requêtes non répétées.

## Évaluation en conditions réelles (si disponible)

Génère 10 fois les chartes des 3 niveaux de l'exemple et mesure : taux de JSON valide (cible
≥ 95 %), cohérence parent/enfant (vérifiée à la main sur 3 cas), présence de *A. pantherina*
dans les confusions d'*A. muscaria*, présence de « toxicité » et « dose » dans les affirmations
sensibles. Note les résultats et les ajustements de prompt dans le journal.

## Hors de cette session

Aucune recherche web réelle (S07) : P02 produit des requêtes, personne ne les exécute encore.

## Critères d'acceptation

- [ ] `ragc theme plan --pending` produit des chartes pour tout l'arbre, parents d'abord.
- [ ] `charte.yaml` lisible, en français, modifiable, et la modification est respectée.
- [ ] P01 et P02 versionnés, conformes aux conventions, rendus visibles par `ragc prompts show`.
- [ ] Mesures en conditions réelles notées (ou « non mesuré »).
- [ ] Procédure de clôture appliquée.
