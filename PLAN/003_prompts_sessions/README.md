# 003 — Prompts des sessions de développement

> Statut : **brouillon en cours de révision** · v0.1 · 2026-10-06
> S11, S12, S13 restent à rédiger ; le plan sera revu pour placer au centre l'agent qui
> construit la logique de recherche, l'arbre relationnel des sources et la vérification
> d'actualisation (retour utilisateur du 2026-10-06).

Chaque fichier `Sxx_*.md` est un **prompt prêt à coller** dans une nouvelle session Claude Code
ouverte sur ce dépôt (copiez tout ce qui suit la ligne `---`). Les sessions s'enchaînent dans
l'ordre ; chacune lit le but, la stratégie, les règles communes et le journal, puis livre du code
testé, met à jour `PLAN/JOURNAL.md` et pousse ses commits.

| Session | Titre | Étapes pipeline | Prompts d'exécution créés | Dépend de | Jalon |
|---|---|---|---|---|---|
| [S01](S01_socle.md) | Socle : projet, configuration, base, arbre des thèmes | — | — | — | J1 |
| [S02](S02_client_llm.md) | Client LLM, bibliothèque de prompts, journal, `ragc doctor` | — | P00 (test) | S01 | J1 |
| [S03](S03_charte_theme.md) | Charte de thème et sous-thèmes | E0 | P01, P02 | S02 | J1 |
| [S04](S04_ingestion_locale.md) | Ingestion locale, extraction, pré-contrôles, découpage | E2, E3, E5 | — | S01 | J1 |
| [S05](S05_verification.md) | **Vérification** des documents et des extraits | E4, E6 | P04, P05, P06 | S03, S04 | J1 |
| [S06](S06_enrichissement_index.md) | Enrichissement, indexation, recherche hybride | E7, E8 | P07, P08 | S05 | J1 |
| [S07](S07_collecte_web.md) | Collecte web autonome | E1, E2 | P02 (sources), P03 | S06 | J2 |
| [S08](S08_graphe_croisement.md) | Graphe d'entités et vérification croisée | E9, E10 | P09, P10 | S06 | J3 |
| [S09](S09_syntheses.md) | Fiches, résumés de communautés, synthèses de thème | E11 | P11, P12, P13 | S08 | J3 |
| [S10](S10_autonomie.md) | Démon, cycles, analyse de couverture, rapports | E12 | P14 | S07, S09 | J4 |
| [S11](S11_consommation.md) | Consommation multithématique : routage, contexte, MCP, proxy, agent MiMo | requête | P17–P20 | S10 | J5 |
| [S12](S12_evaluation.md) | Évaluation, calibrage, comparaison des agents | E13 | P15, P16 | S11 | J5 |
| [S13](S13_lora_agent_mimo.md) | *(conditionnelle)* Spécialisation LoRA de MiMo agent de recherche | — | — | S12 | J6 |

Remarques

- **J1 (S01 → S06)** donne déjà un RAG utilisable à partir de vos fichiers locaux.
- S04 ne dépend que de S01 : elle peut être menée en parallèle de S02–S03 si vous le souhaitez.
- Les prompts d'exécution (ceux que lit MiMo) sont rédigés dans la session qui crée l'étape
  correspondante, selon les conventions de `002_strategie.md` §7.
- S13 n'est lancée que si S12 conclut que le critère de `002_strategie.md` §6.4 est rempli.
