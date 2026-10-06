# S14 — Consommation : outils MCP, proxy OpenAI, navigation libre

> Jalon J6 · Dépend de : S13 · Étapes : — · Prompts d'exécution : Q05, Q06, Q07
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§2, §4, **§9**, §11),
`PLAN/001_but.md` (§6, §8), `PLAN/002_strategie.md` (**§6.5–6.8**, §7),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Que **Qwen3.8-27B / Qwen3.8-Flash-Next** (ou tout modèle local) utilisent le RAG au quotidien :
par un outil de haut niveau qui délègue la recherche à l'agent MiMo, par des outils de bas
niveau, ou de façon transparente via un proxy pour Open WebUI / LM Studio. Ajouter le mode
**navigation libre** de l'agent, à comparer en S15.

## À réaliser

1. **Outils** (définition unique, réutilisée par MCP, l'API et le proxy), **schémas compacts**
   et réponses plafonnées en tokens (EdA §9) :
   - haut niveau : `rag_research(question, focus?, date_reference?, budget?)` → dossier ;
   - bas niveau : `rag_carte(chemin?)`, `rag_chercher(requete, themes?, filtres?, date?)`,
     `rag_lire(id, niveau: extrait|section|document|page)`, `rag_voisins(entite, famille?)`,
     `rag_fiche(entite|chemin)`, `rag_conflits(theme|entite)`.
   Mesure de la taille des schémas en tokens ; version compressée si nécessaire.
2. **Serveur MCP** (extra `mcp`, SDK Python officiel — vérifie la version et l'API actuelles) :
   transport stdio, et HTTP si utile ; documentation de branchement.
3. **Proxy compatible OpenAI** (`ragc serve proxy`) : reçoit une conversation, appelle
   `rag_research` sur la dernière question (avec l'angle du profil utilisateur), injecte le
   dossier et le prompt système **Q06 `consumer_answer`**, relaie vers le `llama-server` de
   Qwen3.8 (streaming), ajoute les sources en fin de réponse ; contournement possible
   (`#norag`). Documentation pas à pas pour **Open WebUI** et **LM Studio**.
4. **Q07 `consumer_agent`** : prompt système pour Qwen3.8 utilisant lui-même les outils de bas
   niveau (citer, s'appuyer sur les preuves, plafonner les appels, signaler lacunes et conflits).
5. **Navigation libre** (`002_strategie.md` §6.7) : boucle d'outils de MiMo avec **Q05
   `research_agent_tools`** via l'appel d'outils de `llama-server` ; budget d'appels et de tokens ;
   sortie = même format de dossier ; option `ragc ask --mode navigation`.
6. **Trajectoires** : toutes les exécutions (plan → exécution, navigation libre, consommateur
   outillé) enregistrées dans `research_runs` au même format (données pour S15 et S16).
7. **API HTTP** (extra `api`) : `/search`, `/research`, `/ask`, `/themes`, `/map`.
8. **Exports** : JSONL (extraits + étiquettes + validité), Markdown (fiches, carte), GraphML.
9. **Tests** : schémas d'outils (taille, validité), proxy (faux serveur Qwen3.8), boucle d'outils
   (faux serveur), budget respecté, format de dossier identique entre modes.

## Expériences en conditions réelles (si disponibles)

Cas A–E via le proxy avec Qwen3.8-27B : temps total, part du dossier réellement citée dans la
réponse (usage du contexte), réponses « absent de la base » correctes. Navigation libre contre
plan → exécution : premiers chiffres (la comparaison complète est en S15).

## Critères d'acceptation

- [ ] Open WebUI (ou `curl`) branché sur le proxy obtient une réponse citée pour le cas B.
- [ ] Un client MCP liste et appelle `rag_research` et les outils de bas niveau.
- [ ] `ragc ask --mode navigation` produit un dossier au même format.
- [ ] Procédure de clôture appliquée.
