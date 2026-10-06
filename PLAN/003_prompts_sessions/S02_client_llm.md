# S02 — Client LLM, bibliothèque de prompts, journal des appels, `ragc doctor`

> Jalon J1 · Dépend de : S01 · Étapes : — · Prompts d'exécution : T00 (test)
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§9), `PLAN/001_but.md`,
`PLAN/002_strategie.md` (§4.1–4.3, §7), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Une couche d'accès aux modèles **fiable, mesurable et agnostique**, par laquelle passera tout
appel : JSON valide garanti, réflexion activée ou non, repli entre profils, appel d'outils,
traçabilité complète.

## À réaliser

1. **Client de chat asynchrone** compatible OpenAI (`/v1/chat/completions`, `httpx`) :
   - profils de `config.yaml`, sémaphore par profil = nombre de slots ;
   - **repli** par étape : santé des serveurs en cache (`/health`, `/v1/models`), bascule sur le
     profil suivant si le préféré ne répond pas ;
   - **réflexion** : `chat_template_kwargs: {"enable_thinking": bool}` par requête ; lecture de
     `reasoning_content`, sinon retrait des blocs `<think>…</think>` ;
   - **appel d'outils** (`tools`, `tool_calls`) — utilisé en S14, à tester dès maintenant ;
   - **images** dans les messages (`image_url` en base64) pour la vision de MiMo et l'OCR (S05) ;
   - délais, nouvelles tentatives avec temporisation croissante, erreurs typées (serveur absent,
     contexte dépassé, réponse invalide) ; en-tête `X-RAGC-Prompt: <id>@<version>`.
2. **Sorties structurées** : `complete_json(prompt_id, variables, schema)` en modes `schema`
   (`response_format` `json_schema`), `prompt` (schéma dans le prompt, JSON extrait), `auto` ;
   validation Pydantic ; jusqu'à 2 **réparations** en renvoyant l'erreur au modèle.
3. **Bibliothèque de prompts** (`ragcreator/prompts/`) : YAML (`id`, `version`, `description`,
   `reflexion`, `temperature`, `max_tokens`, `systeme`, `utilisateur`, `schema`), gabarits
   `${variable}` (variable manquante = erreur), **surcharges par profil de domaine puis par
   thème** ; `ragc prompts list|show|render`. Rédige `ragcreator/prompts/README.md`
   (conventions de `002_strategie.md` §7.1) et le prompt de test **T00 `ping_json`**.
4. **Journal des appels** (`llm_calls`) : prompt@version + empreinte, profil, modèle, réflexion,
   tokens, durées (premier token, total), succès / validation / réparations, références
   (thème, document, extrait, exécution de l'agent). Texte complet optionnel.
5. **Clients embeddings et re-classement** (`/v1/embeddings` par lots, `/v1/rerank`).
6. **Comptage de tokens** : estimation + calibrage via `/tokenize`.
7. **`ragc doctor`** : chaque serveur, modèles présents, T00 avec et sans réflexion, un appel
   d'outil factice, tokens/s, dimension des embeddings, re-classement ; diagnostic clair en
   français avec la commande à lancer en cas de problème.
8. **Scripts** `scripts/llama/start_mimo.sh`, `start_embeddings.sh`, `start_reranker.sh`
   (commandes de `002_strategie.md` §4.1, paramétrables, `nice`) et `docs/llama-server.md`
   (dont Qwen3.8 comme consommateur / renfort, et les scénarios de cohabitation A/B/C).
9. **Faux serveur compatible OpenAI** pour les tests : réponses programmables par
   `X-RAGC-Prompt`, appels d'outils simulés, JSON invalide, panne, lenteur.

## Expériences en conditions réelles (si disponibles) — à noter dans le journal

1. Le mode `schema` fonctionne-t-il **avec la réflexion activée** sur MiMo ? Sinon, quel mode
   par défaut quand la réflexion est active ?
2. Débit (tokens/s) avec 1 et 4 requêtes simultanées.
3. Taux de JSON valide sur 20 appels T00 par mode.
4. Effet du cache de préfixe (temps jusqu'au premier token avec un long préfixe répété).
5. Appel d'outils de MiMo via `--jinja` : format correct sur 10 essais ?
6. **Vision de MiMo** : le module `mmproj` est-il chargé (avec `-hf` ou `--mmproj`) ? une image de
   test envoyée au format OpenAI (`image_url` en base64) est-elle décrite correctement ?

## Critères d'acceptation

- [ ] Tests hors ligne : réflexion on/off, retrait de `<think>`, modes `schema`/`prompt`,
      réparation réussie puis échouée, repli de profil, serveur absent, appel d'outil, journal.
- [ ] `ragc prompts render ping_json` fonctionne ; surcharges profil puis thème respectées.
- [ ] `ragc doctor` donne un diagnostic lisible, serveurs présents ou absents.
- [ ] Résultats des 6 expériences notés (ou « non mesuré »).
- [ ] Procédure de clôture appliquée.
