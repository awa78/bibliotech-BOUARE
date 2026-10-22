# BiblioTech

Application en ligne de commande de gestion d'une bibliothèque municipale : catalogue, membres, emprunts, retours, pénalités de retard, rappels et rapports.

Projet fil rouge du module *Clean Code et Qualité logicielle*, réalisé individuellement par **Awa BOUARE**. Le travail comprend le **TP1 (nettoyage)**, le **TP2 (refactoring et tests unitaires)**, puis une soutenance.

Le point de départ est une application fonctionnelle volontairement difficile à maintenir. L'objectif est d'améliorer sa lisibilité et sa structure en préservant les comportements vérifiés par les tests de caractérisation. Ce README présente le bilan du travail ; [SYNTHESE_TP1.md](SYNTHESE_TP1.md) conserve le journal détaillé des corrections, essais et difficultés.

## État du projet avant le TP2

| Étape | État |
| --- | --- |
| TP1 : nettoyage et corrections de revue | Réalisés sur `tp1/nettoyage` |
| Remise du TP1 | [Pull request nº 1](https://github.com/awa78/bibliotech-BOUARE/pull/1) |
| Version initiale de comparaison | Étiquette Git `v0-initial` |
| TP2 : refactoring et tests unitaires | Étape 1 : préparation et mesure initiale effectuées ; commit et publication en attente |
| Soutenance | À préparer après le TP2 |

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
| `Library.borrow_document` | C | 18 | À mesurer |
| `process` | C | 16 | À mesurer |
| `Library.report` | C | 14 | À mesurer |

La commande affiche seulement les blocs de note C ou supérieure : aucune note D n'est signalée à ce départ. Les résultats diffèrent de l'exemple du guide, car le code a déjà été amélioré au TP1. L'objectif du niveau 2 reste d'obtenir une méthode `borrow` de note A. Les niveaux obligatoires et les nouveaux tests unitaires restent à réaliser.

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
