# S10 — Autonomie : démon, cycles, analyse de couverture, rapports (E12)

> Jalon J4 · Dépend de : S07, S09 · Étape du pipeline : E12 · Prompt : P14
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md`, `PLAN/002_strategie.md` (§3.2 scénarios de
cohabitation, §3.5, §5.1, **§8**), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Que tout tourne **seul, en tâche de fond, sans gêner l'usage du poste** : vous ajoutez un thème,
le programme enchaîne les cycles jusqu'à une couverture satisfaisante, et vous laisse un rapport.

## À réaliser

1. **Démon** (`ragcreator/daemon/`) : `ragc daemon start|stop|status|pause|resume|logs` ;
   mode premier plan (`--foreground`) pour `systemd` ; fichier PID + verrou ; `SIGTERM` = arrêt
   propre (fin des appels en cours dans un délai maximal) ; `SIGHUP` = rechargement de la
   configuration.
2. **Ordonnanceur asynchrone** fondé sur l'exécuteur de S04 : sémaphores par ressource (slots de
   chaque profil, embeddings, re-classement, requêtes par domaine) ; **tourniquet entre
   thèmes** ; priorité aux ajouts manuels (inbox, `add-url`) ; **baux** avec expiration pour
   reprendre une tâche interrompue.
3. **Cycles** (table `cycles`) : E1 → E12 par thème ; transitions de statut du thème (§5.1) ;
   revisite périodique des thèmes `stable` (période configurable).
4. **Prompt P14 `coverage_analysis`** (réflexion activée) : entrées = charte, couverture mesurée
   par sous-thème et mot-clé (nombre d'extraits acceptés trouvés par la recherche hybride),
   échantillon de titres, statistiques du cycle ; sorties = lacunes, nouvelles requêtes (via P02),
   sous-thèmes à proposer, décision `continuer | arreter` motivée.
5. **Critères d'arrêt** codés (configurables) : couverture cible, nombre maximal de cycles,
   **rendements décroissants** (< 10 % de nouveaux documents acceptés), budget horaire.
6. **Discrétion** : `os.nice`, plages horaires, pause sur batterie (optionnel), nombre de slots
   limité ; **constructeur indisponible** (scénario B : Qwen3.8 occupe la mémoire) → les étapes
   LLM attendent avec temporisation croissante sans marquer d'échec, collecte et indexation
   continuent.
7. **Rapport de cycle** `reports/<date>_<theme>.md` : documents vus / acceptés / rejetés (motifs
   regroupés), en revue, contradictions nouvelles, sous-thèmes proposés, couverture avant/après,
   temps et tokens par étape. `ragc report latest|list|show`.
8. **Services** : unité `systemd --user`, `launchd` (plist), documentation `docs/demon.md` ;
   option de lancement automatique des `llama-server` via des commandes configurées.
9. **Tests** : cycle complet de bout en bout sur l'arbre d'exemple avec le faux serveur et des
   sources simulées ; **arrêt brutal** au milieu d'un cycle puis redémarrage → aucune perte,
   aucun double traitement ; constructeur absent puis présent ; critères d'arrêt.

## Expériences en conditions réelles (si disponible)

Une nuit complète sur `pharmacologie/champignons/amanita-muscaria` : nombre de cycles, documents
acceptés, couverture finale, temps total, comportement pendant l'usage de Qwen3.8. Joindre le
rapport au journal.

## Critères d'acceptation

- [ ] `ragc theme add …` puis `ragc daemon start` suffisent pour obtenir, sans autre action, un
      thème `stable` avec rapport.
- [ ] Le test d'arrêt brutal passe.
- [ ] Le poste reste utilisable (priorité basse, slots limités) ; la pause fonctionne.
- [ ] Procédure de clôture appliquée.
