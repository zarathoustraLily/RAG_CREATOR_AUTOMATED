# S07 — Enrichissement, indexation, recherche hybride filtrée (E5, E8, E9)

> Jalon J1 · Dépend de : S06 · Étapes : E5 (partie LLM), E8, E9 · Prompts d'exécution : C07, C08
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§2, §3, §6, §11),
`PLAN/001_but.md`, `PLAN/002_strategie.md` (§4.3–4.5, §5.3, §6, §7.3),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Rendre chaque extrait **autoportant, daté et trouvable de plusieurs façons**, et fournir le
**moteur de recherche** de l'agent : hybride, re-classé, filtrable par étiquettes et par date,
capable de re-classer selon une sous-question.

## À réaliser

1. **C07 `doc_digest`** (phase P2) : résumé, plan, portée, dates de publication et de validité,
   juridiction, version ; fusion avec la datation déterministe (**le déterministe prime**).
2. **C08 `chunk_enrichment`** (phase P2) : contexte (2–3 phrases), 3–5 questions, mots-clés
   FR/EN, entités typées, **relations typées par famille** (vocabulaire du profil : normatives,
   causales, épistémiques, manipulation, attaque) stockées brutes.
3. **Texte indexé** : `[Thème > Sous-thème] Titre — Section (unit_ref, version, page)` + contexte
   + texte ; questions indexées à part.
4. **FTS5** et **vecteurs** (`VectorStore`, float16 + numpy exact, cache par sous-arbre) ;
   embeddings **en lot en phase P3** ; modèle d'embedding enregistré ; `ragc reindex`.
5. **Moteur** `search(query, themes, filters, valid_at, k, rerank_query=None)` : BM25 + dense →
   RRF → re-classement (par `rerank_query` si fourni) → diversité → élargissement petit → grand ;
   filtres d'étiquettes ; **filtre temporel** dur ou souple selon le profil ; mode `explain`.
6. **Re-classement sur CPU ou GPU** selon le profil matériel ; latence mesurée et affichée.
7. **`ragc search "<q>" [--theme …] [--filtre clé=valeur …] [--en-vigueur-le AAAA-MM-JJ] [--explain]`**.
8. **Tests** : embeddings factices, RRF, filtres, filtre temporel sur les deux versions fictives,
   re-classement par sous-question, cache.

## Bancs à ajouter

`ragc bench search` : 15 questions écrites à la main sur les fixtures (dont 3 temporelles) —
Recall@5, MRR par configuration ; latence avec re-classement sur CPU et sur GPU ; temps de C08 en
un ou deux appels.

## Critères d'acceptation

- [ ] Les fixtures arrivent à l'état `indexe` par le travail en fond.
- [ ] Une recherche sur la fiscalité avec `--en-vigueur-le` ne renvoie que la version en vigueur.
- [ ] Procédure de clôture appliquée.
