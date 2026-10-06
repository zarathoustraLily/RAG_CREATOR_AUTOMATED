# S15 — Évaluation, comparaison des modes, calibrage

> Jalon J6 · Dépend de : S14 · Étapes : — · Prompts d'exécution : V01, V02
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (en entier), `PLAN/001_but.md`
(**§7, §9**), `PLAN/002_strategie.md` (§5.1, §6.4, §6.7, **§6.9**, **§9**),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md` (toutes les mesures
précédentes). Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Mesurer honnêtement si le but est atteint (`001_but.md` §9), **calibrer** les réglages sur des
données plutôt qu'à l'intuition, comparer les modes d'agent, et décider s'il faut spécialiser
MiMo (S16).

## À réaliser

1. **Jeu d'évaluation** (`ragc eval build`) — **V01 `eval_questions`** sur un échantillon
   stratifié d'extraits (par profil et sous-thème) : questions factuelles, multi-sauts (chaînes du
   graphe), **transversales** (plusieurs thèmes), **temporelles** (date de référence),
   **sans réponse** ; filtrage (réponse présente uniquement dans l'extrait, pas de recopie mot à
   mot) ; échantillon relu par l'utilisateur.
2. **Contrôles déterministes d'abord** (EdA §3) : versions en vigueur, identifiants cités,
   numéros d'articles, valeurs ; **V02 `eval_judge`** seulement pour la fidélité et la
   complétude, avec un juge différent du constructeur quand c'est possible.
3. **Métriques** (`ragc eval run|compare`) : qualité du plan (cas A–E), Recall@k, MRR, nDCG,
   bonne version, fidélité des citations, étiquetage de la solidité, respect de l'angle,
   présence du contre-point, abstention, latence, tokens, coût par étape ; OCR (jeu de
   référence et cas E) ; **évaluation des trajectoires** (étapes inutiles, boucles, budget) ;
   **gain avec / sans RAG** sur Qwen3.8.
4. **Comparaison des modes** (`002_strategie.md` §6.9 palier 1) : (a) recherche simple
   améliorée, (b) Qwen3.8 outillé, (c) MiMo plan → exécution, (d) MiMo navigation libre.
5. **Calibrage** :
   - poids de la vérification documentaire et de la crédibilité par **pondération entropique**
     sur les décisions annotées (EdA §12), comparée aux poids manuels ;
   - poids et forme de la formule d'importance (`P × S × A × F × R`) ;
   - tailles d'extraits par profil, k, re-classement, réflexion on / off par étape, quantification
     de MiMo (Q4_K_M / Q5_K_M / Q8_0), moteur OCR ;
   - **modèles d'embedding et de re-classement** : bge-m3 / bge-reranker-v2-m3 contre des modèles
     plus récents (EdA §10) — vérifie leur disponibilité en GGUF et leur prise en charge.
6. **Décision S16** : critère de `002_strategie.md` §6.9 rempli ou non, chiffres à l'appui.
7. **Rapport** `reports/eval/<date>.md` + mise à jour du journal ; **proposition** de mise à jour
   des valeurs par défaut de `002_strategie.md` et des cibles de `001_but.md` §9 — à valider par
   l'utilisateur avant modification.
8. **Finitions** : README complet en français (installation, premiers pas avec les cas A–E,
   dépannage), `docs/` à jour.

## Critères d'acceptation

- [ ] Toutes les cibles de `001_but.md` §9 mesurées ; chaque écart expliqué avec une piste.
- [ ] Comparaison des quatre modes chiffrée ; réglages par défaut justifiés par les mesures.
- [ ] Décision S16 argumentée.
- [ ] Procédure de clôture appliquée.
