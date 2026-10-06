# S07 — Enrichissement, indexation, recherche hybride filtrée (E5, E8, E9)

> Jalon J1 · Dépend de : S06 · Étapes : E5 (partie LLM), E8, E9 · Prompts d'exécution : C07, C08
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§2, §3, §6, §11),
`PLAN/001_but.md`, `PLAN/002_strategie.md` (§3.3–3.5, §4.4, §5, §6.3–6.4, §7),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Rendre chaque extrait **autoportant, daté et trouvable de plusieurs façons**, puis offrir le
**moteur de recherche** sur lequel s'appuiera l'agent (S08) : hybride, re-classé, filtrable par
étiquettes et par date, capable de re-classer selon une sous-question.

## À réaliser

1. **C07 `doc_digest`** (sans réflexion, 1 appel par document accepté) : résumé (5 lignes),
   plan, portée, **dates de publication et de validité**, juridiction, référence de version.
   Fusion avec la datation déterministe de S04 : **le déterministe prime** ; les dates issues du
   modèle sont marquées comme telles.
2. **C08 `chunk_enrichment`** (sans réflexion) : contexte (2–3 phrases), 3–5 questions,
   mots-clés FR/EN, entités typées, **relations typées avec leur famille** (normative,
   causale, épistémique, structurelle — vocabulaire du profil) stockées brutes (résolution en
   S10). Option `enrichment.split_calls` (deux appels) à comparer.
3. **Texte indexé** : `[Thème > Sous-thème] Titre — Section (unit_ref, version)` + contexte +
   texte ; questions indexées à part.
4. **FTS5** sur texte contextualisé + mots-clés + questions ; **vecteurs** (interface
   `VectorStore`, float16 + numpy exact, cache par sous-arbre) : texte et questions ; modèle
   d'embedding enregistré ; `ragc reindex`.
5. **Moteur de recherche** (`ragcreator/index/search.py`) :
   - `search(query, themes, filters, valid_at, k, rerank_query=None)` ;
   - BM25 + dense (texte, questions) → **RRF** → **re-classement** par `rerank_query` si fourni
     (sinon `query`) — c'est ce qui permettra la *décomposition au bon moment* (EdA §11) ;
   - filtres d'étiquettes (juridiction, nature, niveau de preuve…) et **filtre temporel**
     (`valid_at` : dur ou souple selon le profil) ;
   - diversité (max 2 extraits par document) ; élargissement petit → grand (section parente) ;
   - mode `explain` (rang de chaque composante, filtres appliqués).
6. **`ragc search "<q>" [--theme …] [--filtre clé=valeur …] [--en-vigueur-le AAAA-MM-JJ] [--k 8] [--explain]`**.
7. **Tests** : embeddings factices déterministes, RRF, filtres, filtre temporel dur sur les deux
   versions de l'article fictif de S04, re-classement par sous-question, diversité, cache.

## Expériences en conditions réelles (si disponibles)

15 questions écrites à la main sur les fixtures (dont 3 temporelles) : Recall@5 et MRR pour
BM25, dense, hybride, hybride + re-classement, avec / sans questions indexées, avec / sans
contexte ; latence ; temps de C08 en un ou deux appels. Tout dans le journal.

## Critères d'acceptation

- [ ] `ragc run --once` mène les fixtures jusqu'à `indexe`.
- [ ] `ragc search "imposition des sociétés étrangères contrôlées" --filtre juridiction=FR
      --en-vigueur-le 2026-10-06 --explain` ne renvoie que la version en vigueur.
- [ ] Un thème parent inclut ses sous-thèmes ; un thème frère est exclu.
- [ ] Mesures notées (ou « non mesuré »).
- [ ] Procédure de clôture appliquée.
