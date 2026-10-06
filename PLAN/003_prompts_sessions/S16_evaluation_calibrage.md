# S16 — Évaluation globale, comparaison des modes, calibrage

> Jalon J6 · Dépend de : S15 · Étapes : — · Prompts d'exécution : V01, V02
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (en entier), `PLAN/001_but.md`
(**§7, §9**), `PLAN/002_strategie.md` (§6, §7, **§8**, **§10**), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md` (toutes les mesures). Respecte-les. En cas de contradiction, arrête-toi et pose
la question.

## Objectif

Mesurer honnêtement si le but est atteint (`001_but.md` §9), **calibrer** les réglages sur des
données, comparer les modes de réponse, et vérifier les promesses structurantes : portabilité,
pilotage, spécialistes, généralisation, changement de modèle de base.

## À réaliser

1. **Jeu d'évaluation** (`ragc eval build`, **V01**) : questions factuelles, multi-sauts,
   transversales, temporelles, sans réponse, réparties sur tous les domaines ; échantillon relu
   par l'utilisateur ; + vos **vraies questions** notées.
2. **Contrôles déterministes d'abord** (versions, identifiants, articles, valeurs) ; **V02** pour
   la fidélité et la complétude, juge différent du constructeur si possible.
3. **Scénarios d'évaluation** (`ragc eval run|compare`, à lancer sur vos PC) :
   - cas A–I, qualité du plan, rappel, bonne version, fidélité, étiquetage, angle, abstention ;
   - modes de réponse : RAG direct (MiMo / spécialistes), Qwen3.8 + adaptateur, Qwen3.8 seul,
     navigation libre ; durée, tokens, **rechargements** ;
   - **spécialistes** : chaque spécialiste contre l'enseignant ; **généralisation** sur le hacking ;
   - **changement de modèle de base** : `retrain --base` complet sur une autre base, de bout en
     bout ;
   - **pilotage** : pause / reprise / arrêt brutal pendant chaque phase ;
   - **installation** sur un PC neuf, Windows et Linux ;
   - OCR (cas E), gain avec / sans RAG sur Qwen3.8.
4. **Calibrage** : poids de la vérification et de la crédibilité (pondération entropique comparée
   aux poids manuels), formule d'importance, tailles d'extraits par profil, k, re-classement CPU /
   GPU, réflexion par étape, quantifications, modèles d'embedding et de re-classement récents
   (EdA §10, disponibilité en GGUF vérifiée).
5. **Rapport** `reports/eval/<date>.md` + journal ; **proposition** de mise à jour des valeurs par
   défaut de `002` et des cibles de `001` §9, à valider par l'utilisateur.
6. **Finitions** : README complet (installation Windows et Linux, premiers pas avec les cas A–I,
   pilotage du travail en fond, réentraînement), `docs/` à jour.

## Critères d'acceptation

- [ ] Toutes les cibles de `001_but.md` §9 mesurées sur vos PC ; chaque écart expliqué avec une
      piste.
- [ ] Modes de réponse comparés ; réglages par défaut justifiés par les mesures.
- [ ] Procédure de clôture appliquée.
