# BiblioTech

Application Python en ligne de commande pour gérer une bibliothèque : catalogue, membres, emprunts, retours, pénalités, rappels, rapports et exports CSV.

Projet fil rouge du module **Clean Code et Qualité logicielle**, réalisé individuellement par **Awa BOUARE**. Le code initial fonctionnait mais présentait des défauts de lisibilité et de structure. Le travail consiste à l'améliorer en vérifiant les comportements couverts par les tests.

Le TP1 porte sur le nettoyage, le TP2 sur les tests unitaires et le refactoring. Le **TP3 est à venir** : ses consignes et ses résultats seront ajoutés après réalisation.

## Sommaire

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Tableau récapitulatif des travaux réalisés](#tableau-récapitulatif-des-travaux-réalisés)
- [TP1 — Bilan et corrections justifiées](#tp1--bilan-et-corrections-justifiées)
- [TP2 — Bilan et corrections justifiées](#tp2--bilan-et-corrections-justifiées)
- [Tests, mesures et limites](#tests-mesures-et-limites)
- [Difficultés et solutions retenues](#difficultés-et-solutions-retenues)
- [TP3 — À venir](#tp3--à-venir)
- [Documentation et workflow Git](#documentation-et-workflow-git)
- [Journal détaillé du TP1](#journal-détaillé-du-tp1)
- [Journal détaillé du TP2](#journal-détaillé-du-tp2)

## Installation

Prérequis : Python 3.10 ou plus récent et Git.

```powershell
git clone https://github.com/awa78/bibliotech-BOUARE.git
cd bibliotech-BOUARE
python -m venv .venv
```

Activer l'environnement sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Sous Linux ou macOS :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

Le travail du TP2 est sur la branche `tp2/refactoring` tant que sa pull request n'est pas fusionnée. Pour consulter cette version après le clonage : `git switch tp2/refactoring`.

## Utilisation

```bash
python bibliotech.py list                    # catalogue et disponibilités
python bibliotech.py members                 # membres et emprunts en cours
python bibliotech.py borrow M005 B005         # emprunter un document
python bibliotech.py return L004              # rendre un document
python bibliotech.py overdue                  # retards et rappels
python bibliotech.py report                   # rapport d'activité
python bibliotech.py export emprunts.csv      # export des emprunts
python bibliotech.py overdue --today 2026-10-21
```

`--today AAAA-MM-JJ` permet de fixer la date. Les données sont dans `data/`. Les commandes `borrow` et `return` modifient `data/loans.csv`. Pour annuler les changements faits pendant un essai et retrouver les données versionnées : `git restore data/`.

### Règles métier

| Règle | Valeur |
| --- | --- |
| Durée d'emprunt | livre 21 jours, DVD 7 jours, magazine 3 jours |
| Emprunts simultanés maximum | standard 3, étudiant 5, premium 8 |
| Pénalité par jour de retard | livre 0,50 €, DVD 1,00 €, magazine 0,20 € |
| Réduction sur les pénalités | étudiant 50 %, premium 100 % |
| Plafond de la pénalité | prix du document |

Un emprunt est refusé si le membre est inactif, s'il a un emprunt en retard, s'il a atteint sa limite, s'il a déjà ce document, ou s'il ne reste aucun exemplaire.

## Tableau récapitulatif des travaux réalisés

Les contrôles ci-dessous correspondent à chaque étape du travail. Le TP3 est explicitement distingué des réalisations terminées.

| TP | Axe de travail | Travaux réalisés | Résultat ou vérification | État |
| --- | --- | --- | --- | --- |
| TP1 | Préparation et Git | Installation dans `.venv`, dépôt personnel, branche `tp1/nettoyage`, étiquette `v0-initial` publiée | Point de départ : 21 tests réussis et 55 signalements Ruff | Réalisé |
| TP1 | Lisibilité | Imports explicites et triés, suppression d'un import inutilisé, conditions et affectations simplifiées, renommage de méthodes, formatage Ruff | Tests de caractérisation conservés et vérifiés au fil des changements | Réalisé |
| TP1 | Fichiers et état partagé | Cinq ouvertures de fichiers avec `with`, suppression du dictionnaire mutable par défaut dans `register_plugin` | Scénarios fournis réussis après les modifications | Réalisé |
| TP1 | Règles et duplication | Durées nommées puis dictionnaires `LOAN_DAYS`, `DAILY_FEE`, `MAX_LOANS` ; extraction de `calculate_late_fee` et remplacement des quatre copies | Calcul commun utilisé dans les retours, les retards, le rapport et l'export | Réalisé ; fonction adaptée en `late_fee` au TP2 |
| TP1 | Corrections de revue | `float` remplace `eval`, exceptions précisées, erreurs de plugins journalisées, `pass` inutile supprimé, f-strings et `join`, arrondi redondant supprimé, commentaires | Fin du TP1 : 21 tests réussis et 5 signalements Ruff ; contrôles ciblés de sécurité et de plugins effectués hors dépôt | Réalisé |
| TP1 | Documentation et remise | Journal TP1 et bilan intégrés au README, commits progressifs et pull request nº 1 | TP1 fusionné par l'enseignant | Terminé |
| TP2 | Préparation et mesure initiale | Branche `tp2/refactoring`, configuration `pythonpath` pour pytest, ajout de Radon | 21 tests réussis ; Radon initial : emprunt C (18), `process` C (16), `report` C (14) | Réalisé |
| TP2 | Tests avant refactoring | `tests/test_rules.py` : 10 cas paramétrés ; `tests/test_borrow.py` : 6 tests ; fixture temporaire et date fixe dans `tests/conftest.py` | Rouge d'import attendu sur `late_fee`, puis vérification des règles et des emprunts | Réalisé |
| TP2 | Niveau 1 : fonction pure | Ajout de `late_fee`, remplacement des appels dans `ret`, `overdue`, `report`, `export`, puis suppression de `calculate_late_fee` | Une implémentation commune ; 37 tests réussis | Réalisé |
| TP2 | Niveau 2 : clauses de garde | Extraction de `has_overdue_loan`, `is_borrowing`, `refusal_reason`, `create_loan` ; méthode principale renommée en `borrow`, appels et tests mis à jour | `borrow` A (4), aucune fonction en note D ou supérieure ; 37 tests réussis | Réalisé |
| TP2 | Documentation et remise | README avec mesures avant/après, commits nommés, branche publiée et pull request nº 2 ouverte | Relecture du professeur et validation à confirmer avant fusion | Réalisations publiées ; revue à confirmer |
| TP3 | À préciser selon le guide | Aucun travail TP3 réalisé à ce stade | Mesures, tests, livrables et lien de remise à renseigner après réalisation | À venir |

## TP1 — Bilan et corrections justifiées

Le nettoyage a été réalisé sur `tp1/nettoyage`, puis complété après les remarques de revue. Le professeur a fusionné la [pull request nº 1](https://github.com/awa78/bibliotech-BOUARE/pull/1). L'étiquette `v0-initial` conserve la version de départ.

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
| Documentation insuffisante | Commentaires sur les règles, valeurs par défaut et choix importants | Compréhension et maintenance du code |

La fonction `calculate_late_fee` gère l'absence de retard, le tarif journalier, les réductions étudiant/premium, le plafond au prix du document et l'arrondi au centime. L'arrondi redondant dans le cumul du rapport a été supprimé après revue.

### Bilan du TP1

- **21 tests de caractérisation réussis**, avant et après les corrections.
- **55 signalements Ruff au départ, 5 à la fin du TP1 après revue**, tous liés à la complexité.
- Calcul des pénalités centralisé dans `calculate_late_fee` au TP1, puis adapté à `late_fee` au TP2. Cette évolution ne signifie pas que les deux fonctions existent encore.
- Remarques de revue traitées : lecture numérique des prix, erreurs de plugins journalisées, `pass` supprimé, f-strings et `join`, dictionnaires de règles et suppression de l'arrondi redondant.
- Formatage initial et corrections de revue identifiables par commit. L'historique publié n'a pas été réécrit ; le diff global conserve donc aussi le formatage initial.

Des contrôles supplémentaires ont vérifié le rejet d'une expression Python dans un prix sans exécution, le journal d'un plugin défaillant, la poursuite du suivant, la propagation de `SystemExit` et les règles de pénalité. Ce script était **extérieur au dépôt** : ces contrôles ne font pas partie des 37 tests versionnés.

Le [journal détaillé du TP1](#journal-détaillé-du-tp1) est intégré à la fin de ce README : les 31 essais et les corrections de revue y sont conservés.

## TP2 — Bilan et corrections justifiées

Les **niveaux obligatoires 1 et 2 sont réalisés et vérifiés**, sans bonus. Les commits, dont le renommage final `e3cb80b`, ont été publiés dans la [pull request nº 2](https://github.com/awa78/bibliotech-BOUARE/pull/2). La relecture du professeur, sa validation et la fusion restent à confirmer ; elles ne sont pas présentées comme acquises.

### Corrections et justification

Le TP2 part du code réellement obtenu au TP1 : le calcul des pénalités était déjà centralisé dans `calculate_late_fee` et les dictionnaires de règles existaient. Le travail a donc consisté à tester ce comportement, adapter le calcul au contrat du guide et restructurer les emprunts, sans réintroduire les anciennes duplications.

| Problème ou besoin de départ | Correction réalisée au TP2 | Justification et principe appliqué | Vérification |
| --- | --- | --- | --- |
| Les nouveaux tests doivent importer le module de l'application | Ajout de `pythonpath = ["."]` à la configuration pytest | Rendre `bibliotech` importable depuis les tests ; préparer l'environnement avant le refactoring | Tests importés correctement après configuration |
| Absence de mesure de complexité initiale pour le TP2 | Ajout de Radon aux dépendances et relevé avant modification | Comparer des mesures avant/après avec le même outil | Départ : emprunt C (18), `process` C (16), `report` C (14) |
| Les tests fournis ne décrivent pas directement chaque règle de pénalité | Ajout de 10 cas paramétrés dans `tests/test_rules.py`, avec `pytest.approx` | Tester les règles avant leur modification, avec des résultats attendus calculés indépendamment | Rouge d'import attendu avant la fonction, puis 10 cas réussis |
| Les tests d'emprunt doivent être reproductibles et indépendants des données originales | Fixture `library` dans `tests/conftest.py` : copie temporaire des CSV et date fixe avec `monkeypatch` | Isoler l'état de chaque test et supprimer la dépendance à la date du jour | Les tests utilisent une copie des données au 21/10/2026 |
| Les refus et le succès d'un emprunt doivent être protégés avant sa restructuration | Six tests dans `tests/test_borrow.py` : inactivité, retard, doublon, indisponibilité, limite et succès | Fixer le comportement observable avant le refactoring, notamment les messages et la création de l'emprunt | 6 tests d'emprunt et 21 tests de caractérisation réussis ensemble |
| La fonction du TP1 reçoit des dictionnaires, alors que le guide demande un contrat explicite | Ajout de `late_fee(days_late, kind, member_type, price)` avec clause de garde, tarif, réduction, plafond et arrondi | Fonction pure à paramètres explicites, facile à tester ; application de KISS et séparation du calcul des entrées/sorties | Les cas sans retard, tarifs, réductions, plafond et type inconnu passent |
| Quatre usages doivent migrer vers la nouvelle fonction sans modifier les traitements voisins | Remplacement successif des appels dans `ret`, `overdue`, `report` et `export` | Petits pas de refactoring ; conserver les jours affichés, les messages et les fichiers produits | Suite complète relancée après chaque remplacement validé |
| Deux fonctions de pénalité subsistent pendant la migration | Suppression de `calculate_late_fee` après le dernier remplacement | DRY : conserver une seule implémentation des règles, sans code devenu inutilisé | Une définition de `late_fee`, quatre appels et 37 tests réussis |
| Une boucle avec drapeau recherche les retards dans la méthode d'emprunt | Extraction de `has_overdue_loan(member_id)` avec `any` | Extract Function : nommer la question métier et alléger la méthode principale | Tests d'emprunt et de caractérisation verts après extraction |
| Une seconde boucle avec drapeau recherche les documents déjà empruntés | Extraction de `is_borrowing(member_id, book_id)` avec `any` | Extract Function : rendre la vérification réutilisable et lisible | Refus pour document déjà emprunté conservé ; suite verte |
| La décision de refus est mêlée à la création et à l'affichage de l'emprunt | Extraction de `refusal_reason(member, book)`, qui renvoie un motif ou `None` | Séparer la décision métier et conserver la priorité des refus | Ordre maintenu : inactivité, retard, limite, doublon, disponibilité ; tests verts |
| Le calcul de l'échéance, de l'identifiant et la sauvegarde encombrent la méthode principale | Extraction de `create_loan(member, book)` | Regrouper la responsabilité de création de l'emprunt | Succès vérifié : L013, membre M005, document B005, échéance 2026-10-28 ; scénarios fournis verts |
| L'imbrication des conditions rend le parcours d'emprunt difficile à suivre | Réécriture avec clauses de garde : erreur ou refus suivi d'un retour immédiat | Guard Clauses : réduire l'imbrication et laisser le cas accepté à la fin | Même résultat dans les cas testés ; méthode finale `borrow` A (4) au lieu de C (18) |
| Le nom de la méthode et ses références doivent suivre la structure demandée par le guide | Renommage de `borrow_document` en `borrow`, mise à jour de `process` et des huit appels des tests d'emprunt | Garder des définitions et appels cohérents ; nom conforme au rôle final | 37 tests réussis après renommage |
| Les règles nommées demandées en section 3.2 existent déjà depuis le TP1 | Vérification et réutilisation de `LOAN_DAYS`, `DAILY_FEE` et `MAX_LOANS` | Conserver les règles centralisées ; éviter une modification artificielle ou une duplication | Valeurs et défauts conservés ; suite complète verte |
| Le résultat du refactoring doit être justifié et traçable | Mesures Radon après modification, README, commits progressifs et publication de la pull request nº 2 | Appuyer le bilan sur des résultats vérifiables et permettre la revue du professeur | 37 tests réussis ; `borrow` A (4), aucune fonction en D ou supérieure ; `process` C (16) et `report` C (14) restent identifiés |

### Tests ajoutés et méthode suivie

| Fichier | Rôle | Cas vérifiés |
| --- | --- | --- |
| `tests/test_rules.py` | 10 cas paramétrés, résultats calculés à la main et `pytest.approx` | À temps, retard négatif, livre, DVD, magazine, étudiant, premium, plafond, type inconnu et montant au centime |
| `tests/test_borrow.py` | 6 tests du comportement d'emprunt | Inactif, retard existant, document déjà emprunté, indisponibilité, limite et succès avec L013 et échéance au 28/10/2026 |
| `tests/conftest.py` | Fixture partagée des tests d'emprunt | Copie des CSV dans un dossier temporaire et date fixée au 21/10/2026 avec `monkeypatch` |

Les tests ont précédé les refactorings. L'erreur d'import sur `late_fee` était le rouge attendu, avant l'écriture de la fonction ; les tests de caractérisation ont été vérifiés séparément à cette étape. La fonction a ensuite été enregistrée avec ses tests au vert, puis les quatre appels ont été remplacés dans des commits séparés. L'ancienne fonction a été supprimée après le dernier remplacement.

Les dictionnaires de règles introduits au TP1 ont été réutilisés. La méthode d'emprunt a été décomposée en `borrow`, `refusal_reason`, `has_overdue_loan`, `is_borrowing` et `create_loan`, avec conservation des messages et de la priorité des refus.

Le détail chronologique des commandes, des essais et des résultats intermédiaires est dans [journal détaillé du TP2](#journal-détaillé-du-tp2).

## Tests, mesures et limites

### Reproduire les vérifications

```bash
python -m pytest -q
python -m ruff check . --statistics
python -m radon cc -s -n C bibliotech.py
python -m radon cc -s bibliotech.py
```

Sous PowerShell, en cas de problème d'accès au dossier temporaire ou au cache de pytest :

```powershell
python -m pytest -q -p no:cacheprovider --basetemp "$env:TEMP\bibliotech-tests-awa"
```

Le dossier `--basetemp` doit être réservé aux tests : pytest peut le vider à la prochaine exécution.

### Résultats enregistrés

| Indicateur | Départ | Résultat vérifié |
| --- | --- | --- |
| Suite de tests | 21 tests fournis au début du TP1 | 37 réussis après le TP2 : 21 de caractérisation, 10 de pénalités et 6 d'emprunt |
| Ruff pendant le TP1 | 55 signalements | 5 après la revue du TP1 |
| Radon : méthode d'emprunt au TP2 | `borrow_document` C (18) | `borrow` A (4) |
| Radon : `process` au TP2 | C (16) | C (16) |
| Radon : `report` au TP2 | C (14) | C (14) |

Le contrôle Ruff effectué lors de la préparation de la présentation du TP2 comptait **8 signalements : 4 C901, 3 W292 et 1 I001**. Ce relevé est distinct des 5 signalements de fin du TP1. Ruff, Radon et pytest fournissent des informations différentes : un signalement de style n'est pas un test échoué.

Les critères Radon du niveau 2 sont vérifiés : **`borrow` en A et aucune fonction en D ou supérieure**. `process` et `report` restent à améliorer. Les tests confirment les scénarios écrits, sans prouver l'absence de bugs dans tous les cas possibles. Aucun pourcentage de couverture n'a été mesuré dans ce bilan.

Les tests fournis `tests/test_caracterisation.py`, les références `tests/golden/` et les données versionnées sont restés inchangés par rapport à `v0-initial` lors des vérifications du travail.

## Difficultés et solutions retenues

| Difficulté | Solution appliquée |
| --- | --- |
| Accès refusé au dossier temporaire de pytest et à son cache | Dossier temporaire dédié et cache désactivé pour les exécutions concernées |
| Préfixe PowerShell ou historique collé avec une commande | Exécuter la commande seule, une à la fois |
| Onglet VS Code plus ancien que le fichier enregistré | Recharger la version du disque avant de reprendre la modification |
| Mauvaise indentation du compteur d'export | Comparer avec `git diff`, remettre le compteur dans la boucle et retester |
| Renommage incomplet ou constantes non définies | Vérifier les définitions et tous les appels, puis relancer les tests |
| Faute `strptie` au lieu de `strptime` dans le retour | Corriger la faute identifiée dans le diff et vérifier les 37 tests |
| Ancienne méthode supprimée sans ajout du nouveau bloc | Insérer la méthode avec clauses de garde, puis vérifier la suite avant commit |

## TP3 — À venir

Les consignes du TP3 ne sont pas encore intégrées et aucun travail du TP3 n'est revendiqué. Après réception du guide, cette section et le tableau récapitulatif seront complétés avec les objectifs, les corrections justifiées, les tests, les mesures et le lien de remise.

## Documentation et workflow Git

- [Journal détaillé du TP1](#journal-détaillé-du-tp1) : nettoyage, essais et corrections de revue, intégrés ci-dessous.
- [journal détaillé du TP2](#journal-détaillé-du-tp2) : essais et résultats intermédiaires du refactoring, conservés comme historique.
- [Pull request TP1](https://github.com/awa78/bibliotech-BOUARE/pull/1) : fusionnée par l'enseignant.
- [Pull request TP2](https://github.com/awa78/bibliotech-BOUARE/pull/2) : travail publié, validation et fusion à confirmer avant de commencer une nouvelle étape depuis `main`.


Le travail est individuel. L'invitation de `Massamba07` comme collaborateur a été confirmée ; le partage du lien dans le document de promotion reste à confirmer. Les supports de présentation du TP1 et du TP2 ont été préparés séparément et devront être complétés après le TP3.

## Journal détaillé du TP1

Les **31 essais**, leur justification, les résultats et les corrections après revue sont intégrés ci-dessous. Ouvrir une entrée pour lire le détail. La synthèse séparée est désormais regroupée dans ce README.

Les numéros de ligne, résultats intermédiaires et mentions « en attente » décrivent **le moment de chaque essai**. Ils ne constituent pas des tâches encore ouvertes : le TP1 a été publié, revu et fusionné. Les bilans en début de document décrivent les réalisations confirmées.

### Préparation et relevés historiques

<details>
<summary>Objectif</summary>

Améliorer la lisibilité et la qualité du code sans changer le comportement de l'application. Conserver les tests fournis et vérifier chaque correction par petits pas.

</details>

<details>
<summary>Bilan avant remise du TP1</summary>

- Contrôle effectué après le commit `5fa5b9a` : **21 tests réussis en 5,19 s**.
- Ruff : **55 problèmes au départ, 5 restants**, soit 50 signalements supprimés. Les 5 restants concernent la complexité des méthodes `load` (9), `find` (10), `borrow_document` (19), `report` (14) et de la fonction `process` (15), pour un seuil configuré à 8.
- Les dossiers `tests/` et `data/` sont inchangés par rapport à `v0-initial`. Aucun changement du code n'était en attente lors du contrôle.
- Améliorations : imports explicites et ordonnés, conditions simplifiées, noms de méthodes explicites, durées nommées, fermeture automatique des fichiers, formatage, gestion des exceptions précisée, suppression d'un argument mutable partagé et centralisation des pénalités dans une fonction commune.
- Le calcul des pénalités est réutilisé par les retours, les retards, l'export et le rapport. Les règles de tarif, réduction, plafond et arrondi restent regroupées dans un seul endroit.
- Limites : la réussite des tests caractérise les scénarios fournis. Les exceptions interceptées ont été volontairement restreintes comme documenté dans les essais 22 et 23. La complexité restante pourra faire l'objet d'un refactoring ultérieur ; le guide TP1 exige une diminution des signalements Ruff, sans imposer zéro problème.
- Organisation : travail individuel ; présence de `Massamba07` dans les collaborateurs confirmée par l'utilisatrice ; acceptation de l'invitation non précisée. Le lien du document partagé de promotion reste à demander à l'enseignant.
- Git : étiquette `v0-initial` publiée, branche locale `tp1/nettoyage`. À terminer : commit de ce bilan, publication de la branche, puis ouverture d'une pull request vers `main` avec résumé des améliorations, sans fusion.

Les entrées ci-dessous constituent le journal des essais ; les états « commit en attente » décrivent le moment de chaque essai et sont complétés par les confirmations des étapes suivantes. Le dernier calcul commun du rapport a été enregistré dans le commit `5fa5b9a`.

</details>

<details>
<summary>Préparation — 21 octobre 2026</summary>

- Dépôt : https://github.com/awa78/bibliotech-BOUARE
- Projet récupéré dans `Documents\bibliotech-BOUARE`.
- Environnement Python `.venv` créé et dépendances de `requirements.txt` installées.
- Vérification initiale : **21 tests réussis**.
- Analyse initiale Ruff : **55 problèmes signalés**.
- Commande `python bibliotech.py list` : le catalogue s'affiche correctement.
- Étiquette locale `v0-initial` et branche `tp1/nettoyage` créées.
- Projet ouvert dans VS Code.

</details>

<details>
<summary>Corrections et essais vérifiés</summary>

| Défaut | Emplacement | Correction | Principe | Vérification |
| --- | --- | --- | --- | --- |
| Deux modules importés sur une même ligne (E401) | `bibliotech.py`, imports au début du fichier | Remplacement de `import os, sys` par deux lignes : `import os` et `import sys` | Conventions Python et lisibilité | 21 tests réussis ; Ruff : 54 problèmes au lieu de 55 |
| Comparaison explicite d'un booléen à True (E712) | `bibliotech.py`, ligne 60, méthode `load()` | Utilisation directe de `debug` dans la condition | Simplicité et lisibilité | Résultat transmis par l'utilisatrice : 21 tests réussis ; Ruff : 53 problèmes au lieu de 54 |

</details>

<details>
<summary>Suivi du guide — accès et publication du point de départ</summary>

- L'utilisatrice confirme travailler seule : aucun binôme à ajouter.
- Elle confirme que `Massamba07` apparaît dans la liste des collaborateurs ; l'acceptation de l'invitation n'a pas été précisée.
- Partage du lien du dépôt dans le document de promotion : en attente. L'utilisatrice doit demander à l'enseignant où trouver ce document.
- Étape 5 : `git push origin v0-initial` exécuté par l'utilisatrice avec succès ; le terminal confirme `[new tag] v0-initial -> v0-initial`. Le point de départ est désormais publié sur GitHub.
- Étape 6 : branche locale `tp1/nettoyage` déjà créée ; prochaine vérification avant de reprendre le nettoyage.

</details>

<details>
<summary>Vérification globale de reprise — 21 octobre 2026</summary>

- Branche active : `tp1/nettoyage` ; dernier commit : `cec41ec`.
- Tests relancés : **21 réussis en 3,29 s** (`.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider`).
- Analyse Ruff relancée : **48 problèmes**, contre 55 initialement.
- Les dossiers `tests/` et `data/` sont identiques à la version `v0-initial`.
- Aucune modification du code en attente ; seul ce rapport a des modifications non commitées.
- Vérification distante avec `git ls-remote` : seule la branche `main`, au commit initial, est présente parmi les références recherchées. La branche `tp1/nettoyage` et l'étiquette `v0-initial` ne sont pas encore publiées sur GitHub.
- Prochaine correction proposée, non appliquée : simplifier les quatre comparaisons booléennes aux lignes 107, 114, 259 et 412.
- Invitations des collaborateurs et dépôt du lien dans le document de promotion : non vérifiés, aucun accès à ces informations dans cet audit.

</details>

### Corrections dans l’ordre de réalisation

<details>
<summary>Essai 1 — Séparer les imports</summary>

La séparation des imports facilite la lecture des dépendances. La correction a été constatée dans le fichier puis vérifiée automatiquement.

Commandes exécutées après la correction :

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check . --statistics
```

Résultats : `21 passed` et `Found 54 errors.`. Le code de sortie 1 de Ruff indique que des problèmes de qualité restent à corriger ; les tests ont réussi.

</details>

<details>
<summary>Essai 2 — Vérification depuis le terminal de VS Code</summary>

Après la proposition de simplifier `if debug == True:` en `if debug:`, l'exécution de `python -m pytest -q` par l'utilisatrice a produit **21 erreurs de préparation** : `PermissionError: [WinError 5]` sur le dossier temporaire `AppData\Local\Temp\pytest-of-awabo`. Des avertissements d'accès au cache `.pytest_cache` sont également présents. Ces erreurs empêchent l'exécution des tests et ne permettent pas de conclure sur le comportement de l'application.

Solution proposée : utiliser un dossier temporaire distinct et désactiver le cache pour cette exécution, sans modifier les tests ni les permissions Windows :

```powershell
python -m pytest -q -p no:cacheprovider --basetemp "$env:TEMP\bibliotech-tests-awa"
```

Résultat transmis par l'utilisatrice : **21 tests réussis en 3,23 s**. La commande `python -m ruff check . --statistics` signale **53 problèmes**, contre 54 après la première correction et 55 au départ. Le nombre de signalements E712 passe de 5 à 4. La deuxième correction est validée par les tests fournis.

Un essai intermédiaire avait collé deux commandes en une seule (`python -m pytest -qpython -m ruff check . --statistics`) : pytest avait alors refusé les arguments. La solution a été de lancer chaque commande séparément. Cette erreur de saisie ne nécessitait aucune modification du programme.

La forme conventionnelle attendue à la ligne 60 est `if debug:` (sans espace avant les deux-points).

Ce document sera complété à chaque nouvel essai, en distinguant les propositions des corrections appliquées et vérifiées. La première correction a été enregistrée dans le commit local `4d50be8`, et la deuxième dans `562b3f0`, confirmés par le terminal de l'utilisatrice. Aucun envoi sur GitHub n'a été confirmé. Le blocage de préparation des tests est résolu avec la commande ci-dessus.

</details>

<details>
<summary>Essai 3 — Supprimer un import inutilisé</summary>

- Défaut : import du module `json` sans utilisation dans le fichier (F401).
- Emplacement : `bibliotech.py`, ancienne ligne 9, bloc des imports.
- Correction : suppression de `import json`.
- Principe : supprimer le code inutile et rendre les dépendances plus lisibles.
- Vérifications transmises par l'utilisatrice : `python -m pytest -q -p no:cacheprovider --basetemp "$env:TEMP\bibliotech-tests-awa"` donne **21 tests réussis en 4,39 s** ; `python -m ruff check . --statistics` donne **52 problèmes**, contre 53 avant cette correction et 55 au départ. Le signalement F401 a disparu.
- État : correction validée par les tests fournis et enregistrée dans le commit local `8f011c9`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 4 — Comparaisons avec None : échec détecté et diagnostic</summary>

- Objectif : remplacer les comparaisons `== None` et `!= None` par `is None` et `is not None` aux lignes 104, 106, 174 et 376.
- Premier résultat transmis : **19 tests réussis et 2 échoués** (`report`, `report_after_returns`) ; Ruff signale **49 problèmes**, dont un E711 restant.
- Diagnostic par comparaison au dernier commit : les lignes 104, 106 et 174 sont correctement modifiées, mais la condition `if bk["kind"] in k:` à la ligne 306 a été remplacée par erreur par `if TODAY is None:`. Cela réinitialise les compteurs par type de document dans le rapport. La comparaison prévue à la ligne 376 n'a pas été modifiée.
- Correction proposée : rétablir `if bk["kind"] in k:` à la ligne 306, puis remplacer `if TODAY == None:` par `if TODAY is None:` à la ligne 376.
- Enseignement : les tests ont détecté une modification involontaire du comportement ; une baisse du nombre de problèmes Ruff ne suffit pas à valider une correction.
- Résultat après correction transmis par l'utilisatrice : **21 tests réussis en 4,44 s**, et **48 problèmes Ruff**, contre 52 avant cet essai. Les quatre signalements E711 ont disparu. Les tests du rapport réussissent à nouveau.
- État : correction validée par les tests fournis et enregistrée dans le commit local `cec41ec`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 5 — Simplifier la condition du membre actif</summary>

- Défaut : comparaison explicite d'un booléen avec `True` (E712).
- Emplacement : `bibliotech.py`, ligne 107, méthode `do_stuff()`.
- Correction : remplacement de `if mb["active"] == True:` par `if mb["active"]:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 2,93 s** avec la commande pytest utilisant le dossier temporaire distinct ; **47 problèmes Ruff**, contre 48 avant cette correction. Les signalements E712 passent de 4 à 3.
- Étape 6 du guide confirmée par `git branch --show-current` : branche active `tp1/nettoyage`.
- État : correction validée ; commit en attente. Les trois autres comparaisons booléennes proposées restent à traiter séparément.

</details>

<details>
<summary>Essai 6 — Simplifier la condition d'absence de retard</summary>

- Défaut : comparaison explicite d'un booléen avec `False` (E712).
- Emplacement : `bibliotech.py`, ligne 114, méthode `do_stuff()`.
- Correction : remplacement de `if late == False:` par `if not late:` sans modifier l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,19 s** ; **46 problèmes Ruff**, contre 47 avant cette correction. Les signalements E712 passent de 3 à 2.
- État : correction validée ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition du membre actif a été enregistrée dans le commit `84e96c9`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 7 — Simplifier la condition du membre actif dans l'affichage</summary>

- Défaut : comparaison explicite d'un booléen avec `True` (E712).
- Emplacement : `bibliotech.py`, ligne 259.
- Correction : remplacement de `if x["active"] == True:` par `if x["active"]:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 2,95 s** ; **45 problèmes Ruff**, contre 46 avant cette correction. Il reste un signalement E712.
- État : correction validée ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition d'absence de retard a été enregistrée dans le commit `f70af4b`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 8 — Simplifier la dernière comparaison booléenne</summary>

- Défaut : comparaison explicite d'un résultat avec `False` (E712).
- Emplacement : `bibliotech.py`, ligne 412.
- Correction : remplacement de `if r == False:` par `if not r:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,37 s** ; **44 problèmes Ruff**, contre 45 avant cette correction et 55 initialement. Aucun signalement E712 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition du membre actif dans l'affichage a été enregistrée dans le commit `848da21`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 9 — Rendre les imports datetime explicites</summary>

- Défaut : import global `from datetime import *` et import redondant `import datetime`, rendant l'origine des noms moins claire (F403 et F405).
- Emplacement : `bibliotech.py`, bloc des imports, anciennes lignes 5 à 8.
- Correction : conserver `import os` et `import sys`, puis importer explicitement `date`, `datetime` et `timedelta` avec `from datetime import date, datetime, timedelta`.
- Principe : dépendances explicites et lisibilité ; suppression d'un import redondant.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,02 s** ; **41 problèmes Ruff**, contre 44 avant cette correction. Le signalement F403 et les deux signalements F405 ont disparu.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la dernière simplification booléenne a été enregistrée dans le commit `9a5b8c5`, confirmé par le terminal de l'utilisatrice.
- Attention pour la suite : la suppression d'une ligne dans les imports décale les numéros des lignes suivantes ; les prochains emplacements devront être vérifiés.

</details>

<details>
<summary>Essai 10 — Trier automatiquement les imports</summary>

- Défaut : ordre des imports non conforme (I001), au début de `bibliotech.py`.
- Correction : exécution ciblée de `python -m ruff check bibliotech.py --select I --fix`.
- Résultat de la correction transmis par l'utilisatrice : `Found 1 error (1 fixed, 0 remaining).` Ce résultat concerne uniquement les règles de tri des imports sélectionnées.
- Principe : conventions Python et organisation lisible des dépendances.
- Incident de saisie : du texte de l'historique et le préfixe `(.venv) PS ...>` ont été recollés dans PowerShell, provoquant une saisie multiligne puis une `ParserError` sur `PS`. Solution : revenir à l'invite normale et exécuter uniquement la commande, sans préfixe ni sortie précédente. Aucune modification du programme n'était nécessaire pour cet incident.
- Vérifications finales transmises par l'utilisatrice : **21 tests réussis en 2,95 s** ; **40 problèmes Ruff**, contre 41 avant cet essai et 55 initialement. Le signalement I001 a disparu.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : les imports datetime explicites ont été enregistrés dans le commit `bbba5a2`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 11 — Éviter un dictionnaire mutable comme argument par défaut</summary>

- Défaut : `options={}` dans la signature de `register_plugin()` (B006) ; le dictionnaire par défaut est partagé entre les appels.
- Emplacement : `bibliotech.py`, méthode `register_plugin()`, ancienne ligne 358.
- Correction : utiliser `options=None`, puis initialiser `options = {}` dans un bloc `if options is None:` avant l'enregistrement du plugin.
- Principe : éviter un état mutable partagé implicitement entre les appels.
- Incident de saisie : une nouvelle `ParserError` sur `PS` provenait du collage du préfixe du terminal ; les tests n'avaient pas démarré. La commande seule a ensuite été exécutée correctement.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,88 s** ; **39 problèmes Ruff**, contre 40 avant cet essai. Le signalement B006 a disparu. Ces résultats valident les scénarios fournis ; ils ne constituent pas un test spécifique de l'indépendance des dictionnaires entre plugins.
- État : correction vérifiée avec la suite fournie ; commit en attente.
- Suivi de l'essai précédent : le tri des imports a été enregistré dans le commit `8394c2a`, confirmé par le terminal de l'utilisatrice.
- Les deux lignes ajoutées décalent les emplacements suivants ; les prochaines lignes seront vérifiées avant modification.

</details>

<details>
<summary>Essai 12 — Fermer automatiquement le fichier du catalogue</summary>

- Défaut : ouverture de `books.csv` et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 25 à 27.
- Correction : utiliser `with open(DATA + "/books.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; le fichier est fermé même si la lecture lève une exception.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,74 s** ; **38 problèmes Ruff**, contre 39 avant cet essai. Les signalements SIM115 passent de 5 à 4.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la suppression du dictionnaire mutable par défaut a été enregistrée dans le commit `f0178fe`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

</details>

<details>
<summary>Essai 13 — Fermer automatiquement le fichier des membres</summary>

- Défaut : ouverture de `members.csv` et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 32 à 34.
- Correction : utiliser `with open(DATA + "/members.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; fermeture du fichier même en cas d'exception pendant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,56 s** ; **37 problèmes Ruff**, contre 38 avant cet essai. Les signalements SIM115 passent de 4 à 3.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture du catalogue avec `with` a été enregistrée dans le commit `4f87db5`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

</details>

<details>
<summary>Essai 14 — Fermer automatiquement le fichier des emprunts à la lecture</summary>

- Défaut : ouverture de `loans.csv` en lecture et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 43 à 45.
- Correction : utiliser `with open(DATA + "/loans.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; fermeture du fichier même en cas d'exception pendant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,77 s** ; **36 problèmes Ruff**, contre 37 avant cet essai. Les signalements SIM115 passent de 3 à 2.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture du fichier des membres avec `with` a été enregistrée dans le commit `90132ab`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

</details>

<details>
<summary>Essai 15 — Fermer automatiquement le fichier des emprunts à la sauvegarde</summary>

- Défaut : ouverture de `loans.csv` en écriture et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `save()`, anciennes lignes 57 à 62.
- Correction : utiliser `with open(DATA + "/loans.csv", "w") as f:`, placer l'écriture de l'en-tête et la boucle d'écriture dans ce bloc et supprimer `f.close()`.
- Principe : gestion fiable des ressources ; fermeture automatique du fichier, y compris si une écriture lève une exception.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,29 s** ; **35 problèmes Ruff**, contre 36 avant cet essai et 55 initialement. Les signalements SIM115 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture des emprunts avec `with` a été enregistrée dans le commit `85fdd8b`, confirmé par le terminal de l'utilisatrice.
- Les prochains numéros de ligne seront vérifiés avant modification.

</details>

<details>
<summary>Essai 16 — Fermer automatiquement le fichier exporté : diagnostic en cours</summary>

- Objectif : remplacer l'ouverture et la fermeture manuelles dans `export()` par un bloc `with`, sans modifier le calcul ni le contenu exporté.
- Premier résultat transmis : **20 tests réussis et 1 échoué en 3,34 s**, scénario `export`. Le message annonce 1 ligne exportée au lieu de 12.
- Diagnostic par comparaison au commit précédent : `n = n + 1` à la ligne 349 est resté hors de la boucle `for x in self.l:`. Il s'exécute une seule fois après la boucle au lieu d'une fois par emprunt.
- Correction proposée : ajouter un niveau d'indentation (4 espaces) à cette ligne pour l'aligner avec `fee = round(fee, 2)` et l'écriture de chaque emprunt.
- Deuxième essai transmis : même échec, **20 tests réussis et 1 échoué en 3,01 s**. La relecture du fichier enregistré confirme que le compteur avait toujours 12 espaces au lieu de 16.
- Correction appliquée par l'assistant : indentation du compteur à 16 espaces, dans la boucle, et suppression des espaces sur la ligne vide suivante.
- Vérification exécutée par l'assistant après correction : **21 tests réussis en 3,07 s** avec le cache désactivé ; **34 problèmes Ruff**, contre 35 avant cet essai. Aucun signalement SIM115 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la sauvegarde avec `with` a été enregistrée dans le commit `b6e37f9`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 17 — Formater le fichier Python</summary>

- Défaut : 19 lignes dépassant la longueur configurée (E501) et présentation du code à harmoniser.
- Emplacement : ensemble du fichier `bibliotech.py`.
- Correction : exécution de `python -m ruff format bibliotech.py` ; résultat transmis : `1 file reformatted`.
- Principe : conventions Python et présentation cohérente facilitant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,69 s** ; **15 problèmes Ruff**, contre 34 avant cet essai et 55 initialement. Les 19 signalements E501 ont disparu.
- Problèmes restants à ce stade : 8 C901, 2 E722, 2 SIM102, 2 SIM108 et 1 SIM105.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la fermeture automatique du fichier exporté a été enregistrée dans le commit `71fa056`, confirmé par le terminal de l'utilisatrice.
- Le formatage modifie de nombreux numéros de ligne ; les prochains emplacements devront être relevés dans le fichier actuel.

</details>

<details>
<summary>Essai 18 — Affecter directement le résultat d'une comparaison</summary>

- Défaut : bloc `if`/`else` affectant `True` ou `False` à `a` (SIM108).
- Emplacement : `bibliotech.py`, lecture des membres dans `load()`, anciennes lignes 46 à 49 de la version enregistrée après formatage.
- Correction : remplacer le bloc par `a = x[4] == "1"`.
- Principe : simplicité ; une comparaison produit déjà un booléen.
- Incident : les numéros affichés dans VS Code différaient de ceux du fichier enregistré. Une capture montrait le message `Failed to save 'bibliotech.py': The content of the file is newer.` Solution conseillée : fermer la version ancienne sans l'enregistrer, puis rouvrir le fichier depuis le disque avant de reprendre la correction.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,74 s** ; **14 problèmes Ruff**, contre 15 avant cet essai. Les signalements SIM108 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le formatage a été enregistré dans le commit `6d8b3d8`, confirmé par le terminal de l'utilisatrice.
- Les numéros de ligne suivants seront vérifiés avant chaque nouvelle modification.

</details>

<details>
<summary>Essai 19 — Simplifier le choix du texte du statut</summary>

- Défaut : bloc `if`/`else` affectant une chaîne à `s` (SIM108).
- Emplacement : `bibliotech.py`, commande `members`, anciennes lignes 544 à 547.
- Correction : remplacer le bloc par `s = "actif" if x["active"] else "inactif"`.
- Principe : expression conditionnelle courte pour une affectation simple et lisible.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,24 s** (sortie complète du message précédent) ; **13 problèmes Ruff**, contre 14 avant cet essai. Aucun signalement SIM108 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le calcul direct du booléen actif a été enregistré dans le commit `d4aa603`, confirmé par le terminal de l'utilisatrice. Les interruptions Ctrl+C ultérieures n'ont pas annulé ce commit terminé.

</details>

<details>
<summary>Essai 20 — Réunir les conditions de sélection des emprunts en retard</summary>

- Défaut : deux conditions `if` imbriquées pouvant être réunies (SIM102).
- Emplacement : `bibliotech.py`, méthode `overdue()`, anciennes lignes 273 à 275.
- Correction : réunir avec `and` la vérification de l'absence de retour et celle du dépassement de la date d'échéance, puis conserver `tmp.append(x)` dans le bloc.
- Principe : réduire l'imbrication et rendre les critères de sélection lisibles ; `and` conserve l'évaluation conditionnelle de la date après le contrôle du retour.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,30 s** ; **12 problèmes Ruff**, contre 13 avant cet essai. Les signalements SIM102 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la simplification du texte du statut a été enregistrée dans le commit `5c6e504`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 21 — Réunir les critères de retard d'un membre</summary>

- Défaut : conditions imbriquées dans la vérification des retards avant un emprunt (SIM102).
- Emplacement : `bibliotech.py`, méthode `do_stuff()`, anciennes lignes 136 à 141.
- Correction : réunir avec `and` les trois critères (identifiant du membre, emprunt non rendu, date d'échéance dépassée), puis conserver `late = True` dans le bloc.
- Principe : réduire l'imbrication en préservant l'ordre de vérification des conditions.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,28 s** ; **11 problèmes Ruff**, contre 12 avant cet essai. Aucun signalement SIM102 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la sélection des emprunts en retard a été enregistrée dans le commit `f8ae461`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 22 — Préciser les exceptions de lecture d'une pénalité</summary>

- Défaut : `except:` sans type d'exception lors de la conversion de `x[6]` en nombre (E722).
- Emplacement : `bibliotech.py`, méthode `load()`, ligne 58 au moment de la correction.
- Correction : remplacer `except:` par `except (ValueError, IndexError):` en conservant `fee = 0`.
- Principe : gérer explicitement les erreurs de conversion d'une valeur non numérique et d'accès à une colonne absente, sans masquer toutes les erreurs inattendues.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,32 s** ; **10 problèmes Ruff**, contre 11 avant cet essai. Les signalements E722 passent de 2 à 1.
- Limite : les tests fournis passent, mais le périmètre des exceptions interceptées est volontairement restreint ; les exceptions autres que ValueError et IndexError ne sont plus masquées par ce bloc.
- État : correction vérifiée avec les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la réunion des critères de retard du membre a été enregistrée dans le commit `247e1c8`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 23 — Délimiter les exceptions interceptées dans les plugins</summary>

- Défaut : `except:` sans type d'exception dans `run_plugins()` (E722).
- Emplacement : `bibliotech.py`, ligne 499 au moment de la correction.
- Correction : remplacer `except:` par `except Exception:` en conservant le bloc `pass`.
- Principe : intercepter les erreurs ordinaires des plugins sans masquer les interruptions comme KeyboardInterrupt (Ctrl+C) et SystemExit.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,75 s** ; **9 problèmes Ruff**, contre 10 avant cet essai. Aucun signalement E722 ne reste.
- Limite : les tests fournis passent ; la propagation des interruptions est une modification intentionnelle de la gestion des exceptions. Ces résultats ne constituent pas une vérification spécifique des plugins.
- État : correction vérifiée avec les tests fournis ; commit en attente.
- Suivi de l'essai précédent : les exceptions de lecture des pénalités ont été précisées dans le commit `957ea42`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 24 — Exprimer explicitement l'ignorance des erreurs des plugins</summary>

- Défaut : bloc `try` / `except Exception: pass` pouvant être exprimé avec `contextlib.suppress` (SIM105).
- Emplacement : imports et méthode `run_plugins()` de `bibliotech.py`, anciennes lignes 494 à 501 après ajout de l'import.
- Correction : ajouter `from contextlib import suppress`, puis remplacer le bloc `try` / `except` par `with suppress(Exception):` autour de l'appel et de l'ajout du résultat ; conserver `return res` après la boucle.
- Principe : exprimer directement l'intention d'ignorer les exceptions ordinaires d'un plugin et continuer les suivants, avec la même portée d'interception que `except Exception`.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,32 s** ; **8 problèmes Ruff**, contre 9 avant cet essai. Le signalement SIM105 a disparu ; les 8 signalements restants sont C901 (complexité des fonctions).
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la capture des erreurs des plugins a été limitée à Exception dans le commit `0a6fb95`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 25 — Renommer la méthode d'emprunt : renommage incomplet détecté</summary>

- Objectif : remplacer le nom vague `do_stuff` par `borrow_document`, dans la définition et son appel.
- Résultat transmis : **7 tests échoués et 14 réussis**, tous les échecs concernant les scénarios d'emprunt ; le dernier lancement transmis dure 3,88 s.
- Diagnostic par comparaison au dernier commit : l'appel à la ligne 564 utilise `lib.borrow_document(...)`, mais la définition à la ligne 128 porte encore le nom `do_stuff`. Le renommage est incomplet.
- Correction proposée : renommer également la définition en `def borrow_document(self, mid, bid):` sans modifier son corps.
- Principe : nommage explicite ; mettre à jour la définition et les références ensemble.
- Résultat après correction transmis par l'utilisatrice : **21 tests réussis en 3,90 s** ; **8 problèmes Ruff**, tous C901, comme avant le renommage. Le changement améliore le nommage sans réduire la complexité.
- État : renommage validé par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : l'utilisation de suppress a été enregistrée dans le commit `ab3065b`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 26 — Donner un nom explicite au comptage des emprunts en cours</summary>

- Défaut : nom `nb` trop vague pour identifier le rôle de la méthode.
- Emplacement : `bibliotech.py`, définition à la ligne 112 et appels aux lignes 152 et 557 au moment de la correction.
- Correction : renommer `nb` en `count_active_loans` dans la définition et les deux appels.
- Principe : nommage explicite décrivant le comptage des emprunts en cours d'un membre.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,27 s** ; **8 problèmes Ruff**, tous C901, comme avant ce renommage. Cette amélioration porte sur la lisibilité, sans réduction de la complexité.
- État : renommage validé par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le renommage de `do_stuff` en `borrow_document` a été enregistré dans le commit `71b061b`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 27 — Nommer les durées d'emprunt : constantes manquantes</summary>

- Objectif : remplacer les durées isolées 21, 7 et 3 par `BOOK_LOAN_DAYS`, `DVD_LOAN_DAYS` et `MAGAZINE_LOAN_DAYS`.
- Premier résultat transmis : **19 tests réussis et 2 échoués en 3,89 s**, scénarios `borrow_limit` et `borrow_ok`.
- Diagnostic : les noms sont utilisés dans `borrow_document()`, mais leurs définitions ne figurent pas dans le fichier enregistré. Les emprunts qui calculent une échéance ne peuvent donc pas utiliser ces constantes.
- Correction proposée : ajouter les trois définitions au niveau du module, après les imports, avec les valeurs 21, 7 et 3 ; conserver ces mêmes valeurs pour préserver les règles métier.
- Résultat après ajout des constantes transmis par l'utilisatrice : **21 tests réussis en 3,37 s** ; Ruff signale 8 C901 et 1 I001 (organisation du bloc des imports).
- Ajustement : `python -m ruff check bibliotech.py --select I --fix` a corrigé le signalement I001 (`1 fixed`).
- Vérifications finales transmises par l'utilisatrice : **21 tests réussis en 3,35 s**, puis **8 problèmes Ruff**, tous C901. Les durées métier sont conservées ; les noms rendent leur rôle explicite sans réduire la complexité.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le renommage en `count_active_loans` a été enregistré dans le commit `f7b4073`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 28 — Extraire le calcul des pénalités et l'utiliser pour les retours</summary>

- Défaut : calcul des pénalités répété dans plusieurs opérations, augmentant la complexité et le risque de divergences.
- Emplacement : nouvelle fonction de module `calculate_late_fee(days_late, book, member)` et méthode `ret()` de `bibliotech.py`.
- Correction : extraire les tarifs par type de document, les réductions par type de membre, le plafond au prix du document et l'arrondi dans la fonction commune ; remplacer le calcul dans `ret()` par un appel à cette fonction. Conserver la normalisation des jours de retard négatifs à zéro avant cet appel.
- Principes : DRY, extraction de fonction et séparation du calcul de la gestion du retour.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,44 s** ; **7 problèmes Ruff**, tous C901, contre 8 avant cet essai.
- État : première utilisation de la fonction commune validée par les tests fournis ; commit en attente. Les autres calculs dupliqués restent à remplacer progressivement.
- Suivi de l'essai précédent : les constantes des durées d'emprunt ont été enregistrées dans le commit `c95d4a3`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 29 — Réutiliser le calcul des pénalités pour les retards</summary>

- Défaut : duplication du calcul des tarifs, réductions, plafond et arrondi dans `overdue()`.
- Emplacement : `bibliotech.py`, méthode `overdue()`, anciennes lignes 301 à 318.
- Correction : remplacer ce calcul par `p = calculate_late_fee(nbj, book, member)`, en conservant le calcul des jours de retard, le cumul et l'affichage.
- Principes : DRY et réduction de la complexité ; les retards et les retours utilisent désormais le même calcul des pénalités.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,41 s** ; **6 problèmes Ruff**, tous C901, contre 7 avant cet essai.
- État : correction validée par les tests fournis ; commit en attente. Les autres duplications seront examinées séparément.
- Suivi de l'essai précédent : l'extraction du calcul pour les retours a été enregistrée dans le commit `85acec4`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 30 — Réutiliser le calcul des pénalités dans l'export</summary>

- Défaut : duplication du calcul des pénalités dans `export()`.
- Emplacement : `bibliotech.py`, méthode `export()`, anciennes lignes 438 à 456.
- Correction : conserver le calcul du retard, ramener les jours négatifs à zéro, puis appeler `fee = calculate_late_fee(dl, bk, mb)` à la place des règles dupliquées ; conserver l'écriture de la ligne exportée.
- Principes : DRY et réduction de la complexité ; retours, liste des retards et export utilisent le même calcul.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,90 s** ; **5 problèmes Ruff**, tous C901, contre 6 avant cet essai.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le calcul commun pour les retards a été enregistré dans le commit `5f58ff3`, confirmé par le terminal de l'utilisatrice.

</details>

<details>
<summary>Essai 31 — Réutiliser le calcul des pénalités dans le rapport d'activité</summary>

- Défaut : dernière duplication des règles de pénalité dans `report()`.
- Emplacement : `bibliotech.py`, méthode `report()`, anciennes lignes 353 à 369.
- Correction : remplacer le calcul par `pen = calculate_late_fee(j, bk, mb)` ; conserver le calcul des jours et le cumul de la pénalité arrondie.
- Principes : DRY et centralisation des règles métier ; retours, retards, export et rapport utilisent désormais la fonction commune.
- Tests transmis par l'utilisatrice après remplacement : **21 tests réussis en 3,44 s**.
- Analyse initiale après cet essai : 5 C901 et 1 W291. Suppression ciblée de l'espace de fin de ligne avec `python -m ruff check bibliotech.py --select W291 --fix` : `1 fixed`.
- Analyse finale transmise : **5 problèmes Ruff**, tous C901, comme avant cet essai. La centralisation réduit la duplication sans faire passer une fonction supplémentaire sous le seuil de complexité configuré.
- État : correction vérifiée avec les tests fournis avant la suppression d'espace final ; commit en attente.
- Suivi de l'essai précédent : le calcul commun dans l'export a été enregistré dans le commit `a1cd59f`, confirmé par le terminal de l'utilisatrice.

</details>

### Corrections et documentation après revue

<details>
<summary>Documentation des corrections de revue</summary>

- Ajout de commentaires et de docstrings en français pour expliquer les unités des dictionnaires métier, les valeurs par défaut, les réductions, le plafond et l'arrondi des pénalités.
- Documentation de la conversion numérique du prix (sans eval), de l'indépendance des options de plugins et de la journalisation des exceptions avec poursuite des plugins suivants.
- Aucun changement de logique dans cette étape. Suite fournie : **21 tests réussis en 4,81 s**. Deux lignes de documentation trop longues signalées lors du premier contrôle ont été raccourcies avant le contrôle final.

</details>

<details>
<summary>Revue de l'enseignant — correction des six remarques</summary>

1. **Prix du CSV** : remplacement de `eval(x[4])` par `float(x[4])` dans `load()`. Un prix est désormais interprété uniquement comme un nombre, sans exécution de code.
2. **Plugins** : suppression de `suppress` et du `pass` inutile. `run_plugins()` intercepte les exceptions ordinaires avec `except Exception`, puis les journalise avec `LOGGER.exception`, le nom du plugin, l'événement et la trace complète. Les plugins suivants continuent de s'exécuter. Les interruptions comme SystemExit restent propagées. Le journal utilise le module standard logging et sa sortie stderr par défaut en l'absence de configuration.
3. **Séparation des changements** : le formatage initial disposait déjà du commit `6d8b3d8` (Ruff, pas Black). Un nouveau commit exclusivement consacré au formatage restant, `f339aef`, précède les corrections de revue et corrige notamment `d =BOOK_LOAN_DAYS`. L'historique déjà publié n'a pas été réécrit ; le diff global de la PR conserve donc aussi le formatage initial. Les nouveaux changements sont consultables séparément par commit.
4. **Chaînes** : remplacement des longues concaténations des messages (emprunt, retour, rappel, rapport, catalogue et membres) par des f-strings, et des lignes CSV/en-têtes par `join`, en conservant les séparateurs, retours à la ligne et deux décimales.
5. **Règles métier** : dictionnaires `LOAN_DAYS`, `DAILY_FEE` et `MAX_LOANS` pour les durées, tarifs journaliers et limites. Les valeurs par défaut sont conservées : durée et tarif d'un livre pour un type de document inconnu, limite standard pour un type de membre inconnu. Les réductions étudiant/premium restent explicitement appliquées.
6. **Arrondi** : suppression de `round(pen, 2)` dans le cumul du rapport ; la fonction commune retourne déjà une pénalité arrondie.

Vérifications après corrections :

- Suite fournie : **21 tests réussis en 7,15 s**.
- Ruff : **5 C901 restants**, aucun nouveau signalement ; `ruff format bibliotech.py --check` confirme le formatage.
- `git diff --check` : aucun défaut d'espacement.
- `tests/` et `data/` inchangés depuis `v0-initial`.
- Vérification ciblée séparée dans `../tmp/verify_bibliotech_review.py`, sans modification des tests fournis : une expression Python dans le prix est rejetée avec ValueError sans créer le fichier témoin ; un plugin défaillant produit un journal avec nom, événement et trace ; le plugin suivant s'exécute ; SystemExit se propage ; tarifs, réductions, plafond, absence de retard et valeur par défaut vérifiés.
- Le diff global ne peut pas être réduit à deux commits sans réécriture de l'historique publié : cette opération n'a pas été effectuée.

</details>

## Journal détaillé du TP2

Les entrées ci-dessous conservent les essais dans leur ordre de réalisation. Les mentions « en attente » et « prochaine étape » décrivent la situation au moment de chaque essai. Le bilan actuel figure plus haut : les niveaux 1 et 2 sont réalisés, les 37 tests ont réussi et le travail a été publié pour revue.

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

### Section 3.4 — Renommage final et mesure après refactoring

- Clauses de garde enregistrées dans le commit `45dbfc3`.
- Renommage de `borrow_document` en `borrow`, avec mise à jour de l'appel dans `process()` et des huit appels dans les six tests d'emprunt.
- Vérification transmise : **37 tests réussis en 4,37 s** (21 de caractérisation, 6 d'emprunt et 10 de pénalités).
- `radon cc -s -n C bibliotech.py` affiche uniquement `process` C (16) et `report` C (14) : aucune fonction en note D ou supérieure.
- `radon cc -s bibliotech.py` confirme **borrow A (4)**, contre **borrow_document C (18)** au départ ; `refusal_reason` B (6), `has_overdue_loan` A (4), `is_borrowing` A (4) et `create_loan` A (3).
- Critères techniques obligatoires vérifiés : calcul unique dans `late_fee`, tests verts, méthode `borrow` en A et aucune fonction en D. Aucun bonus réalisé.
- État : commit de la section 3.4 en attente, puis publication et pull request selon le modèle du guide. La revue croisée et la validation de l'enseignant restent nécessaires avant fusion.
