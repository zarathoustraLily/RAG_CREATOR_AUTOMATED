# S13 — Temps : versions, date de référence, veille (E14)

> Jalon J5 · Dépend de : S12 · Étape : E14 · Prompt d'exécution : C14
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§3**, §16), `PLAN/001_but.md`
(§3, §7 cas A et G), `PLAN/002_strategie.md` (**§4.5**, §6, §7.3), `PLAN/003_prompts_sessions/00_regles_communes.md`,
`PLAN/JOURNAL.md`. Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Que la base **reste vraie dans le temps** — la fiscalité géorgienne change souvent, les CVE
chaque jour, les recommandations cliniques évoluent — et que l'agent réponde **à la bonne date**.

## À réaliser

1. **Classes de volatilité** (profils) → `next_check_at` par document ; priorité aux sources
   souvent utilisées par l'agent.
2. **Veille** (tâche du travail en fond, P0 + P2) : re-récupération (en-têtes conditionnels,
   versions officielles des connecteurs), comparaison du texte normalisé ; si différent → **C14
   `update_check`** : changement substantiel ou cosmétique, nature (modification, abrogation,
   correction, rétractation, nouvelle version de recommandation), portée, date d'effet.
3. **Nouvelle version** : lignée, `valid_to` de l'ancienne, ré-exécution du pipeline pour la
   nouvelle, relations *modifie / abroge* ajoutées, fiches marquées à régénérer.
4. **Rétractations** scientifiques via Crossref ; **CVE** : statut (corrigé, exploité) mis à jour.
5. **« À revérifier »** dans le dossier quand la vérification est trop ancienne ; vérification
   **à la demande** d'une source décisive pendant une question (délai maximal, sans rechargement de
   modèle si elle demande un LLM : sinon reportée).
6. **Date de référence de bout en bout** : question « en 2023 » → ancienne version ; date
   implicite (« l'an dernier ») résolue ; contrôle déterministe des références juridiques citées.
7. **Commandes** : `ragc watch run|status`, `ragc docs versions <id>`, `ragc docs history <unit_ref>`.
8. **Tests** : changement cosmétique ignoré, modification substantielle → nouvelle version,
   abrogation, rétractation, « à revérifier », date de référence (cas A avec versions fictives).

## Bancs à ajouter

`ragc bench watch` : une passe de veille réelle sur les sources de la fiscalité géorgienne et
française — documents vérifiés, changements détectés, faux positifs, durée.

## Critères d'acceptation

- [ ] Aucune version non en vigueur dans les dossiers du cas A (contrôle déterministe).
- [ ] Une modification simulée crée une nouvelle version et met à jour graphe et fiches.
- [ ] Procédure de clôture appliquée.
