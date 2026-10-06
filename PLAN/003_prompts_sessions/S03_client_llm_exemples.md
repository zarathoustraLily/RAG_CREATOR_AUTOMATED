# S03 — Client LLM, prompts, journal, capture des exemples, adaptateurs par requête

> Jalon J1 · Dépend de : S02 · Étapes : — · Prompts d'exécution : T00 (test)
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§9, §14), `PLAN/001_but.md` (§6),
`PLAN/002_strategie.md` (§3.1, §5.1, §5.2, **§8.2**, §9), `PLAN/004_decisions_techniques.md`,
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Une couche d'accès aux modèles **fiable, agnostique et apprenante** : JSON valide garanti,
réflexion activée ou non, adaptateurs LoRA choisis à chaque requête, images, appels d'outils —
et **chaque appel transformé en exemple d'entraînement neutre**, réutilisable avec n'importe quel
futur modèle de base.

## À réaliser

1. **Client de chat asynchrone** compatible OpenAI : profils de modèles, passage obligatoire par
   le gestionnaire de modèles (S02), sémaphores par profil, **réflexion** par requête
   (`chat_template_kwargs.enable_thinking`, lecture de `reasoning_content`, sinon retrait de
   `<think>`), **adaptateur LoRA par requête** (champ `lora`, regroupement par adaptateur),
   **images** (`image_url` en base64), **appel d'outils**, délais, nouvelles tentatives, erreurs
   typées, en-tête `X-RAGC-Prompt`.
2. **Sorties structurées** : `complete_json(task, variables, schema)` en modes `schema` / `prompt`
   / `auto`, validation Pydantic, deux réparations au plus.
3. **Routage par tâche** : le code demande une **tâche** (ex. `passage_verification`), le registre
   (`002_strategie.md` §5.2) dit qui la fait (modèle, adaptateur, variante courte du prompt) ;
   repli automatique sur le généraliste et le prompt complet si l'adaptateur est absent ou
   invalide.
4. **Bibliothèque de prompts** : YAML, gabarits `${variable}`, surcharges profil puis thème,
   **variante courte** pour spécialiste ; `ragc prompts list|show|render` ; T00 `ping_json`.
5. **Journal** (`llm_calls`) et **exemples** (`examples`) : tâche, entrée structurée, sortie
   structurée, prompt@version, modèle et adaptateur, durée, tokens, **statut de validation**
   (`brut` au départ, puis `or` / `argent` / `rejete`), provenance ; **sans gabarit de modèle**
   (format neutre).
6. **Clients** embeddings et re-classement (CPU ou GPU selon le profil) ; comptage de tokens.
7. **`ragc doctor`** complet : serveurs, modèles, réflexion, JSON, outils, vision, adaptateurs.
8. **Faux serveurs** pour les tests : chat (réponses selon `X-RAGC-Prompt` et l'adaptateur),
   outils, images, pannes, lenteurs.

## Bancs à ajouter

`ragc bench llm` : JSON contraint avec et sans réflexion (taux de validité sur 20 appels), débit
1 et 4 requêtes, appel d'outils, vision de MiMo, latence d'un changement d'adaptateur.

## Critères d'acceptation

- [ ] Tests hors ligne : réflexion, modes JSON, réparations, adaptateur absent → repli, images,
      outils, capture d'exemple à chaque appel, format neutre (aucun jeton spécial de modèle).
- [ ] `ragc doctor` lisible avec ou sans serveurs.
- [ ] Procédure de clôture appliquée.
