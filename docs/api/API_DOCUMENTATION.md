# Complete API Documentation - EzQt_App

## Overview

This documentation presents all available components in the EzQt_App framework, organized by functional modules. Each component is designed to provide specialized functionality while maintaining API and design consistency.

## Table of Contents

- [🧠 Core Module](#-core-module-ezqt_appkernel)
  - [Kernel Architecture](#kernel-architecture)
  - [App Functions Package](#app-functions-package)
  - [UI Functions Package](#ui-functions-package)
  - [Resource Definitions](#resource-definitions)
  - [Translation Package](#translation-package)
  - [Helper Functions](#helper-functions)
  - [Standardized Logging System](#standardized-logging-system)
- [🎨 Widget Module](#-widget-module-ezqt_appwidgets)
  - [EzApplication](#ezapplication)
  - [EzQt_App](#ezqt_app)
  - [Core Widgets](#core-widgets)
  - [Extended Widgets](#extended-widgets)
- [🔧 Utility Module](#-utility-module-ezqt_apputils)
  - [CLI](#cli)
  - [QMessageLogger](#qmessagelogger)
  - [Create QM Files](#create-qm-files)

## Module Structure

### 🧠 Core Module (`ezqt_app.kernel`)
Core application functions, resource management, and configuration with modular architecture.

**New Architecture:**
- **Modular Design**: Refactored into specialized packages
- **Helper Functions**: Simplified API for common operations
- **Centralized Resources**: Unified resource management
- **Translation System**: Complete internationalization support with automatic translation
- **Qt Configuration**: High DPI support and cross-platform configuration
- **Initialization System**: Structured initialization sequence

### 🎨 Widget Module (`ezqt_app.widgets`)
Custom widgets and UI components for modern applications.

### 🔧 CLI Module (`ezqt_app.cli`)
Command line interface and project management tools.

## Components by Module

### 🧠 Core Components

#### Kernel Architecture
**Package :** `kernel/`

**New Modular Structure:**
```
kernel/
├── __init__.py              # Main interface
├── common.py                # Common variables (APP_PATH)
├── globals.py               # Global UI state variables
├── qt_config.py             # Qt configuration and High DPI support
├── app_functions/           # Application functions package
│   ├── __init__.py         # Package interface
│   ├── assets_manager.py   # Asset management
│   ├── config_manager.py   # YAML configuration
│   ├── file_maker.py       # File generation utilities
│   ├── resource_manager.py # System resources
│   ├── settings_manager.py # Application settings
│   ├── kernel.py           # Main facade class
│   ├── helpers.py          # Helper functions
│   └── printer.py          # Standardized logging system
├── ui_functions/            # UI functions package
│   ├── __init__.py         # Package interface
│   ├── window_manager.py   # Window state management
│   ├── panel_manager.py    # Panel animations
│   ├── menu_manager.py     # Menu management
│   ├── theme_manager.py    # Theme management
│   ├── ui_definitions.py   # UI definitions
│   ├── ui_functions.py     # Main facade class
│   └── helpers.py          # Helper functions
├── initialization/          # Initialization package
│   ├── __init__.py         # Package interface
│   ├── initializer.py      # Main initializer
│   ├── sequence.py         # Initialization sequence
│   └── startup_config.py   # Startup configuration
├── resource_definitions/    # Resource definitions package
│   ├── __init__.py         # Package interface
│   ├── images.py           # Image definitions
│   ├── icons.py            # Icon definitions
│   └── base_resources.py   # Qt compiled resources
├── translation/             # Translation package
│   ├── __init__.py         # Package interface
│   ├── config.py           # Language configuration
│   ├── manager.py          # Translation manager
│   ├── auto_translator.py  # Multi-provider automatic translation
│   ├── string_collector.py # Automatic string collection
│   └── helpers.py          # Translation helpers
├── app_resources.py         # Resource facade
├── app_settings.py          # Application settings
├── app_components.py        # Base components
└── ui_main.py              # Main UI interface
```

**Style Guide :** [See QSS styles](STYLE_GUIDE.md#kernel)

Core application functions and resource management with modular architecture.

**Features :**
- Asset management and generation
- YAML configuration handling
- Font resource loading
- File and directory management
- Package resource handling
- Modular design with specialized packages
- Qt configuration and High DPI support
- Structured initialization sequence
- Automatic translation system
- Helper functions for simplified API
- Standardized logging system with consistent formatting

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

#### App Functions Package
**Package :** `kernel/app_functions/`

**Specialized Managers:**
- **AssetsManager**: Asset generation and verification
- **ConfigManager**: YAML configuration loading and saving
- **ResourceManager**: System resources like font loading
- **SettingsManager**: Application settings management
- **Kernel**: Main facade class combining all managers

**Helper Functions:**
- `load_config_section(section)` : Load YAML configuration section
- `save_config_section(section, data)` : Save YAML configuration section
- `get_setting(section, key, default)` : Get configuration setting with fallback
- `set_setting(section, key, value)` : Set configuration setting
- `load_fonts()` : Load system fonts
- `verify_assets()` : Verify asset integrity
- `get_resource_path(resource_type, name)` : Get resource path
- `get_kernel_instance()` : Get kernel instance
- `is_development_mode()` : Check development mode
- `get_app_version()` : Get application version
- `get_app_name()` : Get application name

#### UI Functions Package
**Package :** `kernel/ui_functions/`

**Specialized Managers:**
- **WindowManager**: Window state management (maximize/restore)
- **PanelManager**: Menu and settings panel animations
- **MenuManager**: Menu item selection and style refreshing
- **ThemeManager**: QSS theme loading and application
- **UIDefinitions**: General UI definitions and custom grips
- **UIFunctions**: Main facade class combining all UI managers

**Helper Functions:**
- `maximize_window(window)` : Maximize main window
- `restore_window(window)` : Restore main window
- `toggle_window_state(window)` : Toggle window state
- `load_theme(theme_name)` : Load QSS theme
- `apply_theme(widget, theme_content)` : Apply theme to widget
- `animate_panel(panel, direction, duration)` : Animate panel
- `select_menu_item(button, enable)` : Select menu item
- `refresh_menu_style()` : Refresh menu style
- `setup_custom_grips(window)` : Setup custom grips
- `connect_window_events(window)` : Connect window events
- `get_ui_functions_instance()` : Get UI functions instance
- `is_window_maximized(window)` : Check if window is maximized
- `get_window_status(window)` : Get window status
- `apply_default_theme(widget)` : Apply default theme
- `setup_window_title_bar(window, title_bar)` : Setup title bar

#### Resource Definitions Package
**Package :** `kernel/resource_definitions/`

**Components:**
- **Images**: Image resource definitions
- **Icons**: Icon resource definitions
- **BaseResources**: Qt compiled resource data

#### Translation Package
**Package :** `kernel/translation/`

**New Structure:**
```
translation/
├── __init__.py              # Package interface
├── manager.py               # Translation manager with .ts file support
├── auto_translator.py       # Multi-provider automatic translation system
├── string_collector.py      # Automatic string collection for translations
├── config.py                # Language configuration and setup
└── helpers.py               # Translation helper functions
```

**Components:**
- **Config**: Language configuration and supported languages
- **Manager**: Translation manager with .ts file support
- **Auto-Translator**: Multi-provider automatic translation (LibreTranslate, MyMemory, Google)
- **String Collector**: Automatic string collection for translations
- **Helpers**: Translation helper functions

**Translation Helper Functions:**
- `tr(text)` : Translate text
- `set_tr(widget, text)` : Set translatable text on widget
- `register_tr(widget, text)` : Register widget for translation
- `unregister_tr(widget)` : Unregister widget
- `change_language(language_name)` : Change application language
- `get_available_languages()` : Get available languages
- `get_current_language()` : Get current language

**Automatic Translation:**
```python
from ezqt_app.kernel.translation.auto_translator import AutoTranslator

# Create auto-translator instance
translator = AutoTranslator()

# Translate text with specific provider
translated = translator.translate_sync("Hello World", "fr", provider="libretranslate")

# Available providers: libretranslate, mymemory, google
# Note: Automatic translation system is temporarily disabled for development
```

#### Helper Functions
**Package :** `kernel/`

**Simplified API for common operations:**

**Configuration Helpers:**

#### Qt Configuration
**File :** `kernel/qt_config.py`

**Overview :**
Qt environment configuration and High DPI support for cross-platform compatibility.

**Features :**
- **High DPI Support**: Automatic scaling for high-resolution displays
- **Cross-Platform Configuration**: Platform-specific Qt settings
- **Environment Variables**: Qt environment configuration
- **Application Attributes**: Qt application attribute settings

**Usage :**
```python
from ezqt_app.kernel import qt_config

# Qt configuration is automatically applied during initialization
# High DPI scaling is enabled by default
# Platform-specific settings are configured automatically
```

#### Initialization System
**Package :** `kernel/initialization/`

**Overview :**
Structured initialization sequence for the EzQt_App framework.

**Components:**
- **Initializer**: Main initialization controller
- **Sequence**: Step-by-step initialization process
- **Startup Config**: Startup configuration management

**Initialization Steps:**
1. **Configure Startup**: UTF-8 encoding, locale, environment variables
2. **Check Requirements**: Verify assets and dependencies
3. **Load Configuration**: Load application settings
4. **Initialize Resources**: Load fonts, themes, and resources
5. **Setup Translation**: Initialize translation system
6. **Configure Qt**: Apply Qt configuration and High DPI settings
7. **Initialize UI**: Setup UI components and themes
8. **Load Assets**: Load and verify application assets
9. **Setup Logging**: Initialize logging system
10. **Finalize**: Complete initialization and verify system

**Usage :**
```python
from ezqt_app.kernel.initialization import Initializer

# Initialize the framework
initializer = Initializer()
initializer.initialize()

# Or use the main interface
from ezqt_app.kernel import initialize
initialize()
```

#### Standardized Logging System
**Package :** `kernel/app_functions/printer.py`

**Overview :**
The EzQt_App framework implements a standardized logging system that provides consistent message formatting across all components. This system ensures professional output with color-coded messages and subsystem identification.

**Features :**
- **Consistent Formatting** : All messages follow the `[Subsystem] Message` pattern
- **Color Coding** : Different colors for different message types
- **Subsystem Identification** : Clear identification of message sources
- **Verbose Mode** : Optional detailed output for debugging
- **Configuration Display** : ASCII art boxes for configuration data

**Message Types and Colors :**

| Type | Prefix | Color | Usage |
|------|--------|-------|-------|
| **Info** | `~` | White | General information messages |
| **Action** | `+` | Blue | Actions being performed |
| **Success** | `✓` | Green | Successful operations |
| **Warning** | `!` | Orange | Warning messages |
| **Error** | `✗` | Red | Error messages |
| **Init** | `🚀` | Magenta | Initialization messages |

**Usage Examples :**

```python
from ezqt_app.kernel.app_functions.printer import get_printer, Printer

# Get printer instance
printer = get_printer(verbose=True)

# Different message types
printer.info("[TranslationManager] Traductions chargées pour English")
printer.action("[AppKernel] 10 widgets registered for translation.")
printer.success("[FileMaker] Generated app_resources.py file. Ready for use.")
printer.warning("[ThemeManager] Fichier de thème non trouvé")
printer.error("[ConfigManager] Erreur lors de la lecture du fichier YAML")

# Configuration display (verbose mode only)
config_data = {"name": "MyApp", "theme": "dark", "width": 1280}
printer.config_display(config_data)
```

**Output Example :**
```
~ [TranslationManager] Traductions chargées pour English
+ [AppKernel] 10 widgets registered for translation.
+ [AppKernel] Loaded Application settings.
   ┌───────────────────────────────────────────────┐
   |- name: MyApplication
   |- description: This is an example description
   |- theme: dark
   |- app_width: 1280
   └───────────────────────────────────────────────┘
...
```

**Initialization Sequence Format :**

The initialization sequence uses the standardized logging system for consistent output:

```
~ [InitializationSequence] Starting EzQt_App Initialization Sequence
~ [InitializationSequence] Total steps: 10
~
+ [InitializationSequence] [ 1/10] Configure Startup
~     Configure UTF-8 encoding, locale, and environment variables
✓ [InitializationSequence] Step completed successfully (0.00s)
~
+ [InitializationSequence] [ 2/10] Check Requirements
~     Verify that all required assets and dependencies are available
✓ [InitializationSequence] Step completed successfully (0.21s)
~
...
~ [InitializationSequence] Initialization Summary
~ [InitializationSequence] Total Steps: 10
✓ [InitializationSequence] Successful: 10
✗ [InitializationSequence] Failed: 0
⚠️ [InitializationSequence] Skipped: 0
~ [InitializationSequence] Total Time: 0.24s
✓ [InitializationSequence] Initialization completed successfully!
```

**Integration :**

The standardized logging system is integrated throughout the framework:

- **FileMaker** : Uses `[FileMaker]` prefix for file generation messages
- **TranslationManager** : Uses `[TranslationManager]` prefix for translation messages
- **SettingsManager** : Uses `[AppKernel]` prefix for configuration messages
- **InitializationSequence** : Uses `[InitializationSequence]` prefix for initialization messages
- **ThemeManager** : Uses `[ThemeManager]` prefix for theme-related messages
```python
from ezqt_app.kernel import get_setting, set_setting

# Get configuration with fallback
theme = get_setting("app", "theme", "dark")
width = get_setting("ui", "window.width", 800)

# Set configuration
set_setting("app", "theme", "light")
set_setting("ui", "window.width", 1024)
```

**Resource Helpers:**
```python
from ezqt_app.kernel import load_fonts, verify_assets, get_resource_path

# Load system fonts
load_fonts()

# Verify assets
status = verify_assets()

# Get resource path
font_path = get_resource_path("fonts", "Segoe UI.ttf")
```

**UI Helpers:**
```python
from ezqt_app.kernel import maximize_window, apply_theme, load_theme

# Window operations
maximize_window(main_window)

# Theme operations
theme_content = load_theme("dark_theme")
apply_theme(widget, theme_content)
```

**Translation Helpers:**
```python
from ezqt_app.kernel import tr, change_language

# Translate text
translated = tr("Hello")

# Change language
change_language("Français")
```


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
**File :** `main.py`  
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

#### **4. Automatic Translation System**
```python
from ezqt_app.kernel.translation.auto_translator import AutoTranslator

# Create auto-translator instance
translator = AutoTranslator()

# Translate text with specific provider
translated = translator.translate_sync("Hello World", "fr", provider="libretranslate")

# Available providers: libretranslate, mymemory, google
# Note: Automatic translation system is temporarily disabled for development
```

#### **5. String Collection**
```python
from ezqt_app.kernel.translation.string_collector import StringCollector

# Collect strings from widgets automatically
collector = StringCollector()
collector.collect_from_widget(widget)

# Save collected strings to translation files
collector.save_to_ts_file("ezqt_app_fr.ts")
```

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

**New Translation System Structure:**
```
translation/
├── manager.py               # Translation manager with .ts file support
├── auto_translator.py       # Multi-provider automatic translation
├── string_collector.py      # Automatic string collection
├── config.py                # Language configuration
└── helpers.py               # Translation helper functions
```

**Note:** The system uses a priority order to find translations:
1. **User project** (`bin/translations/`) - Priority 1
2. **Local development** (`ezqt_app/resources/translations/`) - Priority 2  
3. **Installed package** - Priority 3

Translations are automatically copied from the package to the user project during initialization.

**Automatic Translation Providers:**
- **LibreTranslate**: Open-source translation service
- **MyMemory**: Free translation API
- **Google Translate**: Google translation service (when available)

**Note:** Automatic translation system is temporarily disabled for development.

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
7. **Multi-Provider** : Support for multiple translation services
8. **String Collection** : Automatic collection of translatable strings
9. **Cross-Platform** : Works on all supported platforms
10. **Extensible** : Easy to add new translation providers

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

# Automatic translation (when enabled)
from ezqt_app.kernel.translation.auto_translator import AutoTranslator
translator = AutoTranslator()
auto_translated = translator.translate_sync("Hello World", "fr")

# String collection
from ezqt_app.kernel.translation.string_collector import StringCollector
collector = StringCollector()
collector.collect_from_widget(label)
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