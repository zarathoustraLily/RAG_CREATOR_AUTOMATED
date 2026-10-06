# S14 — Graphe typé et conflits (E10, E11)

> Jalon J5 · Dépend de : S13 · Étapes : E10, E11 · Prompts d'exécution : C09, C10
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§3, §5, §12, §17**),
`PLAN/001_but.md` (§3, §7), `PLAN/002_strategie.md` (**§4.4**, §4.5, §6, §7.1, **§7.6**),
`PLAN/004_decisions_techniques.md` (tables maison ou LightRAG), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Transformer les relations brutes en un **graphe propre et typé** — normatif, causal, épistémique,
manipulation, attaque —, en tirer des **chaînes** utiles à l'agent (convention → article →
décision ; technique de manipulation → biais exploité → contre-mesure ; mécanisme → comportement
→ traitement) et **qualifier les conflits**.

## À réaliser

1. **Tables** (ou LightRAG selon S01) : `entities`, `entity_aliases`, `relations` (famille, type,
   niveau de preuve, validité, provenance, poids), `communities`, arêtes *confirme / contredit*
   entre affirmations.
2. **Résolution d'entités** : normalisation, noms scientifiques, références juridiques (dont
   articles du Code des impôts géorgien), identifiants techniques (CVE, techniques ATT&CK),
   similarité floue et vectorielle ; **C09** seulement pour les paires ambiguës.
3. **Relations** : vocabulaire du profil, fusion, poids, niveau de preuve et validité hérités.
4. **Chaînes** : `ragc graph chain <A> <B> [--famille]`, maillon le plus faible affiché.
5. **Communautés** (pour S15).
6. **Conflits E11** en deux temps : indices bon marché (négation, chiffres, dates) puis **C10
   `conflict_qualification`** (enseignant, P4) → concordant / contradictoire / nuancé / source
   unique + *évolution / désaccord / incertitude*.
7. **Intégration à l'agent** : escalade « voisins et chaînes du graphe » ; chaînes et conflits
   dans le dossier ; en droit, l'auditeur (R6) élague en cascade les décisions rattachées à une
   règle jugée inapplicable.
7 bis. **Ponts entre littératures** : `concepts_documents` (concepts de chaque document :
   entités, étiquettes, sujets OpenAlex) en fond, puis activation de `ponts_corpus`
   (`methodologie_recherche/transversal/ponts.py`, déjà écrit : modèle ABC et voisins
   d'autres familles) dans le plan transversal ; les ponts sont des **pistes** signalées comme
   telles, jamais des preuves.
8. **Commandes** : `ragc graph show|chain|export`, `ragc conflicts list`.
9. **Tests** : fusions attendues et interdites (*A. muscaria* ≠ *A. pantherina* ; deux CVE
   distinctes), validité après abrogation, chaînes, qualification « évolution ».

## Bancs à ajouter

`ragc bench graph` : fusions correctes sur 30 paires vérifiées à la main ; conflits détectés et
leur qualification ; coût évité par la détection en deux temps.

## Critères d'acceptation

- [ ] Dans le cas A, une chaîne relie convention, article et décision ; dans le cas H, une chaîne
      relie technique de manipulation, biais exploité et contre-mesure.
- [ ] Dans le cas I, au moins un pont du corpus mène à une sous-question que le plan sans ponts
      n'avait pas (mesuré, avec et sans ponts).
- [ ] Procédure de clôture appliquée.
