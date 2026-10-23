# BiblioTech

## 1. Présentation

Application Python en ligne de commande de gestion d'une bibliothèque municipale : catalogue, membres, emprunts, retours, pénalités, rappels, rapports et export CSV. Projet individuel de **Awa BOUARE**, module Clean Code et Qualité logicielle.

Ce README regroupe les résultats, les justifications et les journaux des trois TP. L'objectif est d'améliorer un programme existant par petits pas en conservant les comportements couverts par les tests.

| Fichiers | Rôle |
| --- | --- |
| `bibliotech.py` | Règles métier, chargement CSV et commandes |
| `data/` | Livres, membres et emprunts |
| `tests/test_caracterisation.py`, `tests/golden/` | Scénarios et sorties fournis |
| `tests/test_rules.py`, `tests/test_borrow.py`, `tests/test_find.py` | Tests unitaires ajoutés |
| `tests/conftest.py` | Données isolées et date fixe |
| `pyproject.toml`, `requirements.txt` | Configuration et dépendances |

| TP | Travail réalisé | Trace |
| --- | --- | --- |
| 1 | Nettoyage et corrections de revue ; 21 tests verts | [PR 1 fusionnée](https://github.com/awa78/bibliotech-BOUARE/pull/1), `v0-initial` |
| 2 | Refactoring des pénalités et emprunts ; 37 tests verts | [PR 2 fusionnée](https://github.com/awa78/bibliotech-BOUARE/pull/2), `v2-fin-j2` |
| 3 | Cinq priorités traitées ; 44 tests verts ; zéro erreur Ruff TP3 | Branche `qualite` ; PR finale à ouvrir après publication |

## 2. TP 1 – Clean Code


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

Des vérifications ciblées supplémentaires ont été exécutées pendant la revue : rejet d'une expression Python dans un prix sans exécution, présence du nom et de la trace d'un plugin défaillant dans les journaux, poursuite du plugin suivant, propagation de `SystemExit`, tarifs, réductions, plafond et cas sans retard. Le script de vérification était extérieur au dépôt ; ces contrôles ne constituent pas encore une suite de tests unitaires versionnée. Les tests unitaires ont ensuite été ajoutés au TP2.

### Difficultés rencontrées et solutions

- Accès refusé au dossier temporaire de pytest et à son cache : utilisation d'un autre dossier temporaire et désactivation du cache pour les exécutions concernées.
- Collage du préfixe PowerShell avec la commande : exécution des commandes seules, une à la fois.
- Conflit entre un onglet VS Code ancien et le fichier enregistré : rechargement depuis le disque avant reprise des modifications.
- Erreurs d'indentation dans le compteur de l'export : diagnostic par `git diff`, puis correction avant commit.
- Renommage incomplet de la méthode d'emprunt et constantes non définies : mise en cohérence des définitions et des appels, puis nouvelle exécution des tests.

Les échecs observés et leur résolution sont détaillés dans le journal complet ci-dessous. Les corrections ont été enregistrées par étapes ; les remarques de revue ont donné lieu à de nouveaux commits. Le formatage initial et les corrections de revue sont identifiables par commit, sans réécriture de l'historique publié.


<details>
<summary>Journal complet des essais du TP1</summary>

Journal historique : les mentions de travaux en attente correspondent au moment de chaque essai. Le bilan actuel figure au-dessus.

### Synthèse TP1 — BiblioTech

### Objectif

Améliorer la lisibilité et la qualité du code sans changer le comportement de l'application. Conserver les tests fournis et vérifier chaque correction par petits pas.

### Bilan avant remise du TP1

- Contrôle effectué après le commit `5fa5b9a` : **21 tests réussis en 5,19 s**.
- Ruff : **55 problèmes au départ, 5 restants**, soit 50 signalements supprimés. Les 5 restants concernent la complexité des méthodes `load` (9), `find` (10), `borrow_document` (19), `report` (14) et de la fonction `process` (15), pour un seuil configuré à 8.
- Les dossiers `tests/` et `data/` sont inchangés par rapport à `v0-initial`. Aucun changement du code n'était en attente lors du contrôle.
- Améliorations : imports explicites et ordonnés, conditions simplifiées, noms de méthodes explicites, durées nommées, fermeture automatique des fichiers, formatage, gestion des exceptions précisée, suppression d'un argument mutable partagé et centralisation des pénalités dans une fonction commune.
- Le calcul des pénalités est réutilisé par les retours, les retards, l'export et le rapport. Les règles de tarif, réduction, plafond et arrondi restent regroupées dans un seul endroit.
- Limites : la réussite des tests caractérise les scénarios fournis. Les exceptions interceptées ont été volontairement restreintes comme documenté dans les essais 22 et 23. La complexité restante pourra faire l'objet d'un refactoring ultérieur ; le guide TP1 exige une diminution des signalements Ruff, sans imposer zéro problème.
- Organisation : travail individuel ; présence de `Massamba07` dans les collaborateurs confirmée par l'utilisatrice ; acceptation de l'invitation non précisée. Le lien du document partagé de promotion reste à demander à l'enseignant.
- Git : étiquette `v0-initial` publiée, branche locale `tp1/nettoyage`. À terminer : commit de ce bilan, publication de la branche, puis ouverture d'une pull request vers `main` avec résumé des améliorations, sans fusion.

Les entrées ci-dessous constituent le journal des essais ; les états « commit en attente » décrivent le moment de chaque essai et sont complétés par les confirmations des étapes suivantes. Le dernier calcul commun du rapport a été enregistré dans le commit `5fa5b9a`.

### Préparation — 21 octobre 2026

- Dépôt : https://github.com/awa78/bibliotech-BOUARE
- Projet récupéré dans `Documents\bibliotech-BOUARE`.
- Environnement Python `.venv` créé et dépendances de `requirements.txt` installées.
- Vérification initiale : **21 tests réussis**.
- Analyse initiale Ruff : **55 problèmes signalés**.
- Commande `python bibliotech.py list` : le catalogue s'affiche correctement.
- Étiquette locale `v0-initial` et branche `tp1/nettoyage` créées.
- Projet ouvert dans VS Code.

### Corrections et essais vérifiés

| Défaut | Emplacement | Correction | Principe | Vérification |
| --- | --- | --- | --- | --- |
| Deux modules importés sur une même ligne (E401) | `bibliotech.py`, imports au début du fichier | Remplacement de `import os, sys` par deux lignes : `import os` et `import sys` | Conventions Python et lisibilité | 21 tests réussis ; Ruff : 54 problèmes au lieu de 55 |
| Comparaison explicite d'un booléen à True (E712) | `bibliotech.py`, ligne 60, méthode `load()` | Utilisation directe de `debug` dans la condition | Simplicité et lisibilité | Résultat transmis par l'utilisatrice : 21 tests réussis ; Ruff : 53 problèmes au lieu de 54 |

#### Essai 1 — Séparer les imports

La séparation des imports facilite la lecture des dépendances. La correction a été constatée dans le fichier puis vérifiée automatiquement.

Commandes exécutées après la correction :

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check . --statistics
```

Résultats : `21 passed` et `Found 54 errors.`. Le code de sortie 1 de Ruff indique que des problèmes de qualité restent à corriger ; les tests ont réussi.

### Suivi

#### Documentation des corrections de revue

- Ajout de commentaires et de docstrings en français pour expliquer les unités des dictionnaires métier, les valeurs par défaut, les réductions, le plafond et l'arrondi des pénalités.
- Documentation de la conversion numérique du prix (sans eval), de l'indépendance des options de plugins et de la journalisation des exceptions avec poursuite des plugins suivants.
- Aucun changement de logique dans cette étape. Suite fournie : **21 tests réussis en 4,81 s**. Deux lignes de documentation trop longues signalées lors du premier contrôle ont été raccourcies avant le contrôle final.

#### Revue de l'enseignant — correction des six remarques

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

#### Essai 31 — Réutiliser le calcul des pénalités dans le rapport d'activité

- Défaut : dernière duplication des règles de pénalité dans `report()`.
- Emplacement : `bibliotech.py`, méthode `report()`, anciennes lignes 353 à 369.
- Correction : remplacer le calcul par `pen = calculate_late_fee(j, bk, mb)` ; conserver le calcul des jours et le cumul de la pénalité arrondie.
- Principes : DRY et centralisation des règles métier ; retours, retards, export et rapport utilisent désormais la fonction commune.
- Tests transmis par l'utilisatrice après remplacement : **21 tests réussis en 3,44 s**.
- Analyse initiale après cet essai : 5 C901 et 1 W291. Suppression ciblée de l'espace de fin de ligne avec `python -m ruff check bibliotech.py --select W291 --fix` : `1 fixed`.
- Analyse finale transmise : **5 problèmes Ruff**, tous C901, comme avant cet essai. La centralisation réduit la duplication sans faire passer une fonction supplémentaire sous le seuil de complexité configuré.
- État : correction vérifiée avec les tests fournis avant la suppression d'espace final ; commit en attente.
- Suivi de l'essai précédent : le calcul commun dans l'export a été enregistré dans le commit `a1cd59f`, confirmé par le terminal de l'utilisatrice.

#### Essai 30 — Réutiliser le calcul des pénalités dans l'export

- Défaut : duplication du calcul des pénalités dans `export()`.
- Emplacement : `bibliotech.py`, méthode `export()`, anciennes lignes 438 à 456.
- Correction : conserver le calcul du retard, ramener les jours négatifs à zéro, puis appeler `fee = calculate_late_fee(dl, bk, mb)` à la place des règles dupliquées ; conserver l'écriture de la ligne exportée.
- Principes : DRY et réduction de la complexité ; retours, liste des retards et export utilisent le même calcul.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,90 s** ; **5 problèmes Ruff**, tous C901, contre 6 avant cet essai.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le calcul commun pour les retards a été enregistré dans le commit `5f58ff3`, confirmé par le terminal de l'utilisatrice.

#### Essai 29 — Réutiliser le calcul des pénalités pour les retards

- Défaut : duplication du calcul des tarifs, réductions, plafond et arrondi dans `overdue()`.
- Emplacement : `bibliotech.py`, méthode `overdue()`, anciennes lignes 301 à 318.
- Correction : remplacer ce calcul par `p = calculate_late_fee(nbj, book, member)`, en conservant le calcul des jours de retard, le cumul et l'affichage.
- Principes : DRY et réduction de la complexité ; les retards et les retours utilisent désormais le même calcul des pénalités.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,41 s** ; **6 problèmes Ruff**, tous C901, contre 7 avant cet essai.
- État : correction validée par les tests fournis ; commit en attente. Les autres duplications seront examinées séparément.
- Suivi de l'essai précédent : l'extraction du calcul pour les retours a été enregistrée dans le commit `85acec4`, confirmé par le terminal de l'utilisatrice.

#### Essai 28 — Extraire le calcul des pénalités et l'utiliser pour les retours

- Défaut : calcul des pénalités répété dans plusieurs opérations, augmentant la complexité et le risque de divergences.
- Emplacement : nouvelle fonction de module `calculate_late_fee(days_late, book, member)` et méthode `ret()` de `bibliotech.py`.
- Correction : extraire les tarifs par type de document, les réductions par type de membre, le plafond au prix du document et l'arrondi dans la fonction commune ; remplacer le calcul dans `ret()` par un appel à cette fonction. Conserver la normalisation des jours de retard négatifs à zéro avant cet appel.
- Principes : DRY, extraction de fonction et séparation du calcul de la gestion du retour.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,44 s** ; **7 problèmes Ruff**, tous C901, contre 8 avant cet essai.
- État : première utilisation de la fonction commune validée par les tests fournis ; commit en attente. Les autres calculs dupliqués restent à remplacer progressivement.
- Suivi de l'essai précédent : les constantes des durées d'emprunt ont été enregistrées dans le commit `c95d4a3`, confirmé par le terminal de l'utilisatrice.

#### Essai 27 — Nommer les durées d'emprunt : constantes manquantes

- Objectif : remplacer les durées isolées 21, 7 et 3 par `BOOK_LOAN_DAYS`, `DVD_LOAN_DAYS` et `MAGAZINE_LOAN_DAYS`.
- Premier résultat transmis : **19 tests réussis et 2 échoués en 3,89 s**, scénarios `borrow_limit` et `borrow_ok`.
- Diagnostic : les noms sont utilisés dans `borrow_document()`, mais leurs définitions ne figurent pas dans le fichier enregistré. Les emprunts qui calculent une échéance ne peuvent donc pas utiliser ces constantes.
- Correction proposée : ajouter les trois définitions au niveau du module, après les imports, avec les valeurs 21, 7 et 3 ; conserver ces mêmes valeurs pour préserver les règles métier.
- Résultat après ajout des constantes transmis par l'utilisatrice : **21 tests réussis en 3,37 s** ; Ruff signale 8 C901 et 1 I001 (organisation du bloc des imports).
- Ajustement : `python -m ruff check bibliotech.py --select I --fix` a corrigé le signalement I001 (`1 fixed`).
- Vérifications finales transmises par l'utilisatrice : **21 tests réussis en 3,35 s**, puis **8 problèmes Ruff**, tous C901. Les durées métier sont conservées ; les noms rendent leur rôle explicite sans réduire la complexité.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le renommage en `count_active_loans` a été enregistré dans le commit `f7b4073`, confirmé par le terminal de l'utilisatrice.

#### Essai 26 — Donner un nom explicite au comptage des emprunts en cours

- Défaut : nom `nb` trop vague pour identifier le rôle de la méthode.
- Emplacement : `bibliotech.py`, définition à la ligne 112 et appels aux lignes 152 et 557 au moment de la correction.
- Correction : renommer `nb` en `count_active_loans` dans la définition et les deux appels.
- Principe : nommage explicite décrivant le comptage des emprunts en cours d'un membre.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,27 s** ; **8 problèmes Ruff**, tous C901, comme avant ce renommage. Cette amélioration porte sur la lisibilité, sans réduction de la complexité.
- État : renommage validé par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le renommage de `do_stuff` en `borrow_document` a été enregistré dans le commit `71b061b`, confirmé par le terminal de l'utilisatrice.

#### Essai 25 — Renommer la méthode d'emprunt : renommage incomplet détecté

- Objectif : remplacer le nom vague `do_stuff` par `borrow_document`, dans la définition et son appel.
- Résultat transmis : **7 tests échoués et 14 réussis**, tous les échecs concernant les scénarios d'emprunt ; le dernier lancement transmis dure 3,88 s.
- Diagnostic par comparaison au dernier commit : l'appel à la ligne 564 utilise `lib.borrow_document(...)`, mais la définition à la ligne 128 porte encore le nom `do_stuff`. Le renommage est incomplet.
- Correction proposée : renommer également la définition en `def borrow_document(self, mid, bid):` sans modifier son corps.
- Principe : nommage explicite ; mettre à jour la définition et les références ensemble.
- Résultat après correction transmis par l'utilisatrice : **21 tests réussis en 3,90 s** ; **8 problèmes Ruff**, tous C901, comme avant le renommage. Le changement améliore le nommage sans réduire la complexité.
- État : renommage validé par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : l'utilisation de suppress a été enregistrée dans le commit `ab3065b`, confirmé par le terminal de l'utilisatrice.

#### Essai 24 — Exprimer explicitement l'ignorance des erreurs des plugins

- Défaut : bloc `try` / `except Exception: pass` pouvant être exprimé avec `contextlib.suppress` (SIM105).
- Emplacement : imports et méthode `run_plugins()` de `bibliotech.py`, anciennes lignes 494 à 501 après ajout de l'import.
- Correction : ajouter `from contextlib import suppress`, puis remplacer le bloc `try` / `except` par `with suppress(Exception):` autour de l'appel et de l'ajout du résultat ; conserver `return res` après la boucle.
- Principe : exprimer directement l'intention d'ignorer les exceptions ordinaires d'un plugin et continuer les suivants, avec la même portée d'interception que `except Exception`.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,32 s** ; **8 problèmes Ruff**, contre 9 avant cet essai. Le signalement SIM105 a disparu ; les 8 signalements restants sont C901 (complexité des fonctions).
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la capture des erreurs des plugins a été limitée à Exception dans le commit `0a6fb95`, confirmé par le terminal de l'utilisatrice.

#### Essai 23 — Délimiter les exceptions interceptées dans les plugins

- Défaut : `except:` sans type d'exception dans `run_plugins()` (E722).
- Emplacement : `bibliotech.py`, ligne 499 au moment de la correction.
- Correction : remplacer `except:` par `except Exception:` en conservant le bloc `pass`.
- Principe : intercepter les erreurs ordinaires des plugins sans masquer les interruptions comme KeyboardInterrupt (Ctrl+C) et SystemExit.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,75 s** ; **9 problèmes Ruff**, contre 10 avant cet essai. Aucun signalement E722 ne reste.
- Limite : les tests fournis passent ; la propagation des interruptions est une modification intentionnelle de la gestion des exceptions. Ces résultats ne constituent pas une vérification spécifique des plugins.
- État : correction vérifiée avec les tests fournis ; commit en attente.
- Suivi de l'essai précédent : les exceptions de lecture des pénalités ont été précisées dans le commit `957ea42`, confirmé par le terminal de l'utilisatrice.

#### Essai 22 — Préciser les exceptions de lecture d'une pénalité

- Défaut : `except:` sans type d'exception lors de la conversion de `x[6]` en nombre (E722).
- Emplacement : `bibliotech.py`, méthode `load()`, ligne 58 au moment de la correction.
- Correction : remplacer `except:` par `except (ValueError, IndexError):` en conservant `fee = 0`.
- Principe : gérer explicitement les erreurs de conversion d'une valeur non numérique et d'accès à une colonne absente, sans masquer toutes les erreurs inattendues.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,32 s** ; **10 problèmes Ruff**, contre 11 avant cet essai. Les signalements E722 passent de 2 à 1.
- Limite : les tests fournis passent, mais le périmètre des exceptions interceptées est volontairement restreint ; les exceptions autres que ValueError et IndexError ne sont plus masquées par ce bloc.
- État : correction vérifiée avec les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la réunion des critères de retard du membre a été enregistrée dans le commit `247e1c8`, confirmé par le terminal de l'utilisatrice.

#### Essai 21 — Réunir les critères de retard d'un membre

- Défaut : conditions imbriquées dans la vérification des retards avant un emprunt (SIM102).
- Emplacement : `bibliotech.py`, méthode `do_stuff()`, anciennes lignes 136 à 141.
- Correction : réunir avec `and` les trois critères (identifiant du membre, emprunt non rendu, date d'échéance dépassée), puis conserver `late = True` dans le bloc.
- Principe : réduire l'imbrication en préservant l'ordre de vérification des conditions.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,28 s** ; **11 problèmes Ruff**, contre 12 avant cet essai. Aucun signalement SIM102 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la sélection des emprunts en retard a été enregistrée dans le commit `f8ae461`, confirmé par le terminal de l'utilisatrice.

#### Essai 20 — Réunir les conditions de sélection des emprunts en retard

- Défaut : deux conditions `if` imbriquées pouvant être réunies (SIM102).
- Emplacement : `bibliotech.py`, méthode `overdue()`, anciennes lignes 273 à 275.
- Correction : réunir avec `and` la vérification de l'absence de retour et celle du dépassement de la date d'échéance, puis conserver `tmp.append(x)` dans le bloc.
- Principe : réduire l'imbrication et rendre les critères de sélection lisibles ; `and` conserve l'évaluation conditionnelle de la date après le contrôle du retour.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,30 s** ; **12 problèmes Ruff**, contre 13 avant cet essai. Les signalements SIM102 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la simplification du texte du statut a été enregistrée dans le commit `5c6e504`, confirmé par le terminal de l'utilisatrice.

#### Essai 19 — Simplifier le choix du texte du statut

- Défaut : bloc `if`/`else` affectant une chaîne à `s` (SIM108).
- Emplacement : `bibliotech.py`, commande `members`, anciennes lignes 544 à 547.
- Correction : remplacer le bloc par `s = "actif" if x["active"] else "inactif"`.
- Principe : expression conditionnelle courte pour une affectation simple et lisible.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,24 s** (sortie complète du message précédent) ; **13 problèmes Ruff**, contre 14 avant cet essai. Aucun signalement SIM108 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le calcul direct du booléen actif a été enregistré dans le commit `d4aa603`, confirmé par le terminal de l'utilisatrice. Les interruptions Ctrl+C ultérieures n'ont pas annulé ce commit terminé.

#### Essai 18 — Affecter directement le résultat d'une comparaison

- Défaut : bloc `if`/`else` affectant `True` ou `False` à `a` (SIM108).
- Emplacement : `bibliotech.py`, lecture des membres dans `load()`, anciennes lignes 46 à 49 de la version enregistrée après formatage.
- Correction : remplacer le bloc par `a = x[4] == "1"`.
- Principe : simplicité ; une comparaison produit déjà un booléen.
- Incident : les numéros affichés dans VS Code différaient de ceux du fichier enregistré. Une capture montrait le message `Failed to save 'bibliotech.py': The content of the file is newer.` Solution conseillée : fermer la version ancienne sans l'enregistrer, puis rouvrir le fichier depuis le disque avant de reprendre la correction.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,74 s** ; **14 problèmes Ruff**, contre 15 avant cet essai. Les signalements SIM108 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le formatage a été enregistré dans le commit `6d8b3d8`, confirmé par le terminal de l'utilisatrice.
- Les numéros de ligne suivants seront vérifiés avant chaque nouvelle modification.

#### Essai 17 — Formater le fichier Python

- Défaut : 19 lignes dépassant la longueur configurée (E501) et présentation du code à harmoniser.
- Emplacement : ensemble du fichier `bibliotech.py`.
- Correction : exécution de `python -m ruff format bibliotech.py` ; résultat transmis : `1 file reformatted`.
- Principe : conventions Python et présentation cohérente facilitant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,69 s** ; **15 problèmes Ruff**, contre 34 avant cet essai et 55 initialement. Les 19 signalements E501 ont disparu.
- Problèmes restants à ce stade : 8 C901, 2 E722, 2 SIM102, 2 SIM108 et 1 SIM105.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la fermeture automatique du fichier exporté a été enregistrée dans le commit `71fa056`, confirmé par le terminal de l'utilisatrice.
- Le formatage modifie de nombreux numéros de ligne ; les prochains emplacements devront être relevés dans le fichier actuel.

#### Essai 16 — Fermer automatiquement le fichier exporté : diagnostic en cours

- Objectif : remplacer l'ouverture et la fermeture manuelles dans `export()` par un bloc `with`, sans modifier le calcul ni le contenu exporté.
- Premier résultat transmis : **20 tests réussis et 1 échoué en 3,34 s**, scénario `export`. Le message annonce 1 ligne exportée au lieu de 12.
- Diagnostic par comparaison au commit précédent : `n = n + 1` à la ligne 349 est resté hors de la boucle `for x in self.l:`. Il s'exécute une seule fois après la boucle au lieu d'une fois par emprunt.
- Correction proposée : ajouter un niveau d'indentation (4 espaces) à cette ligne pour l'aligner avec `fee = round(fee, 2)` et l'écriture de chaque emprunt.
- Deuxième essai transmis : même échec, **20 tests réussis et 1 échoué en 3,01 s**. La relecture du fichier enregistré confirme que le compteur avait toujours 12 espaces au lieu de 16.
- Correction appliquée par l'assistant : indentation du compteur à 16 espaces, dans la boucle, et suppression des espaces sur la ligne vide suivante.
- Vérification exécutée par l'assistant après correction : **21 tests réussis en 3,07 s** avec le cache désactivé ; **34 problèmes Ruff**, contre 35 avant cet essai. Aucun signalement SIM115 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la sauvegarde avec `with` a été enregistrée dans le commit `b6e37f9`, confirmé par le terminal de l'utilisatrice.

#### Essai 15 — Fermer automatiquement le fichier des emprunts à la sauvegarde

- Défaut : ouverture de `loans.csv` en écriture et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `save()`, anciennes lignes 57 à 62.
- Correction : utiliser `with open(DATA + "/loans.csv", "w") as f:`, placer l'écriture de l'en-tête et la boucle d'écriture dans ce bloc et supprimer `f.close()`.
- Principe : gestion fiable des ressources ; fermeture automatique du fichier, y compris si une écriture lève une exception.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,29 s** ; **35 problèmes Ruff**, contre 36 avant cet essai et 55 initialement. Les signalements SIM115 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture des emprunts avec `with` a été enregistrée dans le commit `85fdd8b`, confirmé par le terminal de l'utilisatrice.
- Les prochains numéros de ligne seront vérifiés avant modification.

#### Essai 14 — Fermer automatiquement le fichier des emprunts à la lecture

- Défaut : ouverture de `loans.csv` en lecture et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 43 à 45.
- Correction : utiliser `with open(DATA + "/loans.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; fermeture du fichier même en cas d'exception pendant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,77 s** ; **36 problèmes Ruff**, contre 37 avant cet essai. Les signalements SIM115 passent de 3 à 2.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture du fichier des membres avec `with` a été enregistrée dans le commit `90132ab`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

#### Essai 13 — Fermer automatiquement le fichier des membres

- Défaut : ouverture de `members.csv` et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 32 à 34.
- Correction : utiliser `with open(DATA + "/members.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; fermeture du fichier même en cas d'exception pendant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,56 s** ; **37 problèmes Ruff**, contre 38 avant cet essai. Les signalements SIM115 passent de 4 à 3.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture du catalogue avec `with` a été enregistrée dans le commit `4f87db5`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

#### Essai 12 — Fermer automatiquement le fichier du catalogue

- Défaut : ouverture de `books.csv` et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 25 à 27.
- Correction : utiliser `with open(DATA + "/books.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; le fichier est fermé même si la lecture lève une exception.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,74 s** ; **38 problèmes Ruff**, contre 39 avant cet essai. Les signalements SIM115 passent de 5 à 4.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la suppression du dictionnaire mutable par défaut a été enregistrée dans le commit `f0178fe`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

#### Essai 11 — Éviter un dictionnaire mutable comme argument par défaut

- Défaut : `options={}` dans la signature de `register_plugin()` (B006) ; le dictionnaire par défaut est partagé entre les appels.
- Emplacement : `bibliotech.py`, méthode `register_plugin()`, ancienne ligne 358.
- Correction : utiliser `options=None`, puis initialiser `options = {}` dans un bloc `if options is None:` avant l'enregistrement du plugin.
- Principe : éviter un état mutable partagé implicitement entre les appels.
- Incident de saisie : une nouvelle `ParserError` sur `PS` provenait du collage du préfixe du terminal ; les tests n'avaient pas démarré. La commande seule a ensuite été exécutée correctement.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,88 s** ; **39 problèmes Ruff**, contre 40 avant cet essai. Le signalement B006 a disparu. Ces résultats valident les scénarios fournis ; ils ne constituent pas un test spécifique de l'indépendance des dictionnaires entre plugins.
- État : correction vérifiée avec la suite fournie ; commit en attente.
- Suivi de l'essai précédent : le tri des imports a été enregistré dans le commit `8394c2a`, confirmé par le terminal de l'utilisatrice.
- Les deux lignes ajoutées décalent les emplacements suivants ; les prochaines lignes seront vérifiées avant modification.

#### Essai 10 — Trier automatiquement les imports

- Défaut : ordre des imports non conforme (I001), au début de `bibliotech.py`.
- Correction : exécution ciblée de `python -m ruff check bibliotech.py --select I --fix`.
- Résultat de la correction transmis par l'utilisatrice : `Found 1 error (1 fixed, 0 remaining).` Ce résultat concerne uniquement les règles de tri des imports sélectionnées.
- Principe : conventions Python et organisation lisible des dépendances.
- Incident de saisie : du texte de l'historique et le préfixe `(.venv) PS ...>` ont été recollés dans PowerShell, provoquant une saisie multiligne puis une `ParserError` sur `PS`. Solution : revenir à l'invite normale et exécuter uniquement la commande, sans préfixe ni sortie précédente. Aucune modification du programme n'était nécessaire pour cet incident.
- Vérifications finales transmises par l'utilisatrice : **21 tests réussis en 2,95 s** ; **40 problèmes Ruff**, contre 41 avant cet essai et 55 initialement. Le signalement I001 a disparu.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : les imports datetime explicites ont été enregistrés dans le commit `bbba5a2`, confirmé par le terminal de l'utilisatrice.

#### Essai 9 — Rendre les imports datetime explicites

- Défaut : import global `from datetime import *` et import redondant `import datetime`, rendant l'origine des noms moins claire (F403 et F405).
- Emplacement : `bibliotech.py`, bloc des imports, anciennes lignes 5 à 8.
- Correction : conserver `import os` et `import sys`, puis importer explicitement `date`, `datetime` et `timedelta` avec `from datetime import date, datetime, timedelta`.
- Principe : dépendances explicites et lisibilité ; suppression d'un import redondant.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,02 s** ; **41 problèmes Ruff**, contre 44 avant cette correction. Le signalement F403 et les deux signalements F405 ont disparu.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la dernière simplification booléenne a été enregistrée dans le commit `9a5b8c5`, confirmé par le terminal de l'utilisatrice.
- Attention pour la suite : la suppression d'une ligne dans les imports décale les numéros des lignes suivantes ; les prochains emplacements devront être vérifiés.

#### Essai 8 — Simplifier la dernière comparaison booléenne

- Défaut : comparaison explicite d'un résultat avec `False` (E712).
- Emplacement : `bibliotech.py`, ligne 412.
- Correction : remplacement de `if r == False:` par `if not r:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,37 s** ; **44 problèmes Ruff**, contre 45 avant cette correction et 55 initialement. Aucun signalement E712 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition du membre actif dans l'affichage a été enregistrée dans le commit `848da21`, confirmé par le terminal de l'utilisatrice.

#### Essai 7 — Simplifier la condition du membre actif dans l'affichage

- Défaut : comparaison explicite d'un booléen avec `True` (E712).
- Emplacement : `bibliotech.py`, ligne 259.
- Correction : remplacement de `if x["active"] == True:` par `if x["active"]:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 2,95 s** ; **45 problèmes Ruff**, contre 46 avant cette correction. Il reste un signalement E712.
- État : correction validée ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition d'absence de retard a été enregistrée dans le commit `f70af4b`, confirmé par le terminal de l'utilisatrice.

#### Essai 6 — Simplifier la condition d'absence de retard

- Défaut : comparaison explicite d'un booléen avec `False` (E712).
- Emplacement : `bibliotech.py`, ligne 114, méthode `do_stuff()`.
- Correction : remplacement de `if late == False:` par `if not late:` sans modifier l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,19 s** ; **46 problèmes Ruff**, contre 47 avant cette correction. Les signalements E712 passent de 3 à 2.
- État : correction validée ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition du membre actif a été enregistrée dans le commit `84e96c9`, confirmé par le terminal de l'utilisatrice.

#### Essai 5 — Simplifier la condition du membre actif

- Défaut : comparaison explicite d'un booléen avec `True` (E712).
- Emplacement : `bibliotech.py`, ligne 107, méthode `do_stuff()`.
- Correction : remplacement de `if mb["active"] == True:` par `if mb["active"]:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 2,93 s** avec la commande pytest utilisant le dossier temporaire distinct ; **47 problèmes Ruff**, contre 48 avant cette correction. Les signalements E712 passent de 4 à 3.
- Étape 6 du guide confirmée par `git branch --show-current` : branche active `tp1/nettoyage`.
- État : correction validée ; commit en attente. Les trois autres comparaisons booléennes proposées restent à traiter séparément.

#### Suivi du guide — accès et publication du point de départ

- L'utilisatrice confirme travailler seule : aucun binôme à ajouter.
- Elle confirme que `Massamba07` apparaît dans la liste des collaborateurs ; l'acceptation de l'invitation n'a pas été précisée.
- Partage du lien du dépôt dans le document de promotion : en attente. L'utilisatrice doit demander à l'enseignant où trouver ce document.
- Étape 5 : `git push origin v0-initial` exécuté par l'utilisatrice avec succès ; le terminal confirme `[new tag] v0-initial -> v0-initial`. Le point de départ est désormais publié sur GitHub.
- Étape 6 : branche locale `tp1/nettoyage` déjà créée ; prochaine vérification avant de reprendre le nettoyage.

#### Vérification globale de reprise — 21 octobre 2026

- Branche active : `tp1/nettoyage` ; dernier commit : `cec41ec`.
- Tests relancés : **21 réussis en 3,29 s** (`.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider`).
- Analyse Ruff relancée : **48 problèmes**, contre 55 initialement.
- Les dossiers `tests/` et `data/` sont identiques à la version `v0-initial`.
- Aucune modification du code en attente ; seul ce rapport a des modifications non commitées.
- Vérification distante avec `git ls-remote` : seule la branche `main`, au commit initial, est présente parmi les références recherchées. La branche `tp1/nettoyage` et l'étiquette `v0-initial` ne sont pas encore publiées sur GitHub.
- Prochaine correction proposée, non appliquée : simplifier les quatre comparaisons booléennes aux lignes 107, 114, 259 et 412.
- Invitations des collaborateurs et dépôt du lien dans le document de promotion : non vérifiés, aucun accès à ces informations dans cet audit.

#### Essai 4 — Comparaisons avec None : échec détecté et diagnostic

- Objectif : remplacer les comparaisons `== None` et `!= None` par `is None` et `is not None` aux lignes 104, 106, 174 et 376.
- Premier résultat transmis : **19 tests réussis et 2 échoués** (`report`, `report_after_returns`) ; Ruff signale **49 problèmes**, dont un E711 restant.
- Diagnostic par comparaison au dernier commit : les lignes 104, 106 et 174 sont correctement modifiées, mais la condition `if bk["kind"] in k:` à la ligne 306 a été remplacée par erreur par `if TODAY is None:`. Cela réinitialise les compteurs par type de document dans le rapport. La comparaison prévue à la ligne 376 n'a pas été modifiée.
- Correction proposée : rétablir `if bk["kind"] in k:` à la ligne 306, puis remplacer `if TODAY == None:` par `if TODAY is None:` à la ligne 376.
- Enseignement : les tests ont détecté une modification involontaire du comportement ; une baisse du nombre de problèmes Ruff ne suffit pas à valider une correction.
- Résultat après correction transmis par l'utilisatrice : **21 tests réussis en 4,44 s**, et **48 problèmes Ruff**, contre 52 avant cet essai. Les quatre signalements E711 ont disparu. Les tests du rapport réussissent à nouveau.
- État : correction validée par les tests fournis et enregistrée dans le commit local `cec41ec`, confirmé par le terminal de l'utilisatrice.

#### Essai 3 — Supprimer un import inutilisé

- Défaut : import du module `json` sans utilisation dans le fichier (F401).
- Emplacement : `bibliotech.py`, ancienne ligne 9, bloc des imports.
- Correction : suppression de `import json`.
- Principe : supprimer le code inutile et rendre les dépendances plus lisibles.
- Vérifications transmises par l'utilisatrice : `python -m pytest -q -p no:cacheprovider --basetemp "$env:TEMP\bibliotech-tests-awa"` donne **21 tests réussis en 4,39 s** ; `python -m ruff check . --statistics` donne **52 problèmes**, contre 53 avant cette correction et 55 au départ. Le signalement F401 a disparu.
- État : correction validée par les tests fournis et enregistrée dans le commit local `8f011c9`, confirmé par le terminal de l'utilisatrice.

#### Essai 2 — Vérification depuis le terminal de VS Code

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

## 3. TP 2 – Refactoring

Le TP2 a été fusionné par l'enseignant. Les niveaux obligatoires 1 et 2 sont réalisés.

| Travail | Justification |
| --- | --- |
| Fonction pure `late_fee` ; 10 tests paramétrés | Tester tarifs, réductions, plafond et absence de retard sans fichiers |
| Remplacements dans `ret`, `overdue`, `report`, `export` puis suppression de `calculate_late_fee` | Un seul calcul à maintenir ; migration progressive avec tests |
| `has_overdue_loan`, `is_borrowing` | Nommer et isoler les vérifications |
| `refusal_reason`, `create_loan`, clauses de garde | Séparer les refus de la création ; conserver leur ordre et leurs messages |
| Renommage en `borrow` et six tests d'emprunt | Vérifier les cinq refus et le succès avec des données isolées |

La complexité de l'emprunt passe de C (18) à A (4). Les tests passent de 21 à 37 : 21 de caractérisation, 10 de pénalités, six d'emprunt. `process` C (16) et `report` C (14) restent pour l'audit du TP3. Les dictionnaires de règles existaient déjà depuis les corrections de revue du TP1.


<details>
<summary>Journal des essais du TP2</summary>

Journal historique : les mentions de travaux en attente correspondent au moment de chaque essai. Le bilan actuel figure au-dessus.

#### Avancement actuel

Mise à jour après la section 3.4 : les niveaux obligatoires 1 et 2 ont passé leurs vérifications. Les entrées suivantes retracent les étapes précédentes.

#### Section 3.4 — Renommage final et mesure après refactoring

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

#### Section 3.3 — Extraire la recherche d'un emprunt en retard

- Ajout de `has_overdue_loan(member_id)`, méthode demandée par le guide, avec une expression `any` sur les emprunts non rendus du membre dont l'échéance est dépassée.
- Remplacement de la boucle et du drapeau dans `borrow_document()` par `late = self.has_overdue_loan(mid)`, sans modifier les refus ni leur ordre.
- Résultat transmis : **37 tests réussis en 4,36 s**.
- État : extraction vérifiée ; commit en attente. Les autres méthodes de la section 3.3 et le renommage final en `borrow` restent à réaliser.

#### Section 3.3 — Extraire la recherche d'un document déjà emprunté

- L'extraction de `has_overdue_loan` a été enregistrée dans le commit `0c240e7`.
- Ajout de `is_borrowing(member_id, book_id)` avec `any` pour vérifier l'existence d'un emprunt non rendu du membre pour ce document.
- Remplacement de la boucle et du drapeau par `deja = self.is_borrowing(mid, bid)`, en conservant le refus existant et sa priorité.
- Résultat transmis : **37 tests réussis en 4,97 s**.
- État : extraction vérifiée ; commit en attente. La section 3.3 continue ensuite avec les méthodes restantes et les clauses de garde.

#### Section 3.3 — Clauses de garde : remplacement incomplet détecté

- Extraction de `is_borrowing` enregistrée dans le commit `18c5bd8`.
- Ajout de `refusal_reason` et de `create_loan` pour séparer les refus et la création d'un emprunt.
- Premier essai transmis après suppression de l'ancien bloc : **13 tests échoués et 24 réussis en 4,92 s**.
- Diagnostic avec `git diff` : la méthode `borrow_document` a été supprimée, mais le nouveau bloc de clauses de garde n'a pas été ajouté dans le fichier enregistré. Les tests et `process` appellent donc une méthode absente.
- Correction effectuée : insertion de `borrow_document(member_id, book_id)` avec sorties immédiates pour un membre inconnu, un document inconnu et un motif de refus ; délégation à `refusal_reason` et `create_loan`.
- Nouvelle vérification transmise : **37 tests réussis en 4,59 s**. Les messages et les scénarios existants restent vérifiés. Section 3.3 prête à être commitée ; le renommage en `borrow` et la mise à jour des appels restent à faire en section 3.4.

#### Étape 1 : préparation du dépôt — 22 octobre 2026

- Fusion du TP1 par l'enseignant, récupérée sur `main` au commit `7481492`.
- Création de la branche `tp2/refactoring` depuis cette version.
- Récupération du README préparé avant le TP2 par cherry-pick (`c3c1cc5`), car cette mise à jour n'était pas incluse dans la fusion du TP1.
- Ajout de `pythonpath = ["."]` dans la configuration pytest et de `radon>=6.0` dans les dépendances ; Radon 6.0.1 installé dans `.venv`.
- Vérification de départ transmise : **21 tests réussis en 4,90 s**. Aucun refactoring du TP2 n'a encore été effectué.

#### Mesure Radon avant refactoring

Commande exécutée : `radon cc -s -n C bibliotech.py`.

| Fonction | Note initiale TP2 | Complexité initiale TP2 | Après refactoring |
| --- | --- | --- | --- |
| `Library.borrow_document` → `Library.borrow` | C | 18 | A (4) |
| `process` | C | 16 | C (16) |
| `Library.report` | C | 14 | C (14) |

La commande affiche seulement les blocs de note C ou supérieure : aucune note D n'est signalée à ce départ. Les résultats diffèrent de l'exemple du guide, car le code a déjà été amélioré au TP1. L'objectif du niveau 2 reste d'obtenir une méthode `borrow` de note A. Les niveaux obligatoires et les nouveaux tests unitaires restent à réaliser.

#### Tests avant refactoring — sections 2.1 et 3.1

- Préparation enregistrée dans le commit `16847fe`, puis branche `tp2/refactoring` publiée, selon les sorties du terminal transmises.
- Section 2.1 : création de `tests/test_rules.py` avec les cas de pénalité paramétrés. Le lancement ciblé produit l'ImportError attendue : `late_fee` n'existe pas encore sous ce nom. Ce rouge attendu n'est pas commité.
- Vérification séparée de `tests/test_caracterisation.py` : **21 tests réussis en 4,99 s** ; aucune régression constatée dans ces scénarios.
- Section 3.1 : création de `tests/conftest.py` avec la fixture du guide, qui copie les données et fixe la date au 21 octobre 2026.
- Section 3.1 : `tests/test_borrow.py` contient les six cas demandés, avec le nom actuel `borrow_document` à la place de `do_stuff` : membre inactif, retard existant, document déjà emprunté, indisponibilité, limite atteinte et emprunt accepté avec identifiant L013 et échéance au 28 octobre 2026.
- Vérification progressive : les tests d'emprunt passent de 1 à 6 cas réussis au fil de leur ajout. Vérification commune transmise : `tests/test_borrow.py` et `tests/test_caracterisation.py` donnent **27 tests réussis en 4,57 s**.
- `tests/test_rules.py` reste temporairement exclu de cette vérification ciblée : son erreur d'import sur `late_fee` est toujours le rouge attendu de la section 2.1. Il ne doit pas être commité avant l'ajout de la fonction et le passage au vert.
- Section 3.1 : tests des emprunts enregistrés dans le commit `fe6e0d9`, confirmé par le terminal de l'utilisatrice.
- Aucun bonus n'est entrepris.

#### Section 2.2 — Ajouter la fonction late_fee à côté du calcul existant

- Ajout de `late_fee(days_late: int, kind: str, member_type: str, price: float) -> float`, avant `calculate_late_fee`, sans modifier les quatre appels existants.
- La fonction utilise `DAILY_FEE`, une clause de garde sans retard, les réductions étudiant/premium, `min` pour le plafond et `round(..., 2)` pour l'arrondi.
- Les 10 cas paramétrés de `tests/test_rules.py` vérifient les résultats avec `pytest.approx`.
- Résultat transmis : **37 tests réussis en 4,34 s** (21 de caractérisation, 6 d'emprunt, 10 de pénalités). Le rouge attendu de la section 2.1 est résolu.
- État : fonction et tests prêts à être commités ensemble. Prochaine étape : section 2.3, remplacer les appels un par un, avec tests et commit après chacun. Le calcul existant sera retiré quand il ne sera plus utilisé.

#### Section 2.3 — Premier remplacement dans ret : diagnostic

- La fonction et ses tests ont été enregistrés dans le commit `bd98aa7`.
- Premier remplacement : appel à `late_fee(d, bk["kind"], mb["type"], bk["price"])` dans `ret()`.
- Premier essai transmis : **33 tests réussis et 4 échoués en 4,52 s**, concernant les retours.
- Diagnostic par `git diff` : modification involontaire de `datetime.strptime` en `datetime.strptie` dans le calcul des jours (ligne 265). L'appel à `late_fee` est correct.
- Correction effectuée : rétablissement de `strptime`. Nouvelle sortie transmise : **37 tests réussis en 4,31 s**. Le premier remplacement dans `ret()` est validé ; commit en attente. Les tests de caractérisation et leurs références restent inchangés.

#### Section 2.3 — Deuxième remplacement dans overdue

- Le remplacement dans `ret()` a été enregistré dans le commit `e819945`.
- Remplacement de l'appel de `overdue()` par `late_fee(nbj, book["kind"], member["type"], book["price"])`, sans modifier le calcul des jours ni les affichages.
- Résultat transmis : **37 tests réussis en 5,15 s**. Deuxième remplacement validé ; commit en attente. Les appels de `report()` et `export()` restent à adapter.

#### Section 2.3 — Troisième remplacement dans report

- Le remplacement dans `overdue()` a été enregistré dans le commit `ba98289`.
- Remplacement de l'appel de `report()` par `late_fee(j, bk["kind"], mb["type"], bk["price"])`, en conservant le calcul des jours et le cumul des pénalités.
- Résultat transmis : **37 tests réussis en 5,01 s**. Troisième remplacement validé ; commit en attente. L'appel de `export()` reste à adapter avant de retirer le calcul devenu inutilisé.

#### Section 2.3 — Quatrième remplacement dans export et fin du niveau 1

- Le remplacement dans `report()` a été enregistré dans le commit `d01647c`.
- Remplacement du dernier appel par `late_fee(dl, bk["kind"], mb["type"], bk["price"])` dans `export()`, en conservant la remise à zéro des jours négatifs. Vérification transmise : **37 tests réussis en 5,11 s**.
- Suppression de `calculate_late_fee`, devenue inutilisée. Vérification après suppression : **37 tests réussis en 4,81 s**.
- Contrôle du fichier : une définition de `late_fee` et quatre appels, dans `ret`, `overdue`, `report` et `export` ; aucune référence à `calculate_late_fee`.
- Le contrat du niveau 1 est couvert par les 10 cas paramétrés. Les 21 tests de caractérisation et les 6 tests d'emprunt restent verts.
- État : niveau 1 vérifié ; dernier commit de l'extraction en attente. Les cinq commits attendus correspondent à l'ajout de la fonction avec ses tests, puis aux quatre remplacements progressifs.
- Prochaine étape : niveau 2, section 3.2. Les tests de la section 3.1 sont déjà enregistrés ; vérifier les dictionnaires métier existants avant les clauses de garde de la section 3.3.

</details>

## 4. TP 3 – Qualité

### Analyse et priorités

Référence : tag publié `v2-fin-j2`, issu du TP2 fusionné sur `main` (`1ad84e7`). Travail sur `qualite`. L'audit ne signalait aucune anomalie de sécurité ou de fiabilité avec la sélection imposée ; les priorités ont donc porté sur la complexité, la duplication puis le code obsolète.

| Priorité | Amélioration et justification | Commit |
| --- | --- | --- |
| 1 | Extraire affichages et commandes ; dictionnaire de routage pour réduire les décisions dans `process` | [0983b9b](https://github.com/awa78/bibliotech-BOUARE/commit/0983b9b) |
| 2 | Extraire compteurs, classement et statistiques pour séparer calcul et affichage de `report` | [085df42](https://github.com/awa78/bibliotech-BOUARE/commit/085df42) |
| 3 | Recherche commune par identifiant ; sept tests ajoutés avant refactoring | [234030e](https://github.com/awa78/bibliotech-BOUARE/commit/234030e) |
| 4 | `load_books`, `load_members`, `load_loans` : une responsabilité par méthode, ordre et conversions conservés | [70c3ab0](https://github.com/awa78/bibliotech-BOUARE/commit/70c3ab0) |
| 5 | Suppression de `old_calc_fee` après recherche sans appel : éviter des tarifs obsolètes trompeurs | [e5f5434](https://github.com/awa78/bibliotech-BOUARE/commit/e5f5434) |

Exemple de séparation des chargements :

```python
self.load_books()
self.load_members()
self.load_loans()
```

Les messages, codes de sortie, tris et conversions sont conservés dans les scénarios testés. Le diff depuis le tag confirme que les tests de caractérisation et `tests/golden/` sont inchangés. Aucun relèvement du seuil Ruff (8), ajout de `noqa` ou bonus entrepris.

### Comparaison finale


Les mêmes commandes de mesure ont été utilisées avant et après les améliorations, en excluant les tests des analyses Ruff et Radon.

| Indicateur | Avant (`v2-fin-j2`) | Après les cinq priorités | Commentaire |
| --- | --- | --- | --- |
| Erreurs Ruff, sélection TP3 | 4 C901 | 0 | Les quatre fonctions signalées ont été simplifiées sans désactiver de règle. |
| Complexité moyenne Radon | B (5,18), 22 blocs | A (3,34), 32 blocs | Les extractions créent davantage de petites fonctions ; la moyenne se lit avec les scores individuels. |
| Blocs classés C ou plus | 2 : `process` (16), `report` (14) | 0 | `process` passe à A (4) et `report` à B (7). |
| Complexité des autres fonctions ciblées | `find` B (10), `load` B (9) | `find` A (3), `load` A (2) | Une recherche commune remplace trois boucles ; le chargement est réparti entre trois méthodes dédiées. |
| Tests | 37 réussis | 44 réussis en 5,02 s | Sept cas de recherche ont été ajoutés avant le refactoring de `find` ; les tests existants restent verts. |

La complexité maximale passe de 16 à 7. La baisse ne repose donc pas seulement sur l'ajout de petites fonctions dans la moyenne : les fonctions initialement les plus complexes ont elles-mêmes été simplifiées. Les tests vérifient la préservation des comportements couverts, sans constituer une preuve pour tous les cas possibles. Les durées de test ne permettent pas de conclure à un gain de performance.

La suppression effective de `old_calc_fee` a été enregistrée dans `e5f5434`, après le commit documentaire `69ad263`. Les contrôles après cette suppression donnent **44 tests réussis en 5,02 s** et aucune erreur Ruff. La recherche Radon des blocs C ou plus ne renvoie aucun résultat.

Dette restante : `Library` regroupe encore plusieurs responsabilités et ses collections `b`, `m`, `l` gardent des noms peu explicites. `report` reste la méthode la plus complexe (7). Ces points pourront être améliorés ultérieurement ; ils ne sont pas masqués par des exclusions supplémentaires ou des commentaires `noqa`.


<details>
<summary>Journal des mesures et corrections du TP3</summary>

Journal historique : les mentions de travaux en attente correspondent au moment de chaque essai. Le bilan actuel figure au-dessus.

#### Préparation et référence de comparaison

- TP1 et TP2 fusionnés par l'enseignant ; `main` récupéré au commit `1ad84e7` et vérifié propre.
- Vérification sur `main` : **37 tests réussis en 4,83 s**.
- Étiquette **`v2-fin-j2`** créée et publiée ; elle reste fixe comme référence « avant ».
- Branche **`qualite`** créée depuis cet état et publiée. Aucune correction du programme effectuée avant les mesures initiales.

#### Relevé initial

Voir le tableau final ci-dessus pour la comparaison.

Commandes identiques à utiliser pour les mesures avant et après :

```powershell
ruff check . --select E,W,F,B,S,C90,SIM --extend-exclude tests --statistics
radon cc -s -a --exclude "tests/*" .
radon cc -s -n C --exclude "tests/*" .
python -m pytest -q -p no:cacheprovider --basetemp "$env:TEMP\bibliotech-tests-awa"
```

Les options pytest contournent le problème d'accès au cache et au dossier temporaire rencontré sur ce poste ; elles seront conservées pour la mesure finale. Le dossier indiqué est réservé aux tests. La sélection Ruff du TP3 diffère des contrôles des TP précédents : leurs totaux ne doivent pas être comparés directement.

#### Défauts réellement présents et améliorations retenues

Le contrôle initial ne signale aucune règle de sécurité ou de fiabilité parmi les familles S et B, ni E722. Les corrections `eval`, exceptions nues et argument mutable déjà traitées ne sont donc pas revendiquées de nouveau au TP3. La priorité suivante du guide est la complexité, puis la duplication et la lisibilité.

| Priorité | Défaut | Où et comment repéré | Catégorie | Amélioration prévue et justification |
| --- | --- | --- | --- | --- |
| 1 | Routage des commandes, vérification des arguments et affichage mélangés | `process` : Radon C (16), Ruff C901, lecture du code | Complexité | Extraire les traitements des commandes pour réduire la fonction la plus complexe, en conservant les sorties et les codes de retour |
| 2 | Calcul des statistiques et affichages mêlés | `Library.report` : Radon C (14), Ruff C901, lecture du code | Complexité | Séparer les calculs du rapport de leur présentation, en gardant les mêmes montants, compteurs et classements |
| 3 | Trois boucles de recherche presque identiques | `Library.find` : Radon B (10), Ruff C901, lecture du code | Duplication et complexité | Mutualiser la recherche par identifiant tout en préservant les résultats et les cas inconnus |
| 4 | Une méthode charge et transforme trois fichiers | `Library.load` : Radon B (9), Ruff C901, lecture du code | Responsabilités et complexité | Extraire les chargements par fichier pour rendre chaque traitement plus court et distinct |
| 5 | Ancienne fonction avec des tarifs différents, marquée « ne plus utiliser » | `old_calc_fee`, lecture du code et recherche des références | Lisibilité et code inutilisé | Retirer le calcul obsolète après vérification de l'absence d'appels pour éviter de le confondre avec `late_fee` |

**État de l'audit :** mesures initiales relevées et cinq améliorations sélectionnées. Les corrections, leurs tests et leurs commits restent à réaliser, une amélioration à la fois. Aucune activité facultative n'a été commencée. Le README sera ensuite organisé selon les six parties exactes demandées par le guide, en conservant le suivi du travail.

#### Suivi des améliorations — priorité 1 : simplifier process

##### Première extraction : affichage du catalogue

- Problème : `process` assurait lui-même la boucle et la présentation de chaque document, en plus du routage des commandes.
- Modification : extraction de `display_catalog(library)` et remplacement du bloc de la commande `list` par `display_catalog(lib)` ; noms locaux `book` et `available` plus explicites.
- Justification : séparer la responsabilité d'affichage du catalogue du choix de la commande, sans changer le texte produit.
- Résultats transmis après modification : **37 tests réussis en 4,21 s** ; Ruff avec la sélection du TP3 : **4 signalements C901**. Le seuil Ruff reste dépassé ; la priorité 1 se poursuit par petits pas. Le tableau « après » ne sera rempli qu'une fois les améliorations terminées.
- État : étape vérifiée ; commit à effectuer après relecture du diff.

##### Deuxième extraction : affichage des membres

- L'extraction du catalogue a été enregistrée dans le commit `19f12cf`.
- Problème : `process` contenait aussi la boucle d'affichage des membres, le choix du texte actif/inactif et le comptage des emprunts en cours.
- Modification : extraction de `display_members(library)` ; le traitement de la commande `members` appelle désormais `display_members(lib)`. Les variables `member` et `status` décrivent leur rôle.
- Justification : séparer l'affichage des membres du routage des commandes et conserver le texte affiché.
- Résultats transmis : **37 tests réussis en 5,32 s** ; Ruff avec la sélection du TP3 : **4 signalements C901**. Cette étape prépare la simplification complète de `process` ; elle ne suffit pas encore à supprimer son signalement.
- État : deuxième extraction vérifiée ; commit à effectuer après relecture du diff.

##### Troisième extraction : traitement de la commande borrow

- L'extraction de l'affichage des membres a été enregistrée dans le commit `9985c59`.
- Problème : `process` gérait directement la vérification des arguments d'emprunt et la traduction du résultat métier en code de retour.
- Modification : extraction de `handle_borrow(library, args)` ; la commande `borrow` retourne désormais le résultat de cette fonction.
- Justification : isoler le traitement d'une commande du routage général. Les messages et les codes sont conservés : 1 pour arguments manquants, 2 pour refus, 0 pour succès.
- Résultats transmis : **37 tests réussis en 4,34 s** ; Ruff avec la sélection imposée : **4 signalements C901**. La simplification de `process` se poursuit ; les mesures finales seront relevées une fois les améliorations terminées.
- État : extraction vérifiée ; commit à effectuer après relecture du diff.

##### Quatrième extraction : traitement de la commande return

- Le traitement de `borrow` a été extrait dans le commit `3d1bdac`.
- Problème : `process` vérifiait directement l'argument de la commande `return` avant d'appeler la méthode métier.
- Modification : ajout de `handle_return(library, args)` et remplacement du bloc par `return handle_return(lib, args)`.
- Justification : séparer le traitement de la commande du routage, sans changer le comportement existant : code 1 si l'argument manque, sinon appel à `ret` et code 0, y compris pour les erreurs métier déjà gérées par `ret`.
- Résultats transmis : **37 tests réussis en 4,47 s** ; Ruff avec la sélection du TP3 : **4 signalements C901**. La priorité 1 se poursuit avant les mesures finales.
- État : extraction vérifiée ; commit à effectuer après relecture du diff.

##### Cinquième extraction : traitement de la commande export

- Le traitement de `return` a été extrait dans le commit `1f77715`.
- Problème : `process` vérifiait l'argument du fichier d'export et choisissait directement le séparateur.
- Modification : extraction de `handle_export(library, args)` ; la commande `export` retourne désormais le résultat de cette fonction.
- Justification : isoler la commande du routage et conserver son contrat : message d'usage et code 1 si le fichier manque, séparateur `;` et code 0 après export.
- Résultats transmis : **37 tests réussis en 4,38 s** ; Ruff avec la sélection du TP3 : **4 signalements C901**. L'extraction des traitements prépare la simplification du routage restant de `process`.
- État : extraction vérifiée ; commit à effectuer après relecture du diff.

##### Routage par dictionnaire et fin de la priorité 1

- Le traitement de `export` a été extrait dans le commit `ffbb3a5`.
- Problème : la suite de `if`/`elif` de `process` conservait un branchement pour chaque commande, même après extraction des traitements.
- Modification : dictionnaire `commands` associant les noms aux traitements, recherche avec `get` et clause de garde pour une commande inconnue. Le résultat `None` des commandes d'affichage est traduit en code 0 ; les codes explicites des commandes d'emprunt, de retour et d'export sont conservés.
- Justification : séparer le routage des détails de chaque commande et réduire le nombre de décisions dans la fonction principale, sans changer les sorties ni les codes de retour des scénarios vérifiés.
- Tests transmis : **37 réussis en 5,00 s**.
- Ruff avec la sélection TP3 : **3 C901**, contre 4 au départ ; `process` n'est plus signalée.
- Mesure intermédiaire Radon : **`process` A (4)**, contre **C (16)** au départ. Les fonctions extraites sont en A : `display_catalog` (2), `display_members` (3), `handle_borrow` (3), `handle_return` (2) et `handle_export` (2).
- État : priorité 1 vérifiée ; commit du routage à effectuer. Les mesures « après » globales restent réservées à l'étape finale. La prochaine priorité est `Library.report`, toujours C (14).

#### Suivi des améliorations — priorité 2 : restructurer report

##### Première extraction : comptage des emprunts par type

- Le routage simplifié de `process` a été enregistré dans le commit `0983b9b`.
- Problème : `report` calculait directement les compteurs par type de document avant de les afficher.
- Modification : extraction de `count_loans_by_kind()`, qui retourne un dictionnaire sans affichage ; utilisation de `counts.get(kind, 0) + 1` pour incrémenter chaque type. `report` conserve le tri des types et le texte de sortie.
- Justification : séparer ce calcul de sa présentation et réduire les décisions de la méthode de rapport.
- Résultat transmis après extraction : **37 tests réussis en 4,45 s**.
- Ruff a d'abord signalé une ligne vide contenant des espaces (W293), corrigée par `ruff check bibliotech.py --select W293 --fix`. Le contrôle final avec la sélection du TP3 donne **3 C901**, sans signalement de style supplémentaire.
- État : première extraction de la priorité 2 vérifiée ; commit à effectuer après relecture du diff. La restructuration de `report` se poursuit ensuite.

##### Deuxième extraction : classement des documents par emprunts

- Le comptage des emprunts par type a été extrait dans le commit `0749bfd`.
- Problème : `report` construisait et triait directement la liste du classement, en plus de l'afficher.
- Modification : extraction de `rank_books_by_loans(loan_counts)` ; le rapport appelle `self.rank_books_by_loans(data2)` avant son affichage existant.
- Justification : séparer le calcul du classement de sa présentation. Le tri conserve les couples `(-nombre_emprunts, titre)` : nombre décroissant, puis titre alphabétique en cas d'égalité.
- Résultat transmis après extraction : **37 tests réussis en 4,75 s**.
- Une ligne vide contenant des espaces (W293) a été corrigée avec la commande ciblée. Le dernier relevé Ruff transmis ne signale plus que **3 C901**.
- État : deuxième extraction de la priorité 2 vérifiée ; commit à effectuer après relecture du diff. La restructuration de `report` reste en cours.

##### Troisième extraction : statistiques d'emprunts et fin de la priorité 2

- Le classement des documents a été extrait dans le commit `08d7887`.
- Problème : `report` mêlait encore les calculs des emprunts en cours, des retards, des pénalités encaissées et en attente, et des compteurs par document à leur affichage.
- Modification : extraction de `loan_statistics()`, sans affichage, puis récupération des cinq résultats dans `report`. Suppression de l'initialisation `data2 = {}` devenue inutile. Les montants en attente utilisent toujours `late_fee`.
- Justification : séparer le calcul des statistiques de la présentation, en conservant les compteurs, les montants et les sorties des scénarios existants.
- Vérification transmise après suppression de la ligne inutile : **37 tests réussis en 4,50 s**.
- Une ligne vide contenant des espaces (W293) a ensuite été corrigée avec la commande ciblée. Dernier contrôle Ruff transmis : **2 C901**, contre 3 avant cette extraction et 4 au départ du TP3 ; seules `find` et `load` dépassent encore le seuil.
- Radon intermédiaire transmis : **`report` B (7)**, contre **C (14)** au départ. Les calculs extraits sont en A : `count_loans_by_kind` (2), `rank_books_by_loans` (2) et `loan_statistics` (4). `process` reste A (4).
- État : priorité 2 vérifiée ; commit à effectuer après relecture du diff. Les mesures « après » globales seront faites à l'étape finale ; la prochaine priorité est la recherche par identifiant dans `find`.

#### Suivi des améliorations — priorité 3 : mutualiser find

- La séparation des statistiques de `report` a été enregistrée dans le commit `085df42`.
- Problème : `find` répétait trois fois la même boucle de recherche par identifiant, selon le type de collection.
- Tests ajoutés avant refactoring dans `tests/test_find.py` : trois cas vérifient l'objet retrouvé dans les livres, membres et emprunts ; quatre vérifient les identifiants absents et un type inconnu. Première exécution : **44 tests réussis en 6,54 s**, avant changement de `find`.
- Modification : dictionnaire des collections et boucle unique ; un type inconnu sélectionne une liste vide et retourne `None`.
- Justification : supprimer la duplication tout en conservant la recherche du premier objet correspondant et les résultats des cas inconnus testés.
- Vérification après refactoring : **44 tests réussis en 5,34 s**, dont les 37 tests précédents et les 7 nouveaux cas de recherche. Aucun test de caractérisation ni fichier golden modifié.
- Ruff avec la sélection TP3 : **1 C901** restant dans `load`, contre 2 avant cette correction. Radon : **`find` A (3)**, contre **B (10)** au départ. `process` reste A (4) et `report` B (7).
- État : priorité 3 vérifiée ; commit à effectuer après relecture du diff. Prochaine priorité : séparer les chargements de `load`. Le tableau final indiquera l'augmentation des tests de 37 à 44 à ce stade.

#### Suivi des améliorations — priorité 4 : séparer les chargements

- La mutualisation de `find` et ses sept tests ont été enregistrés dans le commit `234030e`.
- Première extraction : `load_books` prend en charge la lecture et la conversion des livres ; `load` appelle cette méthode avant de charger les membres et les emprunts.
- Justification : isoler la responsabilité du chargement des livres sans changer les conversions, l'ordre de lecture ni l'ajout des données aux listes existantes.
- Vérification après extraction : **44 tests réussis en 4,53 s**. Ruff avec la sélection TP3 ne signale plus aucune erreur.
- Radon : **`load` B (7)**, contre **B (9)** avant extraction ; **`load_books` A (3)**. `report` reste B (7) et `process` A (4).
- État : première extraction vérifiée ; les chargements des membres et des emprunts restent à séparer. Le bilan global sera établi après les autres améliorations prévues.

- Première extraction enregistrée dans le commit `95ba931`.
- Deuxième extraction : `load_members` prend en charge la lecture des membres et la conversion du statut actif ; `load` l'appelle après `load_books`. Le traitement des lignes et les valeurs chargées sont conservés.
- Vérification après cette extraction : **44 tests réussis en 5,75 s** ; aucune erreur Ruff avec la sélection TP3.
- Radon : **`load` A (5)**, contre B (7) après la première extraction ; **`load_members` A (3)**. Il reste à extraire le chargement des emprunts.

- Deuxième extraction enregistrée dans le commit `2e1c026`.
- Troisième extraction : `load_loans` prend en charge la lecture des emprunts et la conversion des pénalités. La valeur de repli `0` en cas de pénalité absente ou non numérique est conservée.
- `load` orchestre désormais les trois chargements dans leur ordre initial et conserve l'affichage de débogage après leur exécution.
- Vérification : **44 tests réussis en 4,75 s**. Un avertissement W293 a été corrigé par la suppression d'espaces sur une ligne vide ; le contrôle Ruff TP3 suivant ne signale aucune erreur.
- Radon : **`load` A (2)**, contre **B (9)** au début du TP3 ; `load_books` et `load_members` sont A (3), `load_loans` A (4).
- État : priorité 4 vérifiée. La priorité 5 reste à traiter : vérifier les références à `old_calc_fee` avant de supprimer cette fonction inutilisée.

#### Suivi des améliorations — priorité 5 : supprimer le calcul obsolète

- La dernière extraction du chargement a été enregistrée dans le commit `70c3ab0`.
- Recherche des références à `old_calc_fee` dans le dépôt, hors `.git` et `.venv` : seuls sa définition et les mentions du README étaient présents ; aucun appel trouvé.
- Suppression de cette fonction et de son commentaire « ne plus utiliser ». Ses anciens tarifs pouvaient prêter à confusion avec le calcul métier utilisé, `late_fee`.
- Vérification après suppression : **44 tests réussis en 5,12 s** ; aucune erreur Ruff avec la sélection TP3. Les tests de caractérisation et les fichiers golden n'ont pas été modifiés par cette correction.
- État : les cinq priorités ont été traitées. Il reste à relever les mesures finales avec les commandes initiales, commenter la comparaison avant/après et finaliser le README et la pull request.

</details>

## 5. Bilan des trois jours

### Tableau global des résultats des trois TP

Les colonnes présentent l'état atteint à la fin de chaque TP. Les mesures absentes du relevé historique ne sont pas reconstituées comme si elles avaient été exécutées à l'époque.

| Indicateur | Fin du TP1 — Clean Code | Fin du TP2 — Refactoring | Fin du TP3 — Qualité |
| --- | --- | --- | --- |
| Tests réussis | 21 | 37 | 44 |
| Répartition des tests | 21 de caractérisation | 21 de caractérisation + 10 pénalités + 6 emprunts | Les 37 précédents + 7 cas de recherche |
| Signalements Ruff relevés | 5 C901 | 4 C901, relevés au début du TP3 sur `v2-fin-j2` | 0 avec la sélection TP3 |
| Complexité Radon de l'emprunt | C (18), relevée au départ du TP2 | A (4) | A (4) |
| Complexité Radon de `process` | C (16), relevée au départ du TP2 | C (16) | A (4) |
| Complexité Radon de `report` | C (14), relevée au départ du TP2 | C (14) | B (7) |
| Complexité moyenne Radon | Non relevée à cette étape | B (5,18), 22 blocs, relevée sur `v2-fin-j2` | A (3,34), 32 blocs |
| Blocs Radon classés C ou plus | 3, relevés au départ du TP2 | 2 | 0 |
| Résultat principal | Imports, conditions, noms, fichiers, sécurité et calcul commun nettoyés | Règles testées, `late_fee` unique et emprunt décomposé avec clauses de garde | Routage, rapport, recherche et chargements simplifiés ; calcul obsolète supprimé |
| Préservation des références fournies | Tests de caractérisation et fichiers golden conservés | Références conservées ; tests unitaires ajoutés | Références conservées ; sept cas supplémentaires |

**Lecture des chiffres :** le relevé Ruff du TP1 utilise la sélection configurée à cette étape ; les deux dernières colonnes utilisent la sélection imposée au TP3. La baisse 4 → 0 est donc la comparaison Ruff directement comparable. Les chiffres Radon du départ du TP2 décrivent le code issu du TP1 fusionné ; ils sont distincts des valeurs calculées par Ruff. La moyenne Radon baisse en partie grâce aux extractions, mais les scores individuels de `process`, `report` et de l'emprunt confirment aussi la simplification. Le nombre de tests augmente sans modifier les sorties de référence pour faire passer les corrections.

Le TP1 a amélioré la lisibilité et corrigé les points dangereux. Le TP2 a permis de tester les règles et de séparer les décisions des actions. Le TP3 a utilisé les mesures pour choisir les priorités et comparer les résultats.

Acquis : extraction de fonctions, clauses de garde, tests paramétrés, lecture des métriques et petits commits vérifiés. Les difficultés ont concerné l'indentation, les renommages incomplets, les commandes collées avec le préfixe PowerShell et les fichiers non enregistrés dans VS Code. La solution a été de vérifier le fichier sur disque, lire le diff et relancer les tests avant de poursuivre.

Pour `old_calc_fee`, le premier commit ne contenait que la documentation ; la suppression effective a ensuite été vérifiée et enregistrée séparément. L'historique publié n'a pas été réécrit.

Pistes futures : mieux séparer les responsabilités de `Library`, renommer ses collections et tester davantage les CSV invalides. Ces pistes ne sont pas présentées comme réalisées.

## 6. Exécution du projet

### Installation


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

### Utilisation


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

### Règles métier


| Règle | Valeur |
| --- | --- |
| Durée d'emprunt | livre 21 jours, DVD 7 jours, magazine 3 jours |
| Emprunts simultanés maximum | standard 3, étudiant 5, premium 8 |
| Pénalité par jour de retard | livre 0,50 €, DVD 1,00 €, magazine 0,20 € |
| Réduction sur les pénalités | étudiant 50 %, premium 100 % |
| Plafond de la pénalité | prix du document |

Un emprunt est refusé si le membre est inactif, s'il a un emprunt en retard, s'il a atteint sa limite, s'il a déjà ce document, ou s'il ne reste aucun exemplaire.

### Tests


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

### Mesures et vérification de l'évolution

```powershell
ruff check . --select E,W,F,B,S,C90,SIM --extend-exclude tests --statistics
radon cc -s -a --exclude "tests/*" .
radon cc -s -n C --exclude "tests/*" .
git log --oneline v2-fin-j2..qualite
git diff --stat v2-fin-j2
git diff v2-fin-j2 -- tests/test_caracterisation.py tests/golden/
```

La dernière commande ne produit aucune différence. Ruff et Radon filtrée ne produisent aucun signalement. La sélection Ruff TP3 est explicite : `ruff check .` seul utilise la configuration héritée, qui est différente.

La remise est une pull request de `qualite` vers `main`, avec les cinq améliorations et le tableau avant/après dans la description. La fusion est laissée à l'enseignant.
