# Mode Opératoire - Publication de CleanTiPy

Ce document est une compilation de lignes de commande pour créer et publier le package CleanTiPy

## Création du package

modifier le numéro de version dans pyproject.toml

puis

```bash
cd C:\Users\leiba\Documents\CleanTiPy
py -m build
```

## Installation à partir du package local

Dans l'environnement voulu (par défaut ou virtuel)

```bash
pip install .
```

## Création de la documentation

```bash
cd .\docs\
.\make html 
```

ou

```bash
sphinx-build -M html docs/source docs/build/html
```

## Upload sur Pypi



```bash
py -m twine upload -r pypitest dist/* --verbose
```


