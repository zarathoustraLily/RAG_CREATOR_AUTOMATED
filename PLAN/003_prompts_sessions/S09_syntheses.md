# S09 — Fiches, résumés de communautés, synthèses de thème (E11)

> Jalon J3 · Dépend de : S08 · Étape du pipeline : E11 · Prompts : P11, P12, P13
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/001_but.md`, `PLAN/002_strategie.md` (§6, §7),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md`. Respecte-les. En cas de
contradiction, arrête-toi et pose la question.

## Objectif

Pré-calculer des **fiches de connaissance sourcées phrase par phrase** pour les entités
importantes et des **synthèses par thème**, afin que le modèle consommateur obtienne une réponse
dense et fiable en un seul appel, et que vous puissiez lire ce que le RAG « sait ».

## À réaliser

1. **Sélection des entités à ficher** : par thème, selon mentions, degré dans le graphe et
   centralité ; quota configurable.
2. **Gabarits de fiches par type** (configurables, surchargeables par charte) — ex. organisme :
   identification sommaire, composés actifs, effets, toxicité et symptômes, confusions,
   points de désaccord ; molécule : cibles, mécanisme, effets, toxicité, données de dose
   (toujours marquées), interactions.
3. **Prompt P11 `entity_card`** (réflexion activée, profil préféré `qwen38-27b` avec repli) :
   entrées = entité, alias, relations, extraits numérotés `[c:ID]` avec marquages de
   croisement ; sortie = sections du gabarit, **chaque phrase suivie de ses citations**, section
   « points de désaccord » alimentée par les affirmations contradictoires, `null` si rien.
4. **Contrôle des citations par le code** : identifiant inconnu ou phrase sans citation →
   nouvelle tentative avec l'erreur, puis suppression de la phrase fautive ; une affirmation
   sensible doit porter son statut de croisement.
5. **Prompt P12 `community_summary`** (sans réflexion) : résumé d'un groupe d'entités liées.
6. **Prompt P13 `theme_synthesis`** (réflexion activée) : synthèse du thème à partir de ses
   fiches et résumés de communautés ; pour un thème parent, **agrège les synthèses de ses
   enfants** (ordre feuilles → racine).
7. **Stockage et indexation** : table `cards` ; fiches et synthèses indexées comme extraits de
   type `fiche` (prioritaires au routage, S11) ; **régénération seulement si les entrées
   changent** (empreinte des entrées).
8. **Export lisible** : `themes/<chemin>/fiches/<entité>.md` et `themes/<chemin>/synthese.md`
   avec liens vers les sources.
9. **Commandes** : `ragc synth run [--theme]`, `ragc synth show <entité|chemin>`.
10. **Tests** : contrôle des citations (valide, inconnue, absente), idempotence par empreinte,
    agrégation parent/enfants.

## Expériences en conditions réelles (si disponible)

Fiche d'*Amanita muscaria* et du muscimol : taux de phrases citées valides avant correction,
temps de génération, relecture humaine de 2 fiches (exactitude, utilité). Note dans le journal.

## Critères d'acceptation

- [ ] Les fiches Markdown générées ne contiennent **aucune** citation invalide.
- [ ] Les contradictions de S08 apparaissent dans « points de désaccord ».
- [ ] Relancer `ragc synth run` sans changement des entrées ne régénère rien.
- [ ] Procédure de clôture appliquée.
