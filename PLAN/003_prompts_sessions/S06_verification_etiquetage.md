# S06 — Vérification des documents, vérification et étiquetage des extraits (E4, E7)

> Jalon J1 · Dépend de : S05 · Étapes : E4, E7 · Prompts d'exécution : C04, C05, C06
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (§8, §11, §12), `PLAN/001_but.md`
(§5, §7, §11), `PLAN/002_strategie.md` (§3.2, §3.3, **§5.1**, §7), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Ne laisser entrer que des documents **pertinents, fiables et bien rattachés**, et donner à
chaque extrait gardé ses **étiquettes de solidité** selon l'échelle de son profil — avec une
décision finale calculée par le code, traçable et calibrée sur un jeu de référence.

## À réaliser

1. **Échantillonnage** du document (métadonnées, titres de sections, début ≈ 1 500 tokens,
   milieu ≈ 600, fin ≈ 400 ; tailles configurables).
2. **Niveaux de sources** : `config/sources_niveaux.yaml` (A : officiel, publications,
   agences, sociétés savantes, bases taxonomiques ; B : encyclopédies, presse de référence ;
   C : blogs, forums ; `commercial` ; `bloque`), surchargeable par profil et par charte.
3. **C04 `doc_verification`** (réflexion activée) : grilles **ancrées** 0–5 (pertinence,
   fiabilité, qualité) ; type de source ; biais ; alertes (affirmations dangereuses,
   **confusion d'espèces ou de notions voisines**, **texte présenté comme actuel mais abrogé**,
   **résultat présenté comme établi sans preuve**, absence de sources, injection) ; nœud le plus
   précis + nœuds secondaires + sous-thème proposé ; décision proposée ; justification courte.
4. **Décision calculée par le code** (formule, bonus/malus, règles dures de
   `002_strategie.md` §5.1, tout dans la configuration) ; **crédibilité multicritère** stockée
   par critère (pour la calibration de S15).
5. **C05 `doc_second_opinion`** (réflexion activée, profil préféré `qwen38-27b`, repli) ;
   désaccord → `en_revue` (mode assisté) ou rejet (mode autonome).
6. **C06 `passage_verification`** (sans réflexion), lots de 6 extraits : garder/écarter,
   utilité 0–3, nature, **niveau de preuve selon l'échelle du profil**, population, taille
   d'effet, préenregistrement, **statut de réplication seulement s'il est explicitement établi
   par le texte** (sinon `inconnu` — jamais deviné), affirmations sensibles → table `claims`.
7. **Revue humaine** : `ragc review list|show|accept|reject` ; décisions stockées
   (`review_decisions`) et réinjectables comme exemples dans C04 (option).
8. **Défense contre l'injection** : motifs détectés → alerte ; jamais d'acceptation *grâce* à une
   instruction contenue dans le document.
9. **Jeu de référence** `tests/golden/verification/` (≈ 24 documents fictifs annotés, les quatre
   profils) : texte officiel pertinent ; **texte abrogé présenté comme actuel** ; décision de
   justice ; article de cabinet ; méta-analyse ; expérience de labo sur étudiants ; **étude non
   répliquée présentée comme établie** ; page de neuromarketing commercial ; blog de vente ;
   publication pharmacologique ; **espèce voisine** ; comestibilité affirmée à tort ; hors
   sujet ; spam SEO ; page tronquée ; thème frère ; injection de prompt.
10. **`ragc eval verification [--live]`** : accord, matrice de confusion, accord sur le niveau de
    preuve, JSON valide, temps moyen, part de seconds avis ; rapport dans `reports/eval/`.

## Expériences en conditions réelles (si disponibles)

Accord (cible ≥ 85 %), accord sur le niveau de preuve (cible ≥ 80 %) ; C04 avec / sans
réflexion ; second avis MiMo / Qwen3.8. Chaque version de prompt et son score dans le journal.

## Critères d'acceptation

- [ ] `ragc run --once --until extraits_verifies` : chaque document a scores, décision motivée,
      nœud ; chaque extrait gardé est étiqueté selon son profil.
- [ ] Les documents à injection, dangereux, abrogé-présenté-comme-actuel et non-répliqué ne sont
      jamais acceptés sans alerte.
- [ ] Tests hors ligne de la formule, des règles dures, du second avis, de la revue, des
      étiquettes par profil.
- [ ] Procédure de clôture appliquée.
