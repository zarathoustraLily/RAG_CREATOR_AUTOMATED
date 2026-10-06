# S10 — Interfaces du quotidien (proxy, MCP), phases complètes du travail en fond

> Jalon J3 · Dépend de : S09 · Étapes : — · Prompt d'exécution : Q07
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§9, §11), `PLAN/001_but.md` (§2,
§8), `PLAN/002_strategie.md` (**§3.2, §3.3, §7.5**), `PLAN/004_decisions_techniques.md`,
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

**Première version utilisable au quotidien** : vous posez vos questions dans Open WebUI ou LM
Studio comme d'habitude, le RAG répond ; la construction tourne en fond quand vous le voulez,
avec toutes ses phases, ses plages horaires et ses rapports.

## À réaliser

1. **Proxy compatible OpenAI** (`ragc serve proxy`) : reçoit la conversation, choisit le mode sans
   rechargement selon le modèle chargé, met le travail en fond en pause le temps de la réponse,
   lance l'agent, injecte le dossier et Q06, relaie la réponse en flux, ajoute les sources ;
   contournement `#norag` ; documentation pas à pas **Open WebUI et LM Studio sous Windows**.
2. **Notes des réponses** : récupération des retours d'Open WebUI selon S01, sinon commande
   `ragc rate` ou lien de notation dans la réponse ; tout aboutit dans `questions`.
3. **Outils MCP** (extra `mcp`, SDK officiel — vérifie la version) : `rag_research` et outils de
   bas niveau (`rag_carte`, `rag_chercher`, `rag_lire`, `rag_voisins`, `rag_fiche`,
   `rag_conflits`), schémas compacts ; **Q07 `consumer_agent`**.
4. **Travail en fond complet** : phases P0 → P4 avec les vraies tâches (lecture, construction,
   indexation, enseignant), regroupement par modèle et par adaptateur, boucle tant qu'il reste du
   travail, priorités (demandes manuelles > collectes ciblées > veille > reste).
5. **Plages horaires et démarrage automatique** : Planificateur de tâches (Windows) et
   `systemd --user` (Linux), installés par une commande (`ragc schedule install|remove`).
6. **Rapports** : à chaque arrêt et à heure fixe (`reports/`) — documents vus, acceptés, rejetés
   (motifs), pages lues et douteuses, revues en attente, lacunes comblées, exemples capturés par
   tâche, temps par phase, bascules de modèles ; `ragc report latest|list|show`.
7. **Tests** : proxy (faux serveurs), choix du mode, pause automatique pendant une réponse,
   enchaînement des phases, arrêt brutal pendant chaque phase puis reprise.

## Bancs à ajouter

`ragc bench daily` : une heure de travail en fond réelle (pages traitées, bascules, VRAM libérée
à la pause), puis 10 questions par le proxy (durée, mode choisi, rechargements = 0).

## Critères d'acceptation

- [ ] Open WebUI branché sur le proxy obtient une réponse citée pour les cas A et F.
- [ ] `ragc start` / `pause` / `resume` / `stop` fonctionnent pendant chaque phase ; la VRAM est
      libérée en pause.
- [ ] Rapports lisibles ; plages horaires installables sous Windows et Linux.
- [ ] Procédure de clôture appliquée.
