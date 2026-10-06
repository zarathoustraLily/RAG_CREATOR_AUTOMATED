# S08 — Graphe d'entités et vérification croisée (E9, E10)

> Jalon J3 · Dépend de : S06 · Étapes du pipeline : E9, E10 · Prompts : P09, P10
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md` (§7), `PLAN/002_strategie.md` (§3.3, §5.3,
§11), `PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas
de contradiction, arrête-toi et pose la question.

## Objectif

Transformer les entités et relations brutes de P08 en un **graphe propre** (une entité = un
nœud, quels que soient ses noms), et **croiser les affirmations sensibles** entre sources
indépendantes pour signaler accords et contradictions.

## À réaliser

1. **Tables** (migration) : `entities` (nom canonique, type, description, thème), `entity_aliases`,
   `relations` (source, type, cible, poids = nombre d'extraits, extraits de provenance),
   `communities`.
2. **Résolution d'entités E9** (`ragcreator/graph/resolve.py`) :
   - normalisation (casse, accents, pluriels simples, ponctuation) ;
   - noms scientifiques : détection binomiale, expansion des abréviations (« A. muscaria » →
     « Amanita muscaria » si le genre apparaît dans le document) ;
   - candidats à la fusion par similarité floue (`rapidfuzz`, repli `difflib`) **et** par
     similarité vectorielle du nom + description ;
   - **Prompt P09 `entity_arbitration`** (sans réflexion) pour les paires ambiguës uniquement :
     même entité ?, nom canonique, type ; les paires évidentes sont fusionnées par le code ;
   - vocabulaire contrôlé des types d'entités et de relations (configurable par charte),
     relations normalisées.
3. **Communautés** : détection de groupes (Leiden/Louvain via `networkx` en extra `graph`, repli
   propagation d'étiquettes) ; stockées pour S09.
4. **Vérification croisée E10** (`ragcreator/verify/crosscheck.py`) : pour chaque affirmation
   sensible (table `claims` de S05), recherche hybride dans **les autres documents** du thème
   (et des thèmes parents/enfants), puis **Prompt P10 `claim_crosscheck`** (réflexion activée,
   profil préféré `qwen38-27b` avec repli) → `concordante | contradictoire | nuancee |
   source_unique`, passages cités, explication courte. Les marquages sont attachés aux extraits
   (`flags`) et seront transmis aux modèles consommateurs.
5. **Commandes** : `ragc graph show <entité>` (alias, relations, sources),
   `ragc graph export --format graphml|json [--theme]`,
   `ragc claims list [--theme] [--status contradictoire]`.
6. **Tests** : fusions attendues (« Muscimol » / « muscimol » / « muscimole » ; « acide
   iboténique » / « ibotenic acid »), non-fusions attendues (*A. muscaria* ≠ *A. pantherina*),
   poids des relations, statuts de croisement avec le faux serveur.

## Expériences en conditions réelles (si disponible)

Taux de fusions correctes sur 30 paires vérifiées à la main ; nombre d'affirmations
contradictoires détectées sur le corpus ; temps de P10. Note-les dans le journal.

## Critères d'acceptation

- [ ] `ragc graph show muscimol` montre une entité unique avec ses alias et ses relations
      (ex. agit sur → récepteur GABA-A) sourcées.
- [ ] `ragc claims list --status contradictoire` liste les désaccords avec les passages en regard.
- [ ] Espèces confondables jamais fusionnées.
- [ ] Procédure de clôture appliquée.
