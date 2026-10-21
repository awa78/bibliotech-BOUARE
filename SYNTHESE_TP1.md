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

### Essai 1 — Séparer les imports

La séparation des imports facilite la lecture des dépendances. La correction a été constatée dans le fichier puis vérifiée automatiquement.

Commandes exécutées après la correction :

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check . --statistics
```

Résultats : `21 passed` et `Found 54 errors.`. Le code de sortie 1 de Ruff indique que des problèmes de qualité restent à corriger ; les tests ont réussi.

## Suivi

Ce document sera complété à chaque nouvel essai, en distinguant les propositions des corrections appliquées et vérifiées. Aucun échec des tests n'a été observé à ce stade. Le rapport et la première correction ne sont pas encore commités ni envoyés sur GitHub.
