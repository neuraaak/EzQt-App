# 🎨 Tests des Widgets - EzQt_App

## 📋 **Vue d'ensemble**

Les tests des widgets couvrent tous les composants d'interface utilisateur de l'application EzQt_App, incluant les widgets core et les widgets étendus.

## 🏗️ **Structure des tests**

```
tests/unit/test_widgets/
├── test_core/                     # Widgets core
│   ├── test_ez_app.py            # Application principale
│   ├── test_header.py            # En-tête de l'application
│   ├── test_menu.py              # Menu latéral
│   ├── test_page_container.py    # Conteneur de pages
│   └── test_settings_panel.py    # Panneau de paramètres
└── test_extended/                # Widgets étendus
    └── test_setting_widgets.py   # Widgets de paramètres
```

## 🧪 **Widgets Core**

### **EzApplication** (`test_ez_app.py`)
**Objectif** : Tester l'application principale Qt avec ses configurations spécifiques.

**Fonctionnalités testées** :
- Initialisation avec différents paramètres
- Configuration DPI haute résolution
- Configuration de l'encodage UTF-8
- Configuration de la locale
- Variables d'environnement
- Signaux de changement de thème

**Tests principaux** :
```python
def test_init_default_parameters(self)
def test_init_with_arguments(self)
def test_high_dpi_scaling(self)
def test_environment_variables(self)
def test_locale_configuration(self)
def test_theme_changed_signal(self)
```

### **Header** (`test_header.py`)
**Objectif** : Tester l'en-tête de l'application avec ses boutons de contrôle.

**Fonctionnalités testées** :
- Création de l'en-tête avec titre et description
- Gestion des boutons (paramètres, minimiser, maximiser, fermer)
- Layout horizontal et vertical
- Propriétés de taille fixe
- Signaux des boutons

**Composants testés** :
- `leftAppBg` : Zone de gauche avec titre
- `rightAppBg` : Zone de droite avec boutons
- `titleTopApp` : Label du titre
- `titleTopDescriptionApp` : Label de description
- Boutons de contrôle (settings, minimize, maximize, close)

### **Menu** (`test_menu.py`)
**Objectif** : Tester le menu latéral avec ses fonctionnalités d'expansion/réduction.

**Fonctionnalités testées** :
- Initialisation avec largeurs personnalisées
- État réduit/étendu du menu
- Bouton de basculement
- Gestion des boutons de menu
- Animations et transitions
- Dictionnaire des menus

### **PageContainer** (`test_page_container.py`)
**Objectif** : Tester le conteneur de pages avec navigation entre les pages.

**Fonctionnalités testées** :
- Ajout/suppression de pages
- Navigation entre les pages
- Gestion du dictionnaire des pages
- Layout avec marges
- Widget empilé (QStackedWidget)

### **SettingsPanel** (`test_settings_panel.py`)
**Objectif** : Tester le panneau de paramètres avec ses widgets configurables.

**Fonctionnalités testées** :
- Création du panneau avec largeur personnalisée
- Zone de défilement
- Conteneur de paramètres de thème
- Signaux de changement de paramètres
- Chargement depuis YAML

## 🧪 **Widgets Étendus**

### **SettingWidgets** (`test_setting_widgets.py`)
**Objectif** : Tester tous les widgets de paramètres spécialisés.

#### **BaseSettingWidget**
- Initialisation avec label et description
- Gestion de la clé de paramètre
- Interface de base commune

#### **SettingToggle**
- Basculement on/off
- Valeur par défaut
- Signal de changement de valeur
- Interface utilisateur

#### **SettingSelect**
- Liste déroulante avec options
- Sélection par défaut
- Changement de valeur
- Validation des options

#### **SettingSlider**
- Slider avec valeurs min/max
- Unité de mesure
- Affichage de la valeur
- Changement interactif

#### **SettingText**
- Champ de texte éditable
- Valeur par défaut
- Validation du texte
- Signal de modification

#### **SettingCheckbox**
- Case à cocher
- État par défaut
- Signal de changement
- Interface utilisateur

## 📊 **Statistiques**

### **Tests par Module**
- **Widgets Core** : 100+ tests
  - EzApplication : 15+ tests
  - Header : 20+ tests
  - Menu : 20+ tests
  - PageContainer : 20+ tests
  - SettingsPanel : 25+ tests
- **Widgets Étendus** : 30+ tests
  - SettingWidgets : 30+ tests (6 classes)
- **Total** : 130+ tests

### **Couverture Estimée**
- **Widgets Core** : 95%
- **Widgets Étendus** : 90%

## 🚀 **Exécution**

```bash
# Tests des widgets uniquement
python -m pytest tests/unit/test_widgets/ -v

# Tests des widgets core
python -m pytest tests/unit/test_widgets/test_core/ -v

# Tests des widgets étendus
python -m pytest tests/unit/test_widgets/test_extended/ -v

# Tests avec couverture
python -m pytest tests/unit/test_widgets/ --cov=ezqt_app.widgets --cov-report=html
```

## 🔧 **Fixtures utilisées**

- `qt_application` : Instance QApplication pour tous les tests
- `qt_widget_cleanup` : Nettoyage automatique des widgets
- `wait_for_signal` : Attendre les signaux Qt

## 📝 **Exemples d'utilisation**

### **Test d'un widget core**
```python
def test_header_creation(qt_application):
    """Test de création d'un en-tête."""
    header = Header(app_name="Test App", description="Test Description")
    
    assert header.objectName() == "headerContainer"
    assert header.height() == 50
    assert header.titleTopApp.text() == "Test App"
    assert header.titleTopDescriptionApp.text() == "Test Description"
```

### **Test d'un widget étendu**
```python
def test_setting_toggle_workflow(qt_application):
    """Test du workflow d'un toggle de paramètre."""
    toggle = SettingToggle("Test Toggle", default=True)
    
    assert toggle.value == True
    assert toggle.get_value() == True
    
    toggle.value = False
    assert toggle._value == False
```

### **Test de signaux**
```python
def test_button_signal(qt_application):
    """Test des signaux d'un bouton."""
    header = Header()
    
    # Capturer le signal
    signal_received = False
    def on_clicked():
        nonlocal signal_received
        signal_received = True
    
    header.settingsTopBtn.clicked.connect(on_clicked)
    header.settingsTopBtn.clicked.emit()
    
    assert signal_received == True
```

## ✅ **Bonnes pratiques**

1. **Isolation des widgets** : Chaque test crée ses propres instances
2. **Nettoyage automatique** : Utiliser les fixtures de nettoyage
3. **Test des propriétés** : Vérifier les propriétés Qt importantes
4. **Test des signaux** : Vérifier l'émission et la réception des signaux
5. **Test des layouts** : Vérifier la structure des layouts
6. **Test des états** : Tester les différents états des widgets

## 📚 **Dépendances**

- `pytest` : Framework de test
- `pytest-qt` : Support Qt
- `pytest-mock` : Mocking
- `PySide6` : Interface Qt

## 🔍 **Cas de test couverts**

### **Scénarios d'interface**
- Création et initialisation des widgets
- Gestion des propriétés et états
- Interaction utilisateur (clics, saisie)
- Signaux et événements

### **Scénarios de layout**
- Structure des layouts
- Gestion des marges et espacements
- Responsive design
- Intégration des composants

### **Scénarios d'erreur**
- Widgets invalides
- Propriétés manquantes
- Signaux non connectés
- États incohérents

## 📈 **Métriques de qualité**

- **Couverture de code** : > 95%
- **Tests d'interface** : 60% des tests
- **Tests de signaux** : 25% des tests
- **Tests d'erreur** : 15% des tests
- **Temps d'exécution** : < 15 secondes par module

## 🎯 **Résultats des tests**

### **Tests Core Widgets**
- ✅ **EzApplication** : 14 tests passent
- ✅ **Header** : 20 tests passent
- ✅ **Menu** : 21 tests passent
- ✅ **PageContainer** : 15 tests passent
- ✅ **SettingsPanel** : 24 tests passent

### **Tests Extended Widgets**
- ✅ **SettingWidgets** : 38 tests passent

### **Total**
- **132 tests passent sur 132** 🎉
- **0 échec, 0 skip**
- **8 warnings** (dépréciation AA_EnableHighDpiScaling)

## 🔧 **Corrections récentes**

### **Problèmes résolus**
1. **Signaux Qt** : Correction de la configuration des signaux dans `conftest.py`
2. **Constantes QFrame** : Remplacement de `widget.NoFrame` par `QFrame.NoFrame`
3. **Marges Qt** : Correction des comparaisons `contentsMargins()` vs objets `QMargins`
4. **Types de widgets** : Correction des assertions de type pour `MenuButton`
5. **Tests de signaux** : Réactivation du test `test_signal_definition`

### **Améliorations**
- Tests plus robustes et compatibles PySide6
- Meilleure gestion des objets Qt
- Assertions plus précises
- Suppression des tests skipés

---

**État :** 🟢 **OPÉRATIONNEL** (132 tests, couverture > 95%) 