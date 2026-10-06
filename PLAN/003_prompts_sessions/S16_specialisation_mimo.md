# S16 — *(conditionnelle)* Spécialisation de MiMo comme agent de recherche

> Jalon J7 · Dépend de : S15 (**à lancer seulement si S15 a conclu que le critère est rempli**)
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§1, §7**), `PLAN/001_but.md`
(§6), `PLAN/002_strategie.md` (**§6.9**), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md` (**décision de S15**). Si la décision de S15 n'est pas « spécialiser »,
arrête-toi et dis-le.

## Objectif

Rendre MiMo **meilleur et plus rapide comme agent de recherche** (analyse, plan, sélection des
preuves) par entraînement sur des données **vérifiables** produites par le RAG lui-même, sans
dégrader ses autres rôles.

## À réaliser

1. **Outils d'entraînement** : vérifie à la date de la session quelles bibliothèques prennent en
   charge l'architecture de MiMo (Qwen3.5 hybride) pour LoRA / QLoRA et pour le renforcement
   (GRPO ou équivalent) : Unsloth, TRL / PEFT, LLaMA-Factory… ; mémoire GPU nécessaire ; note le
   choix et ses raisons. Extra `train`.
2. **Données (palier 2, SFT)** : `ragc train dataset` à partir de `research_runs` :
   - un **professeur** (Qwen3.8-27B) produit des trajectoires sur des questions d'entraînement
     (jamais celles de l'évaluation) ;
   - **filtrage par critères vérifiables** : couverture des sous-questions attendues, bonnes
     versions, extraits attendus retrouvés, citations fidèles, budget respecté ;
   - **planificateur (Q01–Q02) et sélecteur (Q03) en jeux séparés** (EdA §1) ;
   - formatage au **modèle de chat exact** de MiMo (appliqué avec le tokenizer officiel) ;
   - séparation par **thèmes** : thèmes tenus à l'écart pour l'évaluation.
3. **Entraînement LoRA** (`scripts/train/lora_sft.py`) : hyperparamètres documentés, suivi des
   pertes, sauvegardes ; conversion de l'adaptateur en GGUF (outil de llama.cpp) ; chargement
   dans `llama-server` (`--lora`) ; profil `mimo-9b-rag` utilisé **uniquement** pour l'agent de
   recherche (les étapes de construction gardent MiMo de base).
4. **Palier 3 (optionnel, renforcement)** : récompense vérifiable composée — couverture du plan,
   bonne version, rappel des extraits attendus, fidélité des citations, **moins** le coût en
   tokens ; étudier plusieurs formes de récompense (EdA §7 : récompenser seulement la réponse
   exacte est la pire option) ; plusieurs graines.
5. **Évaluation** : relancer S15 (modes c et d avec `mimo-9b-rag`) sur les **thèmes tenus à
   l'écart** et les cas A–E ; vérifier l'absence de régression sur les étapes de construction et
   sur le format JSON.
6. **Décision** : garder ou abandonner l'adaptateur, chiffres à l'appui ; procédure de
   ré-entraînement documentée (quand l'interface des outils ou le corpus change beaucoup).

## Critères d'acceptation

- [ ] Gain mesuré sur thèmes tenus à l'écart (qualité du plan, fidélité, latence), ou abandon
      argumenté.
- [ ] Aucune régression des étapes de construction.
- [ ] Adaptateur chargé par `llama-server` et utilisé par le profil `mimo-9b-rag`.
- [ ] Procédure de clôture appliquée.
