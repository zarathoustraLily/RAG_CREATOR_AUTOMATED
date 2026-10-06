# S15 — Carte navigable, fiches, couverture (E12, E13)

> Jalon J5 · Dépend de : S14 · Étapes : E12, E13 · Prompts d'exécution : C11, C12, C13
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§4**, §5, §8),
`PLAN/001_but.md` (§3, §7), `PLAN/002_strategie.md` (**§4.1**, §6, §7.1),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Faire de l'arbre des thèmes une **carte** que l'agent parcourt, pré-calculer des **fiches
sourcées phrase par phrase**, et piloter la collecte par la **couverture** : le système sait ce
qu'il sait, et ce qui lui manque.

## À réaliser

1. **C12 `node_card`** (enseignant, P4), des feuilles vers la racine : contenu en langage simple,
   sous-thèmes, **questions types**, points clés, couverture, lacunes, rayons voisins utiles
   (ex. *escroqueries* ↔ *ingénierie sociale* ↔ *économie comportementale*).
2. **Fichiers de navigation** : `themes/<chemin>/index.md` et `CARTE.md` (métadonnées en tête).
3. **C11 `entity_card`** (enseignant) avec gabarits par profil (ex. technique d'escroquerie : étapes,
   biais exploités, signaux d'alerte, contre-mesures, niveau de preuve ; article fiscal : objet,
   conditions, exceptions, versions, jurisprudence ; traitement : indications, niveau de preuve,
   recommandations, limites) ; **chaque phrase citée** ; contrôle des citations par le code.
4. **Régénération** par empreinte des entrées et après nouvelle version (S13).
5. **C13 `coverage_analysis`** : couverture par sous-thème et par sous-question fréquente des
   dossiers, lacunes, requêtes (via C02), sous-thèmes ; continuer / arrêter ; orienté par votre
   profil utilisateur.
6. **Intégration** : Q02 lit les fiches de nœud comme carte ; les fiches sont indexées et
   consultables par l'agent ; la couverture alimente le travail en fond.
7. **Commandes** : `ragc map`, `ragc synth run|show`, `ragc coverage`.
8. **Tests** : ordre feuilles → racine, citations, empreintes, carte lue par Q02 (faux serveur).

## Bancs à ajouter

`ragc bench map` : qualité du plan des cas B, F et H **avant / après** la carte ; relecture de
3 fiches.

## Critères d'acceptation

- [ ] Aucune citation invalide dans les fiches ; carte lisible ; couverture visible par thème.
- [ ] Procédure de clôture appliquée.
