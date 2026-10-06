# S12 — Spécialistes de l'agent, adaptateur « recherche » sur Qwen3.8, navigation libre

> Jalon J4 · Dépend de : S11 · Étapes : — · Prompt d'exécution : Q05
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§1, §4, §7, §14, §17**),
`PLAN/001_but.md` (§6, §9), `PLAN/002_strategie.md` (**§3.3, §7, dont §7.6, §8**), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md` (rapports de S11). Respecte-les. En cas de contradiction, arrête-toi et pose la
question.

## Objectif

Spécialiser **le cœur de l'agent** — situation et plan, sélection des preuves, dossier et
rédaction — et réaliser votre idée : un **adaptateur « recherche » posé sur Qwen3.8**, activé à
la volée, pour que le modèle du quotidien mène lui-même la recherche **sans changer de modèle**.

## À réaliser

1. **Données de l'agent** : `research_runs` + vos notes et corrections (`questions`) + questions
   générées par l'enseignant sur vos thèmes (jamais les cas de référence ni le hacking) ;
   exemples **or** (vos notes ≥ 4 ou corrigées, contrôles déterministes passés) et **argent**
   (trajectoires de l'enseignant filtrées par critères vérifiables : couverture, bonne version,
   extraits attendus, fidélité, budget).
2. **Spécialistes** (base du profil matériel) : *planif* (Q01–Q02, Q08, supervision avec
   raisonnement), *selection* (Q03), *dossier* (Q04, Q06) ; mêmes porte de promotion et registre
   qu'en S11. *planif* apprend la **procédure** (lire le menu transversal, appliquer chaque
   grille, fusionner, critiquer) : ses exemples contiennent toujours le menu en entrée, jamais
   un répertoire recopié dans la sortie ; le répertoire reste externe et modifiable.
2 bis. **Porte d'étendue** pour *planif* : sur des questions transversales tenues à l'écart
   (dont le hacking et des questions nouvelles), le candidat doit égaler le modèle de base guidé
   par le répertoire en **couverture transversale** (grilles traitées, disciplines distinctes,
   analogues exploités, mesurée sur plusieurs tirages) ; sinon il n'est pas promu, même s'il
   est meilleur sur les sous-questions attendues.
3. **Adaptateur « recherche » sur Qwen3.8-27B** : entraînement avec déchargement de couches (5090
   d'abord), éventuellement en plusieurs nuits avec reprise ; service sur le modèle du quotidien
   (`lora` par requête : actif pendant R1–R8, inactif pour la réponse) ; mode correspondant dans
   §3.3 activé automatiquement s'il est promu.
4. **Renforcement à récompense vérifiable** (GRPO ou équivalent, selon l'outil) pour *planif* et
   *selection* : récompense composée (couverture des sous-questions attendues, **couverture des
   angles** comptée par grilles et disciplines plutôt que par mots, bonne version, extraits
   attendus, fidélité, coût en tokens), **plusieurs formes de récompense comparées**, plusieurs
   graines (EdA §7) ; surveiller la **diversité** des plans (EdA §17) et l'inclure dans la
   récompense si elle baisse ; optionnel si le banc montre que c'est trop long.
5. **Navigation libre** (`002_strategie.md` §7) : boucle d'outils avec **Q05
   `research_agent_tools`**, même format de dossier ; `ragc ask --mode navigation` (comparée en
   S16).
6. **Réentraînement** : ces adaptateurs sont inclus dans `ragc specialists retrain --base` ;
   changement du modèle du quotidien → seul l'adaptateur « recherche » est refait.
7. **Tests** hors ligne : jeux sans fuite, choix du mode selon les adaptateurs promus, adaptateur
   actif pendant la recherche et inactif pour la réponse, boucle d'outils bornée.

## Bancs à ajouter

`ragc bench agent-specialists` : cas A–I et 30 de vos vraies questions — MiMo par prompts,
spécialistes, Qwen3.8 + adaptateur : qualité du plan, fidélité, durée, rechargements ;
généralisation au cas H (domaine tenu à l'écart) ; durée d'entraînement de l'adaptateur Qwen3.8.

## Critères d'acceptation

- [ ] Les spécialistes de l'agent ne sont promus que s'ils passent la porte (sinon, raisons
      chiffrées).
- [ ] L'adaptateur Qwen3.8, s'il est promu, permet une question **sans aucun rechargement** pendant
      une conversation avec Qwen3.8.
- [ ] Procédure de clôture appliquée.
