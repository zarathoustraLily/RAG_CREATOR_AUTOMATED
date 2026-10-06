# S09 — Collecte web, connecteurs par profil, collectes ciblées (E1, E2)

> Jalon J3 · Dépend de : S08 · Étapes : E1, E2 (web) · Prompts d'exécution : C02 (connecteurs), C03
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md`, `PLAN/001_but.md` (§8, §10),
`PLAN/002_strategie.md` (§3.2, **§4.5**, §5, §11), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Que le système **trouve seul** des sources de qualité, en privilégiant les **sources de
référence de chaque domaine**, trie les résultats avant de les télécharger, les récupère
poliment, et comble les **lacunes** signalées par l'agent de recherche.

## À réaliser

1. **Interface de connecteur** (`ragcreator/sources/base.py`) :
   `search(query, lang, filters, limit) -> list[Candidate]` et, si utile, `fetch(id)` pour les API
   qui donnent directement le texte et ses métadonnées (dates, version, juridiction).
2. **Connecteurs génériques** : SearxNG local (API JSON), Wikipédia FR/EN, listes d'URL
   (`ragc add-url`), flux RSS, DuckDuckGo HTML en repli désactivable.
3. **Connecteurs par profil** — **vérifie pour chacun l'accès, la documentation officielle et
   les conditions d'utilisation avant d'écrire du code**, note le résultat dans le journal,
   et rends chaque connecteur optionnel (clé dans une variable d'environnement) :
   - scientifiques : Europe PMC, OpenAlex, Crossref (dont les informations de rétractation) ;
   - juridiques français : Légifrance et Judilibre (API PISTE, clé gratuite), BOFiP, EUR-Lex ;
   - géorgiens : matsne.gov.ge (versions officielles, traductions anglaises éventuelles) ;
   - mycologiques : MycoBank, Index Fungorum.
   Les métadonnées officielles (date d'effet, version, statut) alimentent directement la
   datation de S04 (le déterministe prime).
4. **Requêtes** : C02 étendu aux connecteurs du profil ; table `queries` (origine : charte,
   couverture, **lacune**) ; jamais deux fois la même requête ; budget par thème et par cycle.
5. **C03 `search_triage`** (sans réflexion) : lots de 10–20 résultats avec la charte résumée →
   garder / écarter, priorité, raison ; domaines `bloque` écartés avant le modèle.
6. **Récupérateur** : `httpx` asynchrone, agent utilisateur identifiable, **`robots.txt`**,
   limite par domaine, nouvelles tentatives, taille maximale, routage HTML / PDF, cache brut,
   `ETag` / `Last-Modified`, URL canonique, redirections ; échecs → `echec_recuperation` motivé.
7. **Dédoublonnage** par URL canonique et identifiant officiel avant téléchargement.
8. **Collectes ciblées** : `ragc collect --from-gaps [--run <id>]` transforme les lacunes de
   l'agent (`gaps`) en requêtes ciblées (sous-question + filtres) ; statut des lacunes mis à
   jour ; l'agent indique « collecte programmée ».
9. **Commandes** : `ragc discover <chemin-theme> [--connector …] [--dry-run]`,
   `ragc connectors list|test`.
10. **Documentation** : `docs/searxng.md`, `docs/connecteurs.md` (accès, clés, limites, conditions).
11. **Tests hors ligne** avec réponses HTTP enregistrées : chaque connecteur, tri, `robots.txt`,
    limite par domaine, URL canoniques, métadonnées officielles, collectes ciblées.

## Expériences en conditions réelles (si disponibles)

Collecte sur les thèmes des cas A et D : candidats par connecteur, part gardée au tri, part
acceptée à la vérification, domaines dominants, temps. Puis relancer les cas de référence A–E
et noter l'évolution.

## Critères d'acceptation

- [ ] `ragc discover … --dry-run` montre des requêtes variées, des connecteurs adaptés au profil
      et un tri motivé.
- [ ] Une collecte réelle conduit des documents web jusqu'à `indexe`, avec dates officielles
      quand le connecteur les fournit.
- [ ] Une lacune du cas A produit une collecte ciblée.
- [ ] Aucun site interdisant le robot n'est téléchargé ; aucun domaine n'est martelé.
- [ ] Procédure de clôture appliquée.
