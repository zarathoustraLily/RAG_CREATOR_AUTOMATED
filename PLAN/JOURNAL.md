# Journal de bord du projet

> Une entrée par session, ajoutée à la clôture (gabarit dans
> `003_prompts_sessions/00_regles_communes.md` §8). Les plus récentes en bas.

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

## S00 (révision v0.5) — Une machine, spécialistes, portabilité, domaines — 2026-10-06

- **Fait** :
  - `000` : petits modèles spécialisés et exécution sur une machine (§14), outils existants
    (§15), machines de l'utilisateur, portabilité, fiscalité géorgienne et criminologie des
    escroqueries (§16) ;
  - `001` v0.5 et `002` v0.5 : travail **séquentiel** (un modèle lourd à la fois, par phases),
    **travail en fond pilotable** (démarrer, suspendre, arrêter, reprendre ; pause qui libère la
    carte graphique), **installable sous Windows et Linux**, **usine à spécialistes** (LoRA par
    tâche, porte de promotion, domaine tenu à l'écart), **réentraînement en une commande** après
    changement de modèle de base, option **adaptateur « recherche » sur Qwen3.8** ;
  - nouveaux domaines et profils : criminologie (escroqueries), fiscalité géorgienne, santé
    clinique (traumatismes, phobies), cybersécurité (hacking) ; cas de référence F, G, H ;
  - `003` : 16 sessions réécrites (v0.5).
- **Décisions** :
  - domaines prioritaires de la première version : **escroqueries** et **fiscalité géorgienne** ;
  - **hacking = domaine tenu à l'écart** de l'entraînement des spécialistes ;
  - développement **dans le cloud** ; mesures réelles par **banc** (`bench/`, puis `ragc bench`)
    sur les PC de l'utilisateur ;
  - spécialistes : le gain sûr est la **vitesse** ; la qualité au-delà de l'enseignant vient des
    validations, des contrôles automatiques et du renforcement.
- **Écarts par rapport au plan** : la spécialisation passe de « option finale » à **pilier
  central** ; le service permanent de la v0.3 devient un travailleur de fond pilotable.
- **Mesures** : aucune (pas encore de code).
- **Bancs à lancer par l'utilisateur** : après S01, le banc de mesure sur le PC RTX 5090 et le PC
  RTX 4090.
- **Questions pour l'utilisateur** : voir `001_but.md` §12 (Windows ou Linux, mémoire vive, usage
  conjoint des deux PC, bibliothèque, langues).

## S00 (suite) — Carte du programme et module « Méthodologie et technique de recherche » — 2026-10-06

- **Fait** :
  - convention des **mini-scripts** : un rôle par fichier, un manifeste `__manifeste__` (rôle,
    groupe, ordre chronologique, entrées et sorties avec le nom des variables du code) ;
  - **carte du programme** (`carte_du_programme/`) : `architecture_prevue.yaml` (scripts prévus),
    `generer_carte.py` (lit les manifestes sans exécuter le code, calcule les flux, contrôle la
    cohérence), page HTML5 interactive `index.html` (chronologie, flux, variables, parcours
    guidés, recherche, zoom, thème clair et sombre), 8 tests ;
  - module **`methodologie_recherche/`** (à l'utilisateur) : contrat des techniques
    (`Requete`, `Candidat`, `Document`, `Politesse`, `AccesRefuse`, `Ralentir`,
    `SourceIndisponible`), client HTTP identifié et `robots.txt`, méthodologies YAML avec
    héritage (commun, juridique_fiscal → fiscalite_georgie, criminologie, sante_clinique,
    cybersecurite, sciences_comportementales, pharmaco_medical, mycologie), générateur de
    requêtes, registre, quatre techniques (dossier local, OpenAlex, Wikipédia, liste de lecture)
    et un gabarit, banc de mesure (exécuter, évaluer avec étiquettes, comparer), 57 tests sans
    réseau + 2 tests réseau (`--reseau`), exemples de tests personnels, `LISEZMOI.md` ;
  - carte régénérée : 84 scripts dont 11 réalisés, 0 problème.
- **Décisions** :
  - API : la recherche passe par l'API et suit ses règles (agent identifié avec contact, rythme
    modéré) ; le téléchargement d'une page ou d'un PDF respecte `robots.txt` ;
  - un refus ou une demande de ralentir arrête la technique pour la source concernée et bascule
    vers la collecte assistée ; aucune technique ne masque l'automatisation ;
  - clés et contacts en variables d'environnement (`RAGC_OPENALEX_CLE`, `RAGC_CONTACT`), jamais
    dans le dépôt.
- **Constat** : depuis la machine de développement, OpenAlex (sans clé) et Wikipédia (sans
  contact) répondent « trop de requêtes » ; cause probable des échecs de collecte par API
  signalés par l'utilisateur (`000` §16).
- **Mesures** : aucune mesure de performance (banc hors ligne seulement exécuté pour vérifier
  qu'il fonctionne).
- **Bancs à lancer par l'utilisateur** : `python -m methodologie_recherche.bancs.banc_collecte
  executer --domaine fiscalite_georgie --sujets methodologie_recherche/bancs/sujets_exemple.yaml`
  sur son PC, avec `RAGC_OPENALEX_CLE` et `RAGC_CONTACT` définis.


## S00 (suite) — Décomposition transversale et deuxième lot de références — 2026-10-06

- **Problème soulevé par l'utilisateur** : une LoRA entraînée sur d'excellents exemples ne donne
  pas un « répertoire transversal » ; une question comme « comment convaincre quelqu'un
  d'abandonner le véganisme ? » exige d'identifier, avant de chercher, les disciplines et les
  questions sous-jacentes qu'elle mobilise.
- **Décision** : séparer la **procédure** (apprise : prompts Q02, Q08, puis spécialiste
  *planif*), le **répertoire** (externe, modifiable par l'utilisateur :
  `methodologie_recherche/transversal/`) et les **ponts du corpus** (calculés sur les données,
  modèle ABC de Swanson). Plan transversal en R3 : exploration par le répertoire, ponts,
  K plans candidats, fusion par couverture des angles, critique de complétude (Q08), lacunes →
  collecte ciblée (`002_strategie.md` §7.6).
- **Fait** :
  - `methodologie_recherche/transversal/` : grilles d'analyse (situation, présupposés et taux de
    base, quatre questions de Tinbergen, niveaux d'explication, qui dit quoi à qui, leviers et
    effets pervers, éthique, règle–faits–conclusion, analogues, contre-point), 32 disciplines,
    9 problèmes généraux avec leurs domaines analogues ; scripts `charger_repertoire`,
    `explorer_transversal`, `ponts_corpus`, `fusionner_plans` ; `outils_texte.py` partagé ;
    tests (dont le cas du véganisme et un exemple de test personnel) ;
  - plan : cas de référence **I** (véganisme), critères « couverture transversale » et
    « étendue préservée » (`001` §9), §7.6 et porte d'étendue pour le spécialiste du plan
    (`002` §8.3), sessions S09, S12, S14 ; carte : groupe « Répertoire transversal », étapes
    `critique_completude` et `concepts_documents`, 91 scripts dont 16 réalisés, 0 problème ;
  - deuxième lot de références de l'utilisateur vérifié (`000` §12) : **SyLeR** existe (2025,
    prépublication) mais ses effets étaient exagérés ; **LegalGraphRAG** confirmé (ACL 2026) ;
    **OntoRAG** existe mais « *What Does an Ontology Actually Do in RAG?* » est un billet de blog
    et le chiffre « 80 % du bruit éliminé » est inventé.
- **Retenu de ce lot** : dossier juridique en **règle → faits → conclusion** ; auditeur (R6)
  armé d'une liste de contrôle d'applicabilité par profil, avec élagage en cascade ; ontologie
  comme **points d'entrée multiples**, recherche à plat conservée ; couverture d'ensembles pour
  le choix des preuves.
- **Mesures** : aucune.
