# S03 — Profils de domaine et chartes de thème (E0)

> Jalon J1 · Dépend de : S02 · Étape : E0 · Prompts d'exécution : C01, C02
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§3, §6, §11), `PLAN/001_but.md`
(§3, §7), `PLAN/002_strategie.md` (**§3.1, §3.2**, §7), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md` (résultats des expériences de S02). Respecte-les. En cas de contradiction,
arrête-toi et pose la question.

## Objectif

Donner au système la **connaissance de chaque domaine** — ce qu'on étiquette, comment on juge
la solidité, comment on découpe, à quel rythme on actualise — et transformer un simple nom de
thème en une **charte** précise rattachée au bon profil.

## À réaliser

1. **Schéma `DomainProfile`** (Pydantic) et chargeur de `profils/*.yaml` : étiquettes
   spécifiques (nom, type, valeurs permises), **échelle de solidité** ordonnée (niveaux définis
   en une ligne chacun), règles de découpage (unité naturelle, tailles), vocabulaire de
   relations par famille, classes de volatilité, mode de filtre temporel (dur / souple), types
   d'affirmations sensibles, connecteurs prévus (noms), gabarits de fiches (pour S12).
2. **Cinq profils livrés**, conformes à `002_strategie.md` §3.2 : `juridique_fiscal`,
   `pharmaco_medical`, `mycologie`, `sciences_comportementales`, `generique`.
   `ragc profile list|show <nom>`.
3. **Schéma `ThemeCharter`** : définition, périmètre inclus / exclu, sous-thèmes proposés
   (justifiés), mots-clés FR/EN, synonymes et noms scientifiques, **confusions à éviter**,
   sources prioritaires, affirmations sensibles, **profil choisi** (+ surcharges éventuelles),
   langues, sensibilité.
4. **Prompt C01 `theme_charter`** (réflexion activée) — entrées : nom, chemin, charte du parent,
   thèmes frères, alias, liste des profils avec leur description. Exigences : enfant plus étroit
   que le parent et sans chevauchement avec ses frères ; choix motivé du profil ; pour un
   organisme, nom scientifique, noms vernaculaires et **espèces confondables** ; pour un domaine
   juridique, **juridiction(s)** ; `null` plutôt qu'une invention ; un court exemple.
5. **Prompt C02 `search_queries`** (sans réflexion) — requêtes par connecteur du profil et par
   langue, variées (synonymes, sous-thèmes, mécanismes, revues, textes officiels), sans répéter
   les requêtes passées. Table `queries` (thème, connecteur, langue, texte, cycle, origine :
   charte / couverture / lacune, statut).
6. **Synchronisation charte ↔ `charte.yaml`** (modification manuelle détectée et prioritaire,
   `verrouille: true`) ; synonymes → `theme_aliases` ; sous-thèmes proposés stockés comme
   suggestions (politique `auto` / `validation`) ; `ragc theme plan <chemin>|--pending` (parents
   d'abord), `ragc theme charter`, `ragc theme suggestions|accept`.
7. **Tests** avec le faux serveur : arbres d'exemple des cas de référence A–D
   (`Droit > Fiscalité > {France, Géorgie, International}`,
   `Sciences comportementales > {Négociation, Économie comportementale}`,
   `Neurosciences > Décision`, `Pharmacologie > Champignons > Amanita muscaria`) ; ordre
   parent → enfant ; priorité des modifications manuelles ; profils valides.

## Évaluation en conditions réelles (si disponible)

Chartes générées 5 fois pour chaque arbre d'exemple : JSON valide (cible ≥ 95 %), **profil
correct** (cible 100 %), juridictions présentes pour le droit, *A. pantherina* dans les
confusions d'*A. muscaria*. Note résultats et ajustements dans le journal.

## Critères d'acceptation

- [ ] Les cinq profils se chargent et passent la validation ; `ragc profile show juridique_fiscal`
      est lisible.
- [ ] `ragc theme plan --pending` produit des chartes pour tout l'arbre, avec le bon profil.
- [ ] `charte.yaml` lisible, modifiable, modification respectée.
- [ ] Procédure de clôture appliquée.
