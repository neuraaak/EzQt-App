# 📚 Documentation - EzQt_App

## 📋 **Vue d'ensemble**

Ce dossier contient toute la documentation du projet EzQt_App, organisée par catégorie pour faciliter la navigation et la compréhension du framework.

## 🎯 **À propos d'EzQt_App**

EzQt_App est un framework Python conçu pour faciliter la création d'applications Qt modernes, basé sur un template de Wanderson M. Pimenta. Il automatise la gestion des ressources, génère tous les fichiers requis et offre une expérience de bootstrap de projet rapide avec une commande CLI.

## 🚀 **Fonctionnalités principales**

### **Génération automatique**
- Dossiers et fichiers d'assets (icônes, images, thèmes, etc.)
- Structure de projet complète
- Fichiers de configuration YAML

### **Interface utilisateur**
- Thèmes dynamiques (clair/sombre) avec basculement intégré
- Système de traduction global avec support multi-langues
- Widgets personnalisés avec animations et thèmes
- Gestionnaire de ressources avancé avec détection automatique

### **Outils de développement**
- Commande CLI `ezqt_init` pour initialiser rapidement un nouveau projet
- Exemple `main.py` prêt à l'emploi généré automatiquement
- Structure modulaire et extensible

## 📖 **Documentation par catégorie**

### **📋 Documentation Générale**
- [**TRANSLATION_SYSTEM.md**](./TRANSLATION_SYSTEM.md) - Système de traduction complet
- [**CHANGELOG.md**](../CHANGELOG.md) - Historique des versions et changements

### **🧪 Documentation des Tests**
- [**tests/README.md**](./tests/README.md) - Vue d'ensemble des tests
- [**tests/unit_README.md**](./tests/unit_README.md) - Tests unitaires détaillés
- [**tests/kernel_README.md**](./tests/kernel_README.md) - Tests du kernel
- [**tests/widgets_README.md**](./tests/widgets_README.md) - Tests des widgets
- [**tests/utils_README.md**](./tests/utils_README.md) - Tests des utilitaires
- [**tests/integration_README.md**](./tests/integration_README.md) - Tests d'intégration
- [**tests/translation_manager.md**](./tests/translation_manager.md) - Tests du gestionnaire de traduction

## 🚀 **Installation et utilisation**

### **Installation**
```bash
# Via pip (recommandé)
pip install ezqt_app

# Ou localement
git clone https://github.com/neuraaak/ezqt_app.git
cd ezqt_app
pip install .
```

### **Initialisation d'un projet**
```bash
# Initialiser un nouveau projet dans un dossier vide
ezqt_init
```

### **Utilisation minimale**
```python
import ezqt_app.main as ezqt
from ezqt_app.app import EzQt_App, EzApplication
import sys

ezqt.init()
app = EzApplication(sys.argv)
window = EzQt_App(themeFileName="main_theme.qss")
window.show()
app.exec()
```

## 📦 **Dépendances**

- **PySide6==6.9.1** - Framework Qt moderne
- **PyYaml==6.0.2** - Gestion des fichiers YAML
- **colorama==0.4.6** - Couleurs de terminal
- **requests==2.32.3** - Requêtes HTTP
- **ezqt-widgets>=2.0.0** - Widgets personnalisés

## 🧪 **Tests et qualité**

### **Exécution des tests**
```bash
# Depuis la racine du projet
python tests/run_tests.py --type unit

# Ou directement
python -m pytest tests/unit/ -v

# Tests avec couverture
python tests/run_tests.py --type unit --coverage
```

### **Statistiques des tests**
- **Tests unitaires** : 225+ tests
- **Tests d'intégration** : 15+ tests
- **Total** : 240+ tests
- **Couverture de code** : > 90%

### **Répartition par module**
- **Kernel** : 80+ tests (TranslationManager, Settings, Helper.Maker, AppFunctions)
- **Widgets Core** : 100+ tests (EzApplication, Header, Menu, PageContainer, SettingsPanel)
- **Widgets Étendus** : 30+ tests (SettingWidgets)
- **Utilitaires** : 15+ tests (CLI)

## 🌍 **Système de traduction**

Le framework inclut un système de traduction complet :

```python
from ezqt_app.kernel.translation_manager import get_translation_manager

# Obtenir le gestionnaire de traduction
tm = get_translation_manager()

# Changer la langue
tm.load_language_by_code("fr")

# Traduire du texte
translated_text = tm.translate("Hello World")
```

## 🔧 **Structure du projet**

```
ezqt_app/
├── kernel/                    # Composants fondamentaux
│   ├── translation_manager.py # Gestionnaire de traduction
│   ├── app_settings.py        # Paramètres de l'application
│   ├── app_functions.py       # Fonctions utilitaires
│   └── helper.py              # Classes d'aide
├── widgets/                   # Composants d'interface
│   ├── core/                  # Widgets principaux
│   └── extended/              # Widgets étendus
├── utils/                     # Utilitaires
│   ├── cli.py                 # Interface en ligne de commande
│   └── qmessage_logger.py     # Logger Qt
└── resources/                 # Ressources (icônes, thèmes, etc.)
```

## 📊 **Métriques de qualité**

### **Couverture par module**
- **TranslationManager** : 95%
- **Settings** : 90%
- **Helper.Maker** : 85%
- **AppFunctions** : 90%
- **Widgets Core** : 95%
- **Widgets Étendus** : 90%
- **Utilitaires** : 85%
- **Intégration** : 80%

## 🎯 **Objectifs du framework**

### **Fonctionnels**
- Simplifier la création d'applications Qt
- Automatiser la gestion des ressources
- Fournir une base solide et extensible
- Supporter le développement multi-langues

### **Qualité**
- Maintenir une couverture de tests élevée
- Assurer la stabilité et la performance
- Faciliter la maintenance et l'évolution

## 📚 **Navigation**

- **README principal** : [../README.md](../README.md)
- **Code source** : [../ezqt_app/](../ezqt_app/)
- **Tests** : [../tests/](../tests/)
- **Changelog** : [../CHANGELOG.md](../CHANGELOG.md)

---

**État global :** 🟢 **OPÉRATIONNEL** (240+ tests, couverture > 90%) 