# Helpers Guide - EzQt_App

## Overview

This guide presents the helper functions available in EzQt_App, designed to simplify common operations and provide a more intuitive API for developers.

## Table of Contents

- [🔧 App Functions Helpers](#-app-functions-helpers)
- [🎨 UI Functions Helpers](#-ui-functions-helpers)
- [🌍 Translation Helpers](#-translation-helpers)
- [📋 Usage Examples](#-usage-examples)
- [🎯 Best Practices](#-best-practices)

## 🔧 App Functions Helpers

### Configuration Helpers

#### `load_config_section(section: str) -> Dict[str, Any]`
Load a configuration section from YAML.

```python
from ezqt_app.kernel import load_config_section

# Load settings panel configuration
config = load_config_section("settings_panel")
theme_config = config.get("theme", {})
```

#### `save_config_section(section: str, data: Dict[str, Any]) -> bool`
Save a configuration section to YAML.

```python
from ezqt_app.kernel import save_config_section

# Save theme configuration
success = save_config_section("settings_panel", {
    "theme": {"default": "dark"}
})
```

#### `get_setting(section: str, key: str, default: Any = None) -> Any`
Get a configuration setting with fallback value.

```python
from ezqt_app.kernel import get_setting

# Get theme with fallback
theme = get_setting("settings_panel", "theme.default", "dark")

# Get window width with fallback
width = get_setting("ui", "window.width", 800)
```

#### `set_setting(section: str, key: str, value: Any) -> bool`
Set a configuration setting.

```python
from ezqt_app.kernel import set_setting

# Set theme
success = set_setting("settings_panel", "theme.default", "light")

# Set window width
success = set_setting("ui", "window.width", 1024)
```

### Resource Helpers

#### `load_fonts() -> bool`
Load system fonts.

```python
from ezqt_app.kernel import load_fonts

success = load_fonts()
if success:
    print("Fonts loaded successfully")
```

#### `verify_assets() -> Dict[str, bool]`
Verify asset integrity.

```python
from ezqt_app.kernel import verify_assets

status = verify_assets()
if status.get("fonts", False):
    print("Fonts OK")
```

#### `get_resource_path(resource_type: str, name: str) -> Optional[Path]`
Get the path of a resource.

```python
from ezqt_app.kernel import get_resource_path

# Get font path
font_path = get_resource_path("fonts", "Segoe UI.ttf")

# Get icon path
icon_path = get_resource_path("icons", "cil-home.png")
```

### Application Helpers

#### `get_kernel_instance() -> Kernel`
Get a kernel instance.

```python
from ezqt_app.kernel import get_kernel_instance

kernel = get_kernel_instance()
config = kernel.loadKernelConfig("app")
```

#### `is_development_mode() -> bool`
Check if application is in development mode.

```python
from ezqt_app.kernel import is_development_mode

if is_development_mode():
    print("Debug mode enabled")
```

#### `get_app_version() -> str`
Get application version.

```python
from ezqt_app.kernel import get_app_version

version = get_app_version()
print(f"Version: {version}")
```

#### `get_app_name() -> str`
Get application name.

```python
from ezqt_app.kernel import get_app_name

name = get_app_name()
print(f"Application: {name}")
```

## 🎨 UI Functions Helpers

### Window Helpers

#### `maximize_window(window: QMainWindow) -> bool`
Maximize the main window.

```python
from ezqt_app.kernel import maximize_window

success = maximize_window(main_window)
```

#### `restore_window(window: QMainWindow) -> bool`
Restore the main window.

```python
from ezqt_app.kernel import restore_window

success = restore_window(main_window)
```

#### `toggle_window_state(window: QMainWindow) -> bool`
Toggle window state (maximized/restored).

```python
from ezqt_app.kernel import toggle_window_state

success = toggle_window_state(main_window)
```

#### `is_window_maximized(window: QMainWindow) -> bool`
Check if window is maximized.

```python
from ezqt_app.kernel import is_window_maximized

if is_window_maximized(main_window):
    restore_window(main_window)
```

#### `get_window_status(window: QMainWindow) -> str`
Get window status.

```python
from ezqt_app.kernel import get_window_status

status = get_window_status(main_window)
print(f"Status: {status}")
```

### Theme Helpers

#### `load_theme(theme_name: str) -> Optional[str]`
Load a QSS theme from resources.

```python
from ezqt_app.kernel import load_theme

theme_content = load_theme("dark_theme")
if theme_content:
    apply_theme(widget, theme_content)
```

#### `apply_theme(widget: QWidget, theme_content: str) -> bool`
Apply a QSS theme to a widget.

```python
from ezqt_app.kernel import apply_theme

success = apply_theme(widget, theme_content)
```

#### `apply_default_theme(widget: QWidget) -> bool`
Apply the default theme to a widget.

```python
from ezqt_app.kernel import apply_default_theme

success = apply_default_theme(widget)
```

### Animation Helpers

#### `animate_panel(panel: QFrame, direction: str = "left", duration: int = 300) -> bool`
Animate a panel (menu or settings).

```python
from ezqt_app.kernel import animate_panel

# Animate left menu
success = animate_panel(menu_panel, "left", 500)

# Animate right panel
success = animate_panel(settings_panel, "right", 300)
```

### Menu Helpers

#### `select_menu_item(button: QWidget, enable: bool = True) -> bool`
Select a menu item.

```python
from ezqt_app.kernel import select_menu_item

success = select_menu_item(menu_button, True)
```

#### `refresh_menu_style() -> bool`
Refresh menu style.

```python
from ezqt_app.kernel import refresh_menu_style

success = refresh_menu_style()
```

### Setup Helpers

#### `setup_custom_grips(window: QMainWindow) -> bool`
Setup custom grips for a window.

```python
from ezqt_app.kernel import setup_custom_grips

success = setup_custom_grips(main_window)
```

#### `connect_window_events(window: QMainWindow) -> bool`
Connect window events.

```python
from ezqt_app.kernel import connect_window_events

success = connect_window_events(main_window)
```

#### `setup_window_title_bar(window: QMainWindow, title_bar: QWidget) -> bool`
Setup custom title bar.

```python
from ezqt_app.kernel import setup_window_title_bar

success = setup_window_title_bar(main_window, title_bar)
```

## 🌍 Translation Helpers

### Core Translation

#### `tr(text: str) -> str`
Translate text.

```python
from ezqt_app.kernel import tr

translated = tr("Hello")
```

#### `set_tr(widget: Any, text: str) -> None`
Set translatable text on a widget.

```python
from ezqt_app.kernel import set_tr

set_tr(label, "Welcome")
```

#### `register_tr(widget: Any, text: str) -> None`
Register a widget for translation.

```python
from ezqt_app.kernel import register_tr

register_tr(button, "Click me")
```

#### `unregister_tr(widget: Any) -> None`
Unregister a widget from translation.

```python
from ezqt_app.kernel import unregister_tr

unregister_tr(button)
```

### Language Management

#### `change_language(language_name: str) -> bool`
Change application language.

```python
from ezqt_app.kernel import change_language

success = change_language("Français")
```

#### `get_available_languages() -> List[str]`
Get available languages.

```python
from ezqt_app.kernel import get_available_languages

languages = get_available_languages()
print(f"Available: {languages}")
```

#### `get_current_language() -> str`
Get current language.

```python
from ezqt_app.kernel import get_current_language

current = get_current_language()
print(f"Current: {current}")
```

## 📋 Usage Examples

### Complete Application Setup

```python
from ezqt_app.kernel import (
    get_app_name, get_app_version, is_development_mode,
    get_setting, set_setting, load_fonts, verify_assets,
    setup_custom_grips, connect_window_events
)

# Application information
app_name = get_app_name()
app_version = get_app_version()
dev_mode = is_development_mode()

print(f"Application: {app_name} v{app_version}")
if dev_mode:
    print("Development mode enabled")

# Configuration
theme = get_setting("app", "theme", "dark")
set_setting("ui", "window.width", 1200)

# Resources
load_fonts()
assets_status = verify_assets()

# Window setup
setup_custom_grips(main_window)
connect_window_events(main_window)
```

### Theme Management

```python
from ezqt_app.kernel import load_theme, apply_theme, get_setting

# Load and apply theme
theme_name = get_setting("app", "theme", "dark")
theme_content = load_theme(f"{theme_name}_theme")

if theme_content:
    apply_theme(main_window, theme_content)
```

### Translation Workflow

```python
from ezqt_app.kernel import tr, change_language, get_current_language

# Setup translation
change_language("Français")

# Use translation
welcome_text = tr("Welcome to EzQt_App")
print(welcome_text)

# Check current language
current_lang = get_current_language()
print(f"Current language: {current_lang}")
```

### Window Management

```python
from ezqt_app.kernel import (
    maximize_window, restore_window, toggle_window_state,
    is_window_maximized
)

# Window operations
if is_window_maximized(main_window):
    restore_window(main_window)
else:
    maximize_window(main_window)

# Or simply toggle
toggle_window_state(main_window)
```

## 🎯 Best Practices

### 1. Error Handling
Always check return values for error handling:

```python
from ezqt_app.kernel import set_setting, load_fonts

# Good practice
success = set_setting("app", "theme", "light")
if not success:
    print("Failed to save setting")

fonts_loaded = load_fonts()
if not fonts_loaded:
    print("Failed to load fonts")
```

### 2. Configuration Management
Use dot notation for nested settings:

```python
from ezqt_app.kernel import get_setting, set_setting

# Nested configuration
theme = get_setting("settings_panel", "theme.default", "dark")
set_setting("ui", "window.width", 1024)
```

### 3. Resource Management
Verify resources before using them:

```python
from ezqt_app.kernel import verify_assets, get_resource_path

# Check assets
status = verify_assets()
if status.get("fonts", False):
    font_path = get_resource_path("fonts", "Segoe UI.ttf")
    if font_path:
        # Use font
        pass
```

### 4. Translation Setup
Register widgets early for automatic retranslation:

```python
from ezqt_app.kernel import set_tr, change_language

# Setup translatable widgets
set_tr(welcome_label, "Welcome")
set_tr(settings_button, "Settings")

# Change language (widgets will be retranslated automatically)
change_language("Français")
```

### 5. Performance Considerations
- Use helper functions for common operations
- Cache configuration values when possible
- Load resources only when needed
- Use appropriate error handling

## 🔗 Related Documentation

- [API Documentation](API_DOCUMENTATION.md) - Complete API reference
- [Style Guide](STYLE_GUIDE.md) - QSS customization guide
- [Test Documentation](../tests/TESTS_DOCUMENTATION.md) - Testing guidelines 