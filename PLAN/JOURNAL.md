# Journal de bord du projet

> Une entrée par session, ajoutée à la clôture (gabarit dans
> `003_prompts_sessions/00_regles_communes.md` §7). Les plus récentes en bas.

---

## S00 — Cadrage : but, état de l'art, stratégie, sessions — 2026-10-06

- **Fait** :
  - `000_etat_de_l_art.md` : 37 publications d'octobre 2025 à octobre 2026 (résumés lus) et
    9 références apportées par l'utilisateur, vérifiées une à une ;
  - `001_but.md` v0.2 : deux moments (construire / répondre), quatre couches de connaissance,
    raisonnement de l'agent, priorité ≠ solidité, rôles des modèles, **cinq cas de référence**
    (A Géorgie, B voiture, C voiture « neurosciences d'abord », D amanite, E livre scanné),
    critères mesurables ;
  - `002_strategie.md` v0.2 : architecture, profils de domaine, temps et versions, lecture des
    documents (OCR), pipeline de construction E0–E14, agent de recherche R1–R8, catalogue de
    prompts L/C/Q/V, plan de réalisation ;
  - `003_prompts_sessions/` : règles communes et 16 prompts de sessions (S01–S16).
- **Décisions** :
  - l'agent **planifie**, un moteur classique **exécute** (hybride, EdA §2) ;
  - le **temps est une contrainte dure** pour les profils juridiques (EdA §3) ;
  - **priorité** fixée par l'utilisateur, **solidité** fixée par les preuves, contre-point
    systématique (EdA §11) ;
  - **OCR par un petit modèle spécialisé** (GLM-OCR ou PaddleOCR-VL), MiMo en vision pour les
    figures et l'arbitrage (EdA §13) ;
  - MiMo = constructeur et agent de recherche ; Qwen3.8-27B / Flash-Next = consommateurs (et
    renfort ponctuel) ; spécialisation de MiMo seulement si S15 la justifie ;
  - SQLite + FTS5 + vecteurs exacts ; graphe en tables ; KùzuDB écarté.
- **Écarts par rapport au plan** : première version (v0.1) centrée sur les thèmes, refondue
  après les retours de l'utilisateur (logique de recherche, actualisation, transversalité,
  angle, OCR).
- **Mesures** : aucune (pas encore de code).
- **Dettes / reste à faire** : faire valider par l'utilisateur les listes de sous-questions
  attendues des cas de référence (en S08).
- **Questions pour l'utilisateur** : voir `001_but.md` §12 (matériel, langues, mode de
  vérification, sous-thèmes automatiques, ordre des interfaces).
