# S07 — Collecte web autonome (E1, E2)

> Jalon J2 · Dépend de : S06 · Étapes du pipeline : E1, E2 (web) · Prompts : P02 (sources), P03
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md`, `PLAN/002_strategie.md` (§3.4, §5, §11),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Que le programme **trouve seul** des sources de qualité pour un thème, trie les résultats avant
de les télécharger (économie de calcul), les récupère poliment et les fasse entrer dans le
pipeline de vérification existant.

## À réaliser

1. **Interface de source** (`ragcreator/sources/base.py`) :
   `search(query, lang, limit) -> list[Candidate]` (titre, URL, extrait, source, date, langue).
   Implémentations :
   - **SearxNG** local (API JSON, catégories `general` et `science`) — source web principale ;
   - **Wikipédia** FR/EN (API de recherche + contenu de page) ;
   - **Europe PMC** (API REST : résumés ; texte intégral en accès libre quand il existe) ;
   - **DuckDuckGo HTML** en repli (fragile, désactivable) ;
   - **liste d'URL** (`ragc add-url <chemin-theme> <url…>`) et flux RSS optionnels.
   Activation et quotas par source dans `config.yaml` ; la charte peut prioriser des sources.
2. **Requêtes** : exécution des requêtes P02 en attente (table `queries` de S03) ; jamais deux
   fois la même requête sur la même source ; budget de candidats par thème et par cycle.
3. **Prompt P03 `search_triage`** (sans réflexion) : par lots de 10–20 résultats (titre, URL,
   domaine, extrait) avec la charte résumée → garder/écarter, priorité, raison courte. Les
   domaines `bloque` sont écartés avant le modèle.
4. **Récupérateur** (`ragcreator/ingest/fetch.py`) : `httpx` asynchrone, agent utilisateur
   identifiable, **`robots.txt`** (cache), limite par domaine, nouvelles tentatives, taille
   maximale, routage HTML/PDF selon le type de contenu, cache brut par empreinte,
   `ETag`/`Last-Modified`, normalisation et URL canonique (suppression `utm_*`, fragments),
   redirections. Les erreurs mènent à `echec_recuperation` avec motif, sans bloquer le reste.
5. **Dédoublonnage** des candidats par URL canonique **avant** téléchargement, puis par contenu
   (E3 existant) après.
6. **Commande** `ragc discover <chemin-theme> [--source …] [--dry-run]` : affiche requêtes,
   candidats, décisions de tri ; sans `--dry-run`, les candidats retenus entrent dans le pipeline.
7. **Documentation** : `docs/searxng.md` (installation locale via Docker, configuration JSON).
8. **Tests hors ligne** avec réponses HTTP enregistrées (aucun réseau) : chaque source, tri,
   `robots.txt`, limite par domaine, normalisation d'URL, cache.

## Expériences en conditions réelles (si disponible)

Sur `pharmacologie/champignons/amanita-muscaria` : nombre de candidats par source, part gardée
au tri, part acceptée à la vérification, temps total, domaines les plus fréquents. Note les
ajustements de P02/P03 et des niveaux de sources dans le journal.

## Critères d'acceptation

- [ ] `ragc discover … --dry-run` montre des requêtes variées et un tri motivé.
- [ ] Une collecte réelle conduit des documents web jusqu'à l'état `indexe`, interrogeables
      avec `ragc search`.
- [ ] Aucun site interdisant le robot n'est téléchargé ; aucun domaine n'est martelé.
- [ ] Procédure de clôture appliquée.
