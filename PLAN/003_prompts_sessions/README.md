# 003 — Prompts des sessions de développement

> Statut : **proposition** · v0.5 · 2026-10-06

Chaque fichier `Sxx_*.md` est un **prompt prêt à coller** dans une nouvelle session Claude Code
ouverte sur ce dépôt (copiez tout ce qui suit la ligne `---`). Les sessions se déroulent **dans
le cloud** (sans GPU) ; les mesures réelles se font sur vos PC avec le banc de mesure.

| Session | Titre | Étapes | Prompts d'exécution | Dépend de | Jalon |
|---|---|---|---|---|---|
| [S01](S01_etude_mesures.md) | Étude « réutiliser ou construire », portabilité, banc de mesure | — | — | — | J0 |
| [S02](S02_socle_installable.md) | Socle installable, gestionnaire de modèles, **travail en fond pilotable** | — | — | S01 | J1 |
| [S03](S03_client_llm_exemples.md) | Client LLM, prompts, journal, **capture des exemples**, adaptateurs par requête | — | T00 | S02 | J1 |
| [S04](S04_profils_chartes.md) | Profils de domaine et chartes | E0 | C01, C02 | S03 | J1 |
| [S05](S05_ingestion_lecture.md) | Ingestion, bibliothèque, **lecture (OCR, livres)**, datation, découpage | E2, E3, E5, E6 | L01–L03 | S04 | J1 |
| [S06](S06_verification_etiquetage.md) | Vérification et étiquetage, routine de validation | E4, E7 | C04–C06 | S05 | J1 |
| [S07](S07_enrichissement_recherche.md) | Enrichissement, indexation, recherche hybride filtrée | E5, E8, E9 | C07, C08 | S06 | J1 |
| [S08](S08_collecte_connecteurs.md) | Module **Méthodologie et technique de recherche** branché, collecte assistée, connecteurs prioritaires | E1, E2 | C02, C03 | S07 | J1 |
| [S09](S09_agent_recherche.md) | **Agent de recherche**, modes sans rechargement, journal des questions, cas A–I | R1–R8 | Q01–Q04, Q06 | S08 | J2 |
| [S10](S10_interfaces_quotidien.md) | Interfaces du quotidien (proxy, MCP), phases complètes du travail en fond | — | Q07 | S09 | J3 |
| [S11](S11_usine_specialistes.md) | **Usine à spécialistes**, réentraînement en une commande | P5 | — | S10 | J4 |
| [S12](S12_specialistes_agent.md) | Spécialistes de l'agent, **adaptateur « recherche » sur Qwen3.8**, navigation libre | — | Q05 | S11 | J4 |
| [S13](S13_temps_veille.md) | Temps : versions, date de référence, veille | E14 | C14 | S12 | J5 |
| [S14](S14_graphe_conflits.md) | Graphe typé et conflits | E10, E11 | C09, C10 | S13 | J5 |
| [S15](S15_carte_fiches.md) | Carte navigable, fiches, couverture | E12, E13 | C11–C13 | S14 | J5 |
| [S16](S16_evaluation_calibrage.md) | Évaluation globale, comparaison des modes, calibrage | — | V01, V02 | S15 | J6 |

Remarques

- **Première version utilisable au quotidien : S10** (J3), sur les domaines prioritaires
  (escroqueries, fiscalité géorgienne) et votre bibliothèque.
- Les profils de **tous** les domaines sont écrits en S04 (ce sont des fichiers de
  configuration) ; leurs sources sont branchées en S08 (prioritaires) puis au fil des sessions.
- Le **hacking** est le domaine **tenu à l'écart** de l'entraînement des spécialistes (S11, S12),
  pour vérifier qu'ils généralisent.
- Après S01, lancez le banc sur vos deux PC : ses rapports orientent les choix de S02 à S05.
