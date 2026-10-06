# S01 — Étude « réutiliser ou construire », portabilité, banc de mesure

> Jalon J0 · Dépend de : — · Étapes : — · Prompts d'exécution : —
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§13 à §16**), `PLAN/001_but.md`,
`PLAN/002_strategie.md` (**§3, §5**, §8), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Avant d'écrire le logiciel : décider **ce qu'on réutilise et ce qu'on construit**, vérifier la
**portabilité** (Windows, Linux, cartes Blackwell) et fournir à l'utilisateur un **banc de
mesure** qu'il lance sur ses deux PC (RTX 5090 32 Go, RTX 4090 24 Go, 64 Go de RAM). Tu
travailles dans le cloud sans GPU : tu prépares les mesures, tu ne les fais pas.

## À réaliser

1. **Étude documentée** → `PLAN/004_decisions_techniques.md`. Pour chaque point : options,
   sources **vérifiées** (documentation officielle, dépôts, licences), recommandation
   provisoire, ce que le banc doit confirmer.
   - **Lecture des PDF** : MinerU, Docling, modèle OCR servi par `llama-server` (GLM-OCR,
     PaddleOCR-VL) — qualité, vitesse, Windows, licence (attention aux conditions de MinerU).
   - **Littérature scientifique** : composants de PaperQA2 réutilisables ou non.
   - **Graphe** : tables maison ou LightRAG.
   - **Gestionnaire de modèles** : mode routeur de `llama-server`, `llama-swap`, ou gestion de
     processus maison — sous Windows et Linux.
   - **`llama-server` sous Windows** avec CUDA 12.8+ (5090) : binaires officiels ou compilation ;
     LoRA par requête ; vision (`mmproj`) ; mode routeur.
   - **Travail en fond sous Windows** : processus détaché, canal de contrôle local, démarrage
     automatique (Planificateur de tâches) ; équivalents Linux.
   - **Entraînement** : Unsloth sous Windows natif ou WSL, Linux ; LoRA 16 bits ; déchargement
     de couches ; prise en charge des bases visées (famille Qwen3.5, MiMo 9B, Qwen3.8-27B).
   - **Import de bibliothèque** : lecture des données locales de Zotero et Calibre.
   - **Notes des réponses** : récupération des retours (pouce, note) d'Open WebUI côté proxy, ou
     alternative.
   - **Empaquetage** : `uv` / `pipx`, scripts d'installation PowerShell et shell.
2. **Banc de mesure autonome** (`bench/`, exécutable avant que le logiciel n'existe, Windows et
   Linux, instructions en français dans `bench/README.md`) produisant
   `reports/bench/<machine>_<date>.md` :
   - détection du matériel (OS, CPU, RAM, GPU, VRAM, pilote, CUDA, disque) ;
   - temps de **chargement et déchargement** de MiMo 9B (Q4, Q8) et de Qwen3.8-27B (Q4) ;
   - tokens/s avec 1 et 4 requêtes ; JSON contraint **avec et sans réflexion** ; appel d'outils ;
     **vision** de MiMo sur une image de test ;
   - OCR : les options retenues sur 3 pages de test fournies (fictives, rendues en image) ;
   - embeddings et re-classement **sur processeur et sur GPU** (latence pour 40 passages) ;
   - **faisabilité d'entraînement** : mini-entraînement LoRA (quelques pas) d'un modèle 0,8B, puis
     estimation pour 4B, 9B et 27B avec déchargement (optionnel, long).
3. Le banc télécharge ce dont il a besoin (avec confirmation) et n'écrit rien hors de son dossier.

## Critères d'acceptation

- [ ] `PLAN/004_decisions_techniques.md` complet, sources citées, décisions provisoires claires.
- [ ] `bench/` testé hors ligne (avec des faux serveurs) ; instructions de lancement Windows et
      Linux simples.
- [ ] Message final : demander à l'utilisateur de lancer le banc sur ses deux PC et de transmettre
      les rapports.
- [ ] Procédure de clôture appliquée.
