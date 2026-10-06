# 000 — État de l'art (publications d'octobre 2025 à octobre 2026)

> v0.1 · 2026-10-06 · Sert de base à la révision de `001_but.md` et `002_strategie.md`.

## Méthode et limites

- Recherche ciblée sur arXiv et le web, **uniquement des travaux de moins d'un an**, autour de
  10 questions : planification de la recherche, RAG agentique, temps et versions, structure
  navigable, graphes, découpage, petits modèles agents, citations, contraintes des modèles
  locaux, embeddings.
- 39 publications retenues (dont 5 sur l'OCR, §13, et 2 sur les petits modèles spécialisés,
  §14), des documentations techniques (§14) et des outils existants (§15), plus 9 références
  fournies par l'utilisateur et vérifiées (§12).
  **J'ai lu leurs résumés, pas les articles complets.** Les chiffres
  cités viennent des résumés ; la plupart sont des prépublications non relues par des pairs,
  évaluées sur leurs propres jeux de test. Ce sont des indications fortes, pas des garanties :
  nos propres mesures (bancs sur les PC, évaluation en S16) trancheront.
- Les travaux plus anciens (RAPTOR, HippoRAG 2, Search-R1, Contextual Retrieval, bge-m3,
  Qwen3-Embedding…) n'apparaissent que comme points de comparaison.

---

## 1. Planifier avant de chercher

**Constat.** Les meilleurs systèmes de « recherche approfondie » (*deep research*)
transforment d'abord la question en un **plan explicite**, puis l'exécutent.

- **DecomposeR** (mai 2026) représente le plan comme un **graphe orienté de sous-tâches
  typées** et sépare la planification de l'exécution. Un modèle de 8B gagne 5,1 à 8,0 points
  sur les tests de réponses longues.
  [arXiv:2605.30824](https://arxiv.org/abs/2605.30824)
- **Question's Gambit** (sept. 2026) montre que **le premier coup compte**. Décomposer la
  question en indices, lancer des recherches complémentaires, consolider et re-classer *avant*
  d'itérer fait passer la précision de 83,1 % à 90,5 %.
  [arXiv:2609.14412](https://arxiv.org/abs/2609.14412)

**Pour nous.** C'est exactement votre intuition. L'agent commence par construire un plan :
sous-questions × juridiction × nature de source × période. Ce plan est visible et contrôlable
avant toute recherche.

## 2. Agentique, oui, mais pas partout

- **Is Agentic RAG worth it?** (janv.–avr. 2026) compare un pipeline « amélioré » et un pipeline
  agentique :
  - l'agent est **meilleur pour orienter la question** (domaines de niche) et pour la
    **reformuler** (+2,8 nDCG@10 en moyenne) ;
  - il est **moins bon pour trier les documents** qu'un re-classement classique
    (43,9 contre 49,5 nDCG@10). Les agents se remettent rarement en cause : 53 % des documents
    re-cherchés sont identiques aux premiers ;
  - il **coûte 2,7 à 3,6 fois plus de tokens** et 1,5 fois plus de temps.

  Recommandation des auteurs : un **hybride** où l'agent oriente et reformule, et où un moteur
  classique avec re-classement trie les documents.
  [arXiv:2601.07711](https://arxiv.org/abs/2601.07711)
- **Conformité réglementaire, du RAG naïf au RAG agentique profond** (juin 2026) propose
  l'*escalade progressive* : commencer par une recherche peu coûteuse et précise, et ne lire
  des documents entiers que si le gain attendu le justifie. Selon les auteurs, pour des corpus
  réglementaires volumineux et changeants, **bien organiser le contexte est plus rentable que
  ré-entraîner un modèle**.
  [arXiv:2607.24791](https://arxiv.org/abs/2607.24791)

**Pour nous.** L'agent planifie, oriente et reformule. La recherche hybride et le re-classement
restent un moteur classique, solide et peu coûteux. La lecture s'élargit progressivement :
extrait, puis section, puis document entier.

## 3. Le temps est une contrainte dure (votre « vérificateur d'actualisation »)

- **FiscalQA Pro — droit fiscal français** (août 2026). Corpus de 32 436 versions d'articles,
  de 1938 à 2031 :
  - un RAG statique sur le droit actuel **ne retrouve jamais (0 %) la version applicable** et
    n'atteint que 2,7 % de bonnes réponses ;
  - un RAG sur un **index multi-versions** atteint 98,3 % ;
  - les auteurs déconseillent de faire juger la validité temporelle par un LLM, qui hérite des
    mêmes biais : ils évaluent avec des « pépites » déterministes (valeurs, numéros d'articles).

  [arXiv:2608.09393](https://arxiv.org/abs/2608.09393)
- **Asking For An Old Friend** (mai 2026) identifie deux pannes : des règles périmées appliquées
  après une réforme, et un biais pour le texte le plus récent même quand l'ancien s'applique.
  Parade efficace : **extraire la date des faits de la question et filtrer les textes en
  vigueur à cette date**. La recherche web seule donne des gains instables.
  [arXiv:2605.23497](https://arxiv.org/abs/2605.23497)
- **LegalSearch-R1** (mai 2026) : un modèle de 7B entraîné par renforcement, qui combine une base
  locale de textes de loi et le web, avec des données indexées par période d'amendement. Il gagne
  12,9 à 29,8 % sur les références, et 57,7 à 80,3 % sur la cohérence temporelle.
  [arXiv:2605.25920](https://arxiv.org/abs/2605.25920)
- **TimelyRAG** (sept. 2026) intègre la distance temporelle dans le classement des documents.
  Le gain va jusqu'à +28,6 % nDCG@10 sur des textes réglementaires qui se recouvrent et évoluent.
  [arXiv:2609.11572](https://arxiv.org/abs/2609.11572)
- **VersionRAG** (oct. 2025) : un RAG standard plafonne à 58 % sur des documents versionnés.
  [arXiv:2510.08109](https://arxiv.org/abs/2510.08109)
- **EvoTrustRAG** (août 2026) distingue trois causes de contradiction entre sources : **le
  savoir a évolué**, **manipulation**, **incertitude réelle**. Il atteint 81,4 % de bonnes
  attributions et divise par deux les erreurs sous attaque (de 31,2 % à 16,0 %).
  [arXiv:2608.07933](https://arxiv.org/abs/2608.07933)

**Pour nous.**
- Chaque information porte une **période de validité**. On **garde les versions** au lieu
  d'écraser.
- Chaque question a une **date de référence** (aujourd'hui par défaut), qui sert de filtre dur.
- Une **veille d'actualisation** revérifie les sources selon leur volatilité.
- Une contradiction est qualifiée : « a changé », « se contredit » ou « incertain ».

## 4. Une structure que l'agent peut parcourir

- **Corpus2Skill** (avr.–août 2026) compile le corpus en une **arborescence hiérarchique
  navigable**. L'agent descend de la vue d'ensemble vers les documents, et revient en arrière
  quand une branche ne donne rien. Il bat les RAG denses, hybrides, hiérarchiques et agentiques
  sur un corpus d'entreprise, mais **échoue sur des corpus fourre-tout** sans taxonomie, où la
  recherche à plat reste préférable.
  [arXiv:2604.14572](https://arxiv.org/abs/2604.14572)
- **Knowledge-as-Skill** (sept. 2026) organise le corpus en trois couches : une page
  d'entrée, un index par dossier, et des documents munis de métadonnées (sujet, type,
  provenance, cycle de vie). La factualité passe de 0,767 à 0,889 et le rappel de contexte de
  0,708 à 0,816. En contrepartie, la précision est un peu plus faible et l'agent fait plus
  d'allers-retours. Les auteurs précisent que la comparaison n'est pas contrôlée.
  [arXiv:2609.25991](https://arxiv.org/abs/2609.25991)
- **A-RAG** (févr. 2026) donne au modèle des outils à plusieurs niveaux de détail : recherche
  par mots-clés, recherche sémantique, lecture d'un passage. Il fait mieux avec autant de tokens
  ou moins, et progresse avec la taille du modèle.
  [arXiv:2602.03442](https://arxiv.org/abs/2602.03442)
- **Ψ-RAG** (mai 2026) construit un arbre de résumés qui traverse les documents. Il gagne
  25,9 % de F1 sur RAPTOR et 7,4 % sur HippoRAG 2 pour les questions à plusieurs sauts.
  [arXiv:2605.00529](https://arxiv.org/abs/2605.00529)

**Pour nous.** L'arbre des thèmes ne sert plus seulement à ranger : il devient une **carte que
l'agent parcourt**. Chaque nœud a son résumé, son index et ses métadonnées. La recherche à plat
continue en parallèle pour les questions simples.

## 5. Le graphe : utile pour relier, pas pour tout

- **Do We Still Need GraphRAG?** (avr. 2026) : avec un agent, l'écart entre RAG dense et
  GraphRAG se réduit fortement. Le graphe reste **avantageux pour le raisonnement à plusieurs
  sauts** (A est lié à B, qui est lié à C), et plus stable quand son coût de construction est
  amorti.
  [arXiv:2604.09666](https://arxiv.org/abs/2604.09666)
- **RAGA** (mai 2026) : un agent construit le graphe en boucle **lire → chercher → vérifier →
  construire**, et chaque entrée est ancrée sur son texte source.
  [arXiv:2605.17072](https://arxiv.org/abs/2605.17072)
- **ArbGraph** (avr. 2026) découpe les documents en affirmations élémentaires reliées par des
  arêtes « confirme » et « contredit », puis arbitre **avant** de rédiger. Résultat : meilleur
  rappel des faits et moins d'hallucinations.
  [arXiv:2604.18362](https://arxiv.org/abs/2604.18362)

**Pour nous.** Le graphe porte des **relations typées** : *modifie, abroge, applique, interprète,
cite, confirme, contredit*. C'est lui qui relie « loi française ↔ convention fiscale ↔ loi
géorgienne ↔ jurisprudence ». On le mobilise pour les questions à plusieurs sauts et pour
détecter les contradictions, pas pour chaque recherche.

## 6. Découper selon la structure, et selon le domaine

- **Étude systématique du découpage** (mars 2026) : 36 méthodes, 6 domaines, 5 modèles
  d'embedding.
  - Le regroupement de paragraphes l'emporte (nDCG@5 ≈ 0,459), loin devant le découpage fixe
    en caractères (< 0,244).
  - La taille dynamique est meilleure en biologie et en santé ; le regroupement de paragraphes
    en **droit** et en mathématiques.
  - Un meilleur modèle d'embedding ne compense pas un mauvais découpage.

  [arXiv:2603.06976](https://arxiv.org/abs/2603.06976)

**Pour nous.** Le découpage dépend du domaine : en droit, **un article de loi = une unité**, avec
son numéro, son code et sa version. En pharmacologie, on suit les sections de l'article
scientifique.

## 7. Spécialiser un petit modèle pour chercher : crédible

- **LegalSearch-R1, 7B** (§3) et **DecomposeR, 8B** (§1) : de petits modèles entraînés par
  renforcement dépassent des systèmes plus gros sur leur tâche.
- **Apprentissage par renforcement sur récompense vérifiable pour petits agents de recherche**
  (sept. 2026). Qwen3.5-0.8B, entraîné avec un outil de recherche Wikipédia, multiplie son
  score par 3,8 (de 0,092 à 0,352), sans distillation. **La forme de la récompense est
  décisive** : récompenser seulement la réponse exacte donne le pire résultat.
  [arXiv:2609.28765](https://arxiv.org/abs/2609.28765)
- **AgentIR** (mars 2026) indexe la question **avec le raisonnement de l'agent**. Avec 4B, il
  atteint 68 %, contre 50 % pour un embedding classique deux fois plus gros et 37 % pour BM25.
  [arXiv:2603.04384](https://arxiv.org/abs/2603.04384)
- **Tongyi DeepResearch** (oct. 2025) est un agent de recherche ouvert (30B dont 3B actifs),
  proche d'o3 sur BrowseComp (43,4 contre 49,7).
  [arXiv:2510.24701](https://arxiv.org/abs/2510.24701)

**Pour nous.** La piste « MiMo agent de recherche » est confirmée. Notre RAG peut produire des
récompenses vérifiables : bon article trouvé, bonne version, citations valides, coût en tokens.
Il faut soigner la forme de la récompense. Tongyi DeepResearch est un concurrent à comparer.

## 8. Citations : toujours vérifier

- **Cited but Not Verified** (mai 2026) : les liens cités fonctionnent dans plus de 94 % des cas
  et sont pertinents dans plus de 80 %, mais **les faits attribués ne sont exacts que dans 39 à
  77 % des cas**. Et **chercher davantage dégrade** l'exactitude des citations (−42 % quand les
  appels d'outils se multiplient).
  [arXiv:2605.06635](https://arxiv.org/abs/2605.06635)
- **Verified Misguidance** (mai 2026) : **30,6 % des citations déforment leur source**, et 27,1 %
  viennent d'une source inadaptée au domaine.
  [arXiv:2605.28565](https://arxiv.org/abs/2605.28565)

**Pour nous.** Chaque citation est contrôlée : lien, pertinence, **fidélité** (l'extrait dit-il
vraiment cela ?) et **adéquation de la source** (une question fiscale exige des sources
juridiques officielles). Le nombre d'étapes de recherche est plafonné.

## 9. Modèles locaux : le contexte est une ressource rare

- **Compression des schémas d'outils** (mai 2026), sur 14 modèles locaux de 1,5B à 32B. Avec
  8 000 tokens de contexte, des définitions d'outils JSON standard font tomber le score à
  2,6 %. Compressées (44 à 50 % de tokens en moins), elles regagnent +20,5 points. À 32 000
  tokens, la différence devient négligeable.
  [arXiv:2605.26165](https://arxiv.org/abs/2605.26165)

**Pour nous.** Peu d'outils, décrits de façon compacte. Des réponses d'outils plafonnées en
tokens. Un budget de contexte fixé par modèle.

## 10. Taxonomie et évaluation des RAG agentiques

- **SoK Agentic RAG** (mars 2026) classe les systèmes selon quatre axes : planification,
  orchestration de la recherche, mémoire, appel d'outils. Il recommande d'évaluer **les
  trajectoires** de l'agent, pas seulement la réponse, et signale des risques : propagation
  d'hallucinations, empoisonnement de la mémoire, échecs en cascade.
  [arXiv:2603.07379](https://arxiv.org/abs/2603.07379)
- **Benchmarking Legal RAG** (2026), sur une recherche législative multi-juridictions : un
  système spécialisé atteint 83 %, contre 58 à 64 % pour des outils commerciaux. Les erreurs
  restantes sont des confusions entre notions voisines, des exceptions mal lues, et des textes
  non retrouvés.
  [arXiv:2603.03300](https://arxiv.org/abs/2603.03300)
- **Embeddings et re-classement** : plusieurs modèles multilingues récents sont à comparer à
  bge-m3 et bge-reranker-v2-m3 (Granite Embedding Multilingual R2, Qwen3-VL-Embedding et
  Reranker, LAMAR). Je ne les ai pas étudiés en détail : à mesurer en S16.
  [arXiv:2605.13521](https://arxiv.org/abs/2605.13521) ·
  [arXiv:2601.04720](https://arxiv.org/abs/2601.04720) ·
  [arXiv:2607.22042](https://arxiv.org/abs/2607.22042)

## 11. Hiérarchiser selon l'angle de l'utilisateur, sans complaisance

- **CoRM-RAG** (mai 2026) : quand la question contient une thèse ou une prémisse biaisée,
  chercher par simple similarité ramène les documents qui la confirment et renforce les
  erreurs. Les auteurs proposent de noter les documents sur la **force de la preuve** plutôt que
  sur la ressemblance.
  [arXiv:2605.01302](https://arxiv.org/abs/2605.01302)
- **Opinion-Aware RAG** (avr.–oct. 2026) : un RAG doit représenter la diversité des positions,
  pas une réponse unique ; les évaluateurs humains préfèrent ces réponses dans 79,2 % des cas.
  [arXiv:2604.12138](https://arxiv.org/abs/2604.12138)
- **Personalize Before Retrieve** (oct. 2025, AAAI 2026) : adapter l'élargissement de la
  requête au profil de l'utilisateur donne jusqu'à +10 %.
  [arXiv:2510.08935](https://arxiv.org/abs/2510.08935)
- **Quand décomposer ?** (juin 2026, EMNLP 2026) : découper la requête **dès la première
  recherche** dilue son sens ; découper **au moment du re-classement** améliore la vérification
  fine des conditions.
  [arXiv:2606.08577](https://arxiv.org/abs/2606.08577)
- **Évaluation automatique de la reproductibilité en sciences comportementales** (juin 2026) :
  un LLM retrouve les conclusions d'une étude dans 80 % des cas, mais la taille de l'effet dans
  seulement 24 %. C'est un outil de **tri**, pas un juge de fiabilité.
  [arXiv:2606.13670](https://arxiv.org/abs/2606.13670)
- **Dominance des connaissances internes** (avr. 2026) : face à une contradiction, une API
  commerciale testée passe outre les preuves fournies dans près de la moitié des cas ; les
  petits modèles s'y tiennent mieux.
  [arXiv:2606.23695](https://arxiv.org/abs/2606.23695)

**Pour nous.** Deux réglages séparés :
- la **priorité** (l'angle, par exemple « neurosciences d'abord ») est fixée par l'utilisateur ;
- la **solidité** (niveau de preuve, statut de réplication) est fixée par les preuves.

Le plan contient toujours une sous-question « contre-point », que l'utilisateur peut désactiver.
Le statut de réplication vient de sources explicites (méta-analyses, projets de réplication),
pas de l'avis du modèle.

## 12. Références apportées par l'utilisateur (vérifiées le 2026-10-06)

Chaque référence a été vérifiée sur arXiv. Toutes existent, mais 4 ont plus d'un an et
plusieurs mentions de la bibliographie d'origine étaient inexactes :

| Référence | Date | < 1 an | Vérification |
|---|---|---|---|
| Query Decomposition for RAG: Balancing Exploration-Exploitation (Petcu et al.) [arXiv:2510.18633](https://arxiv.org/abs/2510.18633) | oct. 2025 | oui | Confirmé : +35 % de précision par document, +15 % α-nDCG |
| HERA, Experience as a Compass [arXiv:2604.00901](https://arxiv.org/abs/2604.00901) | avr. 2026 | oui | Confirmé : +38,69 % en moyenne sur 6 jeux de test |
| CausalRAG2 (aussi intitulé HugRAG) [arXiv:2602.05143](https://arxiv.org/abs/2602.05143) | févr. 2026, ICML 2026 | oui | Existe. **L'apport annoncé (« préséance des lois cognition/biologie sur les variables tactiques ») ne figure pas dans l'article.** Apport réel : graphe causal hiérarchique avec « portes causales » qui écartent les corrélations trompeuses ; F1 36,45 % contre 26,87 % pour un RAG standard sur HolisQA-Biology |
| ConflictRAG [arXiv:2605.17301](https://arxiv.org/abs/2605.17301) | mai 2026, IEEE SMC 2026 | oui | Confirmé (Entropy-TOPSIS). Il manque un auteur (Yueyuan Li) dans la liste d'origine |
| Ψ-RAG [arXiv:2605.00529](https://arxiv.org/abs/2605.00529) | mai 2026, ICML 2026 | oui | Confirmé (déjà en §4) |
| MA-RAG [arXiv:2505.20096](https://arxiv.org/abs/2505.20096) | mai 2025 | **non** | Existe ; arXiv seulement |
| CausalRAG [arXiv:2503.19878](https://arxiv.org/abs/2503.19878) | mars 2025, ACL 2025 Findings | **non** | **Auteurs erronés** dans la bibliographie : il s'agit de Nengbo Wang, Xiaotian Han, Jagdip Singh, Jing Ma et Vipin Chaudhary |
| MADAM-RAG [arXiv:2504.13079](https://arxiv.org/abs/2504.13079) | avr. 2025, COLM 2025 | **non** | Premier auteur : **Han** Wang (et non Hao) |
| HiRAG [arXiv:2503.10150](https://arxiv.org/abs/2503.10150) | mars 2025, EMNLP 2025 Findings | **non** | Confirmé |

**Ce que ces travaux apportent en plus :**

- **Relations causales dans le graphe** (CausalRAG2). On distingue « A cause / favorise / inhibe /
  médie B » de « A est associé à B ». La chaîne **mécanisme biologique → effet comportemental →
  tactique** devient explicite, avec un niveau de preuve sur chaque maillon. C'est ce qui permet
  de suivre sérieusement un angle « neurosciences d'abord ».
- **Crédibilité multicritère pilotée par les données** (ConflictRAG) :
  - Entropy-TOPSIS fait 7,1 % mieux que des pondérations réglées à la main. Nos poids de la
    vérification documentaire (`002_strategie.md` §5.3) pourront être calibrés ainsi ;
  - la détection en deux temps (un classifieur léger, puis le LLM seulement si nécessaire)
    réduit le coût de 62 % pour 90,8 % de détection : c'est bien adapté au calcul local.
- **Allouer l'effort entre sous-questions** (Petcu et al.) : le planificateur n'explore pas
  toutes les sous-questions de la même façon. Il insiste sur celles qui rapportent des documents
  pertinents et abandonne les stériles.
- **Apprendre de l'expérience** (HERA) : la forme des plans et les prompts s'améliorent à partir
  des réussites passées. C'est une piste pour une v2, complémentaire de l'entraînement de MiMo
  (§7).
- **Séparation des rôles** (MA-RAG, plus ancien) : planificateur, définition des étapes,
  extracteur, rédacteur. Cela confirme notre découpage : MiMo planifie et extrait, Qwen3.8 rédige.
- **Débat entre agents** (MADAM-RAG, plus ancien) : efficace sur les preuves contradictoires,
  mais coûteux en local. On en garde une version légère : le second avis.

## 13. Lire les PDF scannés et les images (OCR)

- **Classement des modèles OCR libres** (août 2026, synthèse de bancs d'essai publics) :
  - sur OmniDocBench v1.6, les trois premiers sont de **petits modèles spécialisés de 0,9 à
    1,2 milliard de paramètres** : PaddleOCR-VL-1.6 (96,34 %), MinerU2.5-Pro (95,75 %) et
    GLM-OCR (95,22 %). Ils devancent un modèle généraliste de 235 milliards (Qwen3-VL-235B,
    89,78 %) ;
  - sur olmOCR-Bench, en tête : Chandra OCR 2 (85,8 %) et dots.mocr (83,9 %).

  Ce sont des chiffres d'un article de blog, à confirmer par le banc (S01, S05).
  [roboflow.com](https://roboflow.com/blog/best-open-source-ocr-models)
- **llama.cpp prend en charge ces modèles OCR** (avr. 2026) : LightOnOCR, Qianfan-OCR,
  PaddleOCR-VL, GLM-OCR, DeepSeek-OCR, Dots.OCR, HunyuanOCR. On les sert avec `llama-server`
  (modèle + `--mmproj`) et on leur envoie les images au format OpenAI. Recommandations :
  température basse (0,1) et images de bonne qualité pour limiter les inventions.
  [Hugging Face — Using OCR models with llama.cpp](https://huggingface.co/blog/ggml-org/using-ocr-models-with-llama-cpp)
- **Do VLMs Read or Rewrite?** (mai 2026) : les modèles de vision **généralistes** ont tendance à
  **réécrire** un texte imparfait en une forme plus plausible au lieu de le transcrire. Ils
  perdent jusqu'à 6,9 points sous perturbation, contre 0,1 à 3,4 pour les modèles OCR
  spécialisés et moins de 0,8 pour l'OCR classique. Les mots courts (4 à 6 caractères) sont
  réécrits environ 10 % du temps.
  [arXiv:2607.21617](https://arxiv.org/abs/2607.21617)
- **Reading or Guessing?** (mai–sept. 2026) : les erreurs des modèles de vision restent
  **fluides** (texte plausible mais absent de la page) ; il ne faut pas confondre fluidité et
  fidélité.
  [arXiv:2605.27750](https://arxiv.org/abs/2605.27750)
- **When Good OCR Is Not Enough** (avr. 2026) : une bonne précision caractère par caractère ne
  garantit pas un bon RAG. Les erreurs de structure (ordre de lecture, tableaux) font échouer la
  recherche. **Il faut évaluer l'OCR par ses effets sur la recherche.**
  [arXiv:2605.00911](https://arxiv.org/abs/2605.00911)
- **Conversion PDF → Markdown de documents français** (févr. 2026) : sur 15 modèles, les modèles
  ouverts sont **compétitifs sur les mises en page imprimées classiques** ; les formulaires et
  l'écriture manuscrite restent difficiles.
  [arXiv:2602.11960](https://arxiv.org/abs/2602.11960)

**Pour nous.**
1. **Texte natif d'abord.** Si le PDF a une couche texte de bonne qualité, on l'utilise : c'est
   exact et instantané.
2. **OCR spécialisé ensuite**, pour les pages scannées : un petit modèle (PaddleOCR-VL ou
   GLM-OCR) servi par `llama-server`, à température basse.
3. **MiMo en vision pour comprendre**, pas pour transcrire : décrire les figures, schémas et
   tableaux-images pour qu'ils deviennent cherchables, et **arbitrer** les passages douteux.
4. **Vérification de l'OCR** : contrôles automatiques (mots inconnus, répétitions, ordre de
   lecture), comparaison de deux moteurs sur un échantillon de pages, et mesure de l'effet sur la
   recherche.

## 14. Petits modèles spécialisés et exécution sur une seule machine

- **Sub-Billion, Super-Frontier** (juin 2026) : des modèles de 360 millions à 3 milliards de
  paramètres, entraînés pour **une seule tâche** (extraction de relations), battent des modèles
  frontières utilisés tels quels. Le meilleur, Qwen2.5-0.5B, obtient 0,83 de F1, contre 0,69 pour
  GPT-5.4 et 0,66 pour Claude Sonnet 4.6 ; sur des textes littéraires, 0,92 contre 0,83. Les
  auteurs insistent : le gain vient **de l'adaptation à la tâche, pas d'une supériorité
  intrinsèque des petits modèles**, et il exige des données d'entraînement ciblées.
  [arXiv:2606.22606](https://arxiv.org/abs/2606.22606)
- **Lois d'échelle de la distillation spécialisée** (juin–août 2026) : en réduisant la taille,
  la qualité **dans la tâche** baisse de façon prévisible, mais les **connaissances générales
  s'effondrent bien avant**. Une supervision avec raisonnement explicite (*chain-of-thought*)
  en récupère une partie. Conséquence : un spécialiste doit rester **étroit**, et une tâche de
  raisonnement doit être enseignée avec son raisonnement.
  [arXiv:2606.24747](https://arxiv.org/abs/2606.24747)
- **Rappels** : un OCR de 0,9 milliard bat un modèle de 235 milliards (§13) ; DecomposeR-8B
  (planification, §1), LegalSearch-R1-7B (recherche juridique, §3) et un agent de 0,8 milliard
  entraîné par renforcement (§7) progressent fortement **sur leur tâche**.
- **Entraîner sur une machine personnelle** : pour la famille Qwen3.5, dont MiMo fait partie,
  une LoRA en 16 bits demande environ **3 Go de VRAM pour 0,8B, 5 Go pour 2B, 10 Go pour 4B et
  22 Go pour 9B**. Le **4 bits (QLoRA) est déconseillé** pour cette famille. Le renforcement
  (GRPO) est possible. L'export en GGUF et en adaptateur LoRA pour llama.cpp est prévu, mais
  attention au modèle de chat et au jeton de fin, qui doivent être identiques à l'entraînement
  et à l'usage.
  [Unsloth — Qwen3.5 fine-tune](https://unsloth.ai/docs/models/qwen3.5/fine-tune)
- **Ces chiffres supposent tout le modèle en VRAM.** Le **déchargement de couches** (*block
  swap* : la moitié des couches gardée en mémoire vive et ramenée dynamiquement) réduit la VRAM
  d'environ 50 % en masquant les transferts, selon les mainteneurs d'Unsloth (juin 2025). Un
  entraînement LoRA d'un modèle de 27B a été rapporté à environ 19 Go de VRAM (août 2026), et
  Unsloth annonce Gemma 3 27B sous 22 Go. Le prix à payer est la **vitesse** ; à mesurer sur la
  machine réelle.
  [discussion Unsloth #2827](https://github.com/unslothai/unsloth/discussions/2827) ·
  [guide 27B en local](https://www.mindstudio.ai/blog/fine-tune-qwen3-8-27b-locally) ·
  [exigences Unsloth](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements)
- **Plusieurs adaptateurs sur un seul modèle** : `llama-server` charge plusieurs adaptateurs
  LoRA au démarrage (`--lora`) et en choisit l'échelle **à chaque requête** (champ `lora`). Les
  requêtes qui utilisent des adaptateurs différents ne sont pas regroupées : il faut donc
  **traiter les tâches par lots, adaptateur par adaptateur**.
  [llama.cpp — LoRA par requête](https://cdn04132025.gitlink.org.cn/replica/llama.cpp/commit/0da5d860266c6928b8c9408efbd264ae59fedda6) ·
  [guide](https://www.simplified.guide/_export/xhtml/llama-cpp/server-set-lora-adapter)
- **Mode routeur de `llama-server`** : charge et décharge des modèles à la demande sans
  redémarrer ; `--models-max` limite le nombre de modèles chargés en même temps (le moins
  récemment utilisé est déchargé).
  [guide du mode routeur](https://glukhov.org/llm-hosting/llama-cpp/llama-server-router-mode/)

**Pour nous.**
- **Un seul modèle lourd en mémoire à la fois.** Le travail est organisé par **phases**, un
  modèle par phase ; les étapes sans modèle s'intercalent.
- **Une flotte de petits spécialistes** (0,8B à 4B, ou MiMo 9B si la machine le permet), un par
  tâche étroite et répétitive. Ils sont entraînés sur les données que le système produit
  lui-même, validées par vous et par des contrôles automatiques.
- Un **modèle de base + plusieurs adaptateurs LoRA**, choisis à chaque requête : un seul modèle
  en mémoire pour plusieurs rôles.
- Un spécialiste n'est **promu** que s'il fait au moins aussi bien que le modèle enseignant sur
  sa tâche, mesuré.

## 15. Outils existants à évaluer avant de construire (2026)

- **MinerU** (versions 3.x en 2026, OCR PP-OCRv6 dans son pipeline ; modèle MinerU2.5-Pro de
  1,2B parmi les meilleurs OCR) et **Docling** (IBM, modèle Granite-Docling-258M) : conversion de
  PDF, DOCX, images en Markdown ou JSON avec mise en page, tableaux et formules. Docling serait
  plus rapide sur CPU et Mac, MinerU sur GPU.
  [MinerU](https://pypi.org/project/mineru/) ·
  [MinerU2.5-Pro](https://huggingface.co/opendatalab/MinerU2.5-Pro-2604-1.2B) ·
  [comparatif](https://respan.ai/market-map/compare/docling-vs-ragflow)
- **PaperQA2** (FutureHouse) : RAG pour la littérature scientifique, avec citations dans le
  texte et détection de contradictions.
  [FutureHouse](https://futurehouse.org/news/paperqa2-achieves-sota-performance-on-rag-qa-arena-science-benchmark)
- **RAGFlow** (moteur RAG complet, analyse de documents via MinerU ou Docling) et **LightRAG**
  (RAG par graphe).
  [panorama des frameworks](https://www.olostep.com/blog/open-source-rag-frameworks)

**Pour nous.** Avant d'écrire du code, une étude « réutiliser ou construire » (S01) :
réutiliser MinerU ou Docling pour la lecture, s'inspirer de PaperQA2 pour la littérature
scientifique, et ne construire que ce qui fait notre différence (agent, profils, temps,
spécialistes, exécution séquentielle).

## 16. Machines de l'utilisateur, portabilité, domaines retenus

**Matériel et logiciels (vérifié le 2026-10-06)**
- **RTX 5090 (architecture Blackwell)** : il faut **CUDA 12.8 ou plus** et un pilote **R570 ou
  plus**. Des versions de llama.cpp compilées pour Blackwell (sm_120) existent, y compris pour
  Windows.
  [guide NVIDIA Blackwell](https://forums.developer.nvidia.com/t/software-migration-guide-for-nvidia-blackwell-rtx-gpus-a-guide-to-cuda-12-8-pytorch-tensorrt-and-llama-cpp/321330) ·
  [compilation sm_120](https://bestllmfor.com/guides/llama-cpp-cuda-blackwell-sm120-build/)
- **Unsloth** fonctionne sous **Windows** (installateur PowerShell, ou pip avec PyTorch), Linux
  et WSL. L'entraînement est pris en charge sur les RTX 30, 40 et 50 ; CUDA 12.8 ou plus est
  recommandé pour Blackwell ; Python 3.11 à 3.13.
  [exigences Unsloth](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md) ·
  [installation](https://www.unsloth.ai/docs/new/studio/install)

**Fiscalité géorgienne**
- Le **Code des impôts de Géorgie** existe en **version anglaise** sur matsne.gov.ge, le
  portail législatif officiel.
- Depuis la réforme de **2017** (« modèle estonien »), l'impôt sur les sociétés ne frappe plus
  les bénéfices conservés, mais les **distributions** et les sorties assimilées, à **15 %** en
  règle générale (chapitre XIII du Code).
- Ces points sont à confirmer sur le texte en vigueur : le Code change souvent, d'où
  l'importance de la veille.
  [matsne.gov.ge](https://matsne.gov.ge/en/document/download/1043717/99/en/pdf) ·
  [Andersen Géorgie](https://ge.andersen.com/georgian-corporate-income-tax-regime/)

**Criminologie des escroqueries**
- **The scammer's playbook** (*Journal of Economic Criminology*, 2026) : 282 récits de
  victimes d'escroqueries aux cryptomonnaies (2023–2024), codés. Les escrocs suivent un
  **« manuel » reproductible** (usurpation d'identité, persuasion, familiarité), pas de
  l'opportunisme.
  [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2949791426000060)
- **Schéma médico-légal de la manipulation psychologique dans la cyberfraude** (2026) : analyse
  de récits de victimes assistée par LLM.
  [arXiv:2607.07751](https://arxiv.org/abs/2607.07751)
- Cadres de référence du domaine : les principes de persuasion de Cialdini ; des revues
  systématiques sur la fraude sentimentale et sur la vulnérabilité des victimes (2023, 2025).
  [revue sur la fraude sentimentale](https://www.sciencedirect.com/science/article/pii/S2949791423000131) ·
  [vulnérabilité des victimes](https://www.sciencedirect.com/science/article/abs/pii/S0747563225001815)

**Collecte : navigateur plutôt qu'API**
- L'**API Brave Search** n'a plus de formule gratuite pour les nouveaux comptes depuis février
  2026 : un crédit mensuel de 5 $ (≈ 1 000 requêtes) exige une carte bancaire, puis c'est 5 $ les
  1 000 requêtes. Ses conditions d'utilisation ont été mises à jour le 11 février 2026.
  [tarifs](https://www.costbench.com/software/ai-search-apis/brave-search-api/free-plan/) ·
  [alternatives et historique](https://www.firecrawl.dev/blog/brave-search-api-alternatives) ·
  [conditions](https://api-dashboard.search.brave.com/documentation/resources/terms-of-service)
- **Piloter Brave** : Brave est basé sur Chromium ; lancé avec `--remote-debugging-port`, il
  accepte une connexion de Playwright (`connect_over_cdp`), sous Windows comme sous Linux.
  [Playwright Python](https://playwright.dev/python/docs/api/class-browsertype) ·
  [guide](https://www.browserstack.com/guide/playwright-connect-to-existing-browser)
- **Agents de navigation pilotés par un LLM** : browser-use est open source (licence MIT, environ
  108 000 étoiles, version 0.13.7 en juillet 2026) et accepte des modèles locaux. Retour
  d'expérience publié : un modèle de 8B réussit les recherches simples mais échoue sur les tâches
  à plusieurs étapes ; c'est fiable à partir d'environ 30B.
  [présentation](https://www.kunalganglani.com/blog/open-source-ai-projects-developers-2026.md) ·
  [modèles locaux](https://localaimaster.com/blog/browser-use-ollama-local)
- **Détection de l'automatisation** : la plupart des sites et des moteurs détectent les
  navigateurs pilotés (Playwright et équivalents) et les refusent. **Nous ne chercherons pas à
  masquer l'automatisation** (souris simulée, empreinte falsifiée) : ce serait contourner des
  protections, contre les conditions des sites, et finirait par des blocages.
- **Pour nous, trois voies honnêtes** :
  1. **collecte automatique là où elle est permise** : API conçues pour cela (OpenAlex, Europe PMC,
     Crossref, Wikipédia, API Brave en option), et un récupérateur poli et identifié pour les
     sites qui l'autorisent ;
  2. **collecte assistée** : l'agent prépare des listes de lecture et les ouvre dans **votre**
     Brave ; vous lisez, et ce que vous gardez est capturé (bouton « Envoyer au RAG », dossier de
     téléchargements surveillé, Zotero). Vos choix deviennent des exemples **or** pour le
     spécialiste de tri ;
  3. **vos propres documents**.

**Autres domaines demandés** : traitement des traumatismes et des phobies, hacking
(cybersécurité). Leurs sources de référence sont à brancher avec les connecteurs (S08 et suivantes) : recommandations
cliniques, Cochrane, Europe PMC pour le premier ; MITRE ATT&CK, base CVE / NVD, catalogue CISA
KEV, OWASP, arXiv cs.CR pour le second. Accès et conditions d'utilisation à vérifier.

---

## Ce que cela change pour notre projet

| # | Changement | Appuyé par |
|---|---|---|
| A | **Profils de domaine** (juridique-fiscal, pharmaco-médical, mycologie, générique). Chacun définit les étiquettes, les types de sources, les sources officielles, l'unité de découpage (l'article de loi en droit), les relations du graphe et la politique d'actualisation | §3, §6, §8 |
| B | **Corpus versionné et daté** : périodes de validité, versions conservées, date de référence de la question en filtre dur, veille d'actualisation, contradictions qualifiées (« a changé », « se contredit », « incertain ») | §3 |
| C | **Carte navigable** : chaque nœud de l'arbre a un résumé, un index et des métadonnées ; l'agent la parcourt, et la recherche à plat continue en parallèle | §4 |
| D | **Agent planificateur** : un plan explicite (graphe de sous-questions typées), un premier coup soigné (décomposer, rechercher en parallèle, consolider, re-classer), une lecture qui s'élargit progressivement, et un re-classement classique conservé | §1, §2 |
| E | **Graphe à relations typées** (modifie, abroge, applique, interprète, cite, confirme, contredit) + graphe des affirmations pour les contradictions ; mobilisé pour le raisonnement à plusieurs sauts | §5 |
| F | **Contrôle des citations** (lien, pertinence, fidélité, adéquation de la source) ; évaluation déterministe quand c'est possible (articles, versions, valeurs) | §3, §8 |
| G | **MiMo agent de recherche** : piste confirmée, avec un entraînement par récompenses vérifiables tirées de notre RAG ; comparaison avec Tongyi DeepResearch | §7 |
| H | **Contexte compact** : peu d'outils, schémas compacts, réponses plafonnées, budget par modèle | §9 |
| I | **Collecte guidée par les questions** (proposition) : les lacunes révélées par un plan de recherche déclenchent une collecte ciblée en tâche de fond | déduit de §1 et §3 |
| J | **Priorité ≠ solidité** : l'angle est fixé par l'utilisateur (question, option `--focus`, profil durable, validation du plan) ; la solidité est fixée par les preuves ; contre-point systématique | §11 |
| K | **Relations causales et chaînes « mécanisme → comportement → action »**, avec un niveau de preuve par maillon | §12 |
| L | **Crédibilité multicritère calibrée sur données** (pondération entropique) et détection des conflits en deux temps (léger, puis LLM) | §12 |
| M | **Effort réparti entre sous-questions** selon ce qu'elles rapportent (exploration / exploitation) | §12 |
| N | **Lecture de tout document** : texte natif d'abord, OCR spécialisé pour les scans (livres), MiMo en vision pour les figures et l'arbitrage, OCR vérifié et évalué par ses effets sur la recherche | §13 |
| O | **Une seule machine, en séquentiel** : un modèle lourd à la fois, travail par phases (un modèle par phase) | §14 |
| P | **Flotte de petits spécialistes** entraînés sur les données du système, un modèle de base + plusieurs adaptateurs LoRA, promotion seulement s'ils égalent l'enseignant | §14 |
| Q | **Réutiliser avant de construire** (MinerU / Docling, PaperQA2, LightRAG) | §15 |
| R | **Portabilité Windows / Linux**, cartes Blackwell (CUDA 12.8+), entraînement local sous Windows ; domaines prioritaires : escroqueries et fiscalité géorgienne | §16 |

### Votre exemple, revu à la lumière de la recherche

*« Conditions pour ne pas payer d'impôts en Géorgie si j'y crée une société »*, demandé
aujourd'hui par un résident français :

1. **Date de référence** : aujourd'hui. Seuls les textes en vigueur aujourd'hui comptent (§3).
2. **Plan** (graphe de sous-questions, §1) :
   - droit géorgien : régimes d'imposition des sociétés et leurs conditions ;
   - droit français : domicile fiscal, imposition des sociétés étrangères contrôlées, siège de
     direction effective, abus de droit ;
   - convention fiscale franco-géorgienne : qui impose quoi ;
   - jurisprudence française et géorgienne ; doctrine administrative et cas pratiques.
3. **Premier coup** : recherches parallèles, une par sous-question, avec les bonnes étiquettes
   (pays, nature du texte, en vigueur), puis consolidation et re-classement (§1, §2).
4. **Fils du graphe** : de la convention vers les articles qu'elle écarte ou applique ; de
   l'article vers les décisions qui l'interprètent (§5).
5. **Contrôle** : versions en vigueur, citations fidèles, sources officielles (§3, §8).
6. **Lacunes** : par exemple, aucune jurisprudence géorgienne dans le corpus. L'agent le dit,
   et une collecte ciblée est lancée (I).
7. **Dossier de preuves** transmis à Qwen3.8, qui rédige : conditions, risques, sources datées,
   et rappel qu'il ne s'agit pas d'un conseil fiscal.
