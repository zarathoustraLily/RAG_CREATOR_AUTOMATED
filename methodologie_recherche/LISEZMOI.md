# Méthodologie et technique de recherche

Ce dossier est **à vous**. Il décrit *comment* RAG Creator cherche des documents, et vous
pouvez le modifier, le tester et le mesurer sans toucher au reste du logiciel : le reste du
programme ne connaît que le **contrat** (`collecteurs/contrat.py`).

```
methodologie_recherche/
├── strategies/          la méthodologie de chaque domaine (YAML)
│   ├── commun.yaml          ce dont tous les domaines héritent
│   ├── juridique_fiscal.yaml
│   ├── fiscalite_georgie.yaml   hérite de juridique_fiscal
│   ├── criminologie.yaml, sante_clinique.yaml, cybersecurite.yaml,
│   └── sciences_comportementales.yaml, pharmaco_medical.yaml, mycologie.yaml
├── strategies.py        charge une méthodologie (héritage, fusion, retraits)
├── requetes.py          fabrique les requêtes à partir des gabarits
├── registre.yaml        les techniques actives, leur ordre, leurs réglages
├── registre.py          charge les techniques et vérifie le contrat
├── collecteurs/         les techniques, une par fichier
│   ├── contrat.py           le contrat (Requete, Candidat, Document, Politesse, erreurs)
│   ├── outils_http.py       client HTTP identifié, robots.txt
│   ├── dossier_local.py     vos dossiers de documents
│   ├── api_openalex.py      publications scientifiques (OpenAlex)
│   ├── wikipedia.py         Wikipédia (API officielle)
│   ├── liste_lecture.py     liens de recherche que VOUS ouvrez (Brave Search, Scholar…)
│   └── modele_collecteur.py gabarit pour écrire votre technique
├── transversal/         le répertoire qui fait voir une question sous tous ses angles
│   ├── lentilles.yaml       grilles d'analyse (présupposés, Tinbergen, niveaux, éthique…)
│   ├── disciplines.yaml     disciplines, ce qu'elles apportent, leurs mots-clés
│   ├── analogues.yaml       problèmes généraux et domaines qui les ont déjà étudiés
│   ├── repertoire.py        charge et contrôle le répertoire
│   ├── exploration.py       repère les angles d'une question et prépare le menu du plan
│   ├── ponts.py             ponts entre littératures calculés sur votre corpus (modèle ABC)
│   └── couverture.py        fusionne plusieurs plans et liste les angles manquants
├── outils_texte.py      normalisation, mots-clés, ressemblance
├── bancs/
│   ├── banc_collecte.py     mesure et comparaison
│   └── sujets_exemple.yaml  sujets de test par domaine
└── tests/
    ├── test_*.py            tests fournis (sans réseau)
    ├── jeux/                réponses d'API fictives pour les tests
    └── vos_tests/           VOS attentes, à écrire et adapter
```

Chaque fichier Python porte un **manifeste** (`__manifeste__`) : il apparaît ainsi dans la
[carte du programme](../carte_du_programme/index.html), avec ses variables d'entrée et de sortie.

## Le cycle de travail

1. **Modifier** une méthodologie (`strategies/*.yaml`), le registre, ou une technique.
2. **Tester** : `python -m pytest methodologie_recherche/tests`
   (rapide, sans réseau ; ajoutez `--reseau` pour interroger aussi les vraies sources).
3. **Mesurer** sur des sujets fixes :
   ```bash
   python -m methodologie_recherche.bancs.banc_collecte executer \
       --domaine criminologie --sujets methodologie_recherche/bancs/sujets_exemple.yaml
   ```
   Le rapport (JSON et Markdown) va dans `methodologie_recherche/rapports/` (non versionné),
   avec un fichier d'**étiquettes** à remplir : mettez `true` (pertinent) ou `false` devant chaque
   candidat, puis :
   ```bash
   python -m methodologie_recherche.bancs.banc_collecte evaluer RAPPORT.json ETIQUETTES.json
   ```
4. **Comparer** avant et après votre modification :
   ```bash
   python -m methodologie_recherche.bancs.banc_collecte comparer AVANT.json APRES.json
   ```
   Gardez la modification si elle apporte plus de candidats **nouveaux**, **récents** et
   **pertinents** sans multiplier les refus.

Options utiles du banc : `--voies locale,assistee` (sans réseau), `--max-requetes 10`.
En session S08, ces commandes deviendront `ragc methodo test | bench | compare`.

## Modifier une méthodologie

```yaml
domaine: fiscalite_georgie
herite: juridique_fiscal        # par défaut : commun
langues: [fr, en, ka]
fraicheur_mois: 12              # sources de moins de 12 mois privilégiées
filtrer_par_date: false         # vrai : les API ne renvoient que la période
techniques: [dossier_local, openalex, wikipedia, liste_lecture]
gabarits:
  en:
    - "Georgia Tax Code {sujet}"
    - {texte: "{sujet} meta-analysis", sans_date: true}
sources_preferees: [matsne.gov.ge, rs.ge]
retirer: {techniques: [wikipedia]}   # enlève un élément hérité
```

- **Héritage** : valeurs simples remplacées ; listes additionnées (les vôtres d'abord) ;
  `retirer` enlève un élément hérité.
- **Gabarits** : `{sujet}` et `{annee}` sont remplacés. Le sujet peut être donné par langue
  (`{fr: "arnaque aux sentiments", en: "romance scam"}`).
- `angles_obligatoires` dit à l'agent ce que la recherche doit couvrir ; `criteres_tri` guide
  le tri des candidats ; `cadrage` rappelle la finalité (comprendre, prévenir, se soigner…).
- Une faute de frappe dans une clé est signalée par les tests.

## Le répertoire transversal

Une question comme « comment convaincre quelqu'un d'abandonner le véganisme ? » n'appartient à
aucun thème. Le répertoire fait apparaître ses angles **avant** la recherche :

- les **grilles** (`lentilles.yaml`) : chacune pose des questions sous-jacentes (que se passe-t-il
  déjà ? mécanisme, développement, fonction, évolution ? qui dit quoi à qui ? quels effets
  pervers ? où est la limite éthique ?) ; certaines s'appliquent toujours, d'autres selon le
  type de question ;
- les **disciplines** (`disciplines.yaml`) : ce que chacune apporte ;
- les **problèmes analogues** (`analogues.yaml`) : « faire changer quelqu'un d'une conviction qui
  fonde son identité » renvoie à la déconversion, à la sortie des groupes à forte emprise, au
  changement durable d'opinion… des littératures auxquelles on ne penserait pas.

Le modèle reçoit ce menu, propose plusieurs plans, puis une critique vérifie que chaque grille
est traitée ou écartée avec une raison. Une LoRA peut apprendre cette **procédure** ; le
**répertoire**, lui, reste ici, et c'est vous qui l'enrichissez.

Voir ce que le répertoire repère pour une question :
```bash
python -c "from methodologie_recherche.transversal.repertoire import charger_repertoire as c; \
from methodologie_recherche.transversal.exploration import explorer_transversal as e, rendre_menu as m; \
r = c(); print(m(e('Comment convaincre quelqu un d abandonner le véganisme ?', r), r))"
```

Ajoutez une discipline, une grille ou un problème analogue, puis lancez les tests : une
incohérence (type inconnu, discipline absente, groupe d'indices vide) est signalée.

## Ajouter ou modifier une technique

Copiez `collecteurs/modele_collecteur.py`, adaptez-le, déclarez-le dans `registre.yaml`, puis
lancez les tests : `verifier_conformite` signale tout écart au contrat. Une technique qui ne
se charge pas est **écartée et signalée** ; les autres continuent.

Règles du contrat :
- utiliser `self.http` (que les tests remplacent par des réponses simulées) ;
- appeler `self.patienter()` avant chaque appel : le rythme déclaré dans `politesse` est respecté ;
- vérifier `self.autorise(url)` avant de télécharger une page : **robots.txt est respecté** ;
- en cas de refus (`AccesRefuse`) ou de demande de ralentir (`Ralentir`, HTTP 429), **ne pas
  insister** : le logiciel bascule vers la **collecte assistée** (le lien vous est proposé dans
  la liste de lecture et c'est vous qui l'ouvrez).

Les techniques fournies ne contournent aucune protection (captcha, paywall, détection des
robots) et ne déguisent pas un programme en humain : un site qui refuse les programmes est
consulté par vous, dans votre navigateur.

## Clés et contacts (jamais dans le dépôt)

| Variable d'environnement | Pour | Effet |
|---|---|---|
| `RAGC_OPENALEX_CLE` | OpenAlex | clé gratuite (compte sur openalex.org) : budget quotidien 10 fois plus grand, réservé à vous |
| `RAGC_CONTACT` | Wikipédia | votre e-mail ou une URL dans l'agent utilisateur : 200 requêtes/minute au lieu de 10 |

Sans clé, OpenAlex partage un petit budget quotidien entre toutes les machines de la même
adresse IP, puis répond 429 ; sans contact, Wikimedia limite à 10 requêtes par minute. C'est
une cause fréquente de « l'API ne marche pas ».

## Ce qui reste à brancher (session S08)

Europe PMC, Crossref, Légifrance, BOFiP, le récupérateur poli de pages web, la surveillance du
dossier de téléchargements et le bouton « Envoyer au RAG » pour Brave.
