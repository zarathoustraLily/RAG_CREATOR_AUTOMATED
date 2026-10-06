# S02 — Client LLM, bibliothèque de prompts, journal des appels, `ragc doctor`

> Jalon J1 · Dépend de : S01 · Étapes du pipeline : — · Prompts d'exécution : P00 (test)
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md`, `PLAN/002_strategie.md` (en particulier
§3.1, §3.2, §7), `PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`.
Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Une couche d'accès aux modèles **fiable, mesurable et agnostique** : tout le reste du projet
appellera le modèle à travers elle. C'est elle qui garantit le JSON valide, la réflexion
activée ou non, le repli entre profils et la traçabilité.

## À réaliser

1. **Client de chat asynchrone** compatible OpenAI (`/v1/chat/completions`, `httpx`) :
   - profils de `config.yaml` (URL, nom de modèle, échantillonnage, nombre de slots) ;
     sémaphore par profil = nombre de slots ;
   - **liste de profils avec repli** par étape : santé des serveurs mise en cache
     (`/health`, `/v1/models`), bascule sur le profil suivant si le préféré ne répond pas ;
   - **réflexion** : `chat_template_kwargs: {"enable_thinking": bool}` par requête ; lecture de
     `reasoning_content` ; à défaut, retrait des blocs `<think>…</think>` du contenu ;
   - délais, nouvelles tentatives avec temporisation croissante, erreurs typées
     (serveur absent, contexte dépassé, réponse invalide) ;
   - en-tête `X-RAGC-Prompt: <id>@<version>` sur chaque requête (utile au faux serveur).
2. **Sorties structurées** : `complete_json(prompt_id, variables, schema)` avec trois modes :
   `schema` (`response_format` de type `json_schema` → grammaire llama-server), `prompt`
   (schéma décrit dans le prompt, JSON extrait du contenu), `auto`. Validation Pydantic, puis
   jusqu'à 2 tentatives de **réparation** en renvoyant l'erreur au modèle.
3. **Bibliothèque de prompts** (`ragcreator/prompts/`) : fichiers YAML (`id`, `version`,
   `description`, `reflexion`, `temperature`, `max_tokens`, `systeme`, `utilisateur`, `schema`),
   gabarits `${variable}` (variable manquante = erreur), **surcharge par thème** depuis
   `themes/<chemin>/prompts/`. Commandes `ragc prompts list|show|render`.
   Rédige `ragcreator/prompts/README.md` (conventions de `002_strategie.md` §7.1) et le prompt
   de test **P00 `ping_json`**.
4. **Journal des appels** (`llm_calls`) : prompt@version + empreinte, profil, modèle, réflexion,
   tokens entrée/sortie, durées (premier token, total), succès / erreur de validation /
   réparations, références (thème, document, extrait). Stockage du texte complet optionnel
   (`config.yaml`).
5. **Clients embeddings et re-classement** : `/v1/embeddings` par lots (dimension détectée et
   enregistrée), `/v1/rerank` de llama-server.
6. **Comptage de tokens** : estimation rapide + calibrage via l'endpoint `/tokenize`.
7. **`ragc doctor`** : vérifie chaque serveur, la présence des modèles, un appel P00 avec et sans
   réflexion, mesure les tokens/s, la dimension des embeddings, le re-classement ; rapport clair
   en français avec la commande à lancer en cas de problème.
8. **Scripts** `scripts/llama/start_constructeur.sh`, `start_embeddings.sh`, `start_reranker.sh`
   (commandes de `002_strategie.md` §3.1, paramétrables par variables d'environnement, `nice`)
   et `docs/llama-server.md` (dont un exemple pour servir Qwen3.8-27B comme profil secondaire).
9. **Faux serveur compatible OpenAI** pour les tests (transport `httpx` simulé) : réponses
   programmables par `X-RAGC-Prompt`, simulation de JSON invalide, de panne, de lenteur.

## Expériences à mener en conditions réelles (si les serveurs sont disponibles)

Note les résultats dans le journal — ils conditionnent les sessions suivantes :

1. Le mode `schema` fonctionne-t-il **avec la réflexion activée** sur MiMo ? Sinon, quel mode
   retenir par défaut quand la réflexion est active ?
2. Débit en tokens/s avec 1 et 4 requêtes simultanées.
3. Taux de JSON valide sur 20 appels P00 dans chaque mode.
4. Effet du cache de préfixe : temps jusqu'au premier token avec un long préfixe identique répété.

## Hors de cette session

Aucun prompt métier (charte, vérification…) : seulement l'infrastructure et P00.

## Critères d'acceptation

- [ ] Tests hors ligne : réflexion on/off, retrait de `<think>`, modes `schema`/`prompt`,
      réparation réussie puis échouée, repli de profil, serveur absent, journalisation complète.
- [ ] `ragc prompts render ping_json` affiche le prompt rendu ; une surcharge de thème est prise
      en compte.
- [ ] `ragc doctor` donne un diagnostic lisible, serveurs présents ou absents.
- [ ] Résultats des 4 expériences notés dans le journal (ou « non mesuré » explicite).
- [ ] Procédure de clôture appliquée.
