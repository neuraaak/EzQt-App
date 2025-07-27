# 🌍 Système de Traduction Global EzQt_App

## 📋 Vue d'ensemble

Le système de traduction global d'EzQt_App permet de traduire automatiquement tous les textes de l'interface utilisateur, y compris les widgets externes (ezqt-widgets). Il utilise un gestionnaire centralisé qui gère la retraduction automatique lors du changement de langue.

## 🚀 Utilisation rapide

### **1. Traduction simple**
```python
from ezqt_app.kernel import tr

# Traduire un texte
text = tr("Hello World")  # Retourne "Bonjour le monde" en français
```

### **2. Widget avec retraduction automatique**
```python
from ezqt_app.kernel import set_tr

# Définir un texte traduit et l'enregistrer pour retraduction automatique
set_tr(self.my_label, "Welcome")  # Se retraduit automatiquement au changement de langue
```

### **3. Changement de langue**
```python
from ezqt_app.kernel import change_language

# Changer de langue
change_language("Français")  # Retraduit automatiquement tous les widgets enregistrés
```

## 📚 API complète

### **Fonctions principales**

#### `tr(text: str) -> str`
Traduit un texte et retourne la traduction.
```python
from ezqt_app.kernel import tr
message = tr("Settings")  # "Paramètres" en français
```

#### `set_tr(widget, text: str)`
Définit un texte traduit sur un widget et l'enregistre pour retraduction automatique.
```python
from ezqt_app.kernel import set_tr
set_tr(self.button, "Save")  # Le bouton se retraduit automatiquement
```

#### `register_tr(widget, text: str)`
Enregistre un widget pour retraduction automatique sans changer son texte immédiatement.
```python
from ezqt_app.kernel import register_tr
register_tr(self.label, "Status")  # Enregistre pour retraduction future
```

#### `unregister_tr(widget)`
Désenregistre un widget de la retraduction automatique.
```python
from ezqt_app.kernel import unregister_tr
unregister_tr(self.old_widget)  # Ne sera plus retraduit
```

#### `change_language(language_name: str) -> bool`
Change la langue de l'application et retraduit tous les widgets enregistrés.
```python
from ezqt_app.kernel import change_language
success = change_language("Español")  # Change vers l'espagnol
```

#### `get_available_languages() -> list`
Retourne la liste des langues disponibles.
```python
from ezqt_app.kernel import get_available_languages
languages = get_available_languages()  # ["English", "Français", "Español", "Deutsch"]
```

#### `get_current_language() -> str`
Retourne la langue actuelle.
```python
from ezqt_app.kernel import get_current_language
current = get_current_language()  # "Français"
```

### **Gestionnaire direct**

Vous pouvez aussi utiliser directement le gestionnaire :
```python
from ezqt_app.kernel.translation_manager import translation_manager

# Méthodes disponibles
translation_manager.translate("text")
translation_manager.set_translatable_text(widget, "text")
translation_manager.load_language("Français")
translation_manager.get_available_languages()
```

## 🎯 Exemples d'utilisation

### **Widget simple**
```python
from PySide6.QtWidgets import QLabel
from ezqt_app.kernel import set_tr

class MonWidget(QLabel):
    def __init__(self):
        super().__init__()
        set_tr(self, "Mon texte traduisible")
```

### **Widget complexe**
```python
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from ezqt_app.kernel import set_tr, tr

class MonWidgetComplexe(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre traduisible
        self.title = QLabel()
        set_tr(self.title, "Titre de la page")
        layout.addWidget(self.title)
        
        # Bouton traduisible
        self.button = QPushButton()
        set_tr(self.button, "Cliquer ici")
        layout.addWidget(self.button)
        
        # Texte dynamique (non retraduit automatiquement)
        self.dynamic_label = QLabel(tr("Texte dynamique"))
        layout.addWidget(self.dynamic_label)
```

### **Widget externe (ezqt-widgets)**
```python
from ezqt_widgets import CustomWidget
from ezqt_app.kernel import set_tr

class MonWidgetExterne(CustomWidget):
    def __init__(self):
        super().__init__()
        # Fonctionne aussi avec les widgets externes !
        set_tr(self, "Texte du widget externe")
```

## 🔧 Configuration

### **Commandes CLI disponibles**
- **`ezqt_init`** : Initialise un nouveau projet EzQt_App
- **`ezqt_qm_convert`** : Convertit les fichiers .ts en .qm pour les traductions

### **Langues supportées**
- **English** (en) - Par défaut
- **Français** (fr)
- **Español** (es)
- **Deutsch** (de)

### **Fichiers de traduction**
Les traductions sont stockées dans `ezqt_app/resources/translations/` et sont installées avec le package :
- `ezqt_app_en.ts` / `ezqt_app_en.qm` - Anglais
- `ezqt_app_fr.ts` / `ezqt_app_fr.qm` - Français
- `ezqt_app_es.ts` / `ezqt_app_es.qm` - Espagnol
- `ezqt_app_de.ts` / `ezqt_app_de.qm` - Allemand

**Note :** Le système utilise un ordre de priorité pour trouver les traductions :
1. **Projet utilisateur** (`bin/translations/`) - Priorité 1
2. **Développement local** (`ezqt_app/resources/translations/`) - Priorité 2  
3. **Package installé** - Priorité 3

Les traductions sont automatiquement copiées du package vers le projet utilisateur lors de l'initialisation.

### **Ajouter une nouvelle langue**
1. Créer `ezqt_app_xx.ts` dans `resources/translations/`
2. Ajouter le mapping dans `translation_manager.py`
3. Exécuter `ezqt_qm_convert` ou `python -m ezqt_app.utils.create_qm_files`
4. Les traductions seront automatiquement copiées vers les nouveaux projets

### **Personnaliser les traductions**
Pour personnaliser les traductions dans votre projet :
1. Modifiez les fichiers dans `bin/translations/` de votre projet
2. Ou ajoutez de nouveaux fichiers de traduction
3. Les modifications locales ont priorité sur le package

## 🎨 Intégration avec l'interface

### **Panneau de paramètres**
Le changement de langue via le panneau de paramètres déclenche automatiquement la retraduction de tous les widgets enregistrés.

### **Signal de changement**
```python
from ezqt_app.kernel.translation_manager import translation_manager

# Connecter au signal de changement de langue
translation_manager.languageChanged.connect(self.on_language_changed)

def on_language_changed(self, language_code):
    print(f"Langue changée vers: {language_code}")
```

## 🚨 Bonnes pratiques

### **✅ À faire**
- Utiliser `set_tr()` pour les textes statiques de l'interface
- Utiliser `tr()` pour les textes dynamiques
- Enregistrer les widgets dès leur création
- Tester avec différentes langues

### **❌ À éviter**
- Ne pas utiliser `self.tr()` (widget local)
- Ne pas oublier d'enregistrer les widgets pour la retraduction
- Ne pas mélanger les systèmes de traduction

## 🔍 Dépannage

### **Widgets non retraduits**
- Vérifier que `set_tr()` a été utilisé
- Vérifier que le widget est encore valide
- Utiliser `register_tr()` si nécessaire

### **Traductions manquantes**
- Vérifier les fichiers .ts
- Régénérer les fichiers .qm avec `ezqt_qm_convert`
- Vérifier que le texte source correspond exactement

### **Erreurs de chargement**
- Vérifier les chemins des fichiers de traduction
- Vérifier les permissions des fichiers
- Consulter les logs de debug

### **Problèmes avec le package installé**
- Vérifier que les traductions sont bien incluses dans le package
- Utiliser `python -m ezqt_app.utils.create_qm_files` pour régénérer
- Vérifier que `pkg_resources` peut accéder aux ressources

## 📝 Migration depuis l'ancien système

### **Avant (widget local)**
```python
class MonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label.setText(self.tr("Mon texte"))  # ❌ Widget local
```

### **Après (gestionnaire global)**
```python
from ezqt_app.kernel import set_tr

class MonWidget(QWidget):
    def __init__(self):
        super().__init__()
        set_tr(self.label, "Mon texte")  # ✅ Gestionnaire global
```

## 🎉 Avantages du nouveau système

1. **Centralisé** : Un seul point de contrôle
2. **Automatique** : Retraduction sans intervention
3. **Universel** : Fonctionne avec tous les widgets
4. **Simple** : API claire et intuitive
5. **Performant** : Pas de duplication de logique
6. **Maintenable** : Code plus propre et organisé 