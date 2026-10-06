# S11 — Temps : versions, date de référence, veille d'actualisation (E14)

> Jalon J4 · Dépend de : S10 · Étape : E14 · Prompt d'exécution : C14
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§3**), `PLAN/001_but.md`
(§3, §7 cas A), `PLAN/002_strategie.md` (**§3.5**, §5, §6.3), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Que la base **reste vraie dans le temps** : surveiller les sources selon leur volatilité,
détecter les modifications, abrogations et rétractations, créer de nouvelles versions sans
perdre les anciennes, et garantir de bout en bout que l'agent répond **à la bonne date**.

## À réaliser

1. **Classes de volatilité** (profils) → `next_check_at` par document ; priorité aux sources
   souvent consultées par l'agent (`research_runs`).
2. **Veille** (`ragcreator/temporal/watch.py`) : re-récupération (en-têtes conditionnels),
   comparaison du texte normalisé ; si différent → **C14 `update_check`** (réflexion) : changement
   substantiel ou cosmétique ? nature (modification, abrogation, correction, rétractation),
   portée, date d'effet.
3. **Nouvelle version** : lignée, `valid_to` de l'ancienne, ré-exécution E6–E10 pour la nouvelle,
   relations normatives *modifie / abroge* ajoutées au graphe, conflits re-qualifiés
   (« évolution »), fiches concernées marquées à régénérer (S12).
4. **Rétractations scientifiques** : vérification périodique via le connecteur Crossref ;
   document rétracté → étiquette, solidité à zéro, alerte dans les dossiers.
5. **Marquage « à revérifier »** quand la dernière vérification dépasse la période de volatilité ;
   visible dans le dossier ; vérification **à la demande** possible depuis l'agent pour une source
   décisive (option, avec délai maximal).
6. **Date de référence de bout en bout** : tests sur le cas A — question « en 2023 » → ancienne
   version ; question d'aujourd'hui → nouvelle ; version abrogée jamais présentée comme actuelle ;
   date implicite (« l'an dernier ») correctement résolue.
7. **Contrôles déterministes** (EdA §3) : pour toute référence juridique citée dans un dossier,
   vérification par le code que la version citée est en vigueur à la date de référence.
8. **Commandes** : `ragc watch run [--theme] [--due]`, `ragc watch status`,
   `ragc docs versions <id>`, `ragc docs history <unit_ref>`.
9. **Tests** : changement cosmétique ignoré, modification substantielle → nouvelle version,
   abrogation, rétractation, marquage « à revérifier », date de référence.

## Expériences en conditions réelles (si disponibles)

Une passe de veille sur les sources des cas A et D : documents vérifiés, changements détectés,
faux positifs (changements cosmétiques pris pour substantiels), temps. Relance des cas A–E.

## Critères d'acceptation

- [ ] Le contrôle déterministe ne trouve aucune version non en vigueur dans les dossiers du cas A.
- [ ] Une modification simulée d'un article crée une nouvelle version et met à jour graphe et
      conflits.
- [ ] Une rétractation simulée fait chuter la solidité et apparaît dans le dossier.
- [ ] Procédure de clôture appliquée.
