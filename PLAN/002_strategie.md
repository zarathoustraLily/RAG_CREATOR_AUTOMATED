# 002 — Stratégie de réalisation

> Statut : **proposition** · v0.3 · 2026-10-06
> Prérequis : `001_but.md` (le quoi) et `000_etat_de_l_art.md` (ce que dit la recherche,
> cité ci-dessous sous la forme « EdA §n »). Le découpage en sessions est dans
> `003_prompts_sessions/`.

---

## 0. Résumé

1. **Deux moments, un seul système** : *construire* une base vérifiée, datée et reliée (en
   tâche de fond) ; *répondre* avec un agent qui planifie, cherche, contrôle et hiérarchise.
2. **L'agent planifie, le moteur exécute** : le modèle comprend la situation et bâtit le plan ;
   un moteur classique (recherche hybride + re-classement) trouve et trie les preuves. Cet
   hybride est plus juste et ~3× moins coûteux qu'un agent qui fait tout (EdA §2).
3. **Quatre couches de connaissance** : carte des thèmes, étiquettes, graphe typé, horloge.
4. **Profils de domaine** : chaque domaine a ses étiquettes, ses sources de référence, son
   échelle de solidité, son unité de découpage et son rythme d'actualisation.
5. **Le temps est une contrainte dure** : versions conservées, périodes de validité, date de
   référence de la question, veille d'actualisation (EdA §3).
6. **Priorité ≠ solidité** : l'angle vient de l'utilisateur, la solidité vient des preuves ;
   contre-point systématique (EdA §11).
7. **Tout est vérifié et tracé** : JSON contraint, citations contrôlées, chaque décision
   journalisée ; état persistant et reprise après coupure.
8. **MiMo construit et cherche ; Qwen3.8 rédige.** MiMo pourra être spécialisé par
   entraînement sur des récompenses vérifiables tirées de la base elle-même (EdA §7).
9. **Tout document est lu** : texte natif d'abord ; **OCR spécialisé** pour les PDF scannés et
   les livres ; **MiMo en vision** pour décrire figures et schémas et arbitrer les passages
   douteux ; OCR vérifié et jugé sur ses effets sur la recherche (EdA §13).
10. **On mesure** : cinq cas de référence (`001_but.md` §7) servent de tests d'acceptation.

---

## 1. Principes directeurs

| Principe | Conséquence concrète |
|---|---|
| Le LLM transforme et juge, le code décide et exécute | Décisions finales = scores LLM + règles codées et réglables ; recherches exécutées par le moteur |
| Planifier avant de chercher, et soigner le premier coup | Plan explicite et contrôlable ; recherches parallèles initiales, puis approfondissement ciblé (EdA §1) |
| Décomposer au bon moment | Question entière pour la recherche initiale, sous-questions pour le re-classement et le contrôle (EdA §11) |
| Le temps est une contrainte, pas un bonus | Filtre dur « en vigueur à la date de référence » quand le profil l'exige (EdA §3) |
| La solidité ne se négocie pas | Échelles de preuve par profil ; statut de réplication tiré de sources explicites, pas de l'avis du modèle |
| Contenu collecté = donnée non fiable | Toujours entre `<document>…</document>`, consigne d'ignorer ses instructions, détection d'injection |
| Citer, c'est vérifier | Fidélité de chaque citation contrôlée ; nombre d'étapes de recherche plafonné (EdA §8) |
| Contexte compact | Peu d'outils, schémas compacts, réponses plafonnées, budget par modèle (EdA §9) |
| Idempotence et reprise | Machines à états dans SQLite, baux avec expiration |
| Agnostique au modèle | Profils de modèles + affectation par étape avec repli |
| Mesurer avant d'optimiser | Réglages fixés sur mesures (S15) ; journal de toutes les décisions |

---

## 2. Architecture d'ensemble

```
                              CONSTRUIRE (tâche de fond)
┌────────────┐   ┌──────────────────────────────────────────────────────────────┐
│ Connecteurs│   │ E0 charte+profil → E1 découverte → E2 récupération + lecture │
│ par profil │──▶│ → E3 pré-contrôles → E4 vérification doc → E5 datation        │
│ SearxNG    │   │ → E6 découpage → E7 vérification+étiquetage des extraits      │
│ Wikipédia  │   │ → E8 enrichissement → E9 indexation → E10 graphe typé         │
│ Europe PMC │   │ → E11 croisement/conflits → E12 fiches → E13 couverture ↺     │
│ OpenAlex   │   │ E14 veille d'actualisation (planifiée)                        │
│ Légifrance…│   └───────────────▲──────────────────────────────┬───────────────┘
│ inbox/ URL │                   │ collectes ciblées (lacunes)  │
└────────────┘                   │                              ▼
                     ┌───────────┴───────────┐     ┌──────────────────────────────┐
                     │ RÉPONDRE (agent)       │     │ SQLite (WAL)                 │
 question ──────────▶│ R1 situation           │◀───▶│ thèmes·profils·chartes·cartes│
 + angle / profil    │ R2 angle               │     │ documents·versions·validité  │
                     │ R3 plan (sous-questions│     │ extraits·étiquettes·FTS5·vect│
                     │    typées, poids,      │     │ entités·relations typées     │
                     │    contre-point)       │     │ affirmations·conflits·fiches │
                     │ R4 premier coup        │     │ exécutions de l'agent·lacunes│
                     │ R5 approfondissement   │     │ journal des appels LLM       │
                     │ R6 contrôles           │     └──────────────────────────────┘
                     │ R7 hiérarchisation     │
                     │ R8 dossier + lacunes   │──▶ Qwen3.8 rédige (proxy, MCP, ragc ask)
                     └────────────────────────┘
   llama-server : :8080 MiMo 9B (constructeur + agent + vision) · :8081 embeddings · :8082 re-classement
                  :8083 OCR spécialisé (PaddleOCR-VL ou GLM-OCR)
                  :8090 Qwen3.8 (consommateur ; renfort optionnel de construction)
```

---

## 3. Le modèle de connaissance

### 3.1 Arbre des thèmes → carte navigable

- Un thème s'écrit `Droit > Fiscalité > Géorgie` ou `droit/fiscalite/georgie` ; nœuds
  intermédiaires créés au besoin ; alias (« amanite tue-mouches », « fly agaric »).
- Chaque nœud a une **charte** (`charte.yaml`, modifiable à la main) : définition, périmètre
  inclus / exclu, sous-thèmes, mots-clés FR/EN, synonymes, confusions à éviter, sources
  prioritaires, affirmations sensibles, **profil de domaine**, langues.
- Chaque nœud a une **fiche de nœud** (C12) : ce que contient ce rayon, ses sous-thèmes,
  points clés, chiffres de couverture, lacunes connues. L'ensemble des fiches forme la
  **carte** que l'agent lit pour choisir où chercher (EdA §4) — c'est elle qui permet de
  relier « vendre une voiture » à *négociation*, *économie comportementale* et *neurosciences*
  sans dépendre des mots de la question.
- Interroger un nœud = interroger son sous-arbre ; un document a un nœud principal (le plus
  précis) et des nœuds secondaires, sans duplication.

### 3.2 Profils de domaine

Fichiers `profils/<nom>.yaml`, choisis par la charte (C01), surchargeables par thème. Profils
livrés en v1 : `juridique_fiscal`, `pharmaco_medical`, `mycologie`,
`sciences_comportementales` (neurosciences, psychologie, économie comportementale, vente),
`generique`.

Chaque profil définit :

| Élément | `juridique_fiscal` | `sciences_comportementales` |
|---|---|---|
| Étiquettes spécifiques | juridiction, nature de norme, référence d'article, date d'effet, statut (en vigueur / modifié / abrogé) | type d'étude, population (étudiants, professionnels…), taille d'échantillon, taille d'effet, préenregistrement, **statut de réplication** |
| Échelle de solidité (forte → faible) | texte officiel en vigueur > cour suprême > autres juridictions > doctrine administrative > doctrine universitaire > article de cabinet > blog/forum | méta-analyse corrigée du biais de publication / réplication multi-laboratoires > expérience de terrain préenregistrée > expérience de laboratoire > étude corrélationnelle > ouvrage de vulgarisation > blog |
| Unité de découpage | **l'article** (avec son code, son numéro, sa version) ; la décision par motifs | la section d'article scientifique (résumé, méthode, résultats, discussion) |
| Relations privilégiées | modifie, abroge, applique, interprète, cite, déroge à | cause, favorise, inhibe, médie, modère, réplique, échoue à répliquer |
| Actualisation | codes : mensuelle ; barèmes : à chaque loi de finances ; jurisprudence : nouvelles décisions | nouvelles publications : trimestrielle ; rétractations : mensuelle |
| Filtre temporel | **dur** (version en vigueur à la date de référence) | souple (récence comme bonus, sauf rétractation) |
| Sources de référence | Légifrance, Judilibre, BOFiP, EUR-Lex, matsne.gov.ge… | Europe PMC, OpenAlex, Crossref (dont les rétractations), bases de réplication |

`pharmaco_medical` : méta-analyse > essai randomisé > observationnel > série de cas > animal /
in vitro > avis d'expert, plus les avis d'agences sanitaires ; affirmations sensibles (dose,
toxicité, interactions). `mycologie` : bases taxonomiques et sociétés mycologiques > guides >
forums ; espèces confondables obligatoires dans la charte ; jamais de conseil de comestibilité.

### 3.3 Étiquettes

- **Communes** à tout extrait : thème(s), profil, langue, source, niveau de source, nature,
  date de publication, période de validité, référence d'unité (ex. « CGI art. 209 B »),
  section, page, position.
- **Spécifiques** au profil (§3.2), extraites par C06/C08 puis normalisées par le code.
- Utilisées comme **filtres** à la recherche et comme **facteurs** de la hiérarchisation.

### 3.4 Graphe typé

- Entités résolues (alias, noms scientifiques, variantes FR/EN) ; relations typées en
  **familles** : *normative* (modifie, abroge, applique, interprète, cite, déroge à),
  *causale* (cause, favorise, inhibe, médie, modère), *épistémique* (confirme, contredit,
  nuance, réplique, échoue à répliquer), *structurelle* (fait partie de, est un).
- Chaque relation porte : extraits de provenance, niveau de preuve, période de validité.
- Graphe des **affirmations** (EdA §5) : affirmations élémentaires reliées par
  *confirme / contredit*, utilisées pour qualifier les conflits.
- Le graphe sert aux questions **à plusieurs sauts** (convention → article → décision ;
  mécanisme → comportement → tactique, EdA §12) — pas à chaque recherche.

### 3.5 Le temps

- **Versions** : un texte qui change n'est pas écrasé ; nouvelle version avec
  `valid_from` / `valid_to`, lien `remplace` vers l'ancienne (lignée).
- **Date de référence** de chaque question : extraite (« en 2023… »), sinon aujourd'hui.
- **Filtre dur** pour les profils qui l'exigent ; bonus de récence ailleurs.
- **Veille d'actualisation** (E14) : chaque source a une classe de volatilité (profil) et une
  date de prochaine vérification ; re-récupération, comparaison, nouvelle version si
  changement substantiel (C14), ré-indexation et mise à jour du graphe.
- **Qualification des conflits** (EdA §3) : *évolution* (le savoir ou la règle a changé),
  *désaccord* (les sources se contredisent), *incertitude* (impossible de trancher).
- Une source non revérifiée depuis plus que sa période de volatilité est marquée
  « à revérifier » dans le dossier.

### 3.6 Schéma de données (SQLite)

`themes`, `theme_aliases`, `pages` (numéro de page du fichier et page imprimée, méthode
natif / OCR, moteur, indicateurs de qualité, alertes), `figures` (page, description, légende),
`documents` (avec `source_kind`, `jurisdiction`, `published_at`,
`valid_from`, `valid_to`, `legal_status`, `lineage_id`, `version_no`, `supersedes_id`,
`volatility`, `last_checked_at`, `next_check_at`, `credibility`), `document_themes`,
`chunks` (avec `unit_ref`, `facets`, `evidence_level`, `replication_status`, `population`,
`effect_size`, `valid_from`, `valid_to`, `flags`), `chunks_fts`, `embeddings`, `entities`,
`entity_aliases`, `relations` (avec `family`, `evidence_level`, validité, provenance),
`claims` (avec statut de croisement et nature du conflit), `cards` (entité, nœud, communauté),
`queries`, `jobs`, `cycles`, `llm_calls`, `review_decisions`, `research_runs` (question,
analyse, plan, trajectoire, dossier, métriques), `gaps` (lacunes → collectes ciblées),
`user_profiles`, tables d'évaluation. Chaque session ajoute ses tables par migration.

---

## 4. Pile technique

### 4.1 Inférence locale

```bash
# MiMo 9B — constructeur et agent de recherche (≈ 6 Go en Q4_K_M)
nice -n 10 llama-server -hf bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF:Q4_K_M \
  --jinja --reasoning-format deepseek -ngl 99 -c 65536 -np 4 --port 8080
# Embeddings multilingues
llama-server -hf gpustack/bge-m3-GGUF:Q8_0 --embedding --pooling cls -c 8192 -ub 8192 --port 8081
# Re-classement
llama-server -hf gpustack/bge-reranker-v2-m3-GGUF:Q8_0 --reranking -c 8192 -ub 8192 --port 8082
# OCR spécialisé (≈ 0,9 milliard de paramètres) — l'un ou l'autre, comparés en S05
llama-server -hf ggml-org/GLM-OCR-GGUF --temp 0.1 --port 8083
#   ou PaddleOCR-VL-1.6 : -m <modèle>.gguf --mmproj PaddleOCR-VL-1.6-GGUF-mmproj.gguf
# Qwen3.8 (consommateur) — selon votre configuration actuelle, port 8090
```

- **Vision de MiMo** : le dépôt GGUF de MiMo contient son module vision (`mmproj`) ; `-hf` le
  charge en principe automatiquement (sinon `--mmproj <fichier>`) — **à vérifier en S02**.

- MiMo hérite de l'architecture Qwen3.5 (3 couches sur 4 en attention linéaire) → cache KV
  réduit, 4 requêtes parallèles abordables. Réflexion activable par requête
  (`chat_template_kwargs.enable_thinking`). Échantillonnage recommandé : `0.6 / 0.95 / 20`.
- **À vérifier en S02** : contrainte de schéma JSON combinée à la réflexion ; efficacité du
  cache de préfixe.
- Embeddings et re-classement : bge-m3 / bge-reranker-v2-m3 au départ, **comparés en S15** à
  des modèles plus récents (EdA §10) ; ils peuvent tourner sur CPU.

### 4.2 Profils de modèles et affectation par étape

```yaml
models:
  mimo-9b:    {base_url: http://127.0.0.1:8080/v1, model: MiMo-V2.6-Distill-Qwen-9B, slots: 4}
  qwen38-27b: {base_url: http://127.0.0.1:8090/v1, model: Qwen3.8-27B, slots: 1}
  ocr:        {base_url: http://127.0.0.1:8083/v1, model: GLM-OCR, slots: 2}
stages:                         # liste = préférence, avec repli si le serveur ne répond pas
  ocr_page:               {profiles: [ocr]}
  figure_description:     {profiles: [mimo-9b], thinking: false}
  ocr_arbitration:        {profiles: [mimo-9b], thinking: true}
  theme_charter:          {profiles: [qwen38-27b, mimo-9b], thinking: true}
  doc_verification:       {profiles: [mimo-9b], thinking: true}
  doc_second_opinion:     {profiles: [qwen38-27b, mimo-9b], thinking: true}
  passage_verification:   {profiles: [mimo-9b], thinking: false}
  chunk_enrichment:       {profiles: [mimo-9b], thinking: false}
  conflict_qualification: {profiles: [qwen38-27b, mimo-9b], thinking: true}
  situation_analysis:     {profiles: [mimo-9b], thinking: true}
  research_plan:          {profiles: [mimo-9b], thinking: true}
  evidence_selection:     {profiles: [mimo-9b], thinking: false}
consumers:
  qwen38-27b: {context_budget_tokens: 8000}
```

### 4.3 Cohabitation des modèles

| Scénario | Fonctionnement |
|---|---|
| A. Tout tient en mémoire | Démon actif à tout moment, en priorité basse, slots limités |
| B. Alternance | Plages horaires et/ou bascule de modèles (`llama-swap` ou mode multi-modèles de `llama-server`). Constructeur absent → étapes LLM en attente, collecte et indexation continuent ; l'agent de recherche peut alors utiliser Qwen3.8 (repli) |
| C. Un seul modèle | Toutes les étapes sur Qwen3.8-27B : plus lent, meilleure qualité |

### 4.4 Stockage

SQLite (WAL) pour tout l'état ; FTS5 (`unicode61 remove_diacritics 2`) pour la recherche
lexicale ; vecteurs float16 en blobs + recherche exacte numpy par sous-arbre (interface
`VectorStore` pour passer à LanceDB/Qdrant au-delà de ~300 000 extraits) ; graphe en tables ;
exports GraphML/JSON.

### 4.5 Collecte et connecteurs

- Récupérateur `httpx` asynchrone : `robots.txt`, limite par domaine, cache, URL canoniques,
  HTML/PDF/DOCX/EPUB, `trafilatura` + repli ; les PDF passent par la lecture page par page
  (§4.7).
- **Connecteurs génériques** : SearxNG local, Wikipédia, listes d'URL, flux RSS, `inbox/`.
- **Connecteurs par profil** (accès et conditions d'utilisation à confirmer en S09) :
  scientifiques (Europe PMC, OpenAlex, Crossref et ses données de rétractation) ; juridiques
  français (Légifrance et Judilibre via l'API PISTE — clé gratuite —, BOFiP, EUR-Lex) ;
  géorgiens (matsne.gov.ge, site du service des recettes) ; mycologiques (MycoBank, Index
  Fungorum). Les sources dans une langue non couverte peuvent être traduites par le
  constructeur, avec mention.

### 4.6 Démon

Boucle `asyncio`, sémaphores par ressource, tourniquet entre thèmes, priorité aux demandes
manuelles et aux collectes ciblées, fichier PID, `SIGTERM` propre, `SIGHUP` = rechargement,
`os.nice`, plages horaires, `ragc daemon pause`, unités `systemd --user` / `launchd`.

### 4.7 Lecture des documents (PDF, livres scannés, images)

Traitement **page par page**, chaque page gardant son numéro (pour citer « p. 147 ») :

1. **Diagnostic de la page** : couche texte présente ? de bonne qualité (proportion de mots
   reconnus dans la langue, caractères parasites, encodage cassé) ? page surtout image ?
   tableaux, figures, formules ?
2. **Texte natif** (`pymupdf`) si la couche texte est bonne : exact et instantané.
3. **OCR spécialisé** sinon (page rendue en image à résolution suffisante, ≈ 200–300 dpi) :
   modèle OCR servi par `llama-server` (:8083), sortie Markdown (titres, listes, **tableaux**),
   température basse. Une couche texte de mauvaise qualité (ancien OCR) est **refaite**.
4. **Vision de MiMo** (L02) pour les **figures, schémas, photos et graphiques** : description
   factuelle et légende, indexées comme extraits de type `figure` liés à leur page — un schéma
   de mécanisme devient cherchable.
5. **Contrôle de l'OCR** :
   - indicateurs automatiques par page : mots inconnus, répétitions en boucle, lignes
     tronquées, ordre de lecture (colonnes), texte vide ;
   - sur un **échantillon** de pages et sur toute page suspecte : second moteur OCR (ou
     Tesseract), comparaison ; désaccord → **arbitrage par MiMo** (L03), qui voit l'image et
     les deux transcriptions et ne garde que ce qui est **visible** sur la page ;
   - page illisible → marquée, jamais inventée (`[illisible]`).
6. **Structure des livres** : table des matières (signets du PDF, sinon détection des titres),
   chapitres → sections, notes de bas de page rattachées, en-têtes et pieds de page retirés,
   pagination imprimée vs pagination du fichier ; métadonnées : auteur, titre, **édition**,
   année, ISBN (deux éditions = deux versions, §3.5).
7. **Autres formats** : EPUB (structure native), images isolées (JPG, PNG, TIFF), DOCX, HTML.

L'OCR est jugé **sur ses effets sur la recherche**, pas seulement au caractère près
(EdA §13) : le cas E compare la recherche sur un livre scanné et sur le même livre en texte
natif.

---

## 5. Construire : le pipeline en tâche de fond

| # | Étape | Prompts | Réflexion | Ce qu'elle produit |
|---|---|---|---|---|
| E0 | **Charte et profil** | C01, C02 | oui | charte, profil de domaine, requêtes initiales |
| E1 | **Découverte** | C02, C03 | non | candidats des connecteurs du profil, **triés sur titre et extrait** avant téléchargement |
| E2 | **Récupération et lecture** | L01, L02, L03 | non | texte structuré page par page (natif ou OCR), figures décrites, OCR contrôlé, structure du livre, métadonnées (§4.7) |
| E3 | **Pré-contrôles** | — | — | rejets motivés sans LLM : longueur, langue, doublons exacts et quasi-doublons, bruit, domaines |
| E4 | **Vérification documentaire** | C04, C05 | oui | pertinence, fiabilité, qualité, crédibilité multicritère, rattachement, décision |
| E5 | **Datation et versions** | C07 | non | dates de publication et de validité, statut juridique, lignée de versions (règles déterministes pour les sources officielles, LLM sinon) |
| E6 | **Découpage par profil** | — | — | unités naturelles (article de loi, section scientifique), 300–450 tokens, section parente |
| E7 | **Vérification et étiquetage des extraits** | C06 | non | garder/écarter, nature, niveau de preuve, population, taille d'effet, affirmations sensibles |
| E8 | **Enrichissement** | C08 | non | contexte, questions, mots-clés FR/EN, entités, **relations typées** |
| E9 | **Indexation** | — | — | embeddings (texte contextualisé + questions), FTS5, index des étiquettes et des dates |
| E10 | **Graphe** | C09 | non | entités résolues, relations normalisées par famille, communautés |
| E11 | **Croisement et conflits** | C10 | oui | affirmations sensibles croisées ; conflits qualifiés (évolution / désaccord / incertitude) |
| E12 | **Fiches** | C11, C12 | oui | fiches d'entités et **fiches de nœud** (la carte), chaque phrase citée et contrôlée |
| E13 | **Couverture** | C13 | oui | lacunes par sous-thème, nouvelles requêtes, continuer / arrêter |
| E14 | **Veille d'actualisation** | C14 | oui | nouvelles versions, abrogations, rétractations ; marquage « à revérifier » |

### 5.1 Vérification documentaire (E4) et extraits (E7)

- Le modèle reçoit la charte, la carte du sous-arbre, les métadonnées et un **échantillon**
  (début ≈ 1 500 tokens, milieu ≈ 600, fin ≈ 400) ; il note sur des **grilles ancrées**
  pertinence, fiabilité, qualité, et signale biais, alertes (affirmations dangereuses,
  **confusion d'espèces**, absence de sources, injection) et le nœud le plus précis.
- **Décision calculée par le code** :
  `score = 0,45·pertinence + 0,30·fiabilité + 0,25·qualité` + bonus/malus du niveau de source ;
  règles dures (pertinence ≤ 1 → rejet ; profil sensible et fiabilité ≤ 1 → rejet) ;
  ≥ 0,70 accepté, < 0,45 rejeté, entre les deux → **second avis** (C05, de préférence
  Qwen3.8), puis revue humaine (mode assisté) ou rejet (mode autonome).
- **Crédibilité multicritère** : poids réglés à la main au départ, **calibrés sur données**
  (pondération entropique, EdA §12) en S15 ; détection de conflits en deux temps (filtre
  léger, puis LLM seulement si nécessaire).
- **Statut de réplication et rétractations** : tirés de sources explicites (méta-analyses,
  projets de réplication, données de rétractation) — jamais de l'opinion du modèle (EdA §11).
- Jeu de référence annoté (≈ 20–30 documents couvrant les 4 profils, dont espèce voisine,
  texte abrogé, étude non répliquée, injection de prompt, site commercial).

---

## 6. Répondre : l'agent de recherche

### 6.1 Les étapes

| # | Étape | Prompt | Ce qui se passe |
|---|---|---|---|
| R1 | **Situation** | Q01 | acteurs, objectif, contraintes, juridictions, **date de référence**, ambiguïtés, hypothèses |
| R2 | **Angle** | (Q01) | angle détecté dans la question, option `--focus`, profil utilisateur |
| R3 | **Plan** | Q02 | graphe de sous-questions typées : question, thèmes (choisis sur la **carte**), filtres d'étiquettes et de dates, **poids**, dépendances, **contre-point** |
| R4 | **Premier coup** | — | toutes les sous-questions en parallèle : recherche hybride avec la question entière + la sous-question, re-classement **par sous-question**, consolidation (EdA §1, §11) |
| R5 | **Approfondissement** | — | effort réparti selon le rendement de chaque sous-question (exploration / exploitation, EdA §12) ; **escalade** extrait → section → document → voisins du graphe → fiches (EdA §2) ; 2 tours maximum |
| R6 | **Contrôles** | Q03 | version en vigueur, **fidélité** de chaque preuve à la sous-question, adéquation de la source, conflits qualifiés |
| R7 | **Hiérarchisation** | — | calcul de l'importance (§6.4) |
| R8 | **Dossier** | Q04 | dossier classé, étiqueté, sourcé, avec lacunes → collectes ciblées |

Si l'ambiguïté est forte (R1), l'agent **pose la question** avant de chercher (mode
interactif) ou **annonce son hypothèse** (mode autonome). Avec `--show-plan` /
`--validate-plan`, l'utilisateur voit et corrige le plan avant R4.

### 6.2 Format du plan (exemple, cas A)

```json
{
  "date_reference": "2026-10-06",
  "situation": {
    "acteurs": ["résident fiscal français", "société à créer en Géorgie"],
    "objectif": "réduire légalement l'imposition",
    "hypotheses": ["l'utilisateur reste domicilié en France"],
    "ambiguites": []
  },
  "angle": {"source": "defaut", "focus": null},
  "sous_questions": [
    {"id": "SQ1", "question": "Quels régimes d'imposition des sociétés existent en Géorgie, à quelles conditions ?",
     "themes": ["droit/fiscalite/georgie"], "filtres": {"juridiction": "GE", "nature": ["loi", "doctrine_administrative"]},
     "poids": 3, "depend_de": []},
    {"id": "SQ2", "question": "Un résident français reste-t-il imposable en France sur une société étrangère qu'il contrôle ?",
     "themes": ["droit/fiscalite/france"], "filtres": {"juridiction": "FR", "nature": ["loi", "jurisprudence", "doctrine_administrative"]},
     "poids": 3, "depend_de": []},
    {"id": "SQ3", "question": "Que prévoit la convention fiscale franco-géorgienne ?",
     "themes": ["droit/fiscalite/international"], "filtres": {"nature": ["convention"]}, "poids": 3, "depend_de": []},
    {"id": "SQ4", "question": "Quelles décisions ont appliqué ces règles à des montages comparables ?",
     "themes": ["droit/fiscalite/france", "droit/fiscalite/georgie"], "filtres": {"nature": ["jurisprudence"]},
     "poids": 2, "depend_de": ["SQ2", "SQ3"]},
    {"id": "CP1", "type": "contre_point", "question": "Dans quels cas ce montage est-il requalifié ou sanctionné ?",
     "themes": ["droit/fiscalite/france"], "poids": 2, "depend_de": ["SQ2"]}
  ],
  "budget": {"recherches_max": 12, "tokens_dossier": 8000}
}
```

### 6.3 Contrôles (R6)

- **Temps** : filtre dur par profil ; versions remplacées exclues ou présentées comme
  historiques ; sources « à revérifier » signalées.
- **Fidélité** : chaque preuve retenue doit répondre à sa sous-question et dire réellement ce
  qu'on lui fait dire (Q03) ; contrôle automatique des identifiants cités.
- **Adéquation** : une sous-question juridique exige des sources juridiques ; une
  sous-question médicale, des sources médicales (EdA §8).
- **Conflits** : qualifiés (évolution / désaccord / incertitude) et présentés, jamais lissés.

### 6.4 Hiérarchisation (R7)

```
importance = P × S × A × F × R
P  poids de la sous-question (1–3), ajusté par l'angle et le profil utilisateur
S  solidité (0–1) : échelle du profil, statut de réplication, crédibilité de la source
A  applicabilité (0–1) : juridiction, population, contexte comparés à la situation (R1)
F  fraîcheur (0–1) : 1 si à jour ; pénalité si « à revérifier » ; 0 si non en vigueur (filtre dur)
R  pertinence (0–1) : score du re-classement par sous-question
```

Poids et forme (produit ou moyenne géométrique pondérée) dans `config.yaml`, calibrés en S15.

### 6.5 Le dossier de preuves (R8)

```
DOSSIER — question · date de référence · hypothèses · angle
SQ2 (★★★) Un résident français reste-t-il imposable… ?
  [S3] Texte officiel en vigueur · FR · CGI art. … (version du …) · solidité forte
       « … extrait … »
  [S4] Conseil d'État, … · solidité forte · applique [S3]
  ⚠ Évolution : ancienne rédaction jusqu'au … (non applicable à la date de référence)
CP1 (★★) Contre-point : …
LACUNES : jurisprudence géorgienne absente de la base → collecte ciblée programmée
```

Deux formats : Markdown compact (injection dans le contexte) et JSON (réponse d'outil).
Budget plafonné par modèle consommateur.

### 6.6 Angle et profil utilisateur

- Sources de l'angle, de la plus forte à la plus faible : validation du plan > option
  `--focus` > formulation de la question > profil utilisateur > défaut.
- **Profil utilisateur** (`profils_utilisateurs/<nom>.yaml`) : vision exprimée en clair
  (« les décisions sont d'abord biologiques »), thèmes privilégiés et leurs poids, contre-point
  actif ou non, mode ambiguïté (demander / supposer). Il influence aussi la **collecte** :
  les thèmes privilégiés sont approfondis en priorité.
- L'angle **change le plan** (tronc, ponts vers l'action), pas les étiquettes de solidité.

### 6.7 Deux modes d'agent, comparés en S15

| Mode | Principe | Atouts |
|---|---|---|
| **Plan → exécution** (défaut) | MiMo produit le plan ; le code exécute recherches, re-classement, allocation d'effort ; MiMo sélectionne et assemble | Prévisible, économe, contrôlable (EdA §2) |
| **Navigation libre** | MiMo explore lui-même avec des outils : `rag_carte`, `rag_chercher`, `rag_lire` (extrait / section / document), `rag_voisins`, `rag_fiche` | Plus souple sur les corpus très structurés (EdA §4) |

### 6.8 Interfaces de consommation

- **Outil de haut niveau** `rag_research(question, focus?, date_reference?, budget?)` → dossier
  (l'agent MiMo fait le travail) — recommandé pour Qwen3.8.
- **Outils de bas niveau** (ceux de la navigation libre), pour que Qwen3.8 cherche lui-même.
- **Proxy compatible OpenAI** : intercepte la conversation, appelle `rag_research`, injecte
  le dossier et le prompt consommateur (Q06), relaie vers le `llama-server` de Qwen3.8
  → utilisable dans Open WebUI / LM Studio.
- **Serveur MCP** exposant ces outils, schémas compacts (EdA §9).
- `ragc ask "…" [--focus …] [--date …] [--show-plan] [--validate-plan]`, API HTTP, exports.
- Le prompt consommateur impose de s'appuyer sur le dossier : les gros modèles ont tendance à
  préférer leurs connaissances internes (EdA §11).

### 6.9 Spécialiser MiMo (paliers)

| Palier | Contenu | Session |
|---|---|---|
| 0 | MiMo guidé par prompts (Q01–Q05) | S08, S14 |
| 1 | Comparaison : (a) recherche simple améliorée, (b) Qwen3.8 outillé, (c) MiMo plan → exécution, (d) MiMo navigation libre — qualité du plan, rappel, bonne version, fidélité, latence, tokens | S15 |
| 2 | Entraînement **LoRA** (SFT) sur les meilleures trajectoires d'un professeur (Qwen3.8-27B), filtrées par critères vérifiables ; planificateur et sélecteur entraînés séparément (EdA §1) | S16 |
| 3 | **Renforcement à récompense vérifiable** : couverture des sous-questions attendues, bonne version, rappel des extraits attendus, fidélité des citations, coût en tokens — forme de récompense étudiée avec soin (EdA §7) | S16 |

Critère de déclenchement : MiMo guidé ≥ 2× plus rapide que Qwen3.8 outillé mais en retrait de
plus de 5 points sur la qualité du plan ou la fidélité. Données : la table `research_runs`.
Évaluation sur des **thèmes tenus à l'écart** de l'entraînement. Adaptateur chargé dans
`llama-server` (`--lora`), profil `mimo-9b-rag`.

---

## 7. Les prompts du modèle

### 7.1 Conventions

- Un fichier YAML par prompt : `id`, `version`, `description`, `reflexion`, `temperature`,
  `max_tokens`, `systeme`, `utilisateur`, `schema` (classe Pydantic).
- Gabarits `${variable}` ; variable manquante = erreur ; consignes en français, **clés JSON en
  anglais**, valeurs dans la langue de la charte.
- Contenu externe entre `<document>…</document>` + consigne d'ignorer ses instructions.
- Grilles **ancrées** (chaque niveau défini) ; `null` plutôt qu'inventer ; un court exemple
  pour les prompts complexes ; partie stable (système, charte, profil) en tête.
- Surcharges par thème (`themes/<chemin>/prompts/`) et par profil (`profils/<nom>/prompts/`).
- Toute modification incrémente la version ; le journal permet de comparer les versions sur
  les jeux de référence.

### 7.2 Catalogue

**Lecture**

| ID | Étape | Modèle | Réflexion | Sortie |
|---|---|---|---|---|
| L01 `ocr_page` | E2 | OCR spécialisé (:8083) | — | transcription Markdown de la page (consigne courte propre au modèle, ex. « OCR markdown » ; température 0,1) |
| L02 `figure_description` | E2 | MiMo en vision | non | type de figure, description factuelle, légende, éléments lisibles (axes, étiquettes), aucune interprétation non visible |
| L03 `ocr_arbitration` | E2 | MiMo en vision | oui | pour les passages en désaccord entre deux transcriptions : texte retenu, **seulement s'il est visible** sur l'image, sinon `[illisible]` |

**Construction**

| ID | Étape | Rôle | Réflexion | Sortie |
|---|---|---|---|---|
| C01 `theme_charter` | E0 | Documentaliste en chef | oui | charte + **profil de domaine** choisi |
| C02 `search_queries` | E0/E1/E13 | Spécialiste de recherche documentaire | non | requêtes par connecteur et par langue, jamais répétées |
| C03 `search_triage` | E1 | Trieur | non | garder / écarter, priorité, raison |
| C04 `doc_verification` | E4 | Vérificateur documentaire | oui | scores ancrés, type de source, biais, alertes, nœud, décision, justification |
| C05 `doc_second_opinion` | E4 | Contre-vérificateur | oui | confirme / infirme + raisons |
| C06 `passage_verification` | E7 | Contrôleur et étiqueteur d'extraits | non | garder, nature, **niveau de preuve, population, taille d'effet**, affirmations sensibles |
| C07 `doc_digest` | E5/E8 | Résumeur et datation | non | résumé, plan, portée, **dates de publication et de validité**, juridiction, référence de version |
| C08 `chunk_enrichment` | E8 | Indexeur | non | contexte, questions, mots-clés FR/EN, entités, **relations typées par famille** |
| C09 `entity_arbitration` | E10 | Arbitre d'entités | non | même entité ? nom canonique, type |
| C10 `conflict_qualification` | E11 | Contrôleur croisé | oui | concordant / contradictoire / nuancé / source unique + **évolution / désaccord / incertitude** |
| C11 `entity_card` | E12 | Rédacteur de fiches | oui | fiche par sections, chaque phrase citée |
| C12 `node_card` | E12 | Cartographe | oui | fiche de nœud : contenu, sous-thèmes, points clés, lacunes |
| C13 `coverage_analysis` | E13 | Directeur de collection | oui | lacunes, requêtes, sous-thèmes, continuer / arrêter |
| C14 `update_check` | E14 | Veilleur | oui | changement substantiel ? nature, portée, versions concernées |

**Réponse**

| ID | Étape | Rôle | Réflexion | Sortie |
|---|---|---|---|---|
| Q01 `situation_analysis` | R1–R2 | Analyste | oui | situation, date de référence, ambiguïtés, hypothèses, angle détecté |
| Q02 `research_plan` | R3 | Planificateur expert | oui | plan (§6.2) |
| Q03 `evidence_selection` | R6 | Contrôleur de preuves | non | par preuve : garder, fidélité, applicabilité, raison |
| Q04 `evidence_dossier` | R8 | Assembleur | non | synthèse par sous-question, lacunes, avertissements |
| Q05 `research_agent_tools` | navigation libre | Agent de recherche outillé (MiMo) | non | boucle d'outils → dossier |
| Q06 `consumer_answer` | consommation | Assistant documentaire (Qwen3.8) | au choix | réponse citée `[S#]`, prudences, lacunes |
| Q07 `consumer_agent` | consommation | Agent outillé (Qwen3.8) | au choix | usage des outils `rag_*` |

**Évaluation**

| ID | Rôle | Réflexion | Sortie |
|---|---|---|---|
| V01 `eval_questions` | Concepteur d'examen | non | questions + réponses attendues + type (factuelle, multi-sauts, transversale, temporelle, sans réponse) |
| V02 `eval_judge` | Juge (autre modèle que le constructeur si possible) | oui | fidélité, complétude, abstention ; contrôles déterministes privilégiés (EdA §3) |

---

## 8. Fonctionnement en tâche de fond

- **Cycles** par thème : E1 → E13 ; arrêt sur couverture cible, nombre maximal de cycles,
  **rendements décroissants** (< 10 % de nouveaux documents acceptés) ou budget de la nuit.
- **Veille** (E14) planifiée selon la volatilité de chaque source.
- **Collectes ciblées** issues des lacunes des questions (`gaps`), prioritaires.
- **Rapports de cycle** (`reports/`) : vus / acceptés / rejetés avec motifs, revues en
  attente, conflits nouveaux, nouvelles versions, couverture, temps et tokens.
- **Résilience** : serveur absent → attente sans échec ; baux expirés repris ; test d'arrêt
  brutal obligatoire.

---

## 9. Qualité, tests, évaluation

- **Hors ligne par défaut** : faux serveur compatible OpenAI (réponses selon l'en-tête
  `X-RAGC-Prompt`), fixtures rédigées pour le projet, aucun réseau.
- **Conditions réelles** : `pytest --live`.
- **Cas de référence A–E** (`001_but.md` §7) : listes de sous-questions attendues validées par
  l'utilisateur ; corpus de test par cas ; contrôles **déterministes** (articles, versions,
  dates, identifiants cités) privilégiés aux juges LLM (EdA §3).
- **Jeux de référence** : vérification documentaire, étiquetage de la solidité, entités,
  **pages OCR** (pages imprimées, deux colonnes, tableaux, notes, figures, page dégradée)
  transcrites à la main.
- **Évaluation globale** : qualité du plan, Recall@k, MRR, bonne version, fidélité des
  citations, respect de l'angle, abstention, latence, coût ; **évaluation des trajectoires**
  de l'agent (EdA §10) ; gain mesuré avec / sans RAG sur Qwen3.8.

---

## 10. Budget de performance (indicatif, à mesurer)

| Activité | Coût estimé |
|---|---|
| Construction : 1 000 pages ≈ 3 000 extraits ≈ 150–300 documents | ≈ 2 à 4 h (vérification, étiquetage, enrichissement, MiMo Q4, 4 slots) |
| Lecture d'un livre scanné de 300 pages | OCR spécialisé ≈ quelques secondes par page → ≤ 1 h ; + descriptions de figures par MiMo ; à mesurer en S05 |
| Question simple (recherche hybride + re-classement) | < 300 ms ; < 1,5 s avec re-classement |
| Question complexe (Q01 + Q02 + recherches + Q03 + Q04) | ≈ 20 à 60 s avec MiMo, hors rédaction par Qwen3.8 |

---

## 11. Risques et parades

| Risque | Parade |
|---|---|
| JSON invalide d'un modèle 9B | Grammaire de schéma + Pydantic + réparation ; taux de validité suivi |
| Plan à côté de la plaque (mauvaise compréhension) | Analyse de situation explicite, ambiguïtés exposées, plan visible et corrigeable, cas de référence |
| Sur-décomposition (trop de sous-questions, coût) | Budget de recherches, allocation selon le rendement, poids |
| Version périmée présentée comme actuelle | Filtre dur, lignées de versions, veille, contrôle déterministe |
| Complaisance (confirmer l'angle de l'utilisateur) | Solidité non négociable, contre-point, preuves notées sur leur force (EdA §11) |
| Citations infidèles | Contrôle de fidélité (Q03), identifiants vérifiés par le code (EdA §8) |
| Le consommateur ignore le dossier | Prompt Q06 strict ; mesure de l'usage du contexte |
| Références ou affirmations inventées (y compris dans des documents fournis) | Toute référence vérifiée à la source ; leçon de la bibliographie vérifiée (EdA §12) |
| Confusion d'espèces / de notions voisines | Charte (confusions à éviter), cas dédiés dans les jeux de référence |
| Injection de prompt dans une page | Balises, consigne, détection, décision finale par le code |
| Concurrence GPU avec Qwen3.8 | Scénarios A/B/C, plages horaires, attente sans échec |
| Accès aux sources officielles (clés, conditions) | Connecteurs optionnels, documentés, désactivables |
| Agent entraîné qui apprend par cœur | Thèmes tenus à l'écart, palier 2–3 seulement si mesuré utile |
| OCR qui « réécrit » ou invente du texte plausible | Modèle OCR spécialisé à température basse, contrôles automatiques, second moteur sur échantillon, arbitrage visuel limité au visible, `[illisible]` plutôt qu'inventer (EdA §13) |
| OCR correct au caractère près mais mauvais pour la recherche (ordre de lecture, tableaux) | Évaluation par la recherche (cas E), contrôle de l'ordre de lecture et des tableaux |
| Livres volumineux qui saturent le GPU | Lecture en tâche de fond, page par page, reprise au point d'arrêt, priorité basse |
| Droits d'auteur (livres, articles) | Usage personnel et local, `robots.txt`, source toujours citée, pas de redistribution |

---

## 12. Plan de réalisation

16 sessions (dont une conditionnelle), détaillées dans `003_prompts_sessions/` :

| Jalon | Sessions | Résultat visible |
|---|---|---|
| **J1 — Base locale vérifiée, étiquetée, datée** | S01 → S07 | Vos fichiers, **y compris livres et PDF scannés** (S05), → lus, vérifiés, étiquetés, datés, indexés ; `ragc search` avec filtres |
| **J2 — Un RAG qui raisonne** | S08 | `ragc ask --show-plan` : analyse, plan, dossier hiérarchisé, angle respecté (cas B et C) |
| **J3 — Collecte web et sources officielles** | S09 | Collecte autonome par profil + collectes ciblées sur lacunes |
| **J4 — Connaissance reliée et à jour** | S10 → S12 | Graphe typé, conflits qualifiés, veille d'actualisation, carte et fiches (cas A et D) |
| **J5 — Autonomie** | S13 | Démon, cycles, couverture, veille et collectes planifiées |
| **J6 — Consommation et mesure** | S14, S15 | Outils MCP, proxy pour Qwen3.8, navigation libre, évaluation et calibrage |
| **J7 — MiMo spécialisé** *(si S15 le justifie)* | S16 | Agent MiMo entraîné, gain mesuré |
