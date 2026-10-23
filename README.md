# BiblioTech

Application en ligne de commande de gestion d'une bibliothèque municipale : catalogue, membres, emprunts, retours, pénalités de retard, rappels et rapports.

Projet fil rouge du module *Clean Code et Qualité logicielle*, réalisé individuellement par **Awa BOUARE**. Le travail comprend le **TP1 (nettoyage)**, le **TP2 (refactoring et tests unitaires)** et un **TP3 à venir**, dont les consignes restent à intégrer.

Le point de départ est une application fonctionnelle volontairement difficile à maintenir. L'objectif est d'améliorer sa lisibilité et sa structure en préservant les comportements vérifiés par les tests de caractérisation. Ce README présente le bilan du travail ; [SYNTHESE_TP1.md](SYNTHESE_TP1.md) conserve le journal détaillé des corrections, essais et difficultés.

## Tableau récapitulatif des travaux réalisés

Ce tableau regroupe les réalisations confirmées. Les résultats correspondent aux contrôles effectués à chaque étape ; la ligne TP3 sera complétée après réception des consignes et réalisation du travail.

| TP | Axe de travail | Travaux réalisés | Résultat ou vérification | État |
| --- | --- | --- | --- | --- |
| TP1 | Préparation et Git | Installation dans `.venv`, dépôt personnel, branche `tp1/nettoyage`, étiquette `v0-initial` publiée | Point de départ : 21 tests réussis et 55 signalements Ruff | Réalisé |
| TP1 | Lisibilité | Imports explicites et triés, suppression d'un import inutilisé, conditions et affectations simplifiées, renommage de méthodes, formatage Ruff | Tests de caractérisation conservés et vérifiés au fil des changements | Réalisé |
| TP1 | Fichiers et état partagé | Cinq ouvertures de fichiers avec `with`, suppression du dictionnaire mutable par défaut dans `register_plugin` | Scénarios fournis réussis après les modifications | Réalisé |
| TP1 | Règles et duplication | Durées nommées puis dictionnaires `LOAN_DAYS`, `DAILY_FEE`, `MAX_LOANS` ; extraction de `calculate_late_fee` et remplacement des quatre copies | Calcul commun utilisé dans les retours, les retards, le rapport et l'export | Réalisé ; fonction adaptée en `late_fee` au TP2 |
| TP1 | Corrections de revue | `float` remplace `eval`, exceptions précisées, erreurs de plugins journalisées, `pass` inutile supprimé, f-strings et `join`, arrondi redondant supprimé, commentaires | Fin du TP1 : 21 tests réussis et 5 signalements Ruff ; contrôles ciblés de sécurité et de plugins effectués hors dépôt | Réalisé |
| TP1 | Documentation et remise | Journal dans `SYNTHESE_TP1.md`, bilan dans le README, commits progressifs et pull request nº 1 | TP1 fusionné par l'enseignant | Terminé |
| TP2 | Préparation et mesure initiale | Branche `tp2/refactoring`, configuration `pythonpath` pour pytest, ajout de Radon | 21 tests réussis ; Radon initial : emprunt C (18), `process` C (16), `report` C (14) | Réalisé |
| TP2 | Tests avant refactoring | `tests/test_rules.py` : 10 cas paramétrés ; `tests/test_borrow.py` : 6 tests ; fixture temporaire et date fixe dans `tests/conftest.py` | Rouge d'import attendu sur `late_fee`, puis vérification des règles et des emprunts | Réalisé |
| TP2 | Niveau 1 : fonction pure | Ajout de `late_fee`, remplacement des appels dans `ret`, `overdue`, `report`, `export`, puis suppression de `calculate_late_fee` | Une implémentation commune ; 37 tests réussis | Réalisé |
| TP2 | Niveau 2 : clauses de garde | Extraction de `has_overdue_loan`, `is_borrowing`, `refusal_reason`, `create_loan` ; méthode principale renommée en `borrow`, appels et tests mis à jour | `borrow` A (4), aucune fonction en note D ou supérieure ; 37 tests réussis | Réalisé |
| TP2 | Documentation et remise | README avec mesures avant/après, commits nommés, branche publiée et pull request nº 2 ouverte | Relecture du professeur et validation à confirmer avant fusion | Réalisations publiées ; revue à confirmer |
| TP3 | À préciser selon le guide | Aucun travail TP3 réalisé à ce stade | Mesures, tests, livrables et lien de remise à renseigner après réalisation | À venir |

**Repères de lecture :** les 5 signalements Ruff correspondent à la fin du TP1. Le contrôle effectué lors de la préparation de la présentation du TP2 en comptait 8 : 4 de complexité et 4 de style. Ces mesures sont distinctes des notes Radon et des résultats des tests. Aucun bonus du TP2 n'a été réalisé.

## État du projet et remises

| Étape | État |
| --- | --- |
| TP1 : nettoyage et corrections de revue | Réalisés sur `tp1/nettoyage` |
| Remise du TP1 | [Pull request nº 1](https://github.com/awa78/bibliotech-BOUARE/pull/1) |
| Version initiale de comparaison | Étiquette Git `v0-initial` |
| TP2 : refactoring et tests unitaires | Niveaux 1 et 2 vérifiés et publiés dans la [pull request nº 2](https://github.com/awa78/bibliotech-BOUARE/pull/2) ; revue et validation à confirmer |
| TP3 | À venir ; consignes non encore intégrées |
| Présentation du travail | Supports TP1 et TP2 préparés ; à compléter après le TP3 |

Le TP1 a été fusionné par l'enseignant et récupéré sur `main` avant la création de la branche du TP2. Le suivi ci-dessous distingue les étapes effectuées et celles restant à réaliser.

## TP1 — Travail réalisé

### Corrections et justification

| Problème initial | Travail effectué | Intérêt |
| --- | --- | --- |
| Imports multiples, implicites ou inutilisés | Imports séparés, explicites et triés ; suppression de `json` inutilisé | Dépendances plus faciles à identifier |
| Comparaisons booléennes et conditions imbriquées | Conditions directes, `is None` et `is not None`, regroupement de critères avec `and` | Lecture plus simple |
| Noms vagues | `do_stuff` devient `borrow_document` ; `nb` devient `count_active_loans` | Intentions explicites |
| Durées, tarifs et limites dispersés | Dictionnaires `LOAN_DAYS`, `DAILY_FEE` et `MAX_LOANS` | Règles métier regroupées et valeurs par défaut conservées |
| Calcul des pénalités copié quatre fois | Fonction commune `calculate_late_fee`, utilisée dans `ret`, `overdue`, `report` et `export` | Application de DRY ; une seule règle à maintenir |
| Fichiers fermés manuellement | Utilisation de `with` pour les cinq ouvertures de fichiers | Fermeture même en cas d'erreur |
| `eval` utilisé pour lire les prix | Remplacement par `float` | Un prix de CSV ne peut plus être exécuté comme du code Python |
| Erreurs masquées | Exceptions de conversion précisées ; erreurs des plugins journalisées avec leur trace | Diagnostic possible sans arrêter les plugins suivants |
| Dictionnaire mutable par défaut | `options=None`, puis création d'un dictionnaire pour chaque appel | Évite le partage implicite d'état |
| Présentation irrégulière et longues concaténations | Formatage Ruff, f-strings et `join` pour les messages et CSV | Code plus lisible, sorties conservées dans les scénarios testés |
| Documentation insuffisante | Commentaires sur les règles, valeurs par défaut et choix importants | Préparation de la maintenance et de la soutenance |

La fonction `calculate_late_fee` gère l'absence de retard, le tarif journalier, les réductions étudiant/premium, le plafond au prix du document et l'arrondi au centime. L'arrondi redondant dans le cumul du rapport a été supprimé après revue.

### Résultats et vérifications du TP1

| Indicateur | Version initiale | Fin du TP1, après revue |
| --- | --- | --- |
| Tests de caractérisation fournis | 21 réussis | 21 réussis |
| Signalements Ruff | 55 | 5, tous liés à la complexité (`C901`) |
| Emplacements du calcul des pénalités | 4 copies | 1 fonction commune et 4 appels |

Les fichiers `tests/test_caracterisation.py`, `tests/golden/` et les données de référence sont restés inchangés. Les tests vérifient les scénarios fournis : leur réussite ne prouve pas l'absence de bugs dans tous les cas possibles.

Des vérifications ciblées supplémentaires ont été exécutées pendant la revue : rejet d'une expression Python dans un prix sans exécution, présence du nom et de la trace d'un plugin défaillant dans les journaux, poursuite du plugin suivant, propagation de `SystemExit`, tarifs, réductions, plafond et cas sans retard. Le script de vérification était extérieur au dépôt ; ces contrôles ne constituent pas encore une suite de tests unitaires versionnée. Celle-ci sera ajoutée au TP2.

### Difficultés rencontrées et solutions

- Accès refusé au dossier temporaire de pytest et à son cache : utilisation d'un autre dossier temporaire et désactivation du cache pour les exécutions concernées.
- Collage du préfixe PowerShell avec la commande : exécution des commandes seules, une à la fois.
- Conflit entre un onglet VS Code ancien et le fichier enregistré : rechargement depuis le disque avant reprise des modifications.
- Erreurs d'indentation dans le compteur de l'export : diagnostic par `git diff`, puis correction avant commit.
- Renommage incomplet de la méthode d'emprunt et constantes non définies : mise en cohérence des définitions et des appels, puis nouvelle exécution des tests.

Les échecs observés et leur résolution sont détaillés dans [SYNTHESE_TP1.md](SYNTHESE_TP1.md). Les corrections ont été enregistrées par étapes ; les remarques de revue ont donné lieu à de nouveaux commits. Le formatage initial et les corrections de revue sont identifiables par commit, sans réécriture de l'historique publié.

### Limites et transition vers le TP2

Cinq fonctions restent au-dessus du seuil de complexité Ruff : `load`, `find`, `borrow_document`, `report` et `process`. Cette mesure Ruff est distincte de la mesure Radon présentée ci-dessous.

Le calcul des pénalités et les dictionnaires de règles ayant déjà été introduits au TP1, le TP2 partira de cet état réel. Il faudra notamment :

1. Préparer `main` et la branche `tp2/refactoring`, configurer pytest et installer Radon.
2. Écrire les tests unitaires des pénalités et adapter le calcul au contrat `late_fee(days_late, kind, member_type, price)` demandé.
3. Tester les comportements d'emprunt avant de réorganiser la méthode avec des clauses de garde et les méthodes prévues par le guide.
4. Mesurer la complexité avant/après, puis documenter la revue croisée et les corrections.

Cette liste décrit le travail prévu, pas le travail effectué. Les résultats et les éventuels bonus seront ajoutés à ce README au fur et à mesure du TP2.

## TP2 — Suivi du refactoring

### Avancement actuel

Mise à jour après la section 3.4 : les niveaux obligatoires 1 et 2 ont passé leurs vérifications. Les entrées suivantes retracent les étapes précédentes.

### Section 3.4 — Renommage final et mesure après refactoring

- Clauses de garde enregistrées dans le commit `45dbfc3`.
- Renommage de `borrow_document` en `borrow`, avec mise à jour de l'appel dans `process()` et des huit appels dans les six tests d'emprunt.
- Vérification transmise : **37 tests réussis en 4,37 s** (21 de caractérisation, 6 d'emprunt et 10 de pénalités).
- `radon cc -s -n C bibliotech.py` affiche uniquement `process` C (16) et `report` C (14) : aucune fonction en note D ou supérieure.
- `radon cc -s bibliotech.py` confirme **borrow A (4)**, contre **borrow_document C (18)** au départ ; `refusal_reason` B (6), `has_overdue_loan` A (4), `is_borrowing` A (4) et `create_loan` A (3).
- Critères techniques obligatoires vérifiés : calcul unique dans `late_fee`, tests verts, méthode `borrow` en A et aucune fonction en D. Aucun bonus réalisé.
- État : commit de la section 3.4 en attente, puis publication et pull request selon le modèle du guide. La revue croisée et la validation de l'enseignant restent nécessaires avant fusion.

Historique des étapes précédentes :

- Niveau 1 terminé avec le commit `e960d2d` : une fonction `late_fee`, quatre appels et 37 tests réussis au dernier contrôle.
- Niveau 2, section 3.1 : les six tests d'emprunt sont déjà écrits et enregistrés.
- Section 3.2 vérifiée : `LOAN_DAYS` contient 21/7/3 jours ; `MAX_LOANS` contient les limites standard 3, étudiant 5 et premium 8. Ces dictionnaires sont déjà utilisés dans la méthode d'emprunt et se trouvent à côté de `DAILY_FEE`. Aucune modification supplémentaire n'est nécessaire pour cette section, réalisée au TP1 après revue.
- Prochaine étape : section 3.3, décomposer l'emprunt avec les méthodes demandées et des clauses de garde, en conservant l'ordre des refus et leurs messages. Aucun bonus n'est entrepris.

### Section 3.3 — Extraire la recherche d'un emprunt en retard

- Ajout de `has_overdue_loan(member_id)`, méthode demandée par le guide, avec une expression `any` sur les emprunts non rendus du membre dont l'échéance est dépassée.
- Remplacement de la boucle et du drapeau dans `borrow_document()` par `late = self.has_overdue_loan(mid)`, sans modifier les refus ni leur ordre.
- Résultat transmis : **37 tests réussis en 4,36 s**.
- État : extraction vérifiée ; commit en attente. Les autres méthodes de la section 3.3 et le renommage final en `borrow` restent à réaliser.

### Section 3.3 — Extraire la recherche d'un document déjà emprunté

- L'extraction de `has_overdue_loan` a été enregistrée dans le commit `0c240e7`.
- Ajout de `is_borrowing(member_id, book_id)` avec `any` pour vérifier l'existence d'un emprunt non rendu du membre pour ce document.
- Remplacement de la boucle et du drapeau par `deja = self.is_borrowing(mid, bid)`, en conservant le refus existant et sa priorité.
- Résultat transmis : **37 tests réussis en 4,97 s**.
- État : extraction vérifiée ; commit en attente. La section 3.3 continue ensuite avec les méthodes restantes et les clauses de garde.

### Section 3.3 — Clauses de garde : remplacement incomplet détecté

- Extraction de `is_borrowing` enregistrée dans le commit `18c5bd8`.
- Ajout de `refusal_reason` et de `create_loan` pour séparer les refus et la création d'un emprunt.
- Premier essai transmis après suppression de l'ancien bloc : **13 tests échoués et 24 réussis en 4,92 s**.
- Diagnostic avec `git diff` : la méthode `borrow_document` a été supprimée, mais le nouveau bloc de clauses de garde n'a pas été ajouté dans le fichier enregistré. Les tests et `process` appellent donc une méthode absente.
- Correction effectuée : insertion de `borrow_document(member_id, book_id)` avec sorties immédiates pour un membre inconnu, un document inconnu et un motif de refus ; délégation à `refusal_reason` et `create_loan`.
- Nouvelle vérification transmise : **37 tests réussis en 4,59 s**. Les messages et les scénarios existants restent vérifiés. Section 3.3 prête à être commitée ; le renommage en `borrow` et la mise à jour des appels restent à faire en section 3.4.

### Étape 1 : préparation du dépôt — 22 octobre 2026

- Fusion du TP1 par l'enseignant, récupérée sur `main` au commit `7481492`.
- Création de la branche `tp2/refactoring` depuis cette version.
- Récupération du README préparé avant le TP2 par cherry-pick (`c3c1cc5`), car cette mise à jour n'était pas incluse dans la fusion du TP1.
- Ajout de `pythonpath = ["."]` dans la configuration pytest et de `radon>=6.0` dans les dépendances ; Radon 6.0.1 installé dans `.venv`.
- Vérification de départ transmise : **21 tests réussis en 4,90 s**. Aucun refactoring du TP2 n'a encore été effectué.

### Mesure Radon avant refactoring

Commande exécutée : `radon cc -s -n C bibliotech.py`.

| Fonction | Note initiale TP2 | Complexité initiale TP2 | Après refactoring |
| --- | --- | --- | --- |
| `Library.borrow_document` → `Library.borrow` | C | 18 | A (4) |
| `process` | C | 16 | C (16) |
| `Library.report` | C | 14 | C (14) |

La commande affiche seulement les blocs de note C ou supérieure : aucune note D n'est signalée à ce départ. Les résultats diffèrent de l'exemple du guide, car le code a déjà été amélioré au TP1. L'objectif du niveau 2 reste d'obtenir une méthode `borrow` de note A. Les niveaux obligatoires et les nouveaux tests unitaires restent à réaliser.

### Tests avant refactoring — sections 2.1 et 3.1

- Préparation enregistrée dans le commit `16847fe`, puis branche `tp2/refactoring` publiée, selon les sorties du terminal transmises.
- Section 2.1 : création de `tests/test_rules.py` avec les cas de pénalité paramétrés. Le lancement ciblé produit l'ImportError attendue : `late_fee` n'existe pas encore sous ce nom. Ce rouge attendu n'est pas commité.
- Vérification séparée de `tests/test_caracterisation.py` : **21 tests réussis en 4,99 s** ; aucune régression constatée dans ces scénarios.
- Section 3.1 : création de `tests/conftest.py` avec la fixture du guide, qui copie les données et fixe la date au 21 octobre 2026.
- Section 3.1 : `tests/test_borrow.py` contient les six cas demandés, avec le nom actuel `borrow_document` à la place de `do_stuff` : membre inactif, retard existant, document déjà emprunté, indisponibilité, limite atteinte et emprunt accepté avec identifiant L013 et échéance au 28 octobre 2026.
- Vérification progressive : les tests d'emprunt passent de 1 à 6 cas réussis au fil de leur ajout. Vérification commune transmise : `tests/test_borrow.py` et `tests/test_caracterisation.py` donnent **27 tests réussis en 4,57 s**.
- `tests/test_rules.py` reste temporairement exclu de cette vérification ciblée : son erreur d'import sur `late_fee` est toujours le rouge attendu de la section 2.1. Il ne doit pas être commité avant l'ajout de la fonction et le passage au vert.
- Section 3.1 : tests des emprunts enregistrés dans le commit `fe6e0d9`, confirmé par le terminal de l'utilisatrice.
- Aucun bonus n'est entrepris.

### Section 2.2 — Ajouter la fonction late_fee à côté du calcul existant

- Ajout de `late_fee(days_late: int, kind: str, member_type: str, price: float) -> float`, avant `calculate_late_fee`, sans modifier les quatre appels existants.
- La fonction utilise `DAILY_FEE`, une clause de garde sans retard, les réductions étudiant/premium, `min` pour le plafond et `round(..., 2)` pour l'arrondi.
- Les 10 cas paramétrés de `tests/test_rules.py` vérifient les résultats avec `pytest.approx`.
- Résultat transmis : **37 tests réussis en 4,34 s** (21 de caractérisation, 6 d'emprunt, 10 de pénalités). Le rouge attendu de la section 2.1 est résolu.
- État : fonction et tests prêts à être commités ensemble. Prochaine étape : section 2.3, remplacer les appels un par un, avec tests et commit après chacun. Le calcul existant sera retiré quand il ne sera plus utilisé.

### Section 2.3 — Premier remplacement dans ret : diagnostic

- La fonction et ses tests ont été enregistrés dans le commit `bd98aa7`.
- Premier remplacement : appel à `late_fee(d, bk["kind"], mb["type"], bk["price"])` dans `ret()`.
- Premier essai transmis : **33 tests réussis et 4 échoués en 4,52 s**, concernant les retours.
- Diagnostic par `git diff` : modification involontaire de `datetime.strptime` en `datetime.strptie` dans le calcul des jours (ligne 265). L'appel à `late_fee` est correct.
- Correction effectuée : rétablissement de `strptime`. Nouvelle sortie transmise : **37 tests réussis en 4,31 s**. Le premier remplacement dans `ret()` est validé ; commit en attente. Les tests de caractérisation et leurs références restent inchangés.

### Section 2.3 — Deuxième remplacement dans overdue

- Le remplacement dans `ret()` a été enregistré dans le commit `e819945`.
- Remplacement de l'appel de `overdue()` par `late_fee(nbj, book["kind"], member["type"], book["price"])`, sans modifier le calcul des jours ni les affichages.
- Résultat transmis : **37 tests réussis en 5,15 s**. Deuxième remplacement validé ; commit en attente. Les appels de `report()` et `export()` restent à adapter.

### Section 2.3 — Troisième remplacement dans report

- Le remplacement dans `overdue()` a été enregistré dans le commit `ba98289`.
- Remplacement de l'appel de `report()` par `late_fee(j, bk["kind"], mb["type"], bk["price"])`, en conservant le calcul des jours et le cumul des pénalités.
- Résultat transmis : **37 tests réussis en 5,01 s**. Troisième remplacement validé ; commit en attente. L'appel de `export()` reste à adapter avant de retirer le calcul devenu inutilisé.

### Section 2.3 — Quatrième remplacement dans export et fin du niveau 1

- Le remplacement dans `report()` a été enregistré dans le commit `d01647c`.
- Remplacement du dernier appel par `late_fee(dl, bk["kind"], mb["type"], bk["price"])` dans `export()`, en conservant la remise à zéro des jours négatifs. Vérification transmise : **37 tests réussis en 5,11 s**.
- Suppression de `calculate_late_fee`, devenue inutilisée. Vérification après suppression : **37 tests réussis en 4,81 s**.
- Contrôle du fichier : une définition de `late_fee` et quatre appels, dans `ret`, `overdue`, `report` et `export` ; aucune référence à `calculate_late_fee`.
- Le contrat du niveau 1 est couvert par les 10 cas paramétrés. Les 21 tests de caractérisation et les 6 tests d'emprunt restent verts.
- État : niveau 1 vérifié ; dernier commit de l'extraction en attente. Les cinq commits attendus correspondent à l'ajout de la fonction avec ses tests, puis aux quatre remplacements progressifs.
- Prochaine étape : niveau 2, section 3.2. Les tests de la section 3.1 sont déjà enregistrés ; vérifier les dictionnaires métier existants avant les clauses de garde de la section 3.3.

## Installation

Python 3.10 ou plus récent est nécessaire.

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
pip install -r requirements.txt
```

Sous Windows PowerShell, l'activation s'effectue avec :

```powershell
.\.venv\Scripts\Activate.ps1
```

## Utilisation

```bash
python bibliotech.py list                    # catalogue et disponibilités
python bibliotech.py members                 # membres et emprunts en cours
python bibliotech.py borrow M005 B005        # emprunter un document
python bibliotech.py return L004             # rendre un document
python bibliotech.py overdue                 # retards et envoi des rappels
python bibliotech.py report                  # rapport d'activité
python bibliotech.py export emprunts.csv     # export des emprunts
```

L'option `--today AAAA-MM-JJ` permet de simuler une autre date, par exemple :

```bash
python bibliotech.py overdue --today 2026-10-21
```

Les données se trouvent dans le dossier `data/`. Les commandes `borrow` et `return` modifient `data/loans.csv` : pour revenir aux données d'origine, lancez `git restore data/`.

## Règles métier

| Règle | Valeur |
| --- | --- |
| Durée d'emprunt | livre 21 jours, DVD 7 jours, magazine 3 jours |
| Emprunts simultanés maximum | standard 3, étudiant 5, premium 8 |
| Pénalité par jour de retard | livre 0,50 €, DVD 1,00 €, magazine 0,20 € |
| Réduction sur les pénalités | étudiant 50 %, premium 100 % |
| Plafond de la pénalité | prix du document |

Un emprunt est refusé si le membre est inactif, s'il a un emprunt en retard, s'il a atteint sa limite, s'il a déjà ce document, ou s'il ne reste aucun exemplaire.

## Tests

```bash
pytest
```

Le dossier `tests/` contient des **tests de caractérisation** : ils lancent l'application et comparent sa sortie à des résultats de référence. Ils ne dépendent pas de l'organisation interne du code. Leur réussite indique que les comportements couverts sont préservés après les modifications de `bibliotech.py`.

Commande utilisée sous PowerShell en cas de problème d'accès au dossier temporaire ou au cache :

```powershell
python -m pytest -q -p no:cacheprovider --basetemp "$env:TEMP\bibliotech-tests-awa"
```

Le dossier indiqué par `--basetemp` est réservé à ces tests : pytest peut le vider lors d'une nouvelle exécution.

Ne modifiez pas `tests/test_caracterisation.py` ni le dossier `tests/golden/`.

## Analyse statique

```bash
ruff check .            # signaler les problèmes
ruff check . --fix      # corriger automatiquement ce qui peut l'être
ruff format .           # mettre en forme le code
```

## Règles du jeu

1. Lancez `pytest` avant de commencer : tout doit être vert.
2. Travaillez par petits pas : une amélioration, puis `pytest`, puis un commit.
3. Ne committez jamais avec un test rouge.
4. Un message de commit explicite par amélioration.
5. Notez chaque correction dans votre fichier de synthèse.
