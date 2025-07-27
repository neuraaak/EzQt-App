# Complete API Documentation - EzQt_App

## Overview

This documentation presents all available components in the EzQt_App framework, organized by functional modules. Each component is designed to provide specialized functionality while maintaining API and design consistency.

## Table of Contents

- [🧠 Core Module](#-core-module-ezqt_appkernel)
  - [Kernel](#kernel)
  - [TranslationManager](#translationmanager)
  - [Settings](#settings)
  - [Helper.Maker](#helpermaker)
- [🎨 Widget Module](#-widget-module-ezqt_appwidgets)
  - [EzApplication](#ezapplication)
  - [EzQt_App](#ezqt_app)
  - [Core Widgets](#core-widgets)
  - [Extended Widgets](#extended-widgets)
- [🔧 Utility Module](#-utility-module-ezqt_apputils)
  - [CLI](#cli)
  - [QMessageLogger](#qmessagelogger)
  - [Create QM Files](#create-qm-files)
- [🌍 Translation Module](#-translation-module-ezqt_appkerneltranslation)
  - [Translation Helpers](#translation-helpers)
  - [Translation Config](#translation-config)
  - [Translation System Guide](#translation-system-guide)

## Module Structure

### 🧠 Core Module (`ezqt_app.kernel`)
Core application functions, resource management, and configuration.

### 🎨 Widget Module (`ezqt_app.widgets`)
Custom widgets and UI components for modern applications.

### 🔧 CLI Module (`ezqt_app.cli`)
Command line interface and project management tools.

### 🌍 Translation Module (`ezqt_app.kernel.translation`)
Translation system and internationalization support.

## Components by Module

### 🧠 Core Components

#### Kernel
**File :** `kernel/app_functions.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#kernel)

Core application functions and resource management.

**Features :**
- Asset management and generation
- YAML configuration handling
- Font resource loading
- File and directory management
- Package resource handling

**Main methods :**
- `checkAssetsRequirements()` : Check and generate required assets
- `makeRequiredFiles(mkTheme=True)` : Generate required files
- `loadKernelConfig(config_name)` : Load configuration
- `saveKernelConfig(config_name, data)` : Save configuration
- `writeYamlConfig(keys, val)` : Write YAML configuration
- `loadFontsResources(app=False)` : Load font resources

**Configuration methods :**
- `yamlFile(yamlFile)` : Set YAML configuration file
- `getConfigPath(config_name)` : Get configuration file path
- `getPackageResource(resource_path)` : Get package resource path

#### TranslationManager
**File :** `kernel/translation_manager.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#translationmanager)

Multilingual translation management system.

**Features :**
- Language loading and switching
- Widget registration for automatic retranslation
- Support for .ts and .qm files
- Language mapping (name ↔ code)
- Singleton pattern implementation

**Main methods :**
- `load_language(language_name)` : Load language by name
- `load_language_by_code(language_code)` : Load language by code
- `register_widget(widget, original_text)` : Register widget for translation
- `unregister_widget(widget)` : Unregister widget
- `translate(text)` : Translate text
- `get_available_languages()` : Get available languages
- `get_current_language_code()` : Get current language code

**Signals :**
- `languageChanged(str)` : Language changed signal

**Supported languages :**
- English (en)
- Français (fr)
- Español (es)
- Deutsch (de)

#### Settings
**File :** `kernel/app_settings.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#settings)

Application configuration and settings management.

**Features :**
- Application settings structure
- Window configuration
- Theme settings
- Animation settings
- GUI parameters

**Main structures :**
- `Settings.App` : Application settings
- `Settings.Window` : Window configuration
- `Settings.Theme` : Theme settings
- `Settings.Animation` : Animation configuration

#### Helper.Maker
**File :** `helper.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#helpermaker)

File and resource generation utilities.

**Features :**
- Asset binary generation
- QRC file creation
- RC Python file generation
- YAML file creation
- QSS theme file generation
- Translation file copying

**Main methods :**
- `make_assets_binaries()` : Generate asset binaries
- `make_qrc()` : Create QRC file
- `make_rc_py()` : Generate RC Python file
- `make_yaml(yaml_package)` : Create YAML file
- `make_qss(theme_package)` : Generate QSS theme
- `make_translations(translations_package)` : Copy translation files

### 🎨 Widget Components

#### EzApplication
**File :** `widgets/core/ez_app.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#ezapplication)

Extended QApplication with theme support and UTF-8 encoding.

**Features :**
- High DPI scaling support
- UTF-8 encoding configuration
- Theme change signal
- Locale configuration
- Environment variable setup

**Main methods :**
- `__init__(*args, **kwargs)` : Initialize with UTF-8 and high DPI
- `create_for_testing(*args, **kwargs)` : Create instance for testing

**Signals :**
- `themeChanged()` : Theme changed signal

#### EzQt_App
**File :** `app.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#ezqt_app)

Main application window with modern UI components.

**Features :**
- Custom title bar (Windows)
- Dynamic theme switching
- Menu and page management
- Settings panel integration
- Translation system integration
- Signal management

**Main methods :**
- `__init__(themeFileName=None)` : Initialize application window
- `setAppTheme()` : Set application theme
- `updateUI()` : Update user interface
- `setAppIcon(icon, yShrink=0, yOffset=0)` : Set application icon
- `addMenu(name, icon)` : Add menu and page
- `switchMenu()` : Switch between menus
- `set_credits(credits)` : Set credits text
- `set_version(version)` : Set version text

**Signals :**
- Theme change signals
- Menu selection signals
- Settings change signals

#### Core Widgets

##### Header
**File :** `widgets/core/header.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#header)

Application header with control buttons and branding.

**Features :**
- Application title and description
- Control buttons (settings, minimize, maximize, close)
- Logo display
- Theme-aware styling

**Main methods :**
- `set_app_logo(logo, y_shrink=0, y_offset=0)` : Set application logo
- `update_all_theme_icons()` : Update theme icons

##### Menu
**File :** `widgets/core/menu.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#menu)

Side menu with expand/collapse functionality.

**Features :**
- Collapsible side menu
- Menu button management
- Animation support
- Theme integration

**Main methods :**
- `add_menu(name, icon)` : Add menu button
- `update_all_theme_icons()` : Update theme icons

##### PageContainer
**File :** `widgets/core/page_container.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#pagecontainer)

Container for managing application pages.

**Features :**
- Page management
- Navigation between pages
- Stacked widget integration

**Main methods :**
- `add_page(name)` : Add new page
- `setCurrentWidget(page)` : Switch to page

##### SettingsPanel
**File :** `widgets/core/settings_panel.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#settingspanel)

Settings panel with configurable widgets.

**Features :**
- Scrollable settings area
- Theme settings container
- Dynamic widget creation
- YAML configuration integration

**Main methods :**
- `get_theme_toggle_button()` : Get theme toggle button
- `update_all_theme_icons()` : Update theme icons

#### Extended Widgets

##### SettingWidgets
**File :** `widgets/extended/setting_widgets.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#settingwidgets)

Specialized settings widgets with validation.

**Features :**
- Base setting widget class
- Label and description management
- Parameter key handling
- Common interface

### 🔧 Utility Components

#### CLI
**File :** `cli/main.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#cli)

Command line interface for project management and utilities.

**Features :**
- Project initialization (`ezqt init`)
- Translation file conversion (`ezqt convert` / `ezqt mkqm`)
- Test execution (`ezqt test`)
- Documentation serving (`ezqt docs`)
- Project information (`ezqt info`)
- Template creation (`ezqt create`)

**Main commands :**
- `init` : Initialize new EzQt_App project
- `convert` : Convert .ts files to .qm format
- `mkqm` : Convert .ts files to .qm format (alias)
- `test` : Run test suite
- `docs` : Serve documentation locally
- `info` : Show package information
- `create` : Create project templates

**Usage :**
```bash
# Main CLI
ezqt --help

# Initialize project
ezqt init

# Convert translations
ezqt convert
ezqt mkqm

# Run tests
ezqt test --unit --coverage

# Serve documentation
ezqt docs --serve --port 8080

# Create template
ezqt create --template advanced --name my_app
```



#### Create QM Files
**File :** `cli/create_qm_files.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#createqmfiles)

Translation file conversion utilities.

**Features :**
- .ts to .qm file conversion
- Batch processing
- Error handling
- Progress reporting
- Priority: project `bin/translations/` then package fallback

**Main function :**
- `main()` : Main conversion function

**Usage :**
```bash
# Via CLI
ezqt convert
ezqt mkqm
```

**File Priority :**
1. **Project translations** : `bin/translations/` (user's project)
2. **Package fallback** : `ezqt_app/resources/translations/` (development)

#### ProjectRunner
**File :** `cli/runner.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#projectrunner)

Project management and template creation utilities.

**Features :**
- Project structure analysis
- Template creation (basic/advanced)
- Project information gathering
- Template management

**Main class :**
- `ProjectRunner(verbose)` : Project runner with verbose mode

**Main methods :**
- `get_project_info()` : Get current project structure info
- `create_project_template(template_type, project_name)` : Create new project
- `list_available_templates()` : List available templates

**Usage :**
```python
from ezqt_app.cli.runner import ProjectRunner

# Create project runner
runner = ProjectRunner(verbose=True)

# Get project info
info = runner.get_project_info()
print(f"Project status: {info['status']}")

# Create template
success = runner.create_project_template("advanced", "my_app")
```

### 🌍 Translation Components

#### Translation Helpers
**File :** `kernel/translation_helpers.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#translationhelpers)

Utility functions for translations.

**Features :**
- Widget text setting
- Translation registration
- Language management
- Helper functions

**Main functions :**
- `tr(text)` : Translate text
- `set_tr(widget, text)` : Set translatable text
- `register_tr(widget, text)` : Register widget for translation
- `unregister_tr(widget)` : Unregister widget
- `change_language(language)` : Change language
- `get_available_languages()` : Get available languages
- `get_current_language()` : Get current language

#### Translation Config
**File :** `kernel/translation_config.py`  
**Style Guide :** [See QSS styles](STYLE_GUIDE.md#translationconfig)

Translation configuration and setup.

**Features :**
- Translation file configuration
- Language mapping
- Default settings
- Configuration validation

## 🌍 Translation System Guide

### Quick Start

#### **1. Simple Translation**
```python
from ezqt_app.kernel import tr, set_tr

# Translate text
text = tr("Hello World")  # Returns "Bonjour le monde" in French

# Set translated text for widget
from PySide6.QtWidgets import QLabel
label = QLabel("Hello World")
set_tr(label, "Hello World")  # Automatically retranslates on language change
```

#### **2. Language Management**
```python
from ezqt_app.kernel import change_language

# Change language
change_language("Français")  # Automatically retranslates all registered widgets
```

#### **3. Adding New Languages**
1. Create `ezqt_app_xx.ts` in `resources/translations/`
2. Add mapping in `translation_manager.py`
3. Run `ezqt convert` or `python -m ezqt_app.cli.create_qm_files`
4. Translations will be automatically copied to new projects

## 📋 Version Management Guide

### **Automatic Version Detection**

The framework automatically detects the version from your `main.py` file:

```python
# In your main.py
__version__ = "1.5.18"  # This will be automatically detected
```

### **Version Display**

The version is displayed in the bottom bar of the application interface.

### **Compiled Application Support**

When your application is compiled to `.exe`, the version detection uses multiple fallback methods:

1. **Primary**: Look for `__version__` in `main.py` in current directory
2. **Secondary**: Look for `__version__` in script directory
3. **Tertiary**: Look for `__version__` in parent directory
4. **Quaternary**: Try to import `main` module directly
5. **Fallback**: Use EzQt_App version as default

### **Manual Version Setting**

You can manually set the version if automatic detection fails:

```python
# In your main.py
from ezqt_app.app import EzQt_App, EzApplication

app = EzApplication(sys.argv)
window = EzQt_App(themeFileName="main_theme.qss")

# Force version display
window.bottom_bar.set_version_forced("v1.5.18")

window.show()
app.exec()
```

### **Best Practices**

1. **Always define `__version__`** in your `main.py` file
2. **Use semantic versioning** (e.g., "1.5.18")
3. **Test compiled version** to ensure version detection works
4. **Use manual setting** as fallback for compiled applications

### **Troubleshooting**

| Issue | Solution |
|-------|----------|
| Version not showing in compiled app | Use `set_version_forced()` method |
| Version shows as "v3.2.0" | Check that `__version__` is defined in `main.py` |
| Version detection fails | Ensure `main.py` is in the correct directory |

### Complete API Reference

#### **Main Functions**

##### `tr(text: str) -> str`
Translates text and returns the translation.
```python
from ezqt_app.kernel import tr
message = tr("Settings")  # "Paramètres" in French
```

##### `set_tr(widget, text: str)`
Sets translated text on a widget and registers it for automatic retranslation.
```python
from ezqt_app.kernel import set_tr
set_tr(self.button, "Save")  # Button automatically retranslates
```

##### `register_tr(widget, text: str)`
Registers a widget for automatic retranslation without changing its text immediately.
```python
from ezqt_app.kernel import register_tr
register_tr(self.label, "Status")  # Register for future retranslation
```

##### `unregister_tr(widget)`
Unregisters a widget from automatic retranslation.
```python
from ezqt_app.kernel import unregister_tr
unregister_tr(self.old_widget)  # Will no longer be retranslated
```

##### `change_language(language_name: str) -> bool`
Changes the application language and retranslates all registered widgets.
```python
from ezqt_app.kernel import change_language
success = change_language("Español")  # Change to Spanish
```

##### `get_available_languages() -> list`
Returns the list of available languages.
```python
from ezqt_app.kernel import get_available_languages
languages = get_available_languages()  # ["English", "Français", "Español", "Deutsch"]
```

##### `get_current_language() -> str`
Returns the current language.
```python
from ezqt_app.kernel import get_current_language
current = get_current_language()  # "Français"
```

#### **Direct Manager Usage**
You can also use the manager directly:
```python
from ezqt_app.kernel.translation_manager import translation_manager

# Available methods
translation_manager.translate("text")
translation_manager.set_translatable_text(widget, "text")
translation_manager.load_language("Français")
translation_manager.get_available_languages()
```

### Usage Examples

#### **Simple Widget**
```python
from PySide6.QtWidgets import QLabel
from ezqt_app.kernel import set_tr

class MyWidget(QLabel):
    def __init__(self):
        super().__init__()
        set_tr(self, "My translatable text")
```

#### **Complex Widget**
```python
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from ezqt_app.kernel import set_tr, tr

class MyComplexWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Translatable title
        self.title = QLabel()
        set_tr(self.title, "Page Title")
        layout.addWidget(self.title)
        
        # Translatable button
        self.button = QPushButton()
        set_tr(self.button, "Click Here")
        layout.addWidget(self.button)
        
        # Dynamic text (not automatically retranslated)
        self.dynamic_label = QLabel(tr("Dynamic Text"))
        layout.addWidget(self.dynamic_label)
```

#### **External Widget (ezqt-widgets)**
```python
from ezqt_widgets import CustomWidget
from ezqt_app.kernel import set_tr

class MyExternalWidget(CustomWidget):
    def __init__(self):
        super().__init__()
        # Works with external widgets too!
        set_tr(self, "External widget text")
```

### Configuration

#### **Available CLI Commands**
- **`ezqt_init`** : Initialize a new EzQt_App project
- **`ezqt_qm_convert`** : Convert .ts files to .qm for translations

#### **Supported Languages**
- **English** (en) - Default
- **Français** (fr)
- **Español** (es)
- **Deutsch** (de)

#### **Translation Files**
Translations are stored in `ezqt_app/resources/translations/` and installed with the package:
- `ezqt_app_en.ts` / `ezqt_app_en.qm` - English
- `ezqt_app_fr.ts` / `ezqt_app_fr.qm` - French
- `ezqt_app_es.ts` / `ezqt_app_es.qm` - Spanish
- `ezqt_app_de.ts` / `ezqt_app_de.qm` - German

**Note:** The system uses a priority order to find translations:
1. **User project** (`bin/translations/`) - Priority 1
2. **Local development** (`ezqt_app/resources/translations/`) - Priority 2  
3. **Installed package** - Priority 3

Translations are automatically copied from the package to the user project during initialization.

#### **Adding a New Language**
1. Create `ezqt_app_xx.ts` in `resources/translations/`
2. Add mapping in `translation_manager.py`
3. Run `ezqt convert` or `python -m ezqt_app.cli.create_qm_files`
4. Translations will be automatically copied to new projects

#### **Customizing Translations**
To customize translations in your project:
1. Modify files in `bin/translations/` of your project
2. Or add new translation files
3. Local modifications have priority over the package

### Interface Integration

#### **Settings Panel**
Language change via the settings panel automatically triggers retranslation of all registered widgets.

#### **Change Signal**
```python
from ezqt_app.kernel.translation_manager import translation_manager

# Connect to language change signal
translation_manager.languageChanged.connect(self.on_language_changed)

def on_language_changed(self, language_code):
    print(f"Language changed to: {language_code}")
```

### Best Practices

#### **✅ Do**
- Use `set_tr()` for static interface texts
- Use `tr()` for dynamic texts
- Register widgets as soon as they are created
- Test with different languages

#### **❌ Don't**
- Don't use `self.tr()` (local widget)
- Don't forget to register widgets for retranslation
- Don't mix translation systems

### Troubleshooting

#### **Widgets Not Retranslated**
- Check that `set_tr()` was used
- Check that the widget is still valid
- Use `register_tr()` if necessary

#### **Missing Translations**
- Check .ts files
- Regenerate .qm files with `ezqt_qm_convert`
- Check that source text matches exactly

#### **Loading Errors**
- Check translation file paths
- Check file permissions
- Check debug logs

#### **Package Issues**
- Check that translations are included in the package
- Use `python -m ezqt_app.cli.create_qm_files` to regenerate
- Check that `pkg_resources` can access resources

### Migration from Old System

#### **Before (local widget)**
```python
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label.setText(self.tr("My text"))  # ❌ Local widget
```

#### **After (global manager)**
```python
from ezqt_app.kernel import set_tr

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        set_tr(self.label, "My text")  # ✅ Global manager
```

### System Advantages

1. **Centralized** : Single point of control
2. **Automatic** : Retranslation without intervention
3. **Universal** : Works with all widgets
4. **Simple** : Clear and intuitive API
5. **Performant** : No logic duplication
6. **Maintainable** : Cleaner and more organized code

## Example Integrations

### Basic Application Setup

```python
import sys
import ezqt_app.main as ezqt
from ezqt_app.app import EzQt_App, EzApplication

# Initialize the framework
ezqt.init()

# Create application
app = EzApplication(sys.argv)

# Create main window
window = EzQt_App(themeFileName="main_theme.qss")

# Add menus and pages
home_page = window.addMenu("Home", "🏠")
settings_page = window.addMenu("Settings", "⚙️")

# Show application
window.show()
app.exec()
```

### Translation System Integration

```python
from ezqt_app.kernel.translation_manager import get_translation_manager
from ezqt_app.kernel.translation_helpers import tr, set_tr

# Get translation manager
tm = get_translation_manager()

# Change language
tm.load_language("Français")

# Register widgets for translation
from PySide6.QtWidgets import QLabel
label = QLabel("Hello World")
set_tr(label, "Hello World")

# Translate text
translated = tr("Hello World")
```

### Advanced Configuration

```python
from ezqt_app.kernel import Kernel
from ezqt_app.kernel.app_settings import Settings

# Load configuration
config = Kernel.loadKernelConfig("app")

# Update settings
Kernel.writeYamlConfig(
    keys=["settings_panel", "theme", "default"], 
    val="dark"
)

# Access settings
app_name = Settings.App.NAME
window_width = Settings.Window.WIDTH
```

### Custom Theme Integration

```python
from ezqt_app.app import EzQt_App

# Create application with custom theme
window = EzQt_App(themeFileName="custom_theme.qss")

# The theme file should contain QSS styles for all components
# See STYLE_GUIDE.md for detailed QSS examples
```

## Best Practices

### 🎯 Component Selection
1. **Core** : Use Kernel for resource management, TranslationManager for internationalization
2. **Widgets** : Use EzApplication for the main app, EzQt_App for the main window
3. **Utilities** : Use CLI for project setup, QMessageLogger for logging
4. **Translation** : Use TranslationManager for language management, helpers for widget integration

### 🎨 Theming
```python
# Consistent QSS styling for all components
app.setStyleSheet("""
    QMainWindow {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    QMenuBar {
        background-color: #3d3d3d;
        border-bottom: 1px solid #555555;
    }
    
    QPushButton {
        background-color: #0078d4;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        color: white;
    }
    
    QPushButton:hover {
        background-color: #106ebe;
    }
""")
```

### 🔧 Error Handling
```python
# Proper error handling for all components
try:
    # Initialize framework
    ezqt.init()
    
    # Load configuration
    config = Kernel.loadKernelConfig("app")
    
    # Create application
    app = EzApplication(sys.argv)
    window = EzQt_App()
    
except Exception as e:
    print(f"Error initializing application: {e}")
    sys.exit(1)
```

### 📱 Resource Management
```python
# Proper resource management
from pathlib import Path

# Check assets requirements
Kernel.checkAssetsRequirements()

# Load fonts
Kernel.loadFontsResources()

# Generate required files
Kernel.makeRequiredFiles(mkTheme=True)
```

---

**EzQt_App** - Complete framework for modern Qt applications with PySide6 6.9.1. 