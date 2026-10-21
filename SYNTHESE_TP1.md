# Synthèse TP1 — BiblioTech

## Objectif

Améliorer la lisibilité et la qualité du code sans changer le comportement de l'application. Conserver les tests fournis et vérifier chaque correction par petits pas.

## Préparation — 21 octobre 2026

- Dépôt : https://github.com/awa78/bibliotech-BOUARE
- Projet récupéré dans `Documents\bibliotech-BOUARE`.
- Environnement Python `.venv` créé et dépendances de `requirements.txt` installées.
- Vérification initiale : **21 tests réussis**.
- Analyse initiale Ruff : **55 problèmes signalés**.
- Commande `python bibliotech.py list` : le catalogue s'affiche correctement.
- Étiquette locale `v0-initial` et branche `tp1/nettoyage` créées.
- Projet ouvert dans VS Code.

## Corrections et essais vérifiés

| Défaut | Emplacement | Correction | Principe | Vérification |
| --- | --- | --- | --- | --- |
| Deux modules importés sur une même ligne (E401) | `bibliotech.py`, imports au début du fichier | Remplacement de `import os, sys` par deux lignes : `import os` et `import sys` | Conventions Python et lisibilité | 21 tests réussis ; Ruff : 54 problèmes au lieu de 55 |
| Comparaison explicite d'un booléen à True (E712) | `bibliotech.py`, ligne 60, méthode `load()` | Utilisation directe de `debug` dans la condition | Simplicité et lisibilité | Résultat transmis par l'utilisatrice : 21 tests réussis ; Ruff : 53 problèmes au lieu de 54 |

### Essai 1 — Séparer les imports

La séparation des imports facilite la lecture des dépendances. La correction a été constatée dans le fichier puis vérifiée automatiquement.

Commandes exécutées après la correction :

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check . --statistics
```

Résultats : `21 passed` et `Found 54 errors.`. Le code de sortie 1 de Ruff indique que des problèmes de qualité restent à corriger ; les tests ont réussi.

## Suivi

### Essai 21 — Réunir les critères de retard d'un membre

- Défaut : conditions imbriquées dans la vérification des retards avant un emprunt (SIM102).
- Emplacement : `bibliotech.py`, méthode `do_stuff()`, anciennes lignes 136 à 141.
- Correction : réunir avec `and` les trois critères (identifiant du membre, emprunt non rendu, date d'échéance dépassée), puis conserver `late = True` dans le bloc.
- Principe : réduire l'imbrication en préservant l'ordre de vérification des conditions.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,28 s** ; **11 problèmes Ruff**, contre 12 avant cet essai. Aucun signalement SIM102 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la sélection des emprunts en retard a été enregistrée dans le commit `f8ae461`, confirmé par le terminal de l'utilisatrice.

### Essai 20 — Réunir les conditions de sélection des emprunts en retard

- Défaut : deux conditions `if` imbriquées pouvant être réunies (SIM102).
- Emplacement : `bibliotech.py`, méthode `overdue()`, anciennes lignes 273 à 275.
- Correction : réunir avec `and` la vérification de l'absence de retour et celle du dépassement de la date d'échéance, puis conserver `tmp.append(x)` dans le bloc.
- Principe : réduire l'imbrication et rendre les critères de sélection lisibles ; `and` conserve l'évaluation conditionnelle de la date après le contrôle du retour.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,30 s** ; **12 problèmes Ruff**, contre 13 avant cet essai. Les signalements SIM102 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la simplification du texte du statut a été enregistrée dans le commit `5c6e504`, confirmé par le terminal de l'utilisatrice.

### Essai 19 — Simplifier le choix du texte du statut

- Défaut : bloc `if`/`else` affectant une chaîne à `s` (SIM108).
- Emplacement : `bibliotech.py`, commande `members`, anciennes lignes 544 à 547.
- Correction : remplacer le bloc par `s = "actif" if x["active"] else "inactif"`.
- Principe : expression conditionnelle courte pour une affectation simple et lisible.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,24 s** (sortie complète du message précédent) ; **13 problèmes Ruff**, contre 14 avant cet essai. Aucun signalement SIM108 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le calcul direct du booléen actif a été enregistré dans le commit `d4aa603`, confirmé par le terminal de l'utilisatrice. Les interruptions Ctrl+C ultérieures n'ont pas annulé ce commit terminé.

### Essai 18 — Affecter directement le résultat d'une comparaison

- Défaut : bloc `if`/`else` affectant `True` ou `False` à `a` (SIM108).
- Emplacement : `bibliotech.py`, lecture des membres dans `load()`, anciennes lignes 46 à 49 de la version enregistrée après formatage.
- Correction : remplacer le bloc par `a = x[4] == "1"`.
- Principe : simplicité ; une comparaison produit déjà un booléen.
- Incident : les numéros affichés dans VS Code différaient de ceux du fichier enregistré. Une capture montrait le message `Failed to save 'bibliotech.py': The content of the file is newer.` Solution conseillée : fermer la version ancienne sans l'enregistrer, puis rouvrir le fichier depuis le disque avant de reprendre la correction.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,74 s** ; **14 problèmes Ruff**, contre 15 avant cet essai. Les signalements SIM108 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : le formatage a été enregistré dans le commit `6d8b3d8`, confirmé par le terminal de l'utilisatrice.
- Les numéros de ligne suivants seront vérifiés avant chaque nouvelle modification.

### Essai 17 — Formater le fichier Python

- Défaut : 19 lignes dépassant la longueur configurée (E501) et présentation du code à harmoniser.
- Emplacement : ensemble du fichier `bibliotech.py`.
- Correction : exécution de `python -m ruff format bibliotech.py` ; résultat transmis : `1 file reformatted`.
- Principe : conventions Python et présentation cohérente facilitant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,69 s** ; **15 problèmes Ruff**, contre 34 avant cet essai et 55 initialement. Les 19 signalements E501 ont disparu.
- Problèmes restants à ce stade : 8 C901, 2 E722, 2 SIM102, 2 SIM108 et 1 SIM105.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la fermeture automatique du fichier exporté a été enregistrée dans le commit `71fa056`, confirmé par le terminal de l'utilisatrice.
- Le formatage modifie de nombreux numéros de ligne ; les prochains emplacements devront être relevés dans le fichier actuel.

### Essai 16 — Fermer automatiquement le fichier exporté : diagnostic en cours

- Objectif : remplacer l'ouverture et la fermeture manuelles dans `export()` par un bloc `with`, sans modifier le calcul ni le contenu exporté.
- Premier résultat transmis : **20 tests réussis et 1 échoué en 3,34 s**, scénario `export`. Le message annonce 1 ligne exportée au lieu de 12.
- Diagnostic par comparaison au commit précédent : `n = n + 1` à la ligne 349 est resté hors de la boucle `for x in self.l:`. Il s'exécute une seule fois après la boucle au lieu d'une fois par emprunt.
- Correction proposée : ajouter un niveau d'indentation (4 espaces) à cette ligne pour l'aligner avec `fee = round(fee, 2)` et l'écriture de chaque emprunt.
- Deuxième essai transmis : même échec, **20 tests réussis et 1 échoué en 3,01 s**. La relecture du fichier enregistré confirme que le compteur avait toujours 12 espaces au lieu de 16.
- Correction appliquée par l'assistant : indentation du compteur à 16 espaces, dans la boucle, et suppression des espaces sur la ligne vide suivante.
- Vérification exécutée par l'assistant après correction : **21 tests réussis en 3,07 s** avec le cache désactivé ; **34 problèmes Ruff**, contre 35 avant cet essai. Aucun signalement SIM115 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la sauvegarde avec `with` a été enregistrée dans le commit `b6e37f9`, confirmé par le terminal de l'utilisatrice.

### Essai 15 — Fermer automatiquement le fichier des emprunts à la sauvegarde

- Défaut : ouverture de `loans.csv` en écriture et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `save()`, anciennes lignes 57 à 62.
- Correction : utiliser `with open(DATA + "/loans.csv", "w") as f:`, placer l'écriture de l'en-tête et la boucle d'écriture dans ce bloc et supprimer `f.close()`.
- Principe : gestion fiable des ressources ; fermeture automatique du fichier, y compris si une écriture lève une exception.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,29 s** ; **35 problèmes Ruff**, contre 36 avant cet essai et 55 initialement. Les signalements SIM115 passent de 2 à 1.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture des emprunts avec `with` a été enregistrée dans le commit `85fdd8b`, confirmé par le terminal de l'utilisatrice.
- Les prochains numéros de ligne seront vérifiés avant modification.

### Essai 14 — Fermer automatiquement le fichier des emprunts à la lecture

- Défaut : ouverture de `loans.csv` en lecture et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 43 à 45.
- Correction : utiliser `with open(DATA + "/loans.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; fermeture du fichier même en cas d'exception pendant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,77 s** ; **36 problèmes Ruff**, contre 37 avant cet essai. Les signalements SIM115 passent de 3 à 2.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture du fichier des membres avec `with` a été enregistrée dans le commit `90132ab`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

### Essai 13 — Fermer automatiquement le fichier des membres

- Défaut : ouverture de `members.csv` et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 32 à 34.
- Correction : utiliser `with open(DATA + "/members.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; fermeture du fichier même en cas d'exception pendant la lecture.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,56 s** ; **37 problèmes Ruff**, contre 38 avant cet essai. Les signalements SIM115 passent de 4 à 3.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la lecture du catalogue avec `with` a été enregistrée dans le commit `4f87db5`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

### Essai 12 — Fermer automatiquement le fichier du catalogue

- Défaut : ouverture de `books.csv` et fermeture manuelle avec `f.close()` (SIM115).
- Emplacement : `bibliotech.py`, méthode `load()`, anciennes lignes 25 à 27.
- Correction : utiliser `with open(DATA + "/books.csv") as f:`, avec `lines = f.readlines()` dans le bloc ; conserver la boucle de traitement après le bloc.
- Principe : gestion fiable des ressources ; le fichier est fermé même si la lecture lève une exception.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,74 s** ; **38 problèmes Ruff**, contre 39 avant cet essai. Les signalements SIM115 passent de 5 à 4.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la suppression du dictionnaire mutable par défaut a été enregistrée dans le commit `f0178fe`, confirmé par le terminal de l'utilisatrice.
- La suppression d'une ligne décale les emplacements suivants ; ils seront vérifiés avant la prochaine correction.

### Essai 11 — Éviter un dictionnaire mutable comme argument par défaut

- Défaut : `options={}` dans la signature de `register_plugin()` (B006) ; le dictionnaire par défaut est partagé entre les appels.
- Emplacement : `bibliotech.py`, méthode `register_plugin()`, ancienne ligne 358.
- Correction : utiliser `options=None`, puis initialiser `options = {}` dans un bloc `if options is None:` avant l'enregistrement du plugin.
- Principe : éviter un état mutable partagé implicitement entre les appels.
- Incident de saisie : une nouvelle `ParserError` sur `PS` provenait du collage du préfixe du terminal ; les tests n'avaient pas démarré. La commande seule a ensuite été exécutée correctement.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,88 s** ; **39 problèmes Ruff**, contre 40 avant cet essai. Le signalement B006 a disparu. Ces résultats valident les scénarios fournis ; ils ne constituent pas un test spécifique de l'indépendance des dictionnaires entre plugins.
- État : correction vérifiée avec la suite fournie ; commit en attente.
- Suivi de l'essai précédent : le tri des imports a été enregistré dans le commit `8394c2a`, confirmé par le terminal de l'utilisatrice.
- Les deux lignes ajoutées décalent les emplacements suivants ; les prochaines lignes seront vérifiées avant modification.

### Essai 10 — Trier automatiquement les imports

- Défaut : ordre des imports non conforme (I001), au début de `bibliotech.py`.
- Correction : exécution ciblée de `python -m ruff check bibliotech.py --select I --fix`.
- Résultat de la correction transmis par l'utilisatrice : `Found 1 error (1 fixed, 0 remaining).` Ce résultat concerne uniquement les règles de tri des imports sélectionnées.
- Principe : conventions Python et organisation lisible des dépendances.
- Incident de saisie : du texte de l'historique et le préfixe `(.venv) PS ...>` ont été recollés dans PowerShell, provoquant une saisie multiligne puis une `ParserError` sur `PS`. Solution : revenir à l'invite normale et exécuter uniquement la commande, sans préfixe ni sortie précédente. Aucune modification du programme n'était nécessaire pour cet incident.
- Vérifications finales transmises par l'utilisatrice : **21 tests réussis en 2,95 s** ; **40 problèmes Ruff**, contre 41 avant cet essai et 55 initialement. Le signalement I001 a disparu.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : les imports datetime explicites ont été enregistrés dans le commit `bbba5a2`, confirmé par le terminal de l'utilisatrice.

### Essai 9 — Rendre les imports datetime explicites

- Défaut : import global `from datetime import *` et import redondant `import datetime`, rendant l'origine des noms moins claire (F403 et F405).
- Emplacement : `bibliotech.py`, bloc des imports, anciennes lignes 5 à 8.
- Correction : conserver `import os` et `import sys`, puis importer explicitement `date`, `datetime` et `timedelta` avec `from datetime import date, datetime, timedelta`.
- Principe : dépendances explicites et lisibilité ; suppression d'un import redondant.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,02 s** ; **41 problèmes Ruff**, contre 44 avant cette correction. Le signalement F403 et les deux signalements F405 ont disparu.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la dernière simplification booléenne a été enregistrée dans le commit `9a5b8c5`, confirmé par le terminal de l'utilisatrice.
- Attention pour la suite : la suppression d'une ligne dans les imports décale les numéros des lignes suivantes ; les prochains emplacements devront être vérifiés.

### Essai 8 — Simplifier la dernière comparaison booléenne

- Défaut : comparaison explicite d'un résultat avec `False` (E712).
- Emplacement : `bibliotech.py`, ligne 412.
- Correction : remplacement de `if r == False:` par `if not r:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,37 s** ; **44 problèmes Ruff**, contre 45 avant cette correction et 55 initialement. Aucun signalement E712 ne reste.
- État : correction validée par les tests fournis ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition du membre actif dans l'affichage a été enregistrée dans le commit `848da21`, confirmé par le terminal de l'utilisatrice.

### Essai 7 — Simplifier la condition du membre actif dans l'affichage

- Défaut : comparaison explicite d'un booléen avec `True` (E712).
- Emplacement : `bibliotech.py`, ligne 259.
- Correction : remplacement de `if x["active"] == True:` par `if x["active"]:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 2,95 s** ; **45 problèmes Ruff**, contre 46 avant cette correction. Il reste un signalement E712.
- État : correction validée ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition d'absence de retard a été enregistrée dans le commit `f70af4b`, confirmé par le terminal de l'utilisatrice.

### Essai 6 — Simplifier la condition d'absence de retard

- Défaut : comparaison explicite d'un booléen avec `False` (E712).
- Emplacement : `bibliotech.py`, ligne 114, méthode `do_stuff()`.
- Correction : remplacement de `if late == False:` par `if not late:` sans modifier l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 3,19 s** ; **46 problèmes Ruff**, contre 47 avant cette correction. Les signalements E712 passent de 3 à 2.
- État : correction validée ; commit en attente.
- Suivi de l'essai précédent : la simplification de la condition du membre actif a été enregistrée dans le commit `84e96c9`, confirmé par le terminal de l'utilisatrice.

### Essai 5 — Simplifier la condition du membre actif

- Défaut : comparaison explicite d'un booléen avec `True` (E712).
- Emplacement : `bibliotech.py`, ligne 107, méthode `do_stuff()`.
- Correction : remplacement de `if mb["active"] == True:` par `if mb["active"]:` en conservant l'indentation.
- Principe : simplicité et lisibilité des conditions booléennes.
- Vérifications transmises par l'utilisatrice : **21 tests réussis en 2,93 s** avec la commande pytest utilisant le dossier temporaire distinct ; **47 problèmes Ruff**, contre 48 avant cette correction. Les signalements E712 passent de 4 à 3.
- Étape 6 du guide confirmée par `git branch --show-current` : branche active `tp1/nettoyage`.
- État : correction validée ; commit en attente. Les trois autres comparaisons booléennes proposées restent à traiter séparément.

### Suivi du guide — accès et publication du point de départ

- L'utilisatrice confirme travailler seule : aucun binôme à ajouter.
- Elle confirme que `Massamba07` apparaît dans la liste des collaborateurs ; l'acceptation de l'invitation n'a pas été précisée.
- Partage du lien du dépôt dans le document de promotion : en attente. L'utilisatrice doit demander à l'enseignant où trouver ce document.
- Étape 5 : `git push origin v0-initial` exécuté par l'utilisatrice avec succès ; le terminal confirme `[new tag] v0-initial -> v0-initial`. Le point de départ est désormais publié sur GitHub.
- Étape 6 : branche locale `tp1/nettoyage` déjà créée ; prochaine vérification avant de reprendre le nettoyage.

### Vérification globale de reprise — 21 octobre 2026

- Branche active : `tp1/nettoyage` ; dernier commit : `cec41ec`.
- Tests relancés : **21 réussis en 3,29 s** (`.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider`).
- Analyse Ruff relancée : **48 problèmes**, contre 55 initialement.
- Les dossiers `tests/` et `data/` sont identiques à la version `v0-initial`.
- Aucune modification du code en attente ; seul ce rapport a des modifications non commitées.
- Vérification distante avec `git ls-remote` : seule la branche `main`, au commit initial, est présente parmi les références recherchées. La branche `tp1/nettoyage` et l'étiquette `v0-initial` ne sont pas encore publiées sur GitHub.
- Prochaine correction proposée, non appliquée : simplifier les quatre comparaisons booléennes aux lignes 107, 114, 259 et 412.
- Invitations des collaborateurs et dépôt du lien dans le document de promotion : non vérifiés, aucun accès à ces informations dans cet audit.

### Essai 4 — Comparaisons avec None : échec détecté et diagnostic

- Objectif : remplacer les comparaisons `== None` et `!= None` par `is None` et `is not None` aux lignes 104, 106, 174 et 376.
- Premier résultat transmis : **19 tests réussis et 2 échoués** (`report`, `report_after_returns`) ; Ruff signale **49 problèmes**, dont un E711 restant.
- Diagnostic par comparaison au dernier commit : les lignes 104, 106 et 174 sont correctement modifiées, mais la condition `if bk["kind"] in k:` à la ligne 306 a été remplacée par erreur par `if TODAY is None:`. Cela réinitialise les compteurs par type de document dans le rapport. La comparaison prévue à la ligne 376 n'a pas été modifiée.
- Correction proposée : rétablir `if bk["kind"] in k:` à la ligne 306, puis remplacer `if TODAY == None:` par `if TODAY is None:` à la ligne 376.
- Enseignement : les tests ont détecté une modification involontaire du comportement ; une baisse du nombre de problèmes Ruff ne suffit pas à valider une correction.
- Résultat après correction transmis par l'utilisatrice : **21 tests réussis en 4,44 s**, et **48 problèmes Ruff**, contre 52 avant cet essai. Les quatre signalements E711 ont disparu. Les tests du rapport réussissent à nouveau.
- État : correction validée par les tests fournis et enregistrée dans le commit local `cec41ec`, confirmé par le terminal de l'utilisatrice.

### Essai 3 — Supprimer un import inutilisé

- Défaut : import du module `json` sans utilisation dans le fichier (F401).
- Emplacement : `bibliotech.py`, ancienne ligne 9, bloc des imports.
- Correction : suppression de `import json`.
- Principe : supprimer le code inutile et rendre les dépendances plus lisibles.
- Vérifications transmises par l'utilisatrice : `python -m pytest -q -p no:cacheprovider --basetemp "$env:TEMP\bibliotech-tests-awa"` donne **21 tests réussis en 4,39 s** ; `python -m ruff check . --statistics` donne **52 problèmes**, contre 53 avant cette correction et 55 au départ. Le signalement F401 a disparu.
- État : correction validée par les tests fournis et enregistrée dans le commit local `8f011c9`, confirmé par le terminal de l'utilisatrice.

### Essai 2 — Vérification depuis le terminal de VS Code

Après la proposition de simplifier `if debug == True:` en `if debug:`, l'exécution de `python -m pytest -q` par l'utilisatrice a produit **21 erreurs de préparation** : `PermissionError: [WinError 5]` sur le dossier temporaire `AppData\Local\Temp\pytest-of-awabo`. Des avertissements d'accès au cache `.pytest_cache` sont également présents. Ces erreurs empêchent l'exécution des tests et ne permettent pas de conclure sur le comportement de l'application.

Solution proposée : utiliser un dossier temporaire distinct et désactiver le cache pour cette exécution, sans modifier les tests ni les permissions Windows :

```powershell
python -m pytest -q -p no:cacheprovider --basetemp "$env:TEMP\bibliotech-tests-awa"
```

Résultat transmis par l'utilisatrice : **21 tests réussis en 3,23 s**. La commande `python -m ruff check . --statistics` signale **53 problèmes**, contre 54 après la première correction et 55 au départ. Le nombre de signalements E712 passe de 5 à 4. La deuxième correction est validée par les tests fournis.

Un essai intermédiaire avait collé deux commandes en une seule (`python -m pytest -qpython -m ruff check . --statistics`) : pytest avait alors refusé les arguments. La solution a été de lancer chaque commande séparément. Cette erreur de saisie ne nécessitait aucune modification du programme.

La forme conventionnelle attendue à la ligne 60 est `if debug:` (sans espace avant les deux-points).

Ce document sera complété à chaque nouvel essai, en distinguant les propositions des corrections appliquées et vérifiées. La première correction a été enregistrée dans le commit local `4d50be8`, et la deuxième dans `562b3f0`, confirmés par le terminal de l'utilisatrice. Aucun envoi sur GitHub n'a été confirmé. Le blocage de préparation des tests est résolu avec la commande ci-dessus.
