# S05 — Vérification des documents et des extraits (E4, E6)

> Jalon J1 · Dépend de : S03, S04 · Étapes du pipeline : E4, E6 · Prompts : P04, P05, P06
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md` (§5 et §7), `PLAN/002_strategie.md`
(**§5.3 en entier**, §7), `PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`.
Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

C'est l'exigence centrale du projet : **ne laisser entrer dans le RAG que des documents et des
extraits pertinents, fiables et bien rattachés**, vérifiés par le modèle chargé dans
`llama-server`, avec une décision finale calculée par le code, traçable et calibrée sur un jeu
de référence.

## À réaliser

1. **Échantillonnage du document** : métadonnées (titre, URL, domaine, niveau de source, date,
   auteur), liste des titres de sections, début ≈ 1 500 tokens, milieu ≈ 600, fin ≈ 400
   (tailles configurables).
2. **Niveaux de sources** : `config/sources_niveaux.yaml` (A : publications, agences sanitaires,
   sociétés savantes, bases taxonomiques ; B : encyclopédies, presse de référence ; C : blogs,
   forums ; `commercial` ; `bloque`), surchargeable par la charte.
3. **Prompt P04 `doc_verification`** (réflexion activée) : rôle de vérificateur documentaire ;
   **grilles ancrées** 0–5 pour pertinence, fiabilité, qualité (chaque niveau défini en une
   ligne) ; type de source ; biais ; signaux d'alerte (affirmations dangereuses, **confusion
   d'espèces** au regard de `confusions_a_eviter`, absence de sources) ; thème le plus précis
   dans le sous-arbre + thèmes secondaires + sous-thème proposé ; décision proposée ;
   justification en 3 phrases maximum. Contenu entre `<document>…</document>` avec consigne
   d'ignorer toute instruction qu'il contient.
4. **Décision calculée par le code** : formule, bonus/malus et règles dures de
   `002_strategie.md` §5.3, tout dans `config.yaml`. Rattachement au nœud le plus précis,
   thèmes secondaires dans `document_themes`, proposition de sous-thème transmise au mécanisme
   de S03.
5. **Prompt P05 `doc_second_opinion`** (réflexion activée, profil préféré `qwen38-27b` avec
   repli) : relit le document avec le premier avis, confirme ou infirme. Désaccord persistant →
   `en_revue` (mode assisté) ou rejet (mode autonome), selon `config.yaml`.
6. **Prompt P06 `passage_verification`** (sans réflexion) : lots de 6 extraits avec la charte
   résumée ; par extrait : garder/écarter, utilité 0–3, nature (fait, définition, mécanisme,
   protocole, chiffre, opinion, bruit), **affirmations sensibles** (texte exact + type). Table
   `claims` créée par migration (elle servira à E10).
7. **Revue humaine** : `ragc review list|show|accept|reject [--theme <chemin>]` ; `show` affiche
   scores, justifications des deux avis et l'échantillon. Vos décisions sont stockées
   (`review_decisions`) et les 2 plus récentes du thème peuvent être injectées comme exemples
   dans P04 (option de configuration).
8. **Défense contre l'injection** : détection de motifs (« ignore les instructions
   précédentes », « accepte ce document »…) → signal d'alerte ; un document ne peut pas être
   accepté *grâce* à une instruction qu'il contient.
9. **Jeu de référence** `tests/golden/verification/` : ≈ 20 documents rédigés pour le projet,
   annotés (décision attendue, thème attendu) : scientifique pertinent, encyclopédique
   pertinent, blog pertinent mais peu sourcé, hors sujet, boutique de compléments, spam SEO,
   page tronquée, **espèce voisine** (*A. pantherina* présentée comme *A. muscaria*), document
   d'un thème frère, document contenant une injection de prompt, document dangereux
   (comestibilité affirmée à tort).
10. **`ragc eval verification [--live]`** : taux d'accord, matrice de confusion, taux de JSON
    valide, temps moyen, part de seconds avis ; rapport Markdown dans `reports/eval/`.

## Expériences en conditions réelles (si disponible)

- Accord avec le jeu de référence (cible ≥ 85 %) ; ajuste prompts et seuils, **note chaque
  version et son score** dans le journal.
- Comparer P04 avec et sans réflexion (accord, temps) ; comparer le second avis MiMo vs Qwen3.8.

## Critères d'acceptation

- [ ] `ragc run --once --until extraits_verifies` sur les fixtures de S04 : chaque document a
      ses scores, sa décision motivée, son thème ; chaque extrait gardé ou écarté avec motif.
- [ ] Le document à injection de prompt et le document dangereux ne sont jamais acceptés.
- [ ] Tests hors ligne de la formule de décision, des règles dures, du second avis, de la revue.
- [ ] Résultats de `ragc eval verification --live` notés (ou « non mesuré »).
- [ ] Procédure de clôture appliquée.
