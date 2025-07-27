# Tests - EzQt_App

## 📋 Vue d'ensemble

Ce document décrit la stratégie de test complète pour le projet EzQt_App, incluant les tests unitaires, d'intégration et utilitaires.

## 🎯 Types de tests

### **Tests Unitaires** (`tests/unit/`)
- **Objectif** : Tester les composants individuels de manière isolée
- **Modules** : Kernel, Utilitaires, Widgets
- **Couverture** : > 95%

### **Tests d'Intégration** (`tests/integration/`)
- **Objectif** : Tester les interactions entre modules
- **Modules** : AppFlow, TranslationSystem
- **Couverture** : > 90%

### **Tests Utilitaires** (`tests/unit/test_utils/`)
- **Objectif** : Tester les outils et fonctions utilitaires
- **Modules** : CLI, Helpers
- **Couverture** : > 95%

## 📊 Répartition par module

### **Kernel** (15+ tests)
- `test_app_functions.py` - Fonctions d'application
- `test_app_settings.py` - Paramètres d'application
- `test_app_resources.py` - Gestion des ressources
- `test_translation_manager.py` - Gestionnaire de traduction

### **Widgets** (20+ tests)
- `test_core/` - Composants de base
- `test_extended/` - Composants étendus

### **Utilitaires** (6 tests)
- `test_cli.py` - Interface en ligne de commande

### **Intégration** (27 tests)
- `test_app_flow.py` - Flux d'application (12 tests)
- `test_translations.py` - Système de traduction (15 tests)

## 🎯 État actuel (Décembre 2024)

### **Tests Unitaires**
- **Kernel** : ✅ Tous passent (15+ tests)
- **Widgets** : ✅ Tous passent (20+ tests)
- **Utilitaires** : ✅ Tous passent (6 tests)

### **Tests d'Intégration**
- **AppFlow** : ✅ Tous passent (12 tests)
- **TranslationSystem** : ✅ Tous passent (15 tests)

### **Résultats des tests Utilitaires**
- **Tests CLI** : ✅ 6 tests passent
- **Couverture** : > 95%
- **Temps d'exécution** : < 1 seconde
- **Mocking** : Approche simplifiée avec `@patch` decorators

### **Résultats des tests d'Intégration**
- **Tests AppFlow** : ✅ 12 tests passent
- **Tests Translations** : ✅ 15 tests passent
- **Total** : 27 tests d'intégration
- **Gestion des fichiers temporaires** : Utilisation de `%TEMP%` avec nettoyage automatique
- **Mocking stratégique** : Classes mock complètes pour éviter les imports problématiques

## 🚀 Exécution des tests

### **Tous les tests**
```bash
python -m pytest tests/ -v
```

### **Tests unitaires uniquement**
```bash
python -m pytest tests/unit/ -v
```

### **Tests d'intégration uniquement**
```bash
python -m pytest tests/integration/ -v
```

### **Tests avec couverture**
```bash
python -m pytest tests/ --cov=ezqt_app --cov-report=html
```

### **Tests spécifiques**
```bash
# Tests CLI
python -m pytest tests/unit/test_utils/test_cli.py -v

# Tests d'intégration app_flow
python -m pytest tests/integration/test_app_flow.py -v

# Tests de traduction
python -m pytest tests/integration/test_translations.py -v
```

## 🔧 Stratégies de test

### **Tests Unitaires**
- **Isolation** : Chaque test est indépendant
- **Mocking** : Utilisation de `unittest.mock`
- **Fixtures** : Réutilisation des objets de test
- **Assertions** : Vérifications précises et spécifiques

### **Tests d'Intégration**
- **Fichiers temporaires** : Utilisation de `%TEMP%` avec nettoyage automatique
- **Mocking stratégique** : Classes mock complètes pour éviter les imports
- **Workflows** : Test des interactions entre modules
- **Gestion d'erreurs** : Scénarios d'erreur et récupération

### **Tests Utilitaires**
- **Mocking simplifié** : `@patch` decorators au lieu de mocks imbriqués
- **Side effects** : Ordre correct des `side_effect` arrays
- **Isolation** : Tests indépendants des dépendances externes

## 📈 Métriques de qualité

### **Couverture globale**
- **Tests unitaires** : > 95%
- **Tests d'intégration** : > 90%
- **Tests utilitaires** : > 95%

### **Performance**
- **Temps d'exécution unitaires** : < 2 secondes
- **Temps d'exécution intégration** : < 1 seconde
- **Temps d'exécution utilitaires** : < 1 seconde

### **Fiabilité**
- **Tests unitaires** : 100% de réussite
- **Tests d'intégration** : 100% de réussite
- **Tests utilitaires** : 100% de réussite

## 🔄 Corrections majeures effectuées

### **Tests CLI (Décembre 2024)**
- **Problème** : `test_main_without_main_py` échouait avec des mocks incorrects
- **Solution** : Correction de l'ordre des `side_effect` et simplification des mocks
- **Résultat** : 6 tests passent avec une couverture > 95%

### **Tests d'Intégration (Décembre 2024)**
- **Problème** : `FileNotFoundError` pour `app.yaml` et imports circulaires
- **Solution** : Fichiers temporaires dans `%TEMP%` et classes mock complètes
- **Résultat** : 27 tests passent avec une couverture > 90%

### **Tests de Traduction (Décembre 2024)**
- **Problème** : Tests de singleton et persistance incorrects
- **Solution** : Utilisation de `get_translation_manager()` et correction des assertions
- **Résultat** : 15 tests de traduction passent

## 🛠️ Bonnes pratiques

### **Gestion des fichiers temporaires**
1. **Utiliser %TEMP%** : `Path(os.environ.get('TEMP', tempfile.gettempdir()))`
2. **Noms uniques** : `f"app_{os.getpid()}.yaml"` pour éviter les conflits
3. **Nettoyage automatique** : Toujours utiliser `try/finally`
4. **Encodage UTF-8** : `write_text(..., encoding='utf-8')`

### **Mocking**
1. **Simplifier les mocks** : Utiliser `@patch` decorators
2. **Éviter les mocks imbriqués** : Préférer les mocks plats
3. **Ordre des side_effect** : Respecter l'ordre d'exécution du code
4. **Mocking stratégique** : Créer des classes mock complètes si nécessaire

### **Tests d'intégration**
1. **Isolation** : Chaque test doit être indépendant
2. **Nettoyage** : Garantir le nettoyage des ressources
3. **Workflows** : Tester les interactions complètes
4. **Erreurs** : Couvrir les scénarios d'erreur

## 📚 Documentation détaillée

- **[Tests Unitaires](unit_README.md)** - Détails sur les tests unitaires
- **[Tests d'Intégration](integration_README.md)** - Détails sur les tests d'intégration
- **[Tests Utilitaires](utils_README.md)** - Détails sur les tests utilitaires
- **[Tests Kernel](kernel_README.md)** - Détails sur les tests du kernel
- **[Tests Widgets](widgets_README.md)** - Détails sur les tests des widgets

## 🎯 Objectifs futurs

### **Court terme**
- Maintenir la couverture > 90%
- Optimiser les temps d'exécution
- Ajouter des tests pour les nouveaux modules

### **Moyen terme**
- Tests de performance
- Tests de stress
- Tests de sécurité

### **Long terme**
- Tests automatisés en CI/CD
- Tests de régression automatisés
- Tests de compatibilité multi-plateforme

---

**État global :** 🟢 **OPÉRATIONNEL** (68+ tests, couverture > 90%) 