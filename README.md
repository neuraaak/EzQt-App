# EzQt-App

## Description

EzQt-App is a Python framework designed to make it easy to create modern Qt applications, based on a template by Wanderson M. Pimenta. It automates resource management, generates all required files, and offers a fast project bootstrap experience with a CLI command.

## 🚀 New PySide6 6.9.1 Features

### QMessageLogger
The project now includes a utility to use PySide6 6.9.1's QMessageLogger:

```python
from ezqt_app.utils.qmessage_logger import QtLogger

logger = QtLogger("MyApp")
logger.info("Application started")
logger.debug("Debug mode enabled")
logger.warning("Warning: experimental feature")
```

### Type Annotations Improvements
- **Complete type annotations** for better maintainability
- **More robust code** with PySide6 6.9.1 improvements
- **Support for new APIs** and features
- **Better autocompletion** in IDEs

### Windows ARM64 Support
- **Extended compatibility** with new architectures
- **Improved performance** on ARM64 systems

## ✨ Main Features

- **Automatic generation** of asset folders and files (icons, images, themes, etc.)
- **Dynamic themes** (light/dark) with integrated toggle
- **CLI command `ezqt_init`** to quickly initialize a new project
- **Ready-to-use `main.py` example** generated automatically
- **Modular and extensible structure**
- **Global translation system** with multi-language support
- **Advanced resource manager** with automatic detection
- **Custom widgets** with animations and themes

## 📦 Installation

Install the module via pip (recommended):

```bash
pip install ezqt_app
```

Or locally:

```bash
git clone https://github.com/neuraaak/ezqt_app.git
cd ezqt_app
pip install .
```

## 🔧 Dependencies

Main dependencies are installed automatically:
- **PySide6==6.9.1** - Modern Qt framework
- **PyYaml==6.0.2** - YAML file management
- **colorama==0.4.6** - Terminal colors
- **requests==2.32.3** - HTTP requests
- **ezqt-widgets>=2.0.0** - Custom widgets

## 🚀 Project Initialization

After installation, initialize a new project in an empty folder with:

```bash
ezqt_init
```

This command creates the base structure, resource folders, and a sample `main.py` file.

## 💻 Minimal Usage Example

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

## 🌍 Translation System

The framework includes a complete translation system:

```python
from ezqt_app.kernel.translation_manager import get_translation_manager

# Get the translation manager
tm = get_translation_manager()

# Change language
tm.load_language("English")

# Translate text
translated = tm.translate("Hello World")
```

**Supported languages:** English, French, Spanish, German

## 📁 Generated Project Structure

```
my_project/
├── main.py                    # Application entry point
├── bin/                       # Project resources
│   ├── config/               # Configuration files
│   ├── fonts/                # Custom fonts
│   ├── icons/                # Application icons
│   ├── images/               # Images and graphics
│   ├── themes/               # QSS theme files
│   ├── modules/              # Custom modules
│   └── translations/         # Translation files (.ts, .qm)
└── _temp/                    # Temporary files (if migration)
```

## 🏗️ Project Structure

```
ezqt_app/
├── README.md                    # Main documentation
├── CHANGELOG.md                 # Version history
├── docs/                        # Technical documentation
│   ├── README.md               # Documentation overview
│   └── TRANSLATION_SYSTEM.md   # Translation system
├── tests/                       # Unit and integration tests
│   ├── README.md               # Test documentation
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── fixtures/               # Test data
├── ezqt_app/                   # Main source code
│   ├── kernel/                 # Kernel components
│   │   ├── translation_manager.py  # Translation manager
│   │   ├── app_functions.py        # Application functions
│   │   ├── ui_functions.py         # UI functions
│   │   └── ...                    # Other components
│   ├── widgets/                # Custom widgets
│   │   ├── core/               # Base widgets
│   │   ├── extended/           # Extended widgets
│   │   └── custom_grips/       # Resize widgets
│   ├── utils/                  # Utilities
│   │   ├── cli.py              # Command line interface
│   │   ├── qmessage_logger.py  # Logging system
│   │   └── create_qm_files.py  # .qm file creation
│   └── resources/              # Embedded resources
├── modules/                    # External modules
└── pyproject.toml             # Project configuration
```

## 🎨 Customization

### Themes
- Edit the theme in `bin/themes/main_theme.qss` or use the toggle in the interface
- Add your own icons/images in the corresponding folders

### Custom Widgets
The framework includes several ready-to-use widgets:

```python
from ezqt_app.widgets.core.menu import Menu
from ezqt_app.widgets.core.header import Header
from ezqt_app.widgets.extended.menu_button import MenuButton

# Create custom widgets
menu = Menu()
header = Header()
menu_button = MenuButton("My Button")
```

## 🔧 Included Utilities

### CLI Commands
- **`ezqt_init`** - Project initialization
- **`ezqt_qm_convert`** - Convert .ts files to .qm

### Advanced Logging
```python
from ezqt_app.utils.qmessage_logger import QtLogger

logger = QtLogger("MyApp")
logger.info("Application started")
logger.debug("Debug mode enabled")
logger.warning("Warning: experimental feature")
logger.error("Error detected")
```

## 🧪 Testing

The framework includes comprehensive automated tests:

```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# PySide6 migration tests
python _temp/tests/test_remaining_modules.py
```

## 📚 Documentation

- **README.md** - This file (overview)
- **docs/README.md** - Detailed technical documentation
- **docs/TRANSLATION_SYSTEM.md** - Translation system guide
- **CHANGELOG.md** - Complete version history

## 🤝 Contribution

Contributions are welcome! Submit your ideas, fixes, or extensions via issues or pull requests.

### Contribution Guide
1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License & Credits

**MIT License**

This project is inspired by the template of Wanderson M. Pimenta. See the LICENSE file for details.

## 🆕 Migration to PySide6 6.9.1

The project has been completely migrated to PySide6 6.9.1 with:

- ✅ **21/21 files** successfully migrated
- ✅ **No functional regressions**
- ✅ **Significant code quality improvements**
- ✅ **New PySide6 6.9.1 features** integrated
- ✅ **Complete documentation** created
- ✅ **Automated tools** for future migrations

### Migration Benefits
- **Improved performance** thanks to PySide6 6.9.1 optimizations
- **More maintainable code** with complete type annotations
- **Extended support** with Windows ARM64
- **Enhanced stability** with bug fixes
- **Enriched features** with new APIs

---

**EzQt-App 3.0.0** - Modern framework for Qt applications with PySide6 6.9.1 🚀
