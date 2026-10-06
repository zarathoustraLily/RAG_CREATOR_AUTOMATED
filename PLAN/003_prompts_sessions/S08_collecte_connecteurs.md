# S08 — Module « Méthodologie et technique de recherche », collecte assistée, connecteurs prioritaires (E1, E2)

> Jalon J1 · Dépend de : S07 · Étapes : E1, E2 · Prompts d'exécution : C02, C03
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§16**), `PLAN/001_but.md` (§7, §8),
`PLAN/002_strategie.md` (§4.2, **§5.5**, §5.7, §6, §12), `PLAN/004_decisions_techniques.md`,
`methodologie_recherche/LISEZMOI.md`, `PLAN/003_prompts_sessions/00_regles_communes.md`
(**§5 bis : ce dossier appartient à l'utilisateur**), `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Brancher le module **`methodologie_recherche/`** (qui existe déjà, avec son contrat, ses
stratégies, ses premiers collecteurs, ses tests et son banc) sur le travail en fond, compléter
les techniques des **domaines prioritaires** (escroqueries, fiscalité géorgienne et française),
et offrir une **collecte assistée** confortable dans le Brave de l'utilisateur. **Ne modifie pas
les fichiers que l'utilisateur a changés** : ajoute, propose, documente.

## À réaliser

1. **Intégration** (`ragcreator/sources/`) : le cœur ne dépend que du **contrat** du module ;
   chargement des stratégies et du registre ; exécution des collecteurs comme tâches du travail
   en fond (P0), avec la **politesse déclarée** par chacun ; gestion de `AccesRefuse` (bascule de
   la source vers la collecte assistée) et de `SourceIndisponible` (nouvel essai plus tard) ;
   chaque document garde la **stratégie et la technique** qui l'ont trouvé.
2. **Requêtes** : C02 utilise la stratégie du domaine (gabarits, vocabulaire, langues) en plus de
   la charte ; table `queries` (origine : charte, couverture, lacune) ; jamais deux fois la même.
3. **C03 `search_triage`** (phase P2) avec les critères de tri de la stratégie ; décisions
   capturées comme exemples.
4. **Nouveaux collecteurs** (mini-scripts avec manifeste, selon le contrat, avec leurs tests) —
   pour chacun, **vérifie l'accès, la documentation officielle et les conditions d'utilisation**
   avant d'écrire du code, et note-les dans le journal : Europe PMC, Crossref (dont les
   rétractations), Légifrance / Judilibre (API PISTE, clé gratuite), BOFiP, et un **récupérateur
   poli** (agent identifié, `robots.txt`, limites, cache) pour les sites qui l'autorisent
   (matsne.gov.ge et rs.ge si leurs conditions le permettent). Traduction des textes géorgiens
   par le modèle, marquée comme telle.
5. **Collecte assistée** :
   - `ragc read-list build|open <thème>` : listes de lecture (recherches à lancer, documents
     proposés, lacunes) ouvertes dans le Brave de l'utilisateur quand il le décide ;
   - **extension Brave « Envoyer au RAG »** (manifeste v3) : envoie la page ou le PDF affiché au
     logiciel local avec le thème choisi ;
   - surveillance optionnelle du **dossier de téléchargements** ;
   - ce que l'utilisateur garde ou écarte devient un exemple **or** pour le spécialiste de tri.
6. **Collectes ciblées** : les lacunes (`gaps`) deviennent des requêtes ciblées prioritaires.
7. **Commandes** : `ragc methodo test` (contrat + tests de l'utilisateur), `ragc methodo bench`,
   `ragc methodo compare <strategie_a> <strategie_b>`, `ragc discover <thème> [--dry-run]`.
8. **Carte du programme** régénérée ; documentation `docs/collecte.md`.

## Bancs à ajouter

`ragc methodo bench` sur `Fiscalité > Géorgie` et `Criminologie > Escroqueries > Faux placements` :
candidats par technique, part gardée au tri, part acceptée après vérification, doublons, refus,
durée ; comparaison de deux stratégies.

## Critères d'acceptation

- [ ] Une modification d'une stratégie YAML par l'utilisateur change les requêtes sans toucher au
      code ; un collecteur ajouté par l'utilisateur et inscrit au registre est utilisé.
- [ ] `AccesRefuse` fait basculer la source vers la liste de lecture.
- [ ] L'extension envoie une page au logiciel et elle suit le pipeline jusqu'à `indexe`.
- [ ] Procédure de clôture appliquée.
