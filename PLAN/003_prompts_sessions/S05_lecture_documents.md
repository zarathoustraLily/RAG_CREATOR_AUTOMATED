# S05 — Lecture des documents : PDF scannés, livres, OCR spécialisé, figures, contrôle de l'OCR

> Jalon J1 · Dépend de : S04 · Étape : E2 (lecture) · Prompts d'exécution : L01, L02, L03
> Copiez tout ce qui suit la ligne `---` dans une nouvelle session.

---

Tu travailles sur le projet **RAG Creator** (dépôt `RAG_CREATOR_AUTOMATED`).

**Lis d'abord, dans cet ordre** : `PLAN/000_etat_de_l_art.md` (**§13**), `PLAN/001_but.md`
(§6, **§7 cas E**, §9), `PLAN/002_strategie.md` (§4.1, §4.2, **§4.7**, §7.2 « Lecture »),
`PLAN/003_prompts_sessions/00_regles_communes.md`, `PLAN/JOURNAL.md` (dont les résultats de S02
sur la vision de MiMo). Respecte-les. En cas de contradiction, arrête-toi et pose la question.

## Objectif

Que **tout document devienne du texte fidèle et cherchable** — en particulier les **livres et
PDF scannés** : texte natif quand il existe, **OCR spécialisé** sinon, **figures décrites** par
MiMo en vision, **structure du livre** retrouvée, et un **OCR contrôlé** qui n'invente jamais.
Rappel de l'état de l'art : les petits modèles OCR dédiés transcrivent plus fidèlement que les
modèles généralistes, qui ont tendance à « réécrire » ; MiMo sert à **comprendre** les images et
à **arbitrer**, pas à transcrire en masse.

## À réaliser

1. **Serveur OCR** : vérifie (documentation llama.cpp et fiches Hugging Face) la façon exacte de
   servir **GLM-OCR** et **PaddleOCR-VL-1.6** avec `llama-server`, leurs consignes (« OCR
   markdown »…) et leurs limites ; script `scripts/llama/start_ocr.sh` ; profil `ocr` dans la
   configuration ; `ragc doctor` teste l'OCR sur une image fournie avec les tests.
2. **Rendu des pages** (`ragcreator/ingest/reader/`) : pages `a_lire` (S04) et images isolées
   rendues en image (`pymupdf`, résolution configurable, ≈ 200–300 dpi), redressement simple si
   possible ; découpage d'une page très dense en bandes si le modèle l'exige.
3. **L01 `ocr_page`** : appel du modèle OCR (image au format OpenAI, température 0,1), sortie
   Markdown ; consignes propres à chaque modèle stockées comme prompts versionnés.
4. **Contrôle automatique** par page : proportion de mots reconnus dans la langue, répétitions
   en boucle, lignes tronquées, page vide, incohérences d'ordre de lecture (colonnes),
   tableaux mal formés → score de qualité et alertes dans `pages`.
5. **Second moteur et arbitrage** : sur un échantillon configurable de pages (ex. 5 %) et sur
   toute page suspecte, second moteur OCR (l'autre modèle, ou Tesseract en repli) ; comparaison
   ligne à ligne ; désaccords → **L03 `ocr_arbitration`** (MiMo en vision, réflexion) avec
   l'image et les deux transcriptions : texte retenu **seulement s'il est visible**, sinon
   `[illisible]`. Taux de désaccord par document → alerte si trop élevé.
6. **Figures** : détection des zones image, schémas, graphiques et photos ; **L02
   `figure_description`** (MiMo en vision) : type, description factuelle, légende, éléments
   lisibles, sans interprétation non visible ; table `figures` ; extraits de type `figure`
   liés à leur page.
7. **Structure des livres** : table des matières (signets PDF, sinon détection des titres),
   chapitres → sections, notes de bas de page rattachées, en-têtes et pieds de page retirés,
   **pagination imprimée** reliée à la page du fichier ; métadonnées (auteur, titre, édition,
   année, ISBN) depuis le PDF, la page de titre ou l'achevé d'imprimer ; deux éditions = deux
   versions (lignée de S04).
8. **Reprise** : un livre se lit page par page, avec reprise exacte après interruption ;
   priorité basse ; progression visible (`ragc docs show <id>` : pages lues / à lire / douteuses).
9. **Jeu de référence OCR** `tests/golden/ocr/` : pages fictives générées pour le projet (texte
   rédigé pour le projet, rendu en image) — page simple, deux colonnes, tableau, notes de bas de
   page, figure avec légende, page dégradée (flou, bruit, inclinaison), page en anglais ;
   transcriptions de référence. `ragc eval ocr [--live]` : taux d'erreur par caractère et par
   mot, **phrases inventées**, ordre de lecture, tableaux.
10. **Cas de référence E** `tests/cas_reference/E.yaml` : un « livre » fictif de quelques dizaines
    de pages (texte rédigé pour le projet), en version texte natif **et** en version scannée
    (images) ; questions dont la réponse est dans le livre ; métrique : Recall@5 sur la version
    scannée / Recall@5 sur la version native (cible ≥ 0,95) — à compléter quand la recherche
    existera (S07), la structure du test est posée dès maintenant.

## Expériences en conditions réelles (si disponibles)

GLM-OCR contre PaddleOCR-VL-1.6 sur le jeu de référence : erreurs, phrases inventées, tableaux,
temps par page ; MiMo en vision sur les mêmes pages (pour **confirmer** qu'il est moins fidèle en
transcription et le garder pour figures et arbitrage) ; temps de lecture d'un PDF scanné réel de
votre choix ; choix du moteur par défaut noté dans le journal.

## Critères d'acceptation

- [ ] Un PDF scanné déposé dans `inbox/` devient du texte structuré page par page, avec numéros de
      page imprimés, figures décrites et alertes de qualité.
- [ ] Aucune phrase inventée sur le jeu de référence (contrôlé automatiquement) ; les passages
      illisibles sont marqués `[illisible]`.
- [ ] Une couche texte dégradée (ancien OCR) est détectée et refaite.
- [ ] Reprise exacte après interruption au milieu d'un livre.
- [ ] Tests hors ligne avec un faux serveur OCR et un faux serveur de vision.
- [ ] Procédure de clôture appliquée.
