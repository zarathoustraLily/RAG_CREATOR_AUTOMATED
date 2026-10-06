"""Méthodologie et technique de recherche — module modifiable par l'utilisateur.

Ce dossier décrit *comment* RAG Creator cherche des documents :
- `strategies/` : la méthodologie de chaque domaine (sources, formulations, critères), en YAML ;
- `collecteurs/` : les techniques, une par mini-script, toutes conformes à `collecteurs/contrat.py` ;
- `registre.yaml` : les techniques actives, leur ordre et leurs réglages ;
- `tests/` et `bancs/` : pour vérifier et mesurer vos modifications.

Le reste du logiciel ne connaît que le contrat : vous pouvez modifier ce dossier sans toucher
au reste. Voir LISEZMOI.md.
"""

__version__ = "0.1.0"
