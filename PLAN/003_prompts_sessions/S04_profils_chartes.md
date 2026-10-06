# S04 — Profils de domaine et chartes (E0)

> Jalon J1 · Dépend de : S03 · Étape : E0 · Prompts d'exécution : C01, C02
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§3, §6, §11, §16), `PLAN/001_but.md`
(§3, **§7**), `PLAN/002_strategie.md` (**§4.1, §4.2**, §9), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Donner au système la connaissance de **chaque domaine** — étiquettes, échelle de solidité,
découpage, relations, actualisation, sources, **cadrage** — et transformer un nom de thème en une
**charte** rattachée au bon profil. Ajouter un domaine doit se faire **sans code**.

## À réaliser

1. **Schéma `DomainProfile`** et chargeur de `profils/*.yaml` : étiquettes (nom, type, valeurs),
   **échelle de solidité** ordonnée et définie, règles de découpage (dont **blocs de code
   intacts** pour la cybersécurité), relations par famille, classes de volatilité, filtre
   temporel (dur / souple), affirmations sensibles, connecteurs prévus, gabarits de fiches,
   **cadrage** (texte injecté dans les prompts du domaine).
2. **Profils livrés** (`002_strategie.md` §4.2) : `criminologie`, `juridique_fiscal` (France et
   Géorgie), `sante_clinique`, `cybersecurite`, `sciences_comportementales`, `pharmaco_medical`,
   `mycologie`, `generique`. `ragc profile list|show|validate`.
3. **Schéma `ThemeCharter`** : définition, périmètre, sous-thèmes, mots-clés FR/EN (et géorgien si
   pertinent), synonymes, confusions à éviter, sources prioritaires, affirmations sensibles,
   profil, langues, sensibilité, cadrage.
4. **C01 `theme_charter`** (réflexion) : enfant plus étroit que le parent, sans chevauchement avec
   ses frères ; profil choisi et motivé ; juridictions pour le droit ; espèces confondables pour
   un organisme ; cadrage pour les domaines à double usage ou de santé ; `null` plutôt
   qu'inventer.
5. **C02 `search_queries`** : requêtes par connecteur du profil et par langue, jamais répétées ;
   table `queries` (origine : charte, couverture, lacune).
6. **Synchronisation charte ↔ `charte.yaml`** (modification manuelle prioritaire, verrouillage) ;
   suggestions de sous-thèmes ; `ragc theme plan <chemin>|--pending` (parents d'abord), exécuté
   comme **tâche du travail en fond** (phase P2 ou P4).
7. **Arbres d'exemple** (tests, faux serveur) : `Criminologie > Escroqueries > Faux placements` ;
   `Fiscalité > {Géorgie, France, International}` ; `Santé mentale > {Traumatismes, Phobies}` ;
   `Cybersécurité > Ingénierie sociale` ; `Sciences comportementales > Négociation` ;
   `Neurosciences > Décision` ; `Pharmacologie > Champignons > Amanita muscaria`.

## Bancs à ajouter

`ragc bench charters` : chartes générées 5 fois par arbre d'exemple — JSON valide (≥ 95 %), profil
correct (100 %), juridictions pour la fiscalité, cadrage présent pour la cybersécurité et les
escroqueries.

## Critères d'acceptation

- [ ] Les huit profils se chargent et se valident ; un neuvième profil d'essai s'ajoute sans code.
- [ ] `ragc theme plan --pending` produit des chartes pour tous les arbres, profil correct.
- [ ] Procédure de clôture appliquée.
