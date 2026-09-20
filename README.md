# Jeu de Nim

Jeu de Nim : 20 objets sur la table, on en prend 1 à 3 par tour, et celui qui prend
le dernier gagne. Trois niveaux d'adversaire.

En ligne : https://dunandchatellet.fr/Nim/nim.html

## Deux versions du même jeu

| Version | Fichiers |
| --- | --- |
| Originale, en Python (Tkinter) | `python-source/nim.py`, compilée en `Nim.exe` |
| Portage web, jouable sans rien installer | `nim.html`, `nim.css`, `nim.js` |

Le portage suit la version Python règle pour règle, y compris la stratégie de l'adversaire.

## Lancer la version Python

```bash
python python-source/nim.py
```

Tkinter est fourni avec Python. Le `.exe` livré n'est pas signé : Windows affiche
un avertissement SmartScreen au premier lancement.

---

Pierre Dunand-Chatellet — [tous mes projets](https://dunandchatellet.fr/projets.html)
