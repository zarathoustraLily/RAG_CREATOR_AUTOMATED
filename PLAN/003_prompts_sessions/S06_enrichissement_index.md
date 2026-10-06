# S06 — Enrichissement, indexation et recherche hybride (E7, E8)

> Jalon J1 · Dépend de : S05 · Étapes du pipeline : E7, E8 · Prompts : P07, P08
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md` (§5), `PLAN/002_strategie.md` (§3.3, **§6**,
§7), `PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas
de contradiction, arrête-toi et pose la question.

## Objectif

Rendre chaque extrait **autoportant et trouvable de plusieurs façons**, puis offrir une
recherche hybride précise et rapide, filtrable par sous-arbre de thèmes. À la fin de cette
session, le jalon J1 est atteint : un RAG local vérifié et interrogeable.

## À réaliser

1. **Prompt P07 `doc_digest`** (sans réflexion, 1 appel par document accepté) : résumé en
   5 lignes, plan, portée, date de référence. Il sert de contexte parent à P08 (au lieu de
   renvoyer tout le document à chaque extrait).
2. **Prompt P08 `chunk_enrichment`** (sans réflexion) : à partir du résumé du document, du
   chemin de section et de l'extrait :
   - **contexte** de 2–3 phrases situant l'extrait dans le document ;
   - **3–5 questions** auxquelles l'extrait répond (formulées comme un utilisateur les poserait) ;
   - **mots-clés FR et EN** ;
   - **entités typées** (organisme, molécule, récepteur, effet, pathologie, posologie…) et
     **relations** `source → relation → cible` (stockées brutes ; la résolution est en S08).
   Option `enrichment.split_calls` pour séparer contexte/questions et entités/relations en deux
   appels si la qualité l'exige (à comparer en conditions réelles).
3. **Texte indexé** : `[Thème > Sous-thème] Titre — Section` + contexte + texte. Les questions
   sont indexées à part.
4. **FTS5** : table virtuelle sur texte contextualisé + mots-clés + questions
   (`unicode61 remove_diacritics 2`), synchronisée par déclencheurs ou à l'indexation.
5. **Vecteurs** : interface `VectorStore` ; implémentation par défaut = blobs float16 dans SQLite
   + recherche exacte numpy, matrices mises en cache par sous-arbre de thème et invalidées à
   l'écriture. Deux vecteurs par extrait : texte contextualisé, questions concaténées. Le modèle
   d'embedding est enregistré avec chaque vecteur ; `ragc reindex [--theme]` ré-indexe après un
   changement de modèle.
6. **Recherche hybride** (`ragcreator/index/search.py`) : BM25 (top 50) + dense texte et questions
   (top 50) → fusion **RRF** → **re-classement** cross-encoder (top 40 → top k) si disponible →
   diversité (max 2 extraits par document) ; filtres : sous-arbre(s) de thèmes, langue, niveau de
   source, date. Mode `--explain` affichant les rangs de chaque composante.
7. **`ragc search "<question>" [--theme <chemin>…] [--k 8] [--explain]`**.
8. **Tests** : embeddings factices déterministes, mécanique RRF, filtres de sous-arbre,
   diversité, invalidation du cache, réindexation.

## Expériences en conditions réelles (si disponible)

- 15 questions écrites à la main sur le corpus de fixtures, avec extraits attendus : Recall@5 et
  MRR pour BM25 seul, dense seul, hybride, hybride + re-classement, avec/sans questions
  indexées, avec/sans contexte. Latence de chaque mode. Temps d'enrichissement par extrait,
  P08 en un ou deux appels. **Tout noter dans le journal.**

## Critères d'acceptation

- [ ] `ragc run --once` mène les fixtures jusqu'à l'état `indexe`.
- [ ] `ragc search "muscimol récepteur GABA" --theme pharmacologie --explain` renvoie des extraits
      sourcés avec le détail des scores.
- [ ] Interroger un thème parent inclut ses sous-thèmes ; un thème frère est exclu.
- [ ] Mesures notées (ou « non mesuré »).
- [ ] Procédure de clôture appliquée.
