// Fichier généré par generer_carte.py : ne pas modifier à la main.
window.CARTE = {
 "titre": "RAG Creator — carte du programme",
 "version": "0.5",
 "moments": [
  {
   "id": "socle",
   "nom": "Socle et accès aux modèles",
   "couleur": "#64748b"
  },
  {
   "id": "construire",
   "nom": "Construire (travail en fond)",
   "couleur": "#2563eb"
  },
  {
   "id": "repondre",
   "nom": "Répondre",
   "couleur": "#16a34a"
  },
  {
   "id": "apprendre",
   "nom": "Apprendre (spécialistes)",
   "couleur": "#9333ea"
  },
  {
   "id": "evaluer",
   "nom": "Évaluer",
   "couleur": "#ea580c"
  }
 ],
 "groupes": [
  {
   "id": "pilotage",
   "nom": "Socle et pilotage",
   "moment": "socle"
  },
  {
   "id": "modeles",
   "nom": "Accès aux modèles",
   "moment": "socle"
  },
  {
   "id": "chartes",
   "nom": "Profils et chartes",
   "moment": "construire"
  },
  {
   "id": "methodo",
   "nom": "Méthodologie et technique de recherche (à vous)",
   "moment": "construire"
  },
  {
   "id": "collecte",
   "nom": "Collecte",
   "moment": "construire"
  },
  {
   "id": "lecture",
   "nom": "Ingestion et lecture",
   "moment": "construire"
  },
  {
   "id": "verification",
   "nom": "Vérification et étiquetage",
   "moment": "construire"
  },
  {
   "id": "index",
   "nom": "Enrichissement et index",
   "moment": "construire"
  },
  {
   "id": "connaissance",
   "nom": "Temps, graphe, carte",
   "moment": "construire"
  },
  {
   "id": "interfaces",
   "nom": "Interfaces",
   "moment": "repondre"
  },
  {
   "id": "agent",
   "nom": "Agent de recherche",
   "moment": "repondre"
  },
  {
   "id": "specialistes",
   "nom": "Usine à spécialistes",
   "moment": "apprendre"
  },
  {
   "id": "evaluation",
   "nom": "Évaluation",
   "moment": "evaluer"
  }
 ],
 "entrees_externes": {
  "config_file": "fichier config.yaml (vous)",
  "env_vars": "variables d'environnement RAGC_*",
  "machine": "votre PC (GPU, VRAM, RAM, système)",
  "user_command": "vos commandes : ragc start / pause / resume / stop",
  "theme_path": "chemin d'un thème, ex. « Fiscalité > Géorgie » (vous)",
  "profile_files": "profils de domaine (fichiers YAML)",
  "domaine": "nom du domaine (ex. criminologie)",
  "sujet": "sujet ou sous-question à chercher",
  "registre": "registre.yaml du module de méthodologie",
  "user_files": "vos dossiers de documents",
  "zotero_library": "votre bibliothèque Zotero ou Calibre",
  "sent_page": "page ou PDF envoyé depuis Brave (bouton « Envoyer au RAG »)",
  "user_review_decision": "vos décisions de validation (ragc review)",
  "user_question": "votre question",
  "chat_messages": "votre conversation (Open WebUI, LM Studio)",
  "focus": "votre angle (--focus, ou dans la question)",
  "user_profile": "votre profil utilisateur (vision, thèmes privilégiés)",
  "user_rating": "votre note de 1 à 5 et votre correction",
  "tool_call": "appel d'outil d'un modèle (MCP)",
  "base_model": "modèle de base des spécialistes",
  "new_base_model": "nouveau modèle de base (après un changement)",
  "sujets_banc": "liste de sujets pour le banc de mesure",
  "task": "tâche demandée par le script qui appelle un modèle",
  "task_variables": "variables fournies par le script qui appelle un modèle",
  "schema": "schéma de sortie attendu, fourni par le script qui appelle un modèle"
 },
 "parcours": [
  {
   "id": "document",
   "nom": "Vie d'un document",
   "etapes": [
    "import_library",
    "precheck",
    "diagnose_pages",
    "ocr_pages",
    "check_ocr",
    "describe_figures",
    "rebuild_structure",
    "date_and_version",
    "verify_document",
    "decide_document",
    "chunk_document",
    "label_chunks",
    "digest_document",
    "enrich_chunks",
    "index_text",
    "index_vectors"
   ]
  },
  {
   "id": "question",
   "nom": "Vie d'une question",
   "etapes": [
    "receive_question",
    "analyse_situation",
    "resolve_angle",
    "plan_research",
    "validate_plan",
    "first_move",
    "search",
    "deepen",
    "select_evidence",
    "rank_evidence",
    "build_dossier",
    "write_answer",
    "log_question"
   ]
  },
  {
   "id": "collecte",
   "nom": "Une collecte (méthodologie → documents)",
   "etapes": [
    "charger_strategie",
    "generer_requetes_strategie",
    "generate_queries",
    "charger_registre",
    "run_collectors",
    "collecteur_openalex",
    "triage_candidates",
    "build_reading_list",
    "fetch_documents",
    "precheck"
   ]
  },
  {
   "id": "specialiste",
   "nom": "Vie d'un spécialiste",
   "etapes": [
    "capture_example",
    "review_session",
    "teacher_labels",
    "build_datasets",
    "train_adapter",
    "export_adapter",
    "evaluate_specialist",
    "promote_specialist",
    "route_task"
   ]
  },
  {
   "id": "fond",
   "nom": "Le travail en fond (pilotage)",
   "etapes": [
    "control_channel",
    "schedule_jobs",
    "model_manager",
    "run_job"
   ]
  }
 ],
 "scripts": [
  {
   "id": "detect_hardware",
   "fichier": "ragcreator/hardware/detect.py",
   "groupe": "pilotage",
   "ordre": 1,
   "session": "S02",
   "role": "Détecte le matériel (système, GPU, VRAM, CUDA, RAM, disque) et écrit le profil matériel.",
   "entrees": {
    "machine": "votre PC"
   },
   "sorties": {
    "hardware_profile": "profil matériel (taille des modèles, CPU ou GPU…)"
   },
   "statut": "prevu"
  },
  {
   "id": "load_config",
   "fichier": "ragcreator/config/load_config.py",
   "groupe": "pilotage",
   "ordre": 1,
   "session": "S02",
   "role": "Lit config.yaml et les variables RAGC_*, vérifie tout, renvoie la configuration.",
   "entrees": {
    "config_file": "fichier de configuration",
    "env_vars": "surcharges RAGC_*"
   },
   "sorties": {
    "config": "configuration validée"
   },
   "statut": "prevu"
  },
  {
   "id": "control_channel",
   "fichier": "ragcreator/worker/control.py",
   "groupe": "pilotage",
   "ordre": 2,
   "session": "S02",
   "role": "Reçoit vos commandes start / pause / resume / stop (Windows et Linux) et met à jour l'état du travailleur.",
   "entrees": {
    "user_command": "votre commande"
   },
   "sorties": {
    "worker_state": "état du travail en fond (en marche, en pause, arrêté)"
   },
   "ecrit": [
    "worker_state"
   ],
   "statut": "prevu"
  },
  {
   "id": "open_database",
   "fichier": "ragcreator/db/open_db.py",
   "groupe": "pilotage",
   "ordre": 2,
   "session": "S02",
   "role": "Ouvre la base SQLite et applique les migrations.",
   "entrees": {
    "config": "configuration"
   },
   "sorties": {
    "db": "connexion à la base"
   },
   "statut": "prevu"
  },
  {
   "id": "manage_themes",
   "fichier": "ragcreator/themes/tree.py",
   "groupe": "pilotage",
   "ordre": 3,
   "session": "S02",
   "role": "Crée et retrouve les thèmes (arbre) et leurs dossiers sur disque.",
   "entrees": {
    "theme_path": "chemin du thème",
    "db": "base"
   },
   "sorties": {
    "theme_id": "identifiant du thème"
   },
   "ecrit": [
    "themes",
    "theme_aliases"
   ],
   "statut": "prevu"
  },
  {
   "id": "schedule_jobs",
   "fichier": "ragcreator/worker/scheduler.py",
   "groupe": "pilotage",
   "ordre": 3,
   "session": "S02",
   "role": "Choisit la prochaine tâche, en groupant par modèle puis par adaptateur, selon les priorités et l'état (pause).",
   "entrees": {
    "jobs": "file des tâches",
    "worker_state": "état du travailleur"
   },
   "sorties": {
    "next_job": "tâche suivante",
    "model_request": "modèle et adaptateur nécessaires"
   },
   "lit": [
    "jobs"
   ],
   "statut": "prevu"
  },
  {
   "id": "model_manager",
   "fichier": "ragcreator/models/manager.py",
   "groupe": "pilotage",
   "ordre": 4,
   "session": "S02",
   "role": "Charge et décharge les modèles : un seul modèle lourd à la fois ; libère la carte graphique en pause.",
   "entrees": {
    "model_request": "modèle demandé",
    "hardware_profile": "profil matériel",
    "config": "configuration"
   },
   "sorties": {
    "model_endpoint": "adresse du modèle chargé (llama-server)"
   },
   "statut": "prevu"
  },
  {
   "id": "route_task",
   "fichier": "ragcreator/llm/task_router.py",
   "groupe": "modeles",
   "ordre": 4,
   "session": "S03",
   "role": "Pour une tâche, choisit qui la fait : spécialiste promu (adaptateur) ou généraliste avec prompt complet.",
   "entrees": {
    "task": "tâche demandée (ex. passage_verification)",
    "specialists_registry": "registre des spécialistes"
   },
   "sorties": {
    "model_request": "modèle et adaptateur",
    "prompt_variant": "prompt complet ou variante courte"
   },
   "statut": "prevu"
  },
  {
   "id": "call_llm",
   "fichier": "ragcreator/llm/client.py",
   "groupe": "modeles",
   "ordre": 5,
   "session": "S03",
   "role": "Appelle le modèle (réflexion on/off, adaptateur LoRA par requête, images, outils), avec reprises.",
   "entrees": {
    "messages": "messages",
    "model_endpoint": "modèle chargé",
    "model_request": "adaptateur"
   },
   "sorties": {
    "raw_completion": "réponse brute du modèle"
   },
   "ecrit": [
    "llm_calls"
   ],
   "statut": "prevu"
  },
  {
   "id": "render_prompt",
   "fichier": "ragcreator/prompts/render.py",
   "groupe": "modeles",
   "ordre": 5,
   "session": "S03",
   "role": "Construit les messages à partir du prompt YAML (surcharges profil puis thème) et des variables.",
   "entrees": {
    "prompt_variant": "prompt choisi",
    "task_variables": "variables de la tâche"
   },
   "sorties": {
    "messages": "messages pour le modèle"
   },
   "statut": "prevu"
  },
  {
   "id": "run_job",
   "fichier": "ragcreator/worker/run_job.py",
   "groupe": "pilotage",
   "ordre": 5,
   "session": "S02",
   "role": "Exécute une tâche (appelle le bon script), valide le résultat en base, gère reprise et erreurs.",
   "entrees": {
    "next_job": "tâche",
    "model_endpoint": "modèle chargé"
   },
   "sorties": {
    "jobs": "file des tâches mise à jour"
   },
   "ecrit": [
    "jobs"
   ],
   "statut": "prevu"
  },
  {
   "id": "capture_example",
   "fichier": "ragcreator/learning/capture.py",
   "groupe": "modeles",
   "ordre": 6,
   "session": "S03",
   "role": "Enregistre chaque appel comme exemple d'entraînement neutre (sans gabarit de modèle).",
   "entrees": {
    "task": "tâche",
    "task_variables": "entrée",
    "validated_output": "sortie"
   },
   "sorties": {
    "example": "exemple (statut « brut »)"
   },
   "ecrit": [
    "examples"
   ],
   "statut": "prevu"
  },
  {
   "id": "embed_texts",
   "fichier": "ragcreator/llm/embed.py",
   "groupe": "modeles",
   "ordre": 6,
   "session": "S03",
   "role": "Calcule les vecteurs (embeddings) de textes, sur CPU ou GPU.",
   "entrees": {
    "texts": "textes"
   },
   "sorties": {
    "vectors": "vecteurs"
   },
   "statut": "prevu"
  },
  {
   "id": "rerank",
   "fichier": "ragcreator/llm/rerank.py",
   "groupe": "modeles",
   "ordre": 6,
   "session": "S03",
   "role": "Re-classe des extraits selon une question ou une sous-question.",
   "entrees": {
    "rerank_query": "question de re-classement",
    "candidate_chunks": "extraits candidats"
   },
   "sorties": {
    "rerank_scores": "scores de pertinence"
   },
   "statut": "prevu"
  },
  {
   "id": "validate_output",
   "fichier": "ragcreator/llm/structured.py",
   "groupe": "modeles",
   "ordre": 6,
   "session": "S03",
   "role": "Vérifie que la réponse respecte le schéma JSON ; demande une réparation sinon.",
   "entrees": {
    "raw_completion": "réponse brute",
    "schema": "schéma attendu"
   },
   "sorties": {
    "validated_output": "réponse validée"
   },
   "statut": "prevu"
  },
  {
   "id": "load_profiles",
   "fichier": "ragcreator/profiles/load.py",
   "groupe": "chartes",
   "ordre": 7,
   "session": "S04",
   "role": "Charge et valide les profils de domaine (étiquettes, solidité, découpage, actualisation, cadrage).",
   "entrees": {
    "profile_files": "profils YAML"
   },
   "sorties": {
    "domain_profiles": "profils de domaine"
   },
   "statut": "prevu"
  },
  {
   "id": "charger_strategie",
   "fichier": "methodologie_recherche/strategies.py",
   "groupe": "methodo",
   "ordre": 8,
   "session": "S08",
   "role": "Charge la méthodologie d'un domaine (YAML) et la fusionne avec la méthodologie commune.",
   "entrees": {
    "domaine": "nom du domaine"
   },
   "sorties": {
    "strategie": "méthodologie du domaine"
   },
   "statut": "prevu"
  },
  {
   "id": "write_charter",
   "fichier": "ragcreator/themes/charter.py",
   "groupe": "chartes",
   "ordre": 8,
   "session": "S04",
   "role": "Rédige la charte d'un thème et choisit son profil de domaine.",
   "entrees": {
    "theme_id": "thème",
    "domain_profiles": "profils"
   },
   "sorties": {
    "charter": "charte du thème"
   },
   "ecrit": [
    "themes"
   ],
   "modele": {
    "tache": "theme_charter",
    "prompt": "C01"
   },
   "statut": "prevu"
  },
  {
   "id": "charger_registre",
   "fichier": "methodologie_recherche/registre.py",
   "groupe": "methodo",
   "ordre": 9,
   "session": "S08",
   "role": "Charge les techniques actives du registre et vérifie qu'elles respectent le contrat.",
   "entrees": {
    "registre": "registre.yaml"
   },
   "sorties": {
    "collecteurs": "techniques actives"
   },
   "statut": "prevu"
  },
  {
   "id": "generate_queries",
   "fichier": "ragcreator/themes/queries.py",
   "groupe": "chartes",
   "ordre": 9,
   "session": "S04",
   "role": "Produit les requêtes de recherche à partir de la charte, de la stratégie du domaine et des lacunes.",
   "entrees": {
    "charter": "charte",
    "requetes_strategie": "formulations de la méthodologie",
    "gaps": "lacunes"
   },
   "sorties": {
    "queries": "requêtes"
   },
   "ecrit": [
    "queries"
   ],
   "modele": {
    "tache": "search_queries",
    "prompt": "C02"
   },
   "statut": "prevu"
  },
  {
   "id": "generer_requetes_strategie",
   "fichier": "methodologie_recherche/requetes.py",
   "groupe": "methodo",
   "ordre": 9,
   "session": "S08",
   "role": "Applique les gabarits de requêtes de la méthodologie à un sujet, dans chaque langue.",
   "entrees": {
    "strategie": "méthodologie",
    "sujet": "sujet"
   },
   "sorties": {
    "requetes_strategie": "formulations de requêtes"
   },
   "statut": "prevu"
  },
  {
   "id": "collecteur_dossier_local",
   "fichier": "methodologie_recherche/collecteurs/dossier_local.py",
   "groupe": "methodo",
   "ordre": 10,
   "session": "S08",
   "role": "Technique locale : vos documents déposés dans des dossiers.",
   "entrees": {
    "requete": "une requête"
   },
   "sorties": {
    "candidats": "candidats trouvés",
    "document_collecte": "contenu récupéré"
   },
   "statut": "prevu"
  },
  {
   "id": "collecteur_liste_lecture",
   "fichier": "methodologie_recherche/collecteurs/liste_lecture.py",
   "groupe": "methodo",
   "ordre": 10,
   "session": "S08",
   "role": "Technique assistée : prépare des recherches et des liens que VOUS ouvrez dans votre navigateur.",
   "entrees": {
    "requete": "une requête"
   },
   "sorties": {
    "candidats": "liens de recherche à ouvrir"
   },
   "statut": "prevu"
  },
  {
   "id": "collecteur_openalex",
   "fichier": "methodologie_recherche/collecteurs/api_openalex.py",
   "groupe": "methodo",
   "ordre": 10,
   "session": "S08",
   "role": "Technique automatique : publications scientifiques via l'API OpenAlex.",
   "entrees": {
    "requete": "une requête"
   },
   "sorties": {
    "candidats": "candidats trouvés",
    "document_collecte": "PDF en accès libre"
   },
   "statut": "prevu"
  },
  {
   "id": "collecteur_wikipedia",
   "fichier": "methodologie_recherche/collecteurs/wikipedia.py",
   "groupe": "methodo",
   "ordre": 10,
   "session": "S08",
   "role": "Technique automatique : articles de Wikipédia via son API.",
   "entrees": {
    "requete": "une requête"
   },
   "sorties": {
    "candidats": "candidats trouvés",
    "document_collecte": "contenu de l'article"
   },
   "statut": "prevu"
  },
  {
   "id": "banc_collecte",
   "fichier": "methodologie_recherche/bancs/banc_collecte.py",
   "groupe": "methodo",
   "ordre": 11,
   "session": "S08",
   "role": "Mesure vos techniques et stratégies : rendement, doublons, refus, temps ; précision sur échantillon étiqueté.",
   "entrees": {
    "strategie": "méthodologie",
    "collecteurs": "techniques",
    "sujets_banc": "sujets de test"
   },
   "sorties": {
    "rapport_banc": "rapport de mesure"
   },
   "statut": "prevu"
  },
  {
   "id": "run_collectors",
   "fichier": "ragcreator/sources/run_collection.py",
   "groupe": "collecte",
   "ordre": 11,
   "session": "S08",
   "role": "Exécute les techniques actives sur les requêtes, avec leur politesse ; bascule vers la collecte assistée en cas de refus.",
   "entrees": {
    "queries": "requêtes",
    "collecteurs": "techniques",
    "candidats": "réponses des techniques"
   },
   "sorties": {
    "requete": "requête passée à une technique",
    "candidates": "candidats regroupés et dédoublonnés"
   },
   "statut": "prevu"
  },
  {
   "id": "import_library",
   "fichier": "ragcreator/ingest/library.py",
   "groupe": "collecte",
   "ordre": 12,
   "session": "S05",
   "role": "Importe vos dossiers et votre bibliothèque Zotero / Calibre, avec leurs métadonnées.",
   "entrees": {
    "user_files": "vos dossiers",
    "zotero_library": "Zotero / Calibre"
   },
   "sorties": {
    "raw_documents": "documents bruts"
   },
   "ecrit": [
    "documents"
   ],
   "statut": "prevu"
  },
  {
   "id": "triage_candidates",
   "fichier": "ragcreator/sources/triage.py",
   "groupe": "collecte",
   "ordre": 12,
   "session": "S08",
   "role": "Trie les candidats (titre, extrait) avant tout téléchargement, selon la charte et la méthodologie.",
   "entrees": {
    "candidates": "candidats",
    "charter": "charte",
    "strategie": "critères de tri"
   },
   "sorties": {
    "kept_candidates": "candidats retenus"
   },
   "modele": {
    "tache": "search_triage",
    "prompt": "C03"
   },
   "statut": "prevu"
  },
  {
   "id": "browser_inbox",
   "fichier": "ragcreator/sources/browser_inbox.py",
   "groupe": "collecte",
   "ordre": 13,
   "session": "S08",
   "role": "Reçoit ce que vous envoyez depuis Brave (extension « Envoyer au RAG »).",
   "entrees": {
    "sent_page": "page ou PDF envoyé"
   },
   "sorties": {
    "raw_documents": "documents bruts"
   },
   "ecrit": [
    "documents"
   ],
   "statut": "prevu"
  },
  {
   "id": "build_reading_list",
   "fichier": "ragcreator/sources/reading_list.py",
   "groupe": "collecte",
   "ordre": 13,
   "session": "S08",
   "role": "Prépare les listes de lecture (collecte assistée) et les ouvre dans votre Brave quand vous le décidez.",
   "entrees": {
    "kept_candidates": "candidats retenus",
    "gaps": "lacunes"
   },
   "sorties": {
    "reading_list": "liste de lecture (page HTML)"
   },
   "statut": "prevu"
  },
  {
   "id": "fetch_documents",
   "fichier": "ragcreator/ingest/fetch.py",
   "groupe": "collecte",
   "ordre": 13,
   "session": "S08",
   "role": "Récupère les documents retenus, poliment (robots.txt, limites, cache).",
   "entrees": {
    "kept_candidates": "candidats retenus",
    "document_collecte": "contenu fourni par une technique"
   },
   "sorties": {
    "raw_documents": "documents bruts"
   },
   "ecrit": [
    "documents"
   ],
   "statut": "prevu"
  },
  {
   "id": "precheck",
   "fichier": "ragcreator/ingest/precheck.py",
   "groupe": "lecture",
   "ordre": 14,
   "session": "S05",
   "role": "Écarte sans modèle ce qui ne mérite pas d'être lu : doublons, pages vides, langue, bruit.",
   "entrees": {
    "raw_documents": "documents bruts"
   },
   "sorties": {
    "documents": "documents admis",
    "rejections": "rejets motivés"
   },
   "ecrit": [
    "documents"
   ],
   "statut": "prevu"
  },
  {
   "id": "diagnose_pages",
   "fichier": "ragcreator/reader/diagnose.py",
   "groupe": "lecture",
   "ordre": 15,
   "session": "S05",
   "role": "Examine chaque page : couche texte bonne, dégradée ou absente ; figures, tableaux.",
   "entrees": {
    "documents": "documents"
   },
   "sorties": {
    "pages": "pages et leur diagnostic"
   },
   "ecrit": [
    "pages"
   ],
   "statut": "prevu"
  },
  {
   "id": "extract_native_text",
   "fichier": "ragcreator/reader/native.py",
   "groupe": "lecture",
   "ordre": 16,
   "session": "S05",
   "role": "Extrait le texte natif des pages dont la couche texte est bonne.",
   "entrees": {
    "pages": "pages"
   },
   "sorties": {
    "page_texts": "texte des pages"
   },
   "statut": "prevu"
  },
  {
   "id": "ocr_pages",
   "fichier": "ragcreator/reader/ocr.py",
   "groupe": "lecture",
   "ordre": 16,
   "session": "S05",
   "role": "Lit par OCR les pages scannées (outil ou modèle OCR spécialisé, phase P1).",
   "entrees": {
    "pages": "pages à lire"
   },
   "sorties": {
    "page_texts": "texte des pages"
   },
   "modele": {
    "tache": "ocr_page",
    "prompt": "L01"
   },
   "statut": "prevu"
  },
  {
   "id": "arbitrate_ocr",
   "fichier": "ragcreator/reader/arbitrate.py",
   "groupe": "lecture",
   "ordre": 17,
   "session": "S05",
   "role": "MiMo regarde l'image et tranche les passages douteux : seulement le visible, sinon [illisible].",
   "entrees": {
    "ocr_alerts": "pages douteuses",
    "pages": "images des pages"
   },
   "sorties": {
    "page_texts": "texte corrigé"
   },
   "modele": {
    "tache": "ocr_arbitration",
    "prompt": "L03"
   },
   "statut": "prevu"
  },
  {
   "id": "check_ocr",
   "fichier": "ragcreator/reader/ocr_checks.py",
   "groupe": "lecture",
   "ordre": 17,
   "session": "S05",
   "role": "Contrôle l'OCR : mots inconnus, répétitions, ordre de lecture, tableaux ; second moteur sur échantillon.",
   "entrees": {
    "page_texts": "texte des pages"
   },
   "sorties": {
    "ocr_alerts": "pages douteuses"
   },
   "ecrit": [
    "pages"
   ],
   "statut": "prevu"
  },
  {
   "id": "describe_figures",
   "fichier": "ragcreator/reader/figures.py",
   "groupe": "lecture",
   "ordre": 17,
   "session": "S05",
   "role": "MiMo décrit les figures, schémas et graphiques pour qu'ils deviennent cherchables.",
   "entrees": {
    "pages": "pages avec figures"
   },
   "sorties": {
    "figure_descriptions": "descriptions de figures"
   },
   "ecrit": [
    "figures"
   ],
   "modele": {
    "tache": "figure_description",
    "prompt": "L02"
   },
   "statut": "prevu"
  },
  {
   "id": "rebuild_structure",
   "fichier": "ragcreator/reader/structure.py",
   "groupe": "lecture",
   "ordre": 18,
   "session": "S05",
   "role": "Retrouve la structure (chapitres, sections, notes, pagination imprimée) et les métadonnées du livre.",
   "entrees": {
    "page_texts": "texte des pages",
    "figure_descriptions": "figures"
   },
   "sorties": {
    "sections": "sections du document",
    "book_metadata": "auteur, titre, édition, ISBN"
   },
   "statut": "prevu"
  },
  {
   "id": "date_and_version",
   "fichier": "ragcreator/temporal/dating.py",
   "groupe": "lecture",
   "ordre": 19,
   "session": "S05",
   "role": "Date le document et ses versions (déterministe) : validité, lignée, références d'articles.",
   "entrees": {
    "documents": "documents",
    "book_metadata": "métadonnées"
   },
   "sorties": {
    "validity": "périodes de validité",
    "lineage": "lignée de versions"
   },
   "ecrit": [
    "documents"
   ],
   "statut": "prevu"
  },
  {
   "id": "verify_document",
   "fichier": "ragcreator/verify/document.py",
   "groupe": "verification",
   "ordre": 19,
   "session": "S06",
   "role": "Note pertinence, fiabilité et qualité du document ; repère biais, alertes et le bon thème.",
   "entrees": {
    "documents": "document",
    "sections": "échantillon",
    "charter": "charte"
   },
   "sorties": {
    "verification_scores": "notes et alertes"
   },
   "modele": {
    "tache": "doc_verification",
    "prompt": "C04"
   },
   "statut": "prevu"
  },
  {
   "id": "decide_document",
   "fichier": "ragcreator/verify/decide.py",
   "groupe": "verification",
   "ordre": 20,
   "session": "S06",
   "role": "Calcule la décision (accepter, rejeter, second avis) avec des règles réglables.",
   "entrees": {
    "verification_scores": "notes"
   },
   "sorties": {
    "document_decision": "décision"
   },
   "ecrit": [
    "documents"
   ],
   "statut": "prevu"
  },
  {
   "id": "second_opinion",
   "fichier": "ragcreator/verify/second_opinion.py",
   "groupe": "verification",
   "ordre": 20,
   "session": "S06",
   "role": "L'enseignant relit les cas limites (phase P4).",
   "entrees": {
    "document_decision": "décision à confirmer"
   },
   "sorties": {
    "document_decision": "décision confirmée ou infirmée"
   },
   "modele": {
    "tache": "doc_second_opinion",
    "prompt": "C05"
   },
   "statut": "prevu"
  },
  {
   "id": "chunk_document",
   "fichier": "ragcreator/ingest/chunker.py",
   "groupe": "verification",
   "ordre": 21,
   "session": "S05",
   "role": "Découpe selon l'unité naturelle du domaine (article de loi, section, chapitre, bloc de code).",
   "entrees": {
    "sections": "sections",
    "domain_profiles": "profils",
    "document_decision": "documents acceptés"
   },
   "sorties": {
    "chunks": "extraits"
   },
   "ecrit": [
    "chunks"
   ],
   "statut": "prevu"
  },
  {
   "id": "digest_document",
   "fichier": "ragcreator/enrich/digest.py",
   "groupe": "index",
   "ordre": 21,
   "session": "S07",
   "role": "Résume le document et complète ses dates (le déterministe prime).",
   "entrees": {
    "sections": "sections"
   },
   "sorties": {
    "digest": "résumé, plan, portée",
    "validity": "dates complétées"
   },
   "modele": {
    "tache": "doc_digest",
    "prompt": "C07"
   },
   "statut": "prevu"
  },
  {
   "id": "label_chunks",
   "fichier": "ragcreator/verify/label_chunks.py",
   "groupe": "verification",
   "ordre": 22,
   "session": "S06",
   "role": "Garde ou écarte chaque extrait et l'étiquette (niveau de preuve, population, effet, affirmations sensibles).",
   "entrees": {
    "chunks": "extraits"
   },
   "sorties": {
    "chunk_labels": "étiquettes",
    "claims": "affirmations sensibles"
   },
   "ecrit": [
    "chunks",
    "claims"
   ],
   "modele": {
    "tache": "passage_verification",
    "prompt": "C06"
   },
   "statut": "prevu"
  },
  {
   "id": "enrich_chunks",
   "fichier": "ragcreator/enrich/chunks.py",
   "groupe": "index",
   "ordre": 23,
   "session": "S07",
   "role": "Ajoute à chaque extrait son contexte, ses questions, ses mots-clés, ses entités et relations typées.",
   "entrees": {
    "chunks": "extraits",
    "digest": "résumé du document"
   },
   "sorties": {
    "chunk_context": "contexte",
    "chunk_questions": "questions",
    "raw_relations": "entités et relations brutes"
   },
   "modele": {
    "tache": "chunk_enrichment",
    "prompt": "C08"
   },
   "statut": "prevu"
  },
  {
   "id": "review_session",
   "fichier": "ragcreator/verify/review.py",
   "groupe": "verification",
   "ordre": 23,
   "session": "S06",
   "role": "Routine de validation au clavier : vos décisions deviennent des exemples « or ».",
   "entrees": {
    "chunk_labels": "étiquettes à valider",
    "document_decision": "décisions à valider",
    "user_review_decision": "vos décisions"
   },
   "sorties": {
    "gold_examples": "exemples or"
   },
   "ecrit": [
    "examples",
    "review_decisions"
   ],
   "statut": "prevu"
  },
  {
   "id": "index_text",
   "fichier": "ragcreator/index/fts.py",
   "groupe": "index",
   "ordre": 24,
   "session": "S07",
   "role": "Indexe le texte (BM25, FTS5) avec ses étiquettes et ses dates.",
   "entrees": {
    "chunks": "extraits",
    "chunk_context": "contexte",
    "chunk_questions": "questions",
    "chunk_labels": "étiquettes"
   },
   "sorties": {
    "fts_index": "index lexical"
   },
   "ecrit": [
    "chunks_fts"
   ],
   "statut": "prevu"
  },
  {
   "id": "index_vectors",
   "fichier": "ragcreator/index/vectors.py",
   "groupe": "index",
   "ordre": 24,
   "session": "S07",
   "role": "Calcule et stocke les vecteurs des extraits et de leurs questions (phase P3).",
   "entrees": {
    "chunks": "extraits",
    "chunk_context": "contexte",
    "chunk_questions": "questions",
    "vectors": "vecteurs calculés"
   },
   "sorties": {
    "vector_index": "index vectoriel",
    "texts": "textes à vectoriser"
   },
   "ecrit": [
    "embeddings"
   ],
   "appelle": [
    "embed_texts"
   ],
   "statut": "prevu"
  },
  {
   "id": "resolve_entities",
   "fichier": "ragcreator/graph/resolve.py",
   "groupe": "connaissance",
   "ordre": 25,
   "session": "S14",
   "role": "Fusionne les entités (alias, noms scientifiques, articles, CVE) et normalise les relations.",
   "entrees": {
    "raw_relations": "relations brutes"
   },
   "sorties": {
    "graph": "graphe typé"
   },
   "ecrit": [
    "entities",
    "relations"
   ],
   "modele": {
    "tache": "entity_arbitration",
    "prompt": "C09"
   },
   "statut": "prevu"
  },
  {
   "id": "watch_sources",
   "fichier": "ragcreator/temporal/watch.py",
   "groupe": "connaissance",
   "ordre": 25,
   "session": "S13",
   "role": "Revérifie les sources selon leur volatilité ; crée une nouvelle version si le texte a vraiment changé.",
   "entrees": {
    "documents": "documents",
    "validity": "validité"
   },
   "sorties": {
    "raw_documents": "nouvelle version à traiter",
    "lineage": "lignée mise à jour"
   },
   "modele": {
    "tache": "update_check",
    "prompt": "C14"
   },
   "statut": "prevu"
  },
  {
   "id": "qualify_conflicts",
   "fichier": "ragcreator/graph/conflicts.py",
   "groupe": "connaissance",
   "ordre": 26,
   "session": "S14",
   "role": "Croise les affirmations sensibles : concordant, contradictoire, nuancé ; évolution, désaccord, incertitude.",
   "entrees": {
    "claims": "affirmations",
    "graph": "graphe",
    "validity": "versions et dates"
   },
   "sorties": {
    "conflicts": "conflits qualifiés"
   },
   "modele": {
    "tache": "conflict_qualification",
    "prompt": "C10"
   },
   "statut": "prevu"
  },
  {
   "id": "write_entity_cards",
   "fichier": "ragcreator/synth/entity_cards.py",
   "groupe": "connaissance",
   "ordre": 27,
   "session": "S15",
   "role": "Rédige les fiches d'entités, chaque phrase citée.",
   "entrees": {
    "graph": "graphe",
    "conflicts": "conflits"
   },
   "sorties": {
    "entity_cards": "fiches"
   },
   "ecrit": [
    "cards"
   ],
   "modele": {
    "tache": "entity_card",
    "prompt": "C11"
   },
   "statut": "prevu"
  },
  {
   "id": "write_node_cards",
   "fichier": "ragcreator/synth/node_cards.py",
   "groupe": "connaissance",
   "ordre": 27,
   "session": "S15",
   "role": "Rédige la fiche de chaque nœud de l'arbre : la carte que l'agent parcourt.",
   "entrees": {
    "graph": "graphe",
    "chunks": "extraits",
    "charter": "chartes"
   },
   "sorties": {
    "knowledge_map": "carte des thèmes"
   },
   "ecrit": [
    "cards"
   ],
   "modele": {
    "tache": "node_card",
    "prompt": "C12"
   },
   "statut": "prevu"
  },
  {
   "id": "analyse_coverage",
   "fichier": "ragcreator/synth/coverage.py",
   "groupe": "connaissance",
   "ordre": 28,
   "session": "S15",
   "role": "Mesure ce que la base couvre et ce qui manque ; commande des collectes ciblées.",
   "entrees": {
    "knowledge_map": "carte",
    "research_gaps": "lacunes vues par l'agent"
   },
   "sorties": {
    "gaps": "lacunes à combler"
   },
   "ecrit": [
    "gaps"
   ],
   "modele": {
    "tache": "coverage_analysis",
    "prompt": "C13"
   },
   "statut": "prevu"
  },
  {
   "id": "mcp_tools",
   "fichier": "ragcreator/serve/mcp.py",
   "groupe": "interfaces",
   "ordre": 29,
   "session": "S10",
   "role": "Outils MCP pour qu'un modèle interroge le RAG lui-même (rag_research et outils de bas niveau).",
   "entrees": {
    "tool_call": "appel d'outil",
    "dossier": "dossier de preuves"
   },
   "sorties": {
    "question": "question transmise à l'agent"
   },
   "statut": "prevu"
  },
  {
   "id": "receive_question",
   "fichier": "ragcreator/serve/proxy.py",
   "groupe": "interfaces",
   "ordre": 29,
   "session": "S10",
   "role": "Reçoit votre question depuis Open WebUI / LM Studio, choisit le mode sans rechargement, met le fond en pause.",
   "entrees": {
    "user_question": "question",
    "chat_messages": "conversation",
    "answer": "réponse à relayer"
   },
   "sorties": {
    "question": "question",
    "focus": "angle éventuel"
   },
   "statut": "prevu"
  },
  {
   "id": "analyse_situation",
   "fichier": "ragcreator/research/situation.py",
   "groupe": "agent",
   "ordre": 30,
   "session": "S09",
   "role": "Comprend la situation : acteurs, objectif, juridictions, date de référence, ambiguïtés.",
   "entrees": {
    "question": "question",
    "user_profile": "votre profil"
   },
   "sorties": {
    "situation": "situation",
    "reference_date": "date de référence",
    "ambiguities": "ambiguïtés"
   },
   "modele": {
    "tache": "situation_analysis",
    "prompt": "Q01"
   },
   "statut": "prevu"
  },
  {
   "id": "resolve_angle",
   "fichier": "ragcreator/research/angle.py",
   "groupe": "agent",
   "ordre": 31,
   "session": "S09",
   "role": "Fixe l'angle : votre validation du plan > --focus > formulation > profil > défaut.",
   "entrees": {
    "situation": "situation",
    "focus": "angle demandé",
    "user_profile": "profil"
   },
   "sorties": {
    "angle": "angle retenu"
   },
   "statut": "prevu"
  },
  {
   "id": "plan_research",
   "fichier": "ragcreator/research/plan.py",
   "groupe": "agent",
   "ordre": 32,
   "session": "S09",
   "role": "Bâtit le plan : sous-questions pondérées, thèmes lus sur la carte, filtres, contre-point.",
   "entrees": {
    "situation": "situation",
    "angle": "angle",
    "knowledge_map": "carte des thèmes"
   },
   "sorties": {
    "research_plan": "plan de recherche"
   },
   "modele": {
    "tache": "research_plan",
    "prompt": "Q02"
   },
   "statut": "prevu"
  },
  {
   "id": "validate_plan",
   "fichier": "ragcreator/research/validate_plan.py",
   "groupe": "agent",
   "ordre": 33,
   "session": "S09",
   "role": "Vérifie le plan (thèmes, filtres, dépendances, budget) ; vous pouvez le corriger (--validate-plan).",
   "entrees": {
    "research_plan": "plan",
    "domain_profiles": "profils"
   },
   "sorties": {
    "valid_plan": "plan validé"
   },
   "statut": "prevu"
  },
  {
   "id": "first_move",
   "fichier": "ragcreator/research/first_move.py",
   "groupe": "agent",
   "ordre": 34,
   "session": "S09",
   "role": "Premier coup : toutes les sous-questions en parallèle, re-classées chacune selon sa sous-question.",
   "entrees": {
    "valid_plan": "plan",
    "reference_date": "date de référence",
    "ranked_chunks": "résultats de recherche"
   },
   "sorties": {
    "evidence_pool": "réserve de preuves",
    "query": "requête",
    "filters": "filtres",
    "rerank_query": "sous-question"
   },
   "appelle": [
    "search"
   ],
   "statut": "prevu"
  },
  {
   "id": "search",
   "fichier": "ragcreator/index/search.py",
   "groupe": "agent",
   "ordre": 34,
   "session": "S07",
   "role": "Moteur : BM25 + vecteurs → fusion → re-classement → diversité ; filtres d'étiquettes et de date.",
   "entrees": {
    "query": "requête",
    "filters": "filtres",
    "reference_date": "date",
    "rerank_query": "sous-question",
    "fts_index": "index lexical",
    "vector_index": "index vectoriel",
    "rerank_scores": "scores du re-classement"
   },
   "sorties": {
    "ranked_chunks": "extraits classés",
    "candidate_chunks": "extraits candidats au re-classement"
   },
   "appelle": [
    "rerank",
    "embed_texts"
   ],
   "statut": "prevu"
  },
  {
   "id": "deepen",
   "fichier": "ragcreator/research/deepen.py",
   "groupe": "agent",
   "ordre": 35,
   "session": "S09",
   "role": "Approfondit là où les preuves sont riches ; escalade extrait → section → document → graphe → fiches.",
   "entrees": {
    "evidence_pool": "réserve de preuves",
    "valid_plan": "plan",
    "graph": "graphe",
    "entity_cards": "fiches"
   },
   "sorties": {
    "evidence_pool": "réserve enrichie"
   },
   "appelle": [
    "search"
   ],
   "statut": "prevu"
  },
  {
   "id": "select_evidence",
   "fichier": "ragcreator/research/select.py",
   "groupe": "agent",
   "ordre": 36,
   "session": "S09",
   "role": "Contrôle chaque preuve : fidélité, applicabilité, version en vigueur, source adaptée.",
   "entrees": {
    "evidence_pool": "réserve",
    "situation": "situation"
   },
   "sorties": {
    "selected_evidence": "preuves retenues"
   },
   "modele": {
    "tache": "evidence_selection",
    "prompt": "Q03"
   },
   "statut": "prevu"
  },
  {
   "id": "rank_evidence",
   "fichier": "ragcreator/research/rank.py",
   "groupe": "agent",
   "ordre": 37,
   "session": "S09",
   "role": "Hiérarchise : importance = poids × solidité × applicabilité × fraîcheur × pertinence.",
   "entrees": {
    "selected_evidence": "preuves",
    "angle": "angle",
    "chunk_labels": "étiquettes de solidité"
   },
   "sorties": {
    "ranked_evidence": "preuves classées"
   },
   "statut": "prevu"
  },
  {
   "id": "build_dossier",
   "fichier": "ragcreator/research/dossier.py",
   "groupe": "agent",
   "ordre": 38,
   "session": "S09",
   "role": "Assemble le dossier de preuves classé, étiqueté, avec conflits et lacunes.",
   "entrees": {
    "ranked_evidence": "preuves classées",
    "conflicts": "conflits",
    "valid_plan": "plan"
   },
   "sorties": {
    "dossier": "dossier de preuves",
    "research_gaps": "lacunes"
   },
   "ecrit": [
    "research_runs",
    "gaps"
   ],
   "modele": {
    "tache": "evidence_dossier",
    "prompt": "Q04"
   },
   "statut": "prevu"
  },
  {
   "id": "write_answer",
   "fichier": "ragcreator/research/answer.py",
   "groupe": "agent",
   "ordre": 39,
   "session": "S09",
   "role": "Rédige la réponse à partir du dossier uniquement, avec citations et prudences.",
   "entrees": {
    "dossier": "dossier",
    "question": "question"
   },
   "sorties": {
    "answer": "réponse"
   },
   "modele": {
    "tache": "consumer_answer",
    "prompt": "Q06"
   },
   "statut": "prevu"
  },
  {
   "id": "log_question",
   "fichier": "ragcreator/research/questions.py",
   "groupe": "interfaces",
   "ordre": 40,
   "session": "S09",
   "role": "Journal de vos questions, de vos notes et corrections (exemples « or » pour l'agent).",
   "entrees": {
    "question": "question",
    "answer": "réponse",
    "user_rating": "votre note"
   },
   "sorties": {
    "question_log": "journal des questions"
   },
   "ecrit": [
    "questions",
    "examples"
   ],
   "statut": "prevu"
  },
  {
   "id": "teacher_labels",
   "fichier": "ragcreator/specialists/teacher.py",
   "groupe": "specialistes",
   "ordre": 41,
   "session": "S11",
   "role": "L'enseignant traite un échantillon ; accord ou contrôles réussis → exemples « argent ».",
   "entrees": {
    "example": "exemples bruts"
   },
   "sorties": {
    "silver_examples": "exemples argent"
   },
   "ecrit": [
    "examples"
   ],
   "statut": "prevu"
  },
  {
   "id": "build_datasets",
   "fichier": "ragcreator/specialists/datasets.py",
   "groupe": "specialistes",
   "ordre": 42,
   "session": "S11",
   "role": "Construit les jeux par tâche (or + argent), sans fuite, sans le domaine tenu à l'écart.",
   "entrees": {
    "gold_examples": "exemples or",
    "silver_examples": "exemples argent",
    "question_log": "vos questions notées"
   },
   "sorties": {
    "datasets": "jeux d'entraînement, validation, test"
   },
   "statut": "prevu"
  },
  {
   "id": "retrain_all",
   "fichier": "ragcreator/specialists/retrain.py",
   "groupe": "specialistes",
   "ordre": 43,
   "session": "S11",
   "role": "Après un changement de modèle de base : réentraîne, évalue et promeut tous les adaptateurs requis.",
   "entrees": {
    "new_base_model": "nouveau modèle de base",
    "datasets": "jeux"
   },
   "sorties": {
    "base_model": "modèle de base pour l'entraînement"
   },
   "appelle": [
    "train_adapter",
    "export_adapter",
    "evaluate_specialist",
    "promote_specialist"
   ],
   "statut": "prevu"
  },
  {
   "id": "train_adapter",
   "fichier": "ragcreator/specialists/train.py",
   "groupe": "specialistes",
   "ordre": 43,
   "session": "S11",
   "role": "Entraîne un adaptateur LoRA (16 bits, déchargement de couches si besoin), avec reprise.",
   "entrees": {
    "datasets": "jeux",
    "base_model": "modèle de base"
   },
   "sorties": {
    "adapter": "adaptateur LoRA"
   },
   "statut": "prevu"
  },
  {
   "id": "export_adapter",
   "fichier": "ragcreator/specialists/export.py",
   "groupe": "specialistes",
   "ordre": 44,
   "session": "S11",
   "role": "Convertit l'adaptateur en GGUF et vérifie gabarit de chat et jeton de fin.",
   "entrees": {
    "adapter": "adaptateur"
   },
   "sorties": {
    "adapter_gguf": "adaptateur GGUF"
   },
   "statut": "prevu"
  },
  {
   "id": "evaluate_specialist",
   "fichier": "ragcreator/specialists/evaluate.py",
   "groupe": "specialistes",
   "ordre": 45,
   "session": "S11",
   "role": "Compare le spécialiste à l'enseignant sur le test tenu à l'écart et sur le domaine tenu à l'écart.",
   "entrees": {
    "adapter_gguf": "adaptateur",
    "datasets": "jeu de test"
   },
   "sorties": {
    "specialist_metrics": "métriques"
   },
   "statut": "prevu"
  },
  {
   "id": "promote_specialist",
   "fichier": "ragcreator/specialists/promote.py",
   "groupe": "specialistes",
   "ordre": 46,
   "session": "S11",
   "role": "Porte de promotion : promu seulement s'il égale l'enseignant et va plus vite ; rétrogradation si baisse.",
   "entrees": {
    "specialist_metrics": "métriques"
   },
   "sorties": {
    "specialists_registry": "registre des spécialistes"
   },
   "ecrit": [
    "specialists"
   ],
   "statut": "prevu"
  },
  {
   "id": "build_eval_set",
   "fichier": "ragcreator/eval/build.py",
   "groupe": "evaluation",
   "ordre": 47,
   "session": "S16",
   "role": "Construit le jeu d'évaluation (factuel, multi-sauts, transversal, temporel, sans réponse).",
   "entrees": {
    "chunks": "extraits"
   },
   "sorties": {
    "eval_set": "jeu d'évaluation"
   },
   "modele": {
    "tache": "eval_questions",
    "prompt": "V01"
   },
   "statut": "prevu"
  },
  {
   "id": "judge_answers",
   "fichier": "ragcreator/eval/judge.py",
   "groupe": "evaluation",
   "ordre": 48,
   "session": "S16",
   "role": "Contrôles déterministes d'abord, puis juge pour la fidélité et la complétude.",
   "entrees": {
    "answer": "réponses",
    "dossier": "dossiers",
    "eval_set": "jeu"
   },
   "sorties": {
    "eval_scores": "scores"
   },
   "modele": {
    "tache": "eval_judge",
    "prompt": "V02"
   },
   "statut": "prevu"
  },
  {
   "id": "run_benchmarks",
   "fichier": "ragcreator/eval/bench.py",
   "groupe": "evaluation",
   "ordre": 49,
   "session": "S16",
   "role": "Bancs de mesure sur vos PC : qualité, vitesse, rechargements, pilotage, installation.",
   "entrees": {
    "eval_set": "jeu",
    "hardware_profile": "profil matériel",
    "eval_scores": "scores"
   },
   "sorties": {
    "bench_report": "rapport de banc"
   },
   "statut": "prevu"
  }
 ],
 "flux": [
  {
   "de": "analyse_coverage",
   "vers": "build_reading_list",
   "variables": [
    "gaps"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "analyse_coverage",
   "vers": "generate_queries",
   "variables": [
    "gaps"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "analyse_situation",
   "vers": "first_move",
   "variables": [
    "reference_date"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "analyse_situation",
   "vers": "plan_research",
   "variables": [
    "situation"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "analyse_situation",
   "vers": "resolve_angle",
   "variables": [
    "situation"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "analyse_situation",
   "vers": "search",
   "variables": [
    "reference_date"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "analyse_situation",
   "vers": "select_evidence",
   "variables": [
    "situation"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "arbitrate_ocr",
   "vers": "check_ocr",
   "variables": [
    "page_texts"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "arbitrate_ocr",
   "vers": "rebuild_structure",
   "variables": [
    "page_texts"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "browser_inbox",
   "vers": "precheck",
   "variables": [
    "raw_documents"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "build_datasets",
   "vers": "evaluate_specialist",
   "variables": [
    "datasets"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "build_datasets",
   "vers": "retrain_all",
   "variables": [
    "datasets"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "build_datasets",
   "vers": "train_adapter",
   "variables": [
    "datasets"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "build_dossier",
   "vers": "analyse_coverage",
   "variables": [
    "research_gaps"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "build_dossier",
   "vers": "judge_answers",
   "variables": [
    "dossier"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "build_dossier",
   "vers": "mcp_tools",
   "variables": [
    "dossier"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "build_dossier",
   "vers": "write_answer",
   "variables": [
    "dossier"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "build_eval_set",
   "vers": "judge_answers",
   "variables": [
    "eval_set"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "build_eval_set",
   "vers": "run_benchmarks",
   "variables": [
    "eval_set"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "call_llm",
   "vers": "validate_output",
   "variables": [
    "raw_completion"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "capture_example",
   "vers": "teacher_labels",
   "variables": [
    "example"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "charger_registre",
   "vers": "banc_collecte",
   "variables": [
    "collecteurs"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "charger_registre",
   "vers": "run_collectors",
   "variables": [
    "collecteurs"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "charger_strategie",
   "vers": "banc_collecte",
   "variables": [
    "strategie"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "charger_strategie",
   "vers": "generer_requetes_strategie",
   "variables": [
    "strategie"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "charger_strategie",
   "vers": "triage_candidates",
   "variables": [
    "strategie"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "check_ocr",
   "vers": "arbitrate_ocr",
   "variables": [
    "ocr_alerts"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "chunk_document",
   "vers": "build_eval_set",
   "variables": [
    "chunks"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "chunk_document",
   "vers": "enrich_chunks",
   "variables": [
    "chunks"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "chunk_document",
   "vers": "index_text",
   "variables": [
    "chunks"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "chunk_document",
   "vers": "index_vectors",
   "variables": [
    "chunks"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "chunk_document",
   "vers": "label_chunks",
   "variables": [
    "chunks"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "chunk_document",
   "vers": "write_node_cards",
   "variables": [
    "chunks"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "collecteur_dossier_local",
   "vers": "fetch_documents",
   "variables": [
    "document_collecte"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "collecteur_dossier_local",
   "vers": "run_collectors",
   "variables": [
    "candidats"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "collecteur_liste_lecture",
   "vers": "run_collectors",
   "variables": [
    "candidats"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "collecteur_openalex",
   "vers": "fetch_documents",
   "variables": [
    "document_collecte"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "collecteur_openalex",
   "vers": "run_collectors",
   "variables": [
    "candidats"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "collecteur_wikipedia",
   "vers": "fetch_documents",
   "variables": [
    "document_collecte"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "collecteur_wikipedia",
   "vers": "run_collectors",
   "variables": [
    "candidats"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "control_channel",
   "vers": "schedule_jobs",
   "variables": [
    "worker_state"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "date_and_version",
   "vers": "qualify_conflicts",
   "variables": [
    "validity"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "date_and_version",
   "vers": "watch_sources",
   "variables": [
    "validity"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "decide_document",
   "vers": "chunk_document",
   "variables": [
    "document_decision"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "decide_document",
   "vers": "review_session",
   "variables": [
    "document_decision"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "decide_document",
   "vers": "second_opinion",
   "variables": [
    "document_decision"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "deepen",
   "vers": "select_evidence",
   "variables": [
    "evidence_pool"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "describe_figures",
   "vers": "rebuild_structure",
   "variables": [
    "figure_descriptions"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "detect_hardware",
   "vers": "model_manager",
   "variables": [
    "hardware_profile"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "detect_hardware",
   "vers": "run_benchmarks",
   "variables": [
    "hardware_profile"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "diagnose_pages",
   "vers": "arbitrate_ocr",
   "variables": [
    "pages"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "diagnose_pages",
   "vers": "describe_figures",
   "variables": [
    "pages"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "diagnose_pages",
   "vers": "extract_native_text",
   "variables": [
    "pages"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "diagnose_pages",
   "vers": "ocr_pages",
   "variables": [
    "pages"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "digest_document",
   "vers": "enrich_chunks",
   "variables": [
    "digest"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "digest_document",
   "vers": "qualify_conflicts",
   "variables": [
    "validity"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "digest_document",
   "vers": "watch_sources",
   "variables": [
    "validity"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "embed_texts",
   "vers": "index_vectors",
   "variables": [
    "vectors"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "enrich_chunks",
   "vers": "index_text",
   "variables": [
    "chunk_context",
    "chunk_questions"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "enrich_chunks",
   "vers": "index_vectors",
   "variables": [
    "chunk_context",
    "chunk_questions"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "enrich_chunks",
   "vers": "resolve_entities",
   "variables": [
    "raw_relations"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "evaluate_specialist",
   "vers": "promote_specialist",
   "variables": [
    "specialist_metrics"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "export_adapter",
   "vers": "evaluate_specialist",
   "variables": [
    "adapter_gguf"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "extract_native_text",
   "vers": "check_ocr",
   "variables": [
    "page_texts"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "extract_native_text",
   "vers": "rebuild_structure",
   "variables": [
    "page_texts"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "fetch_documents",
   "vers": "precheck",
   "variables": [
    "raw_documents"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "first_move",
   "vers": "deepen",
   "variables": [
    "evidence_pool"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "first_move",
   "vers": "rerank",
   "variables": [
    "rerank_query"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "first_move",
   "vers": "search",
   "variables": [
    "filters",
    "query",
    "rerank_query"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "first_move",
   "vers": "select_evidence",
   "variables": [
    "evidence_pool"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "generate_queries",
   "vers": "run_collectors",
   "variables": [
    "queries"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "generer_requetes_strategie",
   "vers": "generate_queries",
   "variables": [
    "requetes_strategie"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "import_library",
   "vers": "precheck",
   "variables": [
    "raw_documents"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "index_text",
   "vers": "search",
   "variables": [
    "fts_index"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "index_vectors",
   "vers": "embed_texts",
   "variables": [
    "texts"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "index_vectors",
   "vers": "search",
   "variables": [
    "vector_index"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "judge_answers",
   "vers": "run_benchmarks",
   "variables": [
    "eval_scores"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "label_chunks",
   "vers": "index_text",
   "variables": [
    "chunk_labels"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "label_chunks",
   "vers": "qualify_conflicts",
   "variables": [
    "claims"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "label_chunks",
   "vers": "rank_evidence",
   "variables": [
    "chunk_labels"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "label_chunks",
   "vers": "review_session",
   "variables": [
    "chunk_labels"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "load_config",
   "vers": "model_manager",
   "variables": [
    "config"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "load_config",
   "vers": "open_database",
   "variables": [
    "config"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "load_profiles",
   "vers": "chunk_document",
   "variables": [
    "domain_profiles"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "load_profiles",
   "vers": "validate_plan",
   "variables": [
    "domain_profiles"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "load_profiles",
   "vers": "write_charter",
   "variables": [
    "domain_profiles"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "log_question",
   "vers": "build_datasets",
   "variables": [
    "question_log"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "manage_themes",
   "vers": "write_charter",
   "variables": [
    "theme_id"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "mcp_tools",
   "vers": "analyse_situation",
   "variables": [
    "question"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "mcp_tools",
   "vers": "log_question",
   "variables": [
    "question"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "mcp_tools",
   "vers": "write_answer",
   "variables": [
    "question"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "model_manager",
   "vers": "call_llm",
   "variables": [
    "model_endpoint"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "model_manager",
   "vers": "run_job",
   "variables": [
    "model_endpoint"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "ocr_pages",
   "vers": "check_ocr",
   "variables": [
    "page_texts"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "ocr_pages",
   "vers": "rebuild_structure",
   "variables": [
    "page_texts"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "open_database",
   "vers": "manage_themes",
   "variables": [
    "db"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "plan_research",
   "vers": "validate_plan",
   "variables": [
    "research_plan"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "precheck",
   "vers": "date_and_version",
   "variables": [
    "documents"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "precheck",
   "vers": "diagnose_pages",
   "variables": [
    "documents"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "precheck",
   "vers": "verify_document",
   "variables": [
    "documents"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "precheck",
   "vers": "watch_sources",
   "variables": [
    "documents"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "promote_specialist",
   "vers": "route_task",
   "variables": [
    "specialists_registry"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "qualify_conflicts",
   "vers": "build_dossier",
   "variables": [
    "conflicts"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "qualify_conflicts",
   "vers": "write_entity_cards",
   "variables": [
    "conflicts"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "rank_evidence",
   "vers": "build_dossier",
   "variables": [
    "ranked_evidence"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "rebuild_structure",
   "vers": "chunk_document",
   "variables": [
    "sections"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "rebuild_structure",
   "vers": "date_and_version",
   "variables": [
    "book_metadata"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "rebuild_structure",
   "vers": "digest_document",
   "variables": [
    "sections"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "rebuild_structure",
   "vers": "verify_document",
   "variables": [
    "sections"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "receive_question",
   "vers": "analyse_situation",
   "variables": [
    "question"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "receive_question",
   "vers": "log_question",
   "variables": [
    "question"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "receive_question",
   "vers": "resolve_angle",
   "variables": [
    "focus"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "receive_question",
   "vers": "write_answer",
   "variables": [
    "question"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "render_prompt",
   "vers": "call_llm",
   "variables": [
    "messages"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "rerank",
   "vers": "search",
   "variables": [
    "rerank_scores"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "resolve_angle",
   "vers": "plan_research",
   "variables": [
    "angle"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "resolve_angle",
   "vers": "rank_evidence",
   "variables": [
    "angle"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "resolve_entities",
   "vers": "deepen",
   "variables": [
    "graph"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "resolve_entities",
   "vers": "qualify_conflicts",
   "variables": [
    "graph"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "resolve_entities",
   "vers": "write_entity_cards",
   "variables": [
    "graph"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "resolve_entities",
   "vers": "write_node_cards",
   "variables": [
    "graph"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "retrain_all",
   "vers": "train_adapter",
   "variables": [
    "base_model"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "review_session",
   "vers": "build_datasets",
   "variables": [
    "gold_examples"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "route_task",
   "vers": "call_llm",
   "variables": [
    "model_request"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "route_task",
   "vers": "model_manager",
   "variables": [
    "model_request"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "route_task",
   "vers": "render_prompt",
   "variables": [
    "prompt_variant"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "run_collectors",
   "vers": "collecteur_dossier_local",
   "variables": [
    "requete"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "run_collectors",
   "vers": "collecteur_liste_lecture",
   "variables": [
    "requete"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "run_collectors",
   "vers": "collecteur_openalex",
   "variables": [
    "requete"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "run_collectors",
   "vers": "collecteur_wikipedia",
   "variables": [
    "requete"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "run_collectors",
   "vers": "triage_candidates",
   "variables": [
    "candidates"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "run_job",
   "vers": "schedule_jobs",
   "variables": [
    "jobs"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "schedule_jobs",
   "vers": "call_llm",
   "variables": [
    "model_request"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "schedule_jobs",
   "vers": "model_manager",
   "variables": [
    "model_request"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "schedule_jobs",
   "vers": "run_job",
   "variables": [
    "next_job"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "search",
   "vers": "first_move",
   "variables": [
    "ranked_chunks"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "search",
   "vers": "rerank",
   "variables": [
    "candidate_chunks"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "second_opinion",
   "vers": "chunk_document",
   "variables": [
    "document_decision"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "second_opinion",
   "vers": "review_session",
   "variables": [
    "document_decision"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "select_evidence",
   "vers": "rank_evidence",
   "variables": [
    "selected_evidence"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "teacher_labels",
   "vers": "build_datasets",
   "variables": [
    "silver_examples"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "train_adapter",
   "vers": "export_adapter",
   "variables": [
    "adapter"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "triage_candidates",
   "vers": "build_reading_list",
   "variables": [
    "kept_candidates"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "triage_candidates",
   "vers": "fetch_documents",
   "variables": [
    "kept_candidates"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "validate_output",
   "vers": "capture_example",
   "variables": [
    "validated_output"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "validate_plan",
   "vers": "build_dossier",
   "variables": [
    "valid_plan"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "validate_plan",
   "vers": "deepen",
   "variables": [
    "valid_plan"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "validate_plan",
   "vers": "first_move",
   "variables": [
    "valid_plan"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "verify_document",
   "vers": "decide_document",
   "variables": [
    "verification_scores"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "watch_sources",
   "vers": "precheck",
   "variables": [
    "raw_documents"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "write_answer",
   "vers": "judge_answers",
   "variables": [
    "answer"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "write_answer",
   "vers": "log_question",
   "variables": [
    "answer"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "write_answer",
   "vers": "receive_question",
   "variables": [
    "answer"
   ],
   "type": "donnees",
   "boucle": true
  },
  {
   "de": "write_charter",
   "vers": "generate_queries",
   "variables": [
    "charter"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "write_charter",
   "vers": "triage_candidates",
   "variables": [
    "charter"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "write_charter",
   "vers": "verify_document",
   "variables": [
    "charter"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "write_charter",
   "vers": "write_node_cards",
   "variables": [
    "charter"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "write_entity_cards",
   "vers": "deepen",
   "variables": [
    "entity_cards"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "write_node_cards",
   "vers": "analyse_coverage",
   "variables": [
    "knowledge_map"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "write_node_cards",
   "vers": "plan_research",
   "variables": [
    "knowledge_map"
   ],
   "type": "donnees",
   "boucle": false
  },
  {
   "de": "index_vectors",
   "vers": "embed_texts",
   "variables": [],
   "type": "appel",
   "boucle": false
  },
  {
   "de": "first_move",
   "vers": "search",
   "variables": [],
   "type": "appel",
   "boucle": false
  },
  {
   "de": "search",
   "vers": "rerank",
   "variables": [],
   "type": "appel",
   "boucle": false
  },
  {
   "de": "search",
   "vers": "embed_texts",
   "variables": [],
   "type": "appel",
   "boucle": false
  },
  {
   "de": "deepen",
   "vers": "search",
   "variables": [],
   "type": "appel",
   "boucle": false
  },
  {
   "de": "retrain_all",
   "vers": "train_adapter",
   "variables": [],
   "type": "appel",
   "boucle": false
  },
  {
   "de": "retrain_all",
   "vers": "export_adapter",
   "variables": [],
   "type": "appel",
   "boucle": false
  },
  {
   "de": "retrain_all",
   "vers": "evaluate_specialist",
   "variables": [],
   "type": "appel",
   "boucle": false
  },
  {
   "de": "retrain_all",
   "vers": "promote_specialist",
   "variables": [],
   "type": "appel",
   "boucle": false
  }
 ],
 "problemes": []
};
