# Tests Unitaires - Documentation

## Vue d'ensemble

Les tests unitaires d'EzQt_App couvrent les composants individuels du framework avec une approche modulaire et isolée.

## Structure des Tests

```
tests/unit/
├── test_kernel/           # Tests du noyau de l'application
├── test_utils/           # Tests des utilitaires
└── test_widgets/         # Tests des widgets personnalisés
    ├── test_core/        # Tests des widgets de base
    └── test_extended/    # Tests des widgets étendus
```

## Tests par Module

### Kernel Tests (`test_kernel/`)

#### `test_app_functions.py`
- ✅ **Fonctionnalités de base** - Tests des fonctions principales
- ✅ **Gestion des ressources** - Tests de chargement des ressources
- ✅ **Configuration** - Tests de la configuration de l'application

#### `test_app_settings.py`
- ✅ **Paramètres d'application** - Tests de gestion des paramètres
- ✅ **Validation des données** - Tests de validation des configurations
- ✅ **Persistance** - Tests de sauvegarde/chargement des paramètres

#### `test_translation_manager.py`
- ✅ **Gestion des traductions** - Tests du système de traduction
- ✅ **Changement de langue** - Tests de changement de langue
- ✅ **Chargement des fichiers** - Tests de chargement des fichiers .ts/.qm

#### `test_ui_functions.py`
- ✅ **Fonctions UI** - Tests des fonctions d'interface utilisateur
- ✅ **Gestion des thèmes** - Tests de gestion des thèmes
- ✅ **Widgets dynamiques** - Tests des widgets dynamiques

### Utils Tests (`test_utils/`)

#### `test_cli.py`
- ✅ **Interface CLI** - Tests de l'interface en ligne de commande
- ✅ **Commandes** - Tests des commandes disponibles
- ✅ **Validation des arguments** - Tests de validation des paramètres

### Widgets Tests (`test_widgets/`)

#### Core Widgets (`test_core/`)

##### `test_ez_app.py`
- ✅ **Tests de base** - Héritage, définition de classe, méthodes
- ✅ **Tests de documentation** - Documentation des classes et méthodes
- ⏸️ **Tests d'instance** - Tests nécessitant des instances QApplication (SKIP)
  - `test_locale_configuration_success` - Configuration locale réussie
  - `test_locale_configuration_failure` - Configuration locale avec échec
  - `test_environment_variables_setup` - Configuration des variables d'environnement
  - `test_high_dpi_scaling_configuration` - Configuration haute résolution
  - `test_application_properties` - Propriétés de l'application
  - `test_environment_setup_mocked` - Configuration environnement avec mock
  - `test_theme_changed_signal_instance` - Signal themeChanged sur instance

**Problème identifié** : Les tests d'instance échouent avec `AttributeError: MockQApplication does not have the attribute 'instance'`

**Solution en cours** : Amélioration du mocking de QApplication pour les tests

##### `test_header.py`
- ✅ **Composants d'en-tête** - Tests des composants d'en-tête
- ✅ **Boutons d'action** - Tests des boutons d'action
- ✅ **Responsive design** - Tests de design responsive

##### `test_menu.py`
- ✅ **Navigation** - Tests de navigation dans les menus
- ✅ **États des menus** - Tests des états des menus
- ✅ **Interactions** - Tests des interactions utilisateur

##### `test_pages.py`
- ✅ **Gestion des pages** - Tests de gestion des pages
- ✅ **Navigation** - Tests de navigation entre pages
- ✅ **Contenu dynamique** - Tests de contenu dynamique

##### `test_settings.py`
- ✅ **Panneau de paramètres** - Tests du panneau de paramètres
- ✅ **Sauvegarde** - Tests de sauvegarde des paramètres
- ✅ **Validation** - Tests de validation des paramètres

#### Extended Widgets (`test_extended/`)

##### `test_setting_widgets.py`
- ✅ **Widgets de paramètres** - Tests des widgets de paramètres
- ✅ **Validation** - Tests de validation des widgets
- ✅ **Interactions** - Tests des interactions utilisateur

## Configuration des Tests

### Fixtures Globales (`conftest.py`)

- **`qt_application`** - Instance QApplication pour tous les tests
- **`qt_widget_cleanup`** - Nettoyage des widgets après chaque test
- **`ez_application_cleanup`** - Instance EzApplication pour les tests
- **`wait_for_signal`** - Attente de signaux Qt
- **`mock_icon_path`** - Chemin d'icône mocké
- **`mock_svg_path`** - Chemin SVG mocké
- **`mock_translation_files`** - Fichiers de traduction mockés
- **`mock_yaml_config`** - Configuration YAML mockée

### Configuration Pytest (`pytest.ini`)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    unit: Tests unitaires
    integration: Tests d'intégration
    qt: Tests nécessitant Qt
    slow: Tests lents
```

## Exécution des Tests

### Tests Unitaires Complets
```bash
python -m pytest tests/unit/ -v
```

### Tests par Module
```bash
# Tests du kernel
python -m pytest tests/unit/test_kernel/ -v

# Tests des widgets
python -m pytest tests/unit/test_widgets/ -v

# Tests des utilitaires
python -m pytest tests/unit/test_utils/ -v
```

### Tests Spécifiques
```bash
# Test spécifique
python -m pytest tests/unit/test_widgets/test_core/test_ez_app.py::TestEzApplication::test_inheritance -v

# Tests avec marqueurs
python -m pytest tests/unit/ -m "qt" -v
```

## Couverture de Code

### Génération du Rapport
```bash
python -m pytest tests/unit/ --cov=ezqt_app --cov-report=html
```

### Rapport HTML
Le rapport de couverture est généré dans `htmlcov/index.html`

## Problèmes Connus et TODO

### Tests EzApplication en Skip

**Problème** : Les tests d'instance EzApplication échouent avec `AttributeError: MockQApplication does not have the attribute 'instance'`

**Tests affectés** :
- `test_locale_configuration_success`
- `test_locale_configuration_failure`
- `test_environment_variables_setup`
- `test_high_dpi_scaling_configuration`
- `test_application_properties`
- `test_environment_setup_mocked`
- `test_theme_changed_signal_instance`

**Cause** : Le mocking de QApplication ne fonctionne pas correctement pour les méthodes de classe comme `instance()`

**Solution en cours** : Amélioration du système de mocking pour QApplication

### TODO

1. **Corriger les tests EzApplication**
   - Améliorer le mocking de QApplication.instance()
   - Implémenter une solution robuste pour les tests d'instance
   - Tester avec différentes versions de PySide6

2. **Améliorer la couverture**
   - Ajouter des tests pour les cas limites
   - Tester les erreurs et exceptions
   - Augmenter la couverture des widgets complexes

3. **Optimiser les performances**
   - Réduire le temps d'exécution des tests
   - Optimiser les fixtures
   - Paralléliser les tests quand possible

## Bonnes Pratiques

### Écriture de Tests

1. **Nommage clair** - Noms de tests descriptifs
2. **Tests isolés** - Chaque test doit être indépendant
3. **Assertions multiples** - Utiliser des assertions spécifiques
4. **Documentation** - Docstrings pour chaque test

### Gestion des Mocks

1. **Mocking ciblé** - Mocker seulement ce qui est nécessaire
2. **Fixtures** - Utiliser les fixtures pour la configuration
3. **Nettoyage** - Toujours nettoyer après les tests

### Tests Qt

1. **Instance QApplication** - Utiliser la fixture qt_application
2. **Signaux** - Utiliser wait_for_signal pour les signaux
3. **Widgets** - Nettoyer les widgets après utilisation

## Maintenance

### Ajout de Nouveaux Tests

1. Créer le fichier de test dans le bon répertoire
2. Suivre la convention de nommage
3. Ajouter les imports nécessaires
4. Utiliser les fixtures appropriées
5. Documenter le test

### Mise à Jour des Tests Existants

1. Vérifier la compatibilité avec les nouvelles versions
2. Mettre à jour les mocks si nécessaire
3. Ajouter des tests pour les nouvelles fonctionnalités
4. Maintenir la couverture de code

### Debugging

1. Utiliser `-v` pour plus de verbosité
2. Utiliser `--tb=long` pour les traces complètes
3. Utiliser `--pdb` pour le debugging interactif
4. Vérifier les logs de test 