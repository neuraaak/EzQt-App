# Tests pour EzQt_App

Ce dossier contient les tests unitaires et d'intégration pour le projet EzQt_App.

## Structure prévue

```
tests/
├── __init__.py
├── README.md
├── unit/                    # Tests unitaires
│   ├── __init__.py
│   ├── test_kernel.py      # Tests du kernel
│   ├── test_app.py         # Tests de l'application principale
│   ├── test_widgets.py     # Tests des widgets
│   └── test_utils.py       # Tests des utilitaires
├── integration/            # Tests d'intégration
│   ├── __init__.py
│   ├── test_app_flow.py    # Tests du flux d'application
│   └── test_translations.py # Tests du système de traduction
└── fixtures/               # Données de test
    ├── __init__.py
    ├── test_config.yaml    # Configuration de test
    └── test_resources/     # Ressources de test
```

## Exécution des tests

```bash
# Tous les tests
python -m pytest tests/

# Tests unitaires uniquement
python -m pytest tests/unit/

# Tests d'intégration uniquement
python -m pytest tests/integration/

# Avec couverture
python -m pytest tests/ --cov=ezqt_app
```

## Configuration

Les tests utilisent pytest comme framework de test principal. 