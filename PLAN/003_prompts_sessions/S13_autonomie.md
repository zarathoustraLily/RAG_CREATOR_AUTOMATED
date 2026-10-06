# S13 — Autonomie : démon, cycles, couverture, planification (E13)

> Jalon J5 · Dépend de : S12 · Étape : E13 · Prompt d'exécution : C13
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md`, `PLAN/001_but.md` (§2, §10),
`PLAN/002_strategie.md` (§4.3, §4.6, §5, **§8**), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Que tout tourne **seul, en tâche de fond, sans gêner l'usage du poste** : construction par
cycles, lecture des livres, veille d'actualisation, collectes ciblées issues des questions —
avec un rapport clair à chaque cycle.

## À réaliser

1. **Démon** (`ragcreator/daemon/`) : `ragc daemon start|stop|status|pause|resume|logs`,
   `--foreground` pour `systemd`, fichier PID + verrou, `SIGTERM` propre, `SIGHUP` = rechargement.
2. **Ordonnanceur asynchrone** fondé sur l'exécuteur de S04 : sémaphores par ressource (slots de
   chaque profil, OCR, embeddings, re-classement, requêtes par domaine), **tourniquet entre
   thèmes**, priorités : demandes manuelles > **collectes ciblées** (lacunes) > veille due >
   cycles ; baux avec expiration.
3. **Cycles** par thème (E1 → E13) et statuts du thème ; revisite périodique des thèmes stables.
4. **C13 `coverage_analysis`** (réflexion) : couverture par sous-thème et par sous-question
   fréquente des dossiers, lacunes, nouvelles requêtes (via C02), sous-thèmes à proposer,
   `continuer | arreter` motivé ; le **profil utilisateur** oriente l'effort (thèmes privilégiés
   approfondis en premier).
5. **Critères d'arrêt** configurables : couverture cible, cycles maximum, **rendements
   décroissants** (< 10 % de nouveaux documents acceptés), budget horaire.
6. **Planification** de la veille (S11) et des lectures longues (S05) dans les plages autorisées.
7. **Discrétion et cohabitation** (`002_strategie.md` §4.3) : `os.nice`, plages horaires, pause
   sur batterie (optionnel), slots limités ; constructeur ou OCR indisponible (scénario B) →
   étapes concernées en attente sans échec, le reste continue.
8. **Rapport de cycle** `reports/<date>_<theme>.md` : vus / acceptés / rejetés (motifs regroupés),
   pages lues et pages douteuses, revues en attente, conflits nouveaux, nouvelles versions,
   lacunes comblées, couverture avant / après, temps et tokens par étape ;
   `ragc report latest|list|show`.
9. **Services** : unité `systemd --user`, plist `launchd`, `docs/demon.md` ; lancement optionnel
   des `llama-server` via des commandes configurées.
10. **Tests** : cycle complet sur l'arbre d'exemple (faux serveurs, sources simulées), **arrêt
    brutal** au milieu d'un cycle et au milieu d'un livre → reprise sans perte ni double
    traitement ; serveur absent puis présent ; critères d'arrêt ; priorités.

## Expériences en conditions réelles (si disponibles)

Une nuit complète sur les thèmes des cas A, B et D : cycles, documents acceptés, livres lus,
couverture finale, comportement pendant l'usage de Qwen3.8. Joindre le rapport au journal.

## Critères d'acceptation

- [ ] `ragc theme add …` puis `ragc daemon start` suffisent pour obtenir, sans autre action, un
      thème `stable` avec rapport.
- [ ] Une lacune signalée par l'agent est comblée par une collecte ciblée au cycle suivant.
- [ ] Le test d'arrêt brutal passe ; le poste reste utilisable ; la pause fonctionne.
- [ ] Procédure de clôture appliquée.
