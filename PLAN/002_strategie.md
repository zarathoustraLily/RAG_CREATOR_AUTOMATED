# 002 — Stratégie de réalisation

> Statut : **proposition** · v0.4 · 2026-10-06
> Prérequis : `001_but.md` (le quoi) et `000_etat_de_l_art.md` (cité « EdA §n »).
> Le découpage en sessions est dans `003_prompts_sessions/`.

---

## 0. Résumé

1. **Une seule machine, en séquentiel** : un seul modèle lourd en mémoire à la fois. La nuit,
   le travail est découpé en **phases** (un modèle par phase, les étapes sans modèle
   s'intercalent). Le jour, une question est traitée **sans recharger de modèle**.
2. **Spécialiser plutôt que grossir** : chaque tâche étroite et répétitive est confiée à un
   **petit spécialiste** (un modèle de base + un adaptateur LoRA par tâche, choisi à chaque
   requête). Les spécialistes sont entraînés sur les données que le système produit et que vous
   validez, et ne sont **promus** que s'ils égalent l'enseignant (EdA §13, §14).
3. **Réutiliser avant de construire** : lecture des PDF par un outil existant ou un modèle OCR
   spécialisé ; inspiration de PaperQA2 pour la littérature scientifique (EdA §15).
4. **Deux moments de travail et un moment d'apprentissage** : *construire* une base vérifiée,
   datée et reliée ; *répondre* avec un agent qui planifie, cherche, contrôle et hiérarchise ;
   *apprendre* en entraînant les spécialistes.
5. **L'agent planifie, le moteur exécute** : recherche hybride + re-classement classiques ;
   l'agent comprend, planifie, sélectionne (EdA §2).
6. **Quatre couches de connaissance** : carte des thèmes, étiquettes, graphe typé, horloge ;
   **profils de domaine** pour juger chaque domaine selon ses règles.
7. **Le temps est une contrainte dure** pour le droit : versions, validité, date de référence,
   veille (EdA §3).
8. **Priorité ≠ solidité** : l'angle vient de vous, la solidité des preuves ; contre-point
   systématique (EdA §11).
9. **Tout est vérifié, tracé, et devient un exemple** : JSON contraint, citations contrôlées,
   chaque appel journalisé avec son statut de validation.
10. **On mesure** : cinq cas de référence, le **journal de vos vraies questions**, des jeux
    tenus à l'écart pour promouvoir les spécialistes.

---

## 1. Principes directeurs

| Principe | Conséquence concrète |
|---|---|
| Un seul modèle lourd à la fois | Gestionnaire de modèles ; travail groupé par modèle puis par adaptateur ; aucune bascule pendant une question |
| Spécialiser plutôt que grossir | Flotte de spécialistes LoRA ; données d'entraînement capturées dès le premier jour |
| Promouvoir sur preuve | Un spécialiste remplace l'enseignant seulement s'il fait aussi bien sur un jeu tenu à l'écart |
| Réutiliser avant de construire | Étude d'outils en S01 ; on ne code que ce qui fait la différence |
| Le LLM transforme et juge, le code décide et exécute | Décisions finales = scores + règles réglables ; recherches exécutées par le moteur |
| Planifier avant de chercher, soigner le premier coup | Plan explicite, contrôlable ; recherches initiales en parallèle (EdA §1) |
| Le temps est une contrainte | Filtre dur « en vigueur à la date de référence » selon le profil (EdA §3) |
| La solidité ne se négocie pas | Échelles de preuve par profil ; réplication tirée de sources explicites |
| Contenu collecté = donnée non fiable | Balises `<document>`, consigne, détection d'injection |
| Citer, c'est vérifier | Fidélité contrôlée ; étapes de recherche plafonnées (EdA §8) |
| Contexte compact | Peu d'outils, schémas compacts, budgets (EdA §9) |
| Idempotence et reprise | Machines à états dans SQLite, baux, reprise exacte après coupure |

---

## 2. Architecture d'ensemble

```
 LA NUIT — construire, par phases (un modèle chargé par phase)
 ┌───────────────────────────────────────────────────────────────────────────────────┐
 │ P0 sans modèle : import bibliothèque · collecte par API · extraction native ·     │
 │                  pré-contrôles · datation déterministe · découpage · veille (diff)│
 │ P1 lecture     : OCR des pages scannées (outil ou modèle OCR spécialisé)          │
 │ P2 construction: modèle de base + adaptateurs (ou MiMo) — charte, tri,            │
 │                  vérification, étiquetage, résumé, enrichissement, figures…       │
 │                  (les étapes P0 s'intercalent sans décharger le modèle)           │
 │ P3 indexation  : embeddings en lot                                                │
 │ P4 enseignant  : seconds avis, croisements, fiches, exemples d'entraînement       │
 └───────────────────────────────────────────────────────────────────────────────────┘
 PÉRIODIQUEMENT — apprendre
   P5 entraînement : jeux validés → LoRA → évaluation tenue à l'écart → promotion ou non

 LE JOUR — répondre (un seul modèle chargé, aucune bascule pendant une question)
   question → R1 situation → R2 angle → R3 plan → R4 premier coup → R5 approfondissement
            → R6 contrôles → R7 hiérarchisation → R8 dossier → réponse
   recherche hybride + re-classement sur le processeur (petits modèles d'aide)
   interfaces : proxy OpenAI (Open WebUI, LM Studio) · outils MCP · ragc ask

 ÉTAT : SQLite (WAL) — thèmes · profils · documents · pages · versions · extraits · étiquettes ·
        FTS5 · vecteurs · graphe · affirmations · fiches · exécutions de l'agent · lacunes ·
        journal des appels = réservoir d'exemples d'entraînement
```

---

## 3. Exécution séquentielle sur une seule machine

### 3.1 Gestionnaire de modèles

- **Règle** : au plus **un modèle lourd** (≥ 2 Go) chargé à la fois. Les petits modèles d'aide
  (embeddings, re-classement, ≈ 1,2 Go) tournent sur le **processeur** par défaut, sur le GPU
  s'il reste de la place (selon le profil matériel).
- **Mécanisme** (choisi en S01 après essai) : le **mode routeur** de `llama-server`
  (`--models-max 1`, chargement et déchargement à la demande, EdA §14), `llama-swap`, ou un
  gestionnaire de processus maison qui démarre et arrête `llama-server`.
- `ragc models status|load|unload` ; le gestionnaire connaît le modèle chargé et refuse toute
  demande qui provoquerait une bascule en cours de question.
- **Adaptateurs LoRA** : plusieurs adaptateurs chargés avec le modèle de base (`--lora`),
  sélection **par requête** (champ `lora`) ; les requêtes sont **groupées par adaptateur**, car
  des adaptateurs différents ne sont pas traités ensemble (EdA §14).

### 3.2 Les phases de nuit

| Phase | Modèle chargé | Travaux |
|---|---|---|
| P0 | aucun | import de bibliothèque, collecte par API, téléchargements, extraction native, pré-contrôles, datation déterministe, découpage, comparaison de versions (veille) |
| P1 | outil ou modèle **OCR** | lecture des pages scannées, contrôles d'OCR |
| P2 | **base + adaptateurs** (ou MiMo avant les spécialistes) | chartes, tri, vérification, étiquetage, résumés, enrichissement, arbitrage d'entités, descriptions de figures et arbitrage d'OCR (vision de MiMo) |
| P3 | **embeddings** (GPU en lot) | indexation des nouveaux extraits |
| P4 | **enseignant** (Qwen3.8-27B, ou MiMo avec réflexion) | seconds avis, croisements d'affirmations, fiches, analyse de couverture, **étiquettes d'enseignant** sur un échantillon |
| P5 | **entraînement** (occasionnel) | LoRA des spécialistes, évaluation, promotion |

- L'**ordonnanceur de nuit** (`ragc nuit`, lancé par un minuteur `systemd` ou `launchd`, pas de
  service permanent) enchaîne les phases dans la plage horaire autorisée, **boucle** tant qu'il
  reste du travail et du temps, et s'arrête proprement à l'heure dite.
- Les étapes sans modèle (P0) s'exécutent **pendant** qu'un modèle reste chargé : on ne décharge
  pas MiMo pour découper des documents.
- Ordre et durées réglables ; reprise exacte après coupure ; rapport au matin.

### 3.3 Le jour : répondre sans recharger

| Mode | Modèle chargé | Fonctionnement | Quand |
|---|---|---|---|
| **RAG direct** (défaut) | Modèle de recherche : base + adaptateurs *planification, sélection, dossier, rédaction* (MiMo seul avant les spécialistes) | Tout le parcours R1–R8 **et** la réponse | Questions documentaires ; les petits modèles s'en tiennent mieux aux preuves fournies (EdA §11) |
| **Qwen3.8 + adaptateur recherche** (votre idée) | Qwen3.8 + adaptateur LoRA « recherche » activé à la volée | R1–R8 avec l'adaptateur, réponse sans adaptateur | Si l'entraînement sur Qwen3.8 est faisable (S01, S12) : aucune bascule, même en conversation |
| **Qwen3.8 seul** | Qwen3.8 | R1–R8 par prompts | Repli quand Qwen3.8 est chargé et que l'adaptateur n'existe pas encore |

Le proxy (Open WebUI, LM Studio) détecte le modèle chargé et choisit le mode sans bascule. Une
bascule n'a lieu que si vous la demandez.

### 3.4 Profils matériels

Fichier `profils_materiels/<nom>.yaml` établi en S01 à partir de **votre** machine :

| Élément décidé | Selon |
|---|---|
| Taille des spécialistes (0,8B / 2B / 4B / MiMo 9B) | VRAM disponible pour l'inférence et l'entraînement |
| Adaptateur sur Qwen3.8 | Faisabilité de l'entraînement avec déchargement de couches (EdA §14), durée acceptable |
| Petits modèles d'aide sur CPU ou GPU | VRAM restante |
| Outil d'entraînement | CUDA → Unsloth (ou TRL/PEFT) ; Mac → MLX (à vérifier) |
| Quantification de chaque modèle | Mémoire et vitesse mesurées |
| Temps de bascule | Mesuré (cible ≤ 30 s) |

---

## 4. Le modèle de connaissance

### 4.1 Arbre des thèmes → carte navigable

- `Droit > Fiscalité > Géorgie` ou `droit/fiscalite/georgie` ; nœuds intermédiaires créés ;
  alias.
- **Charte** par nœud (`charte.yaml`, modifiable) : définition, périmètre, sous-thèmes,
  mots-clés FR/EN, synonymes, confusions à éviter, sources prioritaires, affirmations sensibles,
  **profil de domaine**, langues.
- **Fiche de nœud** (C12) par nœud : contenu, sous-thèmes, questions types, points clés,
  couverture, lacunes ; l'ensemble forme la **carte** que l'agent lit pour choisir où chercher
  (EdA §4).
- Interroger un nœud = interroger son sous-arbre ; un document a un nœud principal et des
  nœuds secondaires.

### 4.2 Profils de domaine

`profils/<nom>.yaml` : `juridique_fiscal`, `pharmaco_medical`, `mycologie`,
`sciences_comportementales` (neurosciences, psychologie, économie comportementale, vente),
`generique`.

| Élément | `juridique_fiscal` | `sciences_comportementales` |
|---|---|---|
| Étiquettes | juridiction, nature de norme, référence d'article, date d'effet, statut | type d'étude, population, effectif, taille d'effet, préenregistrement, **statut de réplication** |
| Solidité (forte → faible) | texte officiel en vigueur > cour suprême > autres juridictions > doctrine administrative > doctrine universitaire > article de cabinet > blog | méta-analyse corrigée / réplication multi-laboratoires > terrain préenregistré > laboratoire > corrélationnel > vulgarisation > blog |
| Unité de découpage | l'article (code, numéro, version) ; la décision par motifs | la section d'article scientifique ; le chapitre / la section d'un livre |
| Relations | modifie, abroge, applique, interprète, cite, déroge à | cause, favorise, inhibe, médie, modère, réplique, échoue à répliquer |
| Actualisation | codes : mensuelle ; barèmes : à chaque loi de finances | publications : trimestrielle ; rétractations : mensuelle |
| Filtre temporel | dur | souple |
| Sources de référence | Légifrance, Judilibre, BOFiP, EUR-Lex, matsne.gov.ge | Europe PMC, OpenAlex, Crossref (rétractations), vos livres |

`pharmaco_medical` : méta-analyse > essai randomisé > observationnel > cas > animal / in vitro >
avis d'expert, avis d'agences ; affirmations sensibles (dose, toxicité, interactions).
`mycologie` : bases taxonomiques et sociétés mycologiques > guides > forums ; espèces
confondables obligatoires ; jamais de conseil de comestibilité.

### 4.3 Étiquettes

Communes (thème, profil, langue, source, niveau de source, nature, dates, validité, référence
d'unité, section, **page**) et spécifiques au profil ; utilisées comme **filtres** et comme
**facteurs** de hiérarchisation.

### 4.4 Graphe typé

Entités résolues (alias, noms scientifiques, FR/EN) ; relations par **familles** — normative,
causale, épistémique, structurelle — avec provenance, niveau de preuve et validité ; graphe des
**affirmations** (*confirme / contredit*) pour qualifier les conflits ; mobilisé pour les
questions à plusieurs sauts (convention → article → décision ; mécanisme → comportement →
tactique).

### 4.5 Le temps

Versions conservées (lignées, `valid_from` / `valid_to`) ; **date de référence** de chaque
question ; filtre dur ou souple selon le profil ; **veille** selon la volatilité ; conflits
qualifiés (*évolution / désaccord / incertitude*) ; marquage « à revérifier ». Deux éditions
d'un livre = deux versions.

### 4.6 Schéma de données (SQLite)

`themes`, `theme_aliases`, `documents` (source, juridiction, dates, validité, statut, lignée,
version, volatilité, vérifications, crédibilité), `pages` (page du fichier, page imprimée,
méthode natif / OCR, qualité, alertes), `figures`, `document_themes`, `chunks` (référence
d'unité, étiquettes, niveau de preuve, réplication, population, effet, validité, marquages),
`chunks_fts`, `embeddings`, `entities`, `entity_aliases`, `relations`, `claims`, `cards`,
`queries`, `jobs` (avec **modèle et adaptateur requis**, pour l'ordonnancement par phase),
`cycles`, `llm_calls`, **`examples`** (entrée, sortie, tâche, statut de validation : or /
argent / rejeté, source de la validation), **`specialists`** (tâche, base, adaptateur, version,
métriques, statut : candidat / promu / retiré), `review_decisions`, `research_runs`, **`questions`**
(vos questions réelles et votre note), `gaps`, `user_profiles`, tables d'évaluation.

---

## 5. Pile technique

### 5.1 Inférence (un modèle à la fois)

```bash
# Exemples ; le gestionnaire de modèles (§3.1) les charge l'un après l'autre.
llama-server -hf bartowski/MiMo-V2.6-Distill-Qwen-9B-GGUF:Q4_K_M \
  --jinja --reasoning-format deepseek -ngl 99 -c 65536 -np 4          # généraliste + vision
llama-server -m <base-specialistes>.gguf --lora planif.gguf,selection.gguf,etiquetage.gguf \
  --jinja -ngl 99 -c 32768 -np 4                                       # base + adaptateurs
llama-server -hf ggml-org/GLM-OCR-GGUF --temp 0.1                      # OCR (si pas MinerU/Docling)
llama-server -hf gpustack/bge-m3-GGUF:Q8_0 --embedding --pooling cls -ngl 0      # CPU
llama-server -hf gpustack/bge-reranker-v2-m3-GGUF:Q8_0 --reranking -ngl 0        # CPU
```

- MiMo : architecture Qwen3.5 (attention majoritairement linéaire), réflexion activable par
  requête (`chat_template_kwargs.enable_thinking`), échantillonnage `0.6 / 0.95 / 20`, module de
  vision dans le dépôt GGUF — tout cela **à vérifier en S01–S03**.
- Base des spécialistes : famille **Qwen3.5** (0,8B, 2B, 4B) ou MiMo 9B, selon le profil
  matériel ; même famille que MiMo, ce qui facilite la distillation.

### 5.2 Profils de modèles

```yaml
models:
  mimo-9b:   {serve: mimo, slots: 4, vision: true}
  rag-base:  {serve: base-specialistes, slots: 4,
              adapters: {planif: 0, selection: 1, dossier: 2, etiquetage: 3, tri: 4}}
  qwen38:    {serve: qwen38-27b, slots: 1, adapters: {recherche: 0}}   # option
  ocr:       {serve: glm-ocr, slots: 2}
tasks:                    # par tâche : qui la fait aujourd'hui, et le spécialiste visé
  passage_verification: {current: mimo-9b, specialist: rag-base/etiquetage, status: candidat}
  research_plan:        {current: mimo-9b, specialist: rag-base/planif,     status: absent}
```

Le statut d'une tâche (`absent` → `candidat` → `promu`) est mis à jour par l'usine à
spécialistes (§8) ; le code lit ce statut pour savoir quel modèle et quel adaptateur appeler.

### 5.3 Stockage

SQLite (WAL) ; FTS5 (`unicode61 remove_diacritics 2`) ; vecteurs float16 + recherche exacte
numpy par sous-arbre (interface `VectorStore` → LanceDB / Qdrant au-delà de ~300 000 extraits) ;
graphe en tables, ou **LightRAG** si S01 le retient ; exports GraphML / JSON.

### 5.4 Lecture des documents

- **Outil retenu en S01** : MinerU ou Docling (EdA §15), ou modèle OCR spécialisé servi par
  `llama-server` (EdA §13). Dans tous les cas, sortie Markdown page par page.
- Texte natif d'abord ; OCR pour les pages scannées ou à couche texte dégradée ; **MiMo en
  vision** pour les figures et l'arbitrage des passages douteux (seulement ce qui est visible,
  sinon `[illisible]`) ; contrôles automatiques ; second moteur sur échantillon.
- **Structure des livres** : table des matières, chapitres, notes, pagination imprimée,
  métadonnées (auteur, titre, édition, année, ISBN).
- **Import de bibliothèque** : dossiers surveillés ; Zotero et Calibre si leurs données locales
  le permettent (à vérifier en S01) ; métadonnées reprises.

### 5.5 Collecte

API ouvertes d'abord, sans service local (Wikipédia, Europe PMC, OpenAlex, Crossref, Légifrance /
Judilibre avec clé gratuite, BOFiP, EUR-Lex, matsne.gov.ge, MycoBank) ; **SearxNG optionnel**,
démarré seulement pendant la phase P0 ; récupérateur poli (`robots.txt`, limites, cache) ;
collectes ciblées issues des lacunes des questions.

---

## 6. Construire : le pipeline

| # | Étape | Phase | Prompts | Ce qu'elle produit |
|---|---|---|---|---|
| E0 | Charte et profil | P4 (enseignant) ou P2 | C01, C02 | charte, profil, requêtes |
| E1 | Découverte | P0 + P2 | C02, C03 | candidats triés avant téléchargement |
| E2 | Récupération et lecture | P0 + P1 + P2 | L01–L03 | texte page par page, figures, structure, métadonnées |
| E3 | Pré-contrôles | P0 | — | rejets motivés sans LLM |
| E4 | Vérification documentaire | P2 (+ P4 second avis) | C04, C05 | scores, crédibilité, rattachement, décision |
| E5 | Datation et versions | P0 + P2 | C07 | dates, validité, lignées |
| E6 | Découpage par profil | P0 | — | unités naturelles (article, section, chapitre) |
| E7 | Vérification et étiquetage des extraits | P2 | C06 | garder, nature, niveau de preuve, population, effet, affirmations |
| E8 | Enrichissement | P2 | C08 | contexte, questions, mots-clés, entités, relations typées |
| E9 | Indexation | P3 | — | embeddings, FTS5, index des étiquettes et des dates |
| E10 | Graphe | P2 | C09 | entités résolues, relations normalisées, communautés |
| E11 | Croisement et conflits | P4 | C10 | affirmations croisées, conflits qualifiés |
| E12 | Fiches | P4 | C11, C12 | fiches d'entités et de nœuds, citations contrôlées |
| E13 | Couverture | P4 | C13 | lacunes, requêtes, continuer / arrêter |
| E14 | Veille | P0 + P2 | C14 | nouvelles versions, abrogations, rétractations |

**Vérification (E4, E7)** : grilles ancrées ; **décision calculée par le code**
(`score = 0,45·pertinence + 0,30·fiabilité + 0,25·qualité` + niveau de source, règles dures,
seuils 0,70 / 0,45, second avis entre les deux) ; crédibilité multicritère, poids calibrés sur
données en S17 (EdA §12) ; réplication et rétractations tirées de sources explicites ; jeu de
référence annoté couvrant les quatre profils ; revue humaine dont les décisions deviennent des
**exemples or**.

---

## 7. Répondre : l'agent de recherche

### 7.1 Les étapes

| # | Étape | Prompt / adaptateur | Ce qui se passe |
|---|---|---|---|
| R1 | Situation | Q01 / *planif* | acteurs, objectif, juridictions, **date de référence**, ambiguïtés, hypothèses, angle détecté |
| R2 | Angle | — | validation du plan > `--focus` > formulation > profil utilisateur > défaut |
| R3 | Plan | Q02 / *planif* | sous-questions typées, thèmes (lus sur la carte), filtres, **poids**, dépendances, **contre-point**, budget |
| R4 | Premier coup | — | sous-questions en parallèle ; recherche avec la question entière + la sous-question, re-classement par sous-question (EdA §1, §11) |
| R5 | Approfondissement | — | effort selon le rendement (EdA §12) ; escalade extrait → section → document → graphe → fiches ; 2 tours maximum |
| R6 | Contrôles | Q03 / *selection* | fidélité, applicabilité, version en vigueur, adéquation de la source, conflits |
| R7 | Hiérarchisation | — | `importance = P × S × A × F × R` |
| R8 | Dossier et réponse | Q04 / *dossier*, Q06 | dossier classé et étiqueté, lacunes → collectes ciblées ; réponse citée |

Ambiguïté forte : question posée (mode `demander`) ou hypothèse annoncée (mode `supposer`) ;
`--show-plan` / `--validate-plan` pour voir et corriger le plan.

### 7.2 Format du plan (exemple, cas A)

```json
{
  "date_reference": "2026-10-06",
  "situation": {"acteurs": ["résident fiscal français", "société à créer en Géorgie"],
                "objectif": "réduire légalement l'imposition",
                "hypotheses": ["l'utilisateur reste domicilié en France"], "ambiguites": []},
  "angle": {"source": "defaut", "focus": null},
  "sous_questions": [
    {"id": "SQ1", "question": "Quels régimes d'imposition des sociétés existent en Géorgie, à quelles conditions ?",
     "themes": ["droit/fiscalite/georgie"], "filtres": {"juridiction": "GE", "nature": ["loi", "doctrine_administrative"]},
     "poids": 3, "depend_de": []},
    {"id": "SQ2", "question": "Un résident français reste-t-il imposable en France sur une société étrangère qu'il contrôle ?",
     "themes": ["droit/fiscalite/france"], "filtres": {"juridiction": "FR"}, "poids": 3, "depend_de": []},
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

### 7.3 Contrôles, hiérarchisation, dossier

- **Contrôles** : filtre temporel du profil ; fidélité de chaque preuve ; identifiants vérifiés
  par le code ; adéquation de la source ; conflits qualifiés, jamais lissés.
- **Hiérarchisation** : `P` poids de la sous-question (ajusté par l'angle) · `S` solidité
  (échelle du profil, réplication, crédibilité) · `A` applicabilité à la situation · `F`
  fraîcheur (0 si non en vigueur sous filtre dur) · `R` pertinence du re-classement ; poids
  réglables, calibrés en S17.
- **Dossier** : par sous-question, preuves `[S#]` avec étiquettes (nature, solidité, juridiction,
  version, **page**), conflits, contre-point, **lacunes** ; Markdown compact et JSON ; budget
  par modèle.

### 7.4 Angle et profil utilisateur

`profils_utilisateurs/<nom>.yaml` : vision en clair, thèmes privilégiés et poids, contre-point
actif ou non, mode ambiguïté. L'angle **reconstruit le plan** (tronc + ponts vers l'action) sans
toucher aux échelles de solidité ; il oriente aussi la **collecte** et l'**entraînement** (les
thèmes privilégiés fournissent plus d'exemples).

### 7.5 Interfaces

- **Proxy compatible OpenAI** : choisit le mode de §3.3 selon le modèle chargé, injecte le
  dossier et la consigne Q06, relaie la réponse ; contournement `#norag`.
- **Outils MCP** : `rag_research` (haut niveau) et outils de bas niveau (`rag_carte`,
  `rag_chercher`, `rag_lire`, `rag_voisins`, `rag_fiche`, `rag_conflits`), schémas compacts.
- `ragc ask "…" [--focus] [--date] [--mode] [--show-plan] [--validate-plan]`, API HTTP, exports.
- **Journal de vos questions** : chaque question est enregistrée ; une note de 1 à 5 et une
  correction éventuelle (`ragc rate`, ou dans le proxy) en font des **exemples or** pour les
  spécialistes de l'agent.

---

## 8. Apprendre : l'usine à spécialistes

### 8.1 Quelles tâches, dans quel ordre

Priorité = **volume** × **facilité à vérifier** × **gain de vitesse**.

| Ordre | Tâche | Prompt de référence | Base visée | Vérification des exemples |
|---|---|---|---|---|
| 1 | Tri des résultats de recherche | C03 | 0,8B | vos décisions, accord de l'enseignant |
| 2 | Étiquetage des extraits | C06 | 2B | revue, accord enseignant ×2, contrôles |
| 3 | Enrichissement (contexte, questions, entités, relations) | C08 | 2B–4B | relations retrouvées dans le texte, accord enseignant ; EdA §14 (extraction de relations) |
| 4 | Vérification documentaire | C04 | 4B | vos décisions, second avis |
| 5 | Sélection des preuves et fidélité | Q03 | 4B | extraits attendus, contrôle de fidélité |
| 6 | Situation et plan | Q01–Q02 | 4B–9B | sous-questions attendues des cas, vos notes ; supervision **avec raisonnement** (EdA §14) ; renforcement ensuite |
| 7 | Dossier et rédaction | Q04, Q06 | 4B–9B | citations valides, vos notes |
| option | Adaptateur « recherche » sur Qwen3.8 | Q01–Q04 | Qwen3.8-27B | idem 5–7 ; si l'entraînement est faisable (§3.4) |

L'OCR n'est pas entraîné : on utilise un outil ou un modèle déjà spécialisé (EdA §13).

### 8.2 Données

- **Capture** dès S03 : chaque appel LLM produit un exemple (entrée rendue, sortie validée par
  le schéma) dans `examples`, avec la tâche et le prompt@version.
- **Statuts** : **or** (validé par vous ou par un contrôle déterministe : version, citation,
  identifiant) ; **argent** (accord de deux passes de l'enseignant, ou enseignant + contrôles) ;
  **rejeté**. Seuls or et argent servent à l'entraînement.
- **Enseignant** : le meilleur modèle disponible **en lot la nuit** (Qwen3.8-27B, ou MiMo avec
  réflexion), choisi en S01 sur mesures.
- **Séparation** : jeu d'entraînement / validation / **test tenu à l'écart**, découpé **par
  thème et par document** (pas de fuite entre jeux) ; les questions des cas de référence et
  d'évaluation ne servent jamais à l'entraînement.

### 8.3 Entraînement, service, promotion

- **Entraînement** (phase P5) : LoRA en 16 bits (le 4 bits est déconseillé pour cette famille,
  EdA §14) ; déchargement de couches si la VRAM manque ; outil selon la machine (Unsloth / TRL
  sur CUDA, MLX sur Mac — à vérifier en S01) ; **même modèle de chat et même jeton de fin** à
  l'entraînement et à l'usage.
- **Consignes courtes** : un spécialiste entraîné reçoit une consigne réduite (le format est
  appris), d'où un prompt plus court et une réponse plus rapide.
- **Service** : export de l'adaptateur en GGUF, ajout à la liste `--lora` du modèle de base,
  sélection par requête.
- **Porte de promotion** : sur le test tenu à l'écart, le candidat doit égaler l'enseignant à une
  tolérance près sur la métrique de sa tâche **et** être plus rapide ; sinon il reste candidat.
  Un spécialiste promu est **rétrogradé** automatiquement si vos corrections montrent une baisse.
- **Renforcement** (planification, sélection) : après le premier entraînement supervisé, GRPO
  avec récompense vérifiable composée (couverture des sous-questions attendues, bonne version,
  extraits attendus, fidélité, coût en tokens), formes de récompense comparées (EdA §7).
- **Boucle continue** : réentraînement quand assez de nouveaux exemples or et argent se sont
  accumulés.

### 8.4 Réalisme

Au démarrage, aucun spécialiste n'existe : le système travaille avec MiMo et l'enseignant, plus
lentement. Les premiers spécialistes (tri, étiquetage) peuvent apparaître dès que quelques
milliers d'exemples sont accumulés, par exemple après l'ingestion de quelques livres. Les
spécialistes de l'agent demandent **vos vraies questions** et vos notes : ils viennent en
dernier.

---

## 9. Les prompts

### 9.1 Conventions

YAML par prompt (`id`, `version`, `reflexion`, `temperature`, `max_tokens`, `systeme`,
`utilisateur`, `schema`) ; gabarits `${variable}` ; consignes en français, clés JSON en anglais ;
contenu externe entre `<document>` ; grilles ancrées ; `null` plutôt qu'inventer ; surcharges par
profil puis par thème ; version incrémentée à chaque modification. Chaque prompt a une **variante
courte** pour le spécialiste qui le remplace.

### 9.2 Catalogue

| Famille | ID | Rôle |
|---|---|---|
| Lecture | L01 `ocr_page` · L02 `figure_description` · L03 `ocr_arbitration` | OCR (modèle ou outil) ; description de figures et arbitrage visuel (MiMo) |
| Construction | C01 `theme_charter` · C02 `search_queries` · C03 `search_triage` · C04 `doc_verification` · C05 `doc_second_opinion` · C06 `passage_verification` · C07 `doc_digest` · C08 `chunk_enrichment` · C09 `entity_arbitration` · C10 `conflict_qualification` · C11 `entity_card` · C12 `node_card` · C13 `coverage_analysis` · C14 `update_check` | voir §6 |
| Réponse | Q01 `situation_analysis` · Q02 `research_plan` · Q03 `evidence_selection` · Q04 `evidence_dossier` · Q05 `research_agent_tools` · Q06 `consumer_answer` · Q07 `consumer_agent` | voir §7 |
| Évaluation | V01 `eval_questions` · V02 `eval_judge` | jeu d'évaluation ; juge (contrôles déterministes d'abord) |

---

## 10. Qualité, tests, évaluation

- **Hors ligne** par défaut (faux serveurs OpenAI, OCR, vision ; fixtures fictives) ;
  `pytest --live` en conditions réelles.
- **Cas de référence A–E** ; **journal de vos vraies questions** (objectif : 50 questions notées) ;
  jeux de référence (vérification, étiquetage, entités, pages OCR) ; **tests tenus à l'écart par
  spécialiste**.
- Contrôles **déterministes** d'abord (versions, identifiants, articles, valeurs), juge LLM
  ensuite (EdA §3).
- Métriques : qualité du plan, Recall@k, MRR, bonne version, fidélité, étiquetage, angle,
  abstention, latence, **bascules de modèle**, tokens ; évaluation des trajectoires ; gain avec /
  sans RAG.

---

## 11. Budget de performance (indicatif, à mesurer en S01)

| Activité | Estimation |
|---|---|
| Bascule de modèle | quelques secondes (9B) à ~15 s (27B) depuis un SSD rapide |
| Nuit de construction | ≈ 1 000 pages (vérification, étiquetage, enrichissement) avec MiMo ; plus avec les spécialistes |
| Livre scanné de 300 pages | ≤ 1 h d'OCR + descriptions de figures |
| Question simple | < 300 ms (embeddings et re-classement sur CPU : à mesurer) |
| Question complexe | ≈ 20 à 60 s avec MiMo ; objectif ≤ 30 s avec les spécialistes |
| Entraînement d'un spécialiste | de quelques heures (0,8B–4B) à une nuit ou plus (9B, 27B avec déchargement) |

---

## 12. Risques et parades

| Risque | Parade |
|---|---|
| Bascules de modèles trop fréquentes | Travail groupé par modèle puis par adaptateur ; aucune bascule pendant une question |
| Spécialiste médiocre faute de bonnes données | Statuts or / argent, contrôles déterministes, porte de promotion, rétrogradation |
| Spécialiste qui perd ses connaissances générales | Spécialistes étroits ; raisonnement inclus dans la supervision des tâches de raisonnement (EdA §14) |
| Fuite entre entraînement et évaluation | Découpage par thème et par document ; cas de référence jamais utilisés pour entraîner |
| Écart de modèle de chat entre entraînement et usage | Même gabarit et même jeton de fin ; test de non-régression après export |
| Entraînement impossible sur la machine | Spécialistes plus petits, déchargement de couches, nuits plus longues ; à défaut, prompts |
| Plan à côté de la plaque | Analyse explicite, ambiguïtés exposées, plan visible et corrigeable, cas de référence |
| Version périmée présentée comme actuelle | Filtre dur, lignées, veille, contrôle déterministe |
| Complaisance envers l'angle | Solidité non négociable, contre-point (EdA §11) |
| Citations infidèles | Contrôle de fidélité, identifiants vérifiés (EdA §8) |
| OCR qui réécrit ou invente | Outil ou modèle OCR spécialisé, contrôles, second moteur, `[illisible]` (EdA §13) |
| Références inventées (y compris dans des documents fournis) | Toute référence vérifiée à la source (EdA §12) |
| Injection de prompt | Balises, consigne, détection, décision par le code |
| Accès aux sources officielles | Connecteurs optionnels, documentés |
| Droits d'auteur (livres, articles) | Usage personnel et local, source citée, pas de redistribution |

---

## 13. Plan de réalisation

17 sessions, dans `003_prompts_sessions/` :

| Jalon | Sessions | Résultat visible |
|---|---|---|
| **J0 — Décisions techniques** | S01 | Outils retenus, profil matériel de votre machine, mesures de base |
| **J1 — Base locale lue, vérifiée, datée** | S02 → S08 | Votre bibliothèque (livres scannés compris) lue, vérifiée, étiquetée, datée, indexée ; exemples capturés dès le début |
| **J2 — Un RAG qui raisonne** | S09 | `ragc ask --show-plan` : plan, dossier hiérarchisé, angle (cas B, C, E) |
| **J3 — Utilisable au quotidien** | S10 | Nuits séquentielles automatiques + Open WebUI / LM Studio via le proxy + journal des questions |
| **J4 — Spécialistes** | S11, S12 | Usine à spécialistes ; premiers spécialistes promus ; spécialistes de l'agent ; option adaptateur Qwen3.8 |
| **J5 — Web et connaissance reliée et à jour** | S13 → S16 | Connecteurs officiels, graphe, veille, carte et fiches (cas A, D) |
| **J6 — Évaluation globale** | S17 | Cibles mesurées, modes comparés, réglages calibrés |
