# 003 — Prompts des sessions de développement

> Statut : **proposition** · v0.3 · 2026-10-06

Chaque fichier `Sxx_*.md` est un **prompt prêt à coller** dans une nouvelle session Claude Code
ouverte sur ce dépôt (copiez tout ce qui suit la ligne `---`). Les sessions s'enchaînent dans
l'ordre ; chacune lit l'état de l'art, le but, la stratégie, les règles communes et le journal,
livre du code testé, met à jour `PLAN/JOURNAL.md` et pousse ses commits.

| Session | Titre | Étapes | Prompts d'exécution | Dépend de | Jalon |
|---|---|---|---|---|---|
| [S01](S01_socle.md) | Socle : projet, configuration, base, arbre des thèmes | — | — | — | J1 |
| [S02](S02_client_llm.md) | Client LLM, bibliothèque de prompts, journal, `ragc doctor` | — | T00 (test) | S01 | J1 |
| [S03](S03_profils_chartes.md) | Profils de domaine et chartes de thème | E0 | C01, C02 | S02 | J1 |
| [S04](S04_ingestion_datation_decoupage.md) | Ingestion locale, pré-contrôles, datation, versions, découpage par profil | E2, E3, E5, E6 | — | S03 | J1 |
| [S05](S05_lecture_documents.md) | **Lecture des documents** : PDF scannés, livres, OCR spécialisé, figures, contrôle de l'OCR | E2 (lecture) | L01, L02, L03 | S04 | J1 |
| [S06](S06_verification_etiquetage.md) | Vérification des documents, vérification et étiquetage des extraits | E4, E7 | C04, C05, C06 | S05 | J1 |
| [S07](S07_enrichissement_recherche.md) | Enrichissement, indexation, recherche hybride filtrée | E5, E8, E9 | C07, C08 | S06 | J1 |
| [S08](S08_agent_recherche.md) | **Agent de recherche** : situation, plan, recherche, contrôles, hiérarchisation, dossier, angle | R1–R8 | Q01–Q04, Q06 | S07 | J2 |
| [S09](S09_collecte_web.md) | Collecte web, connecteurs par profil, collectes ciblées | E1, E2 | C02, C03 | S08 | J3 |
| [S10](S10_graphe_conflits.md) | Graphe typé, chaînes, qualification des conflits | E10, E11 | C09, C10 | S09 | J4 |
| [S11](S11_temps_veille.md) | Temps : versions, date de référence, veille d'actualisation | E14 | C14 | S10 | J4 |
| [S12](S12_carte_fiches.md) | Carte navigable et fiches | E12 | C11, C12 | S11 | J4 |
| [S13](S13_autonomie.md) | Démon, cycles, couverture, planification | E13 | C13 | S12 | J5 |
| [S14](S14_consommation.md) | Consommation : MCP, proxy OpenAI, navigation libre | — | Q05, Q06, Q07 | S13 | J6 |
| [S15](S15_evaluation_calibrage.md) | Évaluation, comparaison des modes, calibrage | — | V01, V02 | S14 | J6 |
| [S16](S16_specialisation_mimo.md) | *(conditionnelle)* Spécialisation de MiMo | — | — | S15 | J7 |

Remarques

- **J1 (S01 → S07)** donne une base locale vérifiée, étiquetée, datée et interrogeable, qui
  **lit aussi les livres et PDF scannés** (S05).
- **J2 (S08)** apporte tôt le cœur du projet : un RAG qui **raisonne** (plan, hiérarchisation,
  angle). Les sessions suivantes lui ajoutent des capacités (web, graphe, temps, carte).
- Les cas de référence (`001_but.md` §7) : E est créé en S05, A–D en S08 ; ils sont relancés à chaque
  session qui touche à la recherche.
- S16 n'est lancée que si S15 conclut que le critère de `002_strategie.md` §6.9 est rempli.
