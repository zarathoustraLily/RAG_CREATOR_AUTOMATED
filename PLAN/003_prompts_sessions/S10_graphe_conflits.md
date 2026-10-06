# S10 — Graphe typé, chaînes, qualification des conflits (E10, E11)

> Jalon J4 · Dépend de : S09 · Étapes : E10, E11 · Prompts d'exécution : C09, C10
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§3, §5, §12**),
`PLAN/001_but.md` (§3, §7), `PLAN/002_strategie.md` (**§3.4**, §3.5, §5, §6.1),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Transformer les entités et relations brutes de C08 en un **graphe propre et typé** — normatif,
causal, épistémique, structurel —, en tirer des **chaînes** utiles à l'agent (convention →
article → décision ; mécanisme → comportement → tactique), et **qualifier les conflits** entre
sources.

## À réaliser

1. **Tables** (migration) : `entities`, `entity_aliases`, `relations` (famille, type, niveau de
   preuve, validité, provenance, poids), `communities`, graphe des affirmations (`claims` +
   arêtes *confirme / contredit*).
2. **Résolution d'entités** : normalisation (casse, accents, pluriels, ponctuation), noms
   scientifiques (binômes, « A. muscaria » → « Amanita muscaria » si le genre est attesté),
   références juridiques normalisées (« art. 209 B CGI » = « article 209 B du code général des
   impôts »), similarité floue (`rapidfuzz`, repli `difflib`) **et** vectorielle ; **C09
   `entity_arbitration`** seulement pour les paires ambiguës.
3. **Relations** : vocabulaire du profil, normalisation, fusion des doublons, poids = nombre
   d'extraits ; niveau de preuve hérité des extraits ; validité héritée des versions (une
   relation issue d'une version abrogée n'est plus valide après `valid_to`).
4. **Chaînes** : recherche de chemins courts par famille (`ragc graph chain <A> <B> [--famille]`)
   avec le maillon le plus faible affiché (solidité minimale de la chaîne).
5. **Communautés** (Leiden/Louvain via `networkx` en extra `graph`, repli propagation
   d'étiquettes) pour S12.
6. **Croisement et conflits E11** : détection en **deux temps** (EdA §12) — candidats par
   similarité + indices bon marché (négation, chiffres, dates divergents), puis **C10
   `conflict_qualification`** (réflexion, profil préféré `qwen38-27b`) seulement pour ces
   candidats → concordant / contradictoire / nuancé / source unique **et** cause : *évolution*
   (versions, dates), *désaccord*, *incertitude*. Marquages attachés aux extraits.
7. **Intégration à l'agent** : nouvelle étape d'escalade « voisins et chaînes du graphe » dans
   l'exécuteur de S08 ; les chaînes pertinentes et les conflits qualifiés apparaissent dans le
   dossier.
8. **Commandes** : `ragc graph show <entité>`, `ragc graph chain …`, `ragc graph export
   --format graphml|json`, `ragc conflicts list [--theme] [--cause evolution|desaccord|incertitude]`.
9. **Tests** : fusions attendues (« muscimol » / « Muscimol » / « muscimole » ; « art. 209 B
   CGI » / « article 209 B du CGI »), non-fusions (*A. muscaria* ≠ *A. pantherina*), validité des
   relations après abrogation, qualification « évolution » sur les deux versions fictives,
   chaînes.

## Expériences en conditions réelles (si disponibles)

Fusions correctes sur 30 paires vérifiées à la main ; conflits détectés et leur
qualification sur le corpus ; coût évité par la détection en deux temps ; relance des cas A–E.

## Critères d'acceptation

- [ ] `ragc graph chain` relie dans le cas A la convention, un article et une décision, avec la
      solidité de chaque maillon.
- [ ] Dans le cas C, une chaîne mécanisme → comportement → tactique apparaît dans le dossier.
- [ ] Conflits qualifiés et visibles dans le dossier ; espèces confondables jamais fusionnées.
- [ ] Procédure de clôture appliquée.
