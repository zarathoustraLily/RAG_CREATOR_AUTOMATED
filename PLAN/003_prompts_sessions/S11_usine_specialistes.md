# S11 — Usine à spécialistes, réentraînement en une commande (P5)

> Jalon J4 · Dépend de : S10 · Étape : P5 (entraînement) · Prompts d'exécution : —
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§7, §13, §14, §16**),
`PLAN/001_but.md` (**§6**, §9), `PLAN/002_strategie.md` (**§8 en entier**, §3.1, §5.2, §5.6),
`PLAN/004_decisions_techniques.md` (outil d'entraînement), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md` (dont les rapports de banc sur l'entraînement). Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Transformer les exemples accumulés en **petits spécialistes** (adaptateurs LoRA) qui font le
travail répétitif **aussi bien que l'enseignant et beaucoup plus vite** — avec une **porte de
promotion** mesurée, un **domaine tenu à l'écart** pour vérifier la généralisation, et une
**commande unique** pour tout réentraîner quand un modèle de base change.

## À réaliser

1. **Jeux de données** (`ragcreator/specialists/datasets.py`) à partir de `examples` : par tâche,
   exemples **or** et **argent** seulement ; découpage entraînement / validation / test **par
   thème et par document** ; **aucun exemple du domaine hacking** (tenu à l'écart) ni des cas de
   référence ; application du **gabarit du modèle de base au moment de l'entraînement** (format
   neutre en base) ; supervision **avec raisonnement** pour les tâches de raisonnement.
2. **Étiquettes d'enseignant** (phase P4) : tâches qui demandent à l'enseignant de traiter un
   échantillon ; statut **argent** si deux passes concordent ou si les contrôles passent.
3. **Entraînement** (phase P5, tâche du travail en fond, interruptible avec points de reprise) :
   LoRA 16 bits, déchargement de couches si nécessaire, outil retenu en S01 (Unsloth sous
   Windows et Linux) ; **recettes** enregistrées (hyperparamètres, versions des outils, graine)
   pour un entraînement reproductible.
4. **Export et service** : adaptateur → GGUF, ajout à la liste `--lora` du modèle de base via le
   gestionnaire de modèles ; test de non-régression du **gabarit et du jeton de fin** après export.
5. **Registre** (`specialists`) : tâche, base (nom + **empreinte du fichier**), adaptateur,
   version, jeu, recette, métriques, statut (`candidat`, `promu`, `retire`).
6. **Porte de promotion** : sur le test tenu à l'écart, ≥ l'enseignant à une tolérance près **et**
   ≥ 3× plus rapide ; **test de généralisation** sur le domaine tenu à l'écart (≥ 90 % de
   l'enseignant) ; rétrogradation automatique si vos corrections montrent une baisse.
7. **Changement de modèle de base** : à chaque chargement, adaptateurs dont l'empreinte de base ne
   correspond pas → désactivés, repli sur prompts ; **`ragc specialists retrain --base
   <modèle>`** réentraîne, évalue et promeut **tous** les adaptateurs requis, dans l'ordre de
   `002_strategie.md` §8.1, reprise possible.
8. **Premiers spécialistes** : **tri** (C03) et **étiquetage d'extraits** (C06) ; leur variante
   courte de prompt.
9. **Commandes** : `ragc specialists status|datasets|train|evaluate|promote|demote|retrain`.
10. **Tests** hors ligne : jeux sans fuite, exclusion du domaine tenu à l'écart, registre et
    empreintes, repli sur prompts, porte de promotion (avec métriques simulées), reprise d'un
    entraînement interrompu (faux entraîneur).

## Bancs à ajouter

`ragc bench train` : entraînement réel des spécialistes de tri et d'étiquetage sur le 5090 et le
4090 — durée, VRAM, métriques contre l'enseignant, vitesse ; essai de `retrain --base` avec une
autre base de la même taille.

## Critères d'acceptation

- [ ] Les jeux ne contiennent ni hacking ni cas de référence (test).
- [ ] Un changement simulé de modèle de base désactive les adaptateurs, garde le logiciel
      fonctionnel, et `retrain --base` les reconstruit.
- [ ] Procédure de clôture appliquée.
