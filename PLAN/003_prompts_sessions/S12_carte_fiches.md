# S12 — Carte navigable et fiches (E12)

> Jalon J4 · Dépend de : S11 · Étape : E12 · Prompts d'exécution : C11, C12
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§4**, §5, §8),
`PLAN/001_but.md` (§3, §7), `PLAN/002_strategie.md` (**§3.1**, §3.2, §6.1, §7),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Transformer l'arbre des thèmes en une **carte** que l'agent parcourt (une fiche de nœud par
rayon, du plus précis au plus général), et pré-calculer des **fiches d'entités sourcées phrase
par phrase**. La carte permet à l'agent de relier une question à des thèmes qu'elle ne nomme
pas ; les fiches lui donnent des réponses denses et fiables.

## À réaliser

1. **C12 `node_card`** (réflexion activée) — pour chaque nœud, **des feuilles vers la racine** :
   ce que contient ce rayon (en langage simple), sous-thèmes et leur contenu, **questions types
   auxquelles il sait répondre**, points clés, chiffres de couverture, lacunes connues, profil et
   échelle de solidité, liens vers des rayons voisins utiles (ex. *négociation* ↔ *économie
   comportementale*).
2. **Fichiers de navigation** sur disque (EdA §4) : `themes/<chemin>/index.md` (fiche de nœud +
   liens), un `CARTE.md` racine ; métadonnées en tête de fichier (sujet, type, provenance, date).
3. **Sélection des entités à ficher** : mentions, degré dans le graphe, fréquence dans les
   dossiers de l'agent (`research_runs`) ; quota configurable.
4. **Gabarits de fiches par profil** (définis en S03) — ex. organisme, molécule, texte de loi
   (objet, champ d'application, conditions, exceptions, versions, jurisprudence liée), notion
   comportementale (définition, mécanisme, niveau de preuve, réplication, conditions
   d'application, limites).
5. **C11 `entity_card`** (réflexion activée, profil préféré `qwen38-27b`) : sections du gabarit,
   **chaque phrase suivie de ses citations** `[c:ID]`, solidité indiquée, « points de désaccord »
   alimentés par les conflits qualifiés (S10), validité temporelle (S11).
6. **Contrôle des citations par le code** : identifiant inconnu ou phrase sans citation → nouvelle
   tentative, puis suppression de la phrase ; affirmation sensible sans statut de croisement →
   refus.
7. **Régénération par empreinte des entrées** ; régénération forcée quand S11 crée une nouvelle
   version d'une source utilisée.
8. **Intégration à l'agent** : Q02 lit les **fiches de nœud** comme carte (au lieu des chartes
   résumées) ; l'escalade de l'exécuteur peut lire une fiche d'entité ; les fiches indexées comme
   extraits de type `fiche`.
9. **Commandes** : `ragc map [--depth N]`, `ragc synth run [--theme]`, `ragc synth show <entité|chemin>`.
10. **Tests** : ordre feuilles → racine, contrôle des citations, empreinte, fiches de nœud lues
    par Q02 (faux serveur).

## Expériences en conditions réelles (si disponibles)

Cas B : la carte permet-elle au plan de trouver *négociation*, *économie comportementale* et
*neurosciences* sans que la question les nomme ? Qualité du plan avant / après la carte ;
relecture humaine de 3 fiches. Relance des cas A–E.

## Critères d'acceptation

- [ ] `ragc map` affiche une carte lisible ; `themes/**/index.md` existent et sont à jour.
- [ ] Aucune citation invalide dans les fiches ; conflits présents dans « points de désaccord ».
- [ ] La qualité du plan du cas B progresse ou reste stable avec la carte (mesure notée).
- [ ] Procédure de clôture appliquée.
