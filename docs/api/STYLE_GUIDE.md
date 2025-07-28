# EzQt_App – Style Guide

## Summary

### **Core Components**
- [Kernel](#kernel)
- [TranslationManager](#translationmanager)
- [Settings](#settings)
- [Helper.Maker](#helpermaker)

### **Widget Components**
- [EzApplication](#ezapplication)
- [EzQt_App](#ezqt_app)
- [Header](#header)
- [Menu](#menu)
- [PageContainer](#pagecontainer)
- [SettingsPanel](#settingspanel)
- [SettingWidgets](#settingwidgets)

### **Utility Components**
- [CLI](#cli)
- [Create QM Files](#create-qm-files)
- [ProjectRunner](#projectrunner)

### **Translation Components**
- [Translation Helpers](#translation-helpers)
- [Translation Config](#translation-config)

---

This document defines the style conventions (QSS) for custom components in the EzQt_App framework.

## General Principles
- Use consistent colors, borders, and rounded corners for all components.
- Prefer specific QSS selectors for each custom component.
- Centralize colors and spacing to facilitate maintenance.
- Support both light and dark themes.

---

### Kernel
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#kernel)

**Note:** The Kernel component does not use QSS for styling as it's a backend component. It manages resources and configuration but doesn't have a visual interface.

**Configuration example:**
```yaml
# app.yaml configuration file
app:
  name: "My Application"
  version: "1.0.0"
  theme: "dark"

settings_panel:
  theme:
    default: "dark"
  language:
    default: "English"
```

---

### TranslationManager
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#translationmanager)

**Note:** The TranslationManager component does not use QSS for styling as it's a backend component. It manages translations and language switching.

**Usage example:**
```python
from ezqt_app.kernel.translation_manager import get_translation_manager

tm = get_translation_manager()
tm.load_language("Français")
```

---

### Settings
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#settings)

**Note:** The Settings component does not use QSS for styling as it's a configuration structure. It defines application settings and parameters.

**Settings structure:**
```python
from ezqt_app.kernel.app_settings import Settings

# Access settings
app_name = Settings.App.NAME
window_width = Settings.Window.WIDTH
theme_mode = Settings.Gui.THEME
```

---

### Helper.Maker
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#helpermaker)

**Note:** The Helper.Maker component does not use QSS for styling as it's a utility component. It generates files and resources.

**Usage example:**
```python
from ezqt_app.kernel.app_functions import FileMaker

maker = FileMaker()
maker.make_assets_binaries()
maker.make_qrc()
```

---

### EzApplication
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#ezapplication)

**Note:** The EzApplication component extends QApplication and doesn't require specific QSS styling. It provides theme change signals and UTF-8 configuration.

**Usage example:**
```python
from ezqt_app.widgets.core.ez_app import EzApplication

app = EzApplication(sys.argv)
app.themeChanged.connect(self.on_theme_changed)
```

---

### EzQt_App
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#ezqt_app)

<details>
<summary>View QSS</summary>

```css
/* Main application window */
QMainWindow {
    background-color: #2d2d2d;
    color: #ffffff;
    border: none;
}

/* Custom title bar (Windows) */
QMainWindow::title {
    background-color: #3d3d3d;
    color: #ffffff;
    padding: 8px;
    border-bottom: 1px solid #555555;
}

/* Menu bar */
QMenuBar {
    background-color: #3d3d3d;
    color: #ffffff;
    border-bottom: 1px solid #555555;
}

QMenuBar::item {
    background-color: transparent;
    padding: 8px 12px;
}

QMenuBar::item:selected {
    background-color: #0078d4;
}

/* Status bar */
QStatusBar {
    background-color: #3d3d3d;
    color: #ffffff;
    border-top: 1px solid #555555;
}

/* Scroll bars */
QScrollBar:vertical {
    background-color: #3d3d3d;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #555555;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #0078d4;
}

QScrollBar:horizontal {
    background-color: #3d3d3d;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #555555;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #0078d4;
}
```
</details>

- Adapt colors according to your application's graphic charter.
- The main window supports both light and dark themes.
- Custom title bar is automatically enabled on Windows.

---

### Header
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#header)

<details>
<summary>View QSS</summary>

```css
/* Header container */
HeaderContainer {
    background-color: #3d3d3d;
    border-bottom: 1px solid #555555;
    min-height: 60px;
    max-height: 60px;
}

/* Left side - App info */
HeaderContainer QWidget[objectName="leftAppBg"] {
    background-color: transparent;
    border: none;
}

/* App title */
HeaderContainer QLabel[objectName="titleTopApp"] {
    background-color: transparent;
    border: none;
    color: #ffffff;
    font-size: 16px;
    font-weight: bold;
    padding: 8px 16px;
}

/* App description */
HeaderContainer QLabel[objectName="titleTopDescriptionApp"] {
    background-color: transparent;
    border: none;
    color: #cccccc;
    font-size: 12px;
    padding: 0px 16px 8px 16px;
}

/* Right side - Control buttons */
HeaderContainer QWidget[objectName="rightAppBg"] {
    background-color: transparent;
    border: none;
}

/* Control buttons */
HeaderContainer QPushButton {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 8px;
    margin: 4px;
    min-width: 32px;
    min-height: 32px;
}

HeaderContainer QPushButton:hover {
    background-color: #555555;
}

HeaderContainer QPushButton:pressed {
    background-color: #0078d4;
}

/* Settings button */
HeaderContainer QPushButton[objectName="settingsTopBtn"] {
    background-color: transparent;
    border: none;
}

/* Window control buttons */
HeaderContainer QPushButton[objectName="minimizeAppBtn"] {
    background-color: transparent;
    border: none;
}

HeaderContainer QPushButton[objectName="maximizeRestoreAppBtn"] {
    background-color: transparent;
    border: none;
}

HeaderContainer QPushButton[objectName="closeAppBtn"] {
    background-color: transparent;
    border: none;
}

HeaderContainer QPushButton[objectName="closeAppBtn"]:hover {
    background-color: #e81123;
}
```
</details>

- Adapt colors according to your application's graphic charter.
- The header supports both light and dark themes.
- Control buttons automatically adapt to the current theme.

---

### Menu
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#menu)

<details>
<summary>View QSS</summary>

```css
/* Menu container */
MenuContainer {
    background-color: #2d2d2d;
    border-right: 1px solid #555555;
    min-width: 200px;
    max-width: 200px;
}

/* Toggle button */
MenuContainer QPushButton[objectName="toggleButton"] {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 8px;
    margin: 8px;
    min-width: 32px;
    min-height: 32px;
}

MenuContainer QPushButton[objectName="toggleButton"]:hover {
    background-color: #555555;
}

/* Menu buttons */
MenuContainer QPushButton[objectName^="menu_"] {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 2px 8px;
    text-align: left;
    color: #ffffff;
    font-size: 14px;
}

MenuContainer QPushButton[objectName^="menu_"]:hover {
    background-color: #555555;
}

MenuContainer QPushButton[objectName^="menu_"][class="active"] {
    background-color: #0078d4;
    color: #ffffff;
}

/* Menu icons */
MenuContainer QPushButton[objectName^="menu_"] QLabel {
    background-color: transparent;
    border: none;
    color: inherit;
    font-size: 16px;
    margin-right: 8px;
}

/* Menu text */
MenuContainer QPushButton[objectName^="menu_"] QLabel[objectName="text_label"] {
    background-color: transparent;
    border: none;
    color: inherit;
    font-size: 14px;
}
```
</details>

- Adapt colors according to your application's graphic charter.
- The menu supports both light and dark themes.
- Active menu items are highlighted with the accent color.

---

### PageContainer
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#pagecontainer)

<details>
<summary>View QSS</summary>

```css
/* Page container */
PagesContainer {
    background-color: #2d2d2d;
    border: none;
}

/* Stacked widget */
PagesContainer QStackedWidget {
    background-color: transparent;
    border: none;
}

/* Individual pages */
PagesContainer QWidget {
    background-color: transparent;
    border: none;
    padding: 16px;
}

/* Page title */
PagesContainer QLabel[objectName="pageTitle"] {
    background-color: transparent;
    border: none;
    color: #ffffff;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 16px;
}

/* Page content */
PagesContainer QWidget[objectName="pageContent"] {
    background-color: transparent;
    border: none;
}
```
</details>

- Adapt colors according to your application's graphic charter.
- Pages support both light and dark themes.
- Individual page content can be styled separately.

---

### SettingsPanel
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#settingspanel)

<details>
<summary>View QSS</summary>

```css
/* Settings panel */
SettingsPanel {
    background-color: #3d3d3d;
    border-left: 1px solid #555555;
    min-width: 300px;
    max-width: 300px;
}

/* Scroll area */
SettingsPanel QScrollArea {
    background-color: transparent;
    border: none;
}

SettingsPanel QScrollArea QWidget {
    background-color: transparent;
    border: none;
}

/* Settings container */
SettingsPanel QWidget[objectName="settingsContainer"] {
    background-color: transparent;
    border: none;
    padding: 16px;
}

/* Setting groups */
SettingsPanel QGroupBox {
    background-color: #2d2d2d;
    border: 1px solid #555555;
    border-radius: 6px;
    margin: 8px 0px;
    padding: 12px;
    color: #ffffff;
    font-weight: bold;
}

SettingsPanel QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0px 8px 0px 8px;
}

/* Setting items */
SettingsPanel QWidget[objectName^="setting_"] {
    background-color: transparent;
    border: none;
    padding: 8px 0px;
}

/* Setting labels */
SettingsPanel QLabel {
    background-color: transparent;
    border: none;
    color: #ffffff;
    font-size: 14px;
    padding: 4px 0px;
}

/* Setting descriptions */
SettingsPanel QLabel[objectName="description"] {
    background-color: transparent;
    border: none;
    color: #cccccc;
    font-size: 12px;
    font-style: italic;
    padding: 2px 0px;
}

/* Theme toggle button */
SettingsPanel QWidget[objectName="themeToggleButton"] {
    background-color: transparent;
    border: none;
}
```
</details>

- Adapt colors according to your application's graphic charter.
- The settings panel supports both light and dark themes.
- Setting groups are organized in collapsible sections.

---

### SettingWidgets
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#settingwidgets)

<details>
<summary>View QSS</summary>

```css
/* Base setting widget */
BaseSettingWidget {
    background-color: transparent;
    border: none;
    padding: 8px 0px;
}

/* Setting label */
BaseSettingWidget QLabel[objectName="label"] {
    background-color: transparent;
    border: none;
    color: #ffffff;
    font-size: 14px;
    font-weight: normal;
    padding: 4px 0px;
}

/* Setting description */
BaseSettingWidget QLabel[objectName="description"] {
    background-color: transparent;
    border: none;
    color: #cccccc;
    font-size: 12px;
    font-style: italic;
    padding: 2px 0px;
}

/* Setting value widget */
BaseSettingWidget QWidget[objectName="valueWidget"] {
    background-color: transparent;
    border: none;
    padding: 4px 0px;
}

/* Input fields */
BaseSettingWidget QLineEdit {
    background-color: #2d2d2d;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 8px 12px;
    color: #ffffff;
    selection-color: #ffffff;
    selection-background-color: #0078d4;
}

BaseSettingWidget QLineEdit:hover {
    border-color: #666666;
}

BaseSettingWidget QLineEdit:focus {
    border-color: #0078d4;
}

/* Combo boxes */
BaseSettingWidget QComboBox {
    background-color: #2d2d2d;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 8px 12px;
    color: #ffffff;
    min-width: 120px;
}

BaseSettingWidget QComboBox:hover {
    border-color: #666666;
}

BaseSettingWidget QComboBox:focus {
    border-color: #0078d4;
}

BaseSettingWidget QComboBox::drop-down {
    border: none;
    width: 20px;
}

BaseSettingWidget QComboBox::down-arrow {
    image: url(:/icons/cil-chevron-bottom.png);
    width: 12px;
    height: 12px;
}

/* Check boxes */
BaseSettingWidget QCheckBox {
    background-color: transparent;
    border: none;
    color: #ffffff;
    font-size: 14px;
    padding: 4px 0px;
}

BaseSettingWidget QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #555555;
    border-radius: 3px;
    background-color: #2d2d2d;
}

BaseSettingWidget QCheckBox::indicator:checked {
    background-color: #0078d4;
    border-color: #0078d4;
    image: url(:/icons/cil-check.png);
}

/* Spin boxes */
BaseSettingWidget QSpinBox {
    background-color: #2d2d2d;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 8px 12px;
    color: #ffffff;
    min-width: 80px;
}

BaseSettingWidget QSpinBox:hover {
    border-color: #666666;
}

BaseSettingWidget QSpinBox:focus {
    border-color: #0078d4;
}
```
</details>

- Adapt colors according to your application's graphic charter.
- Setting widgets support both light and dark themes.
- Input fields automatically adapt to the current theme.

---

### CLI
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#cli)

**Note:** The CLI component does not use QSS for styling as it's a command-line interface. It provides project management and utilities.

**Usage example:**
```bash
# Main CLI with help
ezqt --help

# Initialize a new project
ezqt init

# Convert translation files
ezqt convert
ezqt mkqm

# Run tests
ezqt test --unit --coverage

# Create project template
ezqt create --template advanced --name my_app
```

---



---

### Create QM Files
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#create-qm-files)

**Note:** The Create QM Files component does not use QSS for styling as it's a utility tool. It converts .ts files to .qm files for translations.

**Usage example:**
```bash
# Convert translation files via CLI
ezqt convert
ezqt mkqm

# The command will convert .ts files to .qm files
```

---

### ProjectRunner
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#projectrunner)

**Note:** The ProjectRunner component does not use QSS for styling as it's a utility class. It manages project creation and template generation.

**Usage example:**
```python
from ezqt_app.cli.runner import ProjectRunner

# Create project runner
runner = ProjectRunner(verbose=True)

# Get project information
info = runner.get_project_info()
print(f"Project status: {info['status']}")

# Create project template
success = runner.create_project_template("advanced", "my_app")
```

---

### Translation Helpers
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#translation-helpers)

**Note:** The Translation Helpers component does not use QSS for styling as it's a utility module. It provides helper functions for translations.

**Usage example:**
```python
from ezqt_app.kernel.translation_helpers import tr, set_tr

# Translate text
translated = tr("Hello World")

# Set translatable text for widget
from PySide6.QtWidgets import QLabel
label = QLabel("Hello World")
set_tr(label, "Hello World")
```

---

### Translation Config
[⬆️ Back to top](#summary) | [📖 Complete documentation](API_DOCUMENTATION.md#translation-config)

**Note:** The Translation Config component does not use QSS for styling as it's a configuration module. It manages translation settings and language mapping.

**Configuration example:**
```python
from ezqt_app.kernel.translation_config import get_language_mapping

# Get language mapping
mapping = get_language_mapping()
# Returns: {"English": "en", "Français": "fr", "Español": "es", "Deutsch": "de"}
```

---

## Theme Integration

### Light Theme Variables
```css
/* Light theme color variables */
:root {
    --main-bg: #ffffff;
    --main-surface: #f8f9fa;
    --main-border: #dee2e6;
    --accent-color1: #0078d4;
    --accent-color2: #106ebe;
    --accent-color3: #005a9e;
    --accent-color4: #004578;
    --base-text: #212529;
    --muted-text: #6c757d;
    --select-text: #ffffff;
}
```

### Dark Theme Variables
```css
/* Dark theme color variables */
:root {
    --main-bg: #2d2d2d;
    --main-surface: #3d3d3d;
    --main-border: #555555;
    --accent-color1: #0078d4;
    --accent-color2: #106ebe;
    --accent-color3: #005a9e;
    --accent-color4: #004578;
    --base-text: #ffffff;
    --muted-text: #cccccc;
    --select-text: #ffffff;
}
```

### Theme Switching
```python
# Theme switching is handled automatically by the framework
# The QSS styles automatically adapt to the current theme
window.setAppTheme()  # This triggers theme change
```

---

## Good Practices

[⬆️ Back to top](#summary)

- Use consistent colors and spacing across all components.
- Test appearance on different operating systems and Qt themes.
- Support both light and dark themes for better user experience.
- Use CSS variables for colors to facilitate theme switching.
- Document each QSS section in this file for maintainability.
- Test QSS styles with different font sizes and DPI settings. 