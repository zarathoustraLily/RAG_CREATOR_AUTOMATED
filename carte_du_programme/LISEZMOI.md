# Carte du programme

Une page HTML5 interactive qui montre **comment fonctionne RAG Creator** :
- tous les **mini-scripts**, rangés par moment (socle, construire, répondre, apprendre,
  évaluer) et par groupe ;
- leur **ordre chronologique** : dans chaque moment, le temps s'écoule de gauche à droite ;
- les **flux** entre scripts, avec le **nom des variables** qui entrent et qui sortent ;
- des **parcours guidés** : vie d'un document, d'une question, d'un spécialiste, d'une
  collecte, et le pilotage du travail en fond.

## Ouvrir la carte

Double-cliquez sur `index.html` : elle s'ouvre dans votre navigateur, sans connexion ni
installation.

- **Cliquer un script** : sa fiche (rôle, fichier, session, modèle utilisé), ses entrées avec
  leur provenance, ses sorties avec leurs destinataires.
- **Chercher** un script ou une **variable** : la variable est suivie de son producteur à tous
  ses utilisateurs.
- **Parcours guidés** : étape par étape, ou en lecture automatique.
- **Glisser** pour se déplacer, **molette** pour zoomer, **⤢** ou la touche **0** pour tout voir,
  **Échap** pour revenir à la vue d'ensemble.
- Cases à cocher : noms des variables sur les flèches, boucles de retour, appels au modèle.

Un cadre **en pointillés** est un script **prévu** ; un cadre **plein** est un script
**réalisé** (il existe dans le code avec son manifeste).

## D'où viennent les données

`generer_carte.py` assemble :
1. les **manifestes** `__manifeste__` placés en tête de chaque script du code, lus **sans
   exécuter** le code ;
2. `architecture_prevue.yaml`, pour les scripts qui n'existent pas encore.

Il calcule les flux (une variable produite par un script et utilisée par un autre), contrôle
la cohérence, puis écrit `donnees.js`, que la page lit.

```bash
python carte_du_programme/generer_carte.py              # régénérer la carte
python carte_du_programme/generer_carte.py --verifier   # contrôler (échoue si problème ou carte périmée)
python -m pytest carte_du_programme/tests               # tests de la carte
```

## Manifeste d'un script

```python
__manifeste__ = {
    "nom": "label_chunks",
    "role": "Garde ou écarte chaque extrait et l'étiquette (niveau de preuve, population…).",
    "groupe": "verification",
    "ordre": 22,
    "session": "S06",
    "entrees": {"chunks": "extraits"},
    "sorties": {"chunk_labels": "étiquettes", "claims": "affirmations sensibles"},
    "lit": [],
    "ecrit": ["chunks", "claims"],
    "appelle": [],
    "modele": {"tache": "passage_verification", "prompt": "C06"},
}
```

Règles contrôlées automatiquement :
- chaque script du code (`ragcreator/`, `methodologie_recherche/`) a un manifeste ;
- chaque entrée est produite par un autre script, ou déclarée dans `entrees_externes` de
  `architecture_prevue.yaml` ;
- les noms de variables du manifeste sont ceux du code ;
- la carte enregistrée (`donnees.js`) est à jour.
