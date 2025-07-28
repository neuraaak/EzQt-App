# Standardized Logging System - EzQt_App

## Overview

The EzQt_App framework implements a comprehensive standardized logging system that ensures consistent message formatting across all components. This system provides professional output with color-coded messages, subsystem identification, and optional verbose mode for debugging.

## Features

### **Consistent Formatting**
All messages follow the standardized pattern: `[Subsystem] Message`

### **Color Coding**
Different message types use distinct colors for easy identification:

| Type | Prefix | Color | Usage |
|------|--------|-------|-------|
| **Info** | `~` | White | General information messages |
| **Action** | `+` | Blue | Actions being performed |
| **Success** | `✓` | Green | Successful operations |
| **Warning** | `!` | Orange | Warning messages |
| **Error** | `✗` | Red | Error messages |
| **Init** | `🚀` | Magenta | Initialization messages |

### **Subsystem Identification**
Each message includes a subsystem prefix for clear identification:
- `[TranslationManager]` - Translation-related messages
- `[AppKernel]` - Application kernel messages
- `[FileMaker]` - File generation messages
- `[ThemeManager]` - Theme-related messages
- `[InitializationSequence]` - Initialization messages
- `[ConfigManager]` - Configuration messages

### **Verbose Mode**
Optional detailed output for debugging and development.

### **Configuration Display**
ASCII art boxes for displaying configuration data in verbose mode.

## Usage

### **Basic Usage**

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
```

### **Configuration Display**

```python
# Display configuration data in ASCII art box
config_data = {
    "name": "MyApplication",
    "description": "This is an example description",
    "theme": "dark",
    "app_width": 1280,
    "app_height": 720,
    "time_animation": 400
}

printer.config_display(config_data)
```

**Output:**
```
+ [AppKernel] Loaded Application settings.
   ┌───────────────────────────────────────────────┐
   |- name: MyApplication
   |- description: This is an example description
   |- theme: dark
   |- app_width: 1280
   |- app_height: 720
   |- time_animation: 400
   └───────────────────────────────────────────────┘
...
```

## Integration Examples

### **Translation Manager**

```python
# In translation/manager.py
def load_language_by_code(self, language_code: str) -> bool:
    # ... implementation ...
    if self._load_ts_file(ts_file_path):
        get_printer().info(f"[TranslationManager] Traductions chargées pour {language_info['name']}")
    else:
        get_printer().warning(f"Impossible de charger les traductions pour {language_info['name']}")
    
    self.current_language = language_code
    get_printer().info(f"[TranslationManager] Langue changée vers {language_info['name']}")
```

### **File Maker**

```python
# In app_functions/file_maker.py
def make_app_resources_module(self) -> None:
    # ... implementation ...
    self.printer.info("[FileMaker] Generated app_resources.py file. Ready for use.")
```

### **Settings Manager**

```python
# In app_functions/settings_manager.py
def load_app_settings(yaml_file: Optional[Path] = None) -> Dict[str, str]:
    # ... implementation ...
    printer = Printer(verbose=True)
    printer.config_display(app_data)
```

### **Initialization Sequence**

```python
# In initialization/sequence.py
def execute(self, verbose: bool = True) -> Dict[str, Any]:
    if verbose:
        self.printer.info("[InitializationSequence] Starting EzQt_App Initialization Sequence")
        self.printer.info(f"[InitializationSequence] Total steps: {len(self.steps)}")
    
    # ... implementation ...
    
    if verbose:
        self.printer.action(f"[InitializationSequence] [{i:2d}/{len(self.steps):2d}] {step.name}")
        self.printer.success(f"[InitializationSequence] Step completed successfully ({step.duration:.2f}s)")
```

## Initialization Sequence Output

The initialization sequence provides a comprehensive example of the standardized logging system:

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
~ [FileMaker] Generated QRC file from bin folder content.
⚠️ QRC compilation skipped: PySide6 not available or compilation failed
~ [FileMaker] Generated app_resources.py file. Ready for use.
✓ [InitializationSequence] Step completed successfully (0.21s)
~
+ [InitializationSequence] [ 3/10] Generate Files
~     Generate required configuration and resource files
~ [FileMaker] Generated YAML config file.
~ [FileMaker] Generated QSS theme files.
~ [FileMaker] Generated translation files.
✓ [InitializationSequence] Step completed successfully (0.01s)
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

## Best Practices

### **1. Use Appropriate Message Types**
- Use `info()` for general information
- Use `action()` for actions being performed
- Use `success()` for successful operations
- Use `warning()` for warnings
- Use `error()` for errors

### **2. Include Subsystem Prefix**
Always include the subsystem prefix in square brackets:
```python
# Good
printer.info("[TranslationManager] Language changed to English")

# Avoid
printer.info("Language changed to English")
```

### **3. Be Descriptive**
Provide clear, descriptive messages:
```python
# Good
printer.success("[FileMaker] Generated app_resources.py file with 15 images and 8 icons")

# Avoid
printer.success("[FileMaker] Done")
```

### **4. Use Verbose Mode Appropriately**
- Use `verbose=True` for development and debugging
- Use `verbose=False` for production environments
- Configuration display only shows in verbose mode

### **5. Consistent Subsystem Names**
Use consistent subsystem names across the framework:
- `[TranslationManager]` for translation operations
- `[FileMaker]` for file generation
- `[AppKernel]` for application kernel operations
- `[ThemeManager]` for theme operations
- `[InitializationSequence]` for initialization steps
- `[ConfigManager]` for configuration operations

## Migration Guide

### **From print() Statements**

**Before:**
```python
print("Loading configuration...")
print("Configuration loaded successfully")
print("Error: Could not load configuration")
```

**After:**
```python
from ezqt_app.kernel.app_functions.printer import get_printer

printer = get_printer()
printer.info("[ConfigManager] Loading configuration...")
printer.success("[ConfigManager] Configuration loaded successfully")
printer.error("[ConfigManager] Could not load configuration")
```

### **From Custom Logging**

**Before:**
```python
logger.info("File generated successfully")
logger.warning("Theme file not found")
```

**After:**
```python
from ezqt_app.kernel.app_functions.printer import get_printer

printer = get_printer()
printer.success("[FileMaker] File generated successfully")
printer.warning("[ThemeManager] Theme file not found")
```

## Troubleshooting

### **Messages Not Displaying**
- Check if verbose mode is enabled: `get_printer(verbose=True)`
- Ensure the printer instance is created correctly
- Verify that the message type is appropriate

### **Colors Not Showing**
- Ensure colorama is installed: `pip install colorama`
- Check if the terminal supports color output
- Verify that the color constants are imported correctly

### **Inconsistent Formatting**
- Always use the standardized `[Subsystem] Message` format
- Use appropriate message types (info, action, success, warning, error)
- Include subsystem prefixes consistently

## Conclusion

The standardized logging system in EzQt_App provides a professional, consistent, and user-friendly way to display application messages. By following the established patterns and best practices, developers can ensure that their applications provide clear, informative, and visually appealing output to users. 