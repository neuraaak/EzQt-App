# EzQt-App

## Description

EzQt-App is a Python framework designed to make it easy to create modern Qt applications, based on a template by Wanderson M. Pimenta. It automates resource management, generates all required files, and offers a fast project bootstrap experience with a CLI command.

## Features

- Automatic generation of asset folders and files (icons, images, themes, etc.)
- Dynamic themes (light/dark) with integrated toggle
- CLI command `ezqt_init` to quickly initialize a new project
- Ready-to-use `main.py` example generated automatically
- Modular and extensible structure

## Installation

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

## Dependencies

Main dependencies are installed automatically:
- PySide6
- PyYaml
- colorama

## Project Initialization

After installation, initialize a new project in an empty folder with:

```bash
ezqt_init
```

This command creates the base structure, resource folders, and a sample `main.py` file.

## Minimal Usage Example

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

## Generated Project Structure

```
my_project/
  main.py
  bin/
    config/
    fonts/
    icons/
    images/
    themes/
    modules/
```

## Project Structure

```
ezqt_app/
├── README.md                    # Documentation principale
├── docs/                        # Documentation technique
│   ├── README.md               # Vue d'ensemble de la documentation
│   └── TRANSLATION_SYSTEM.md   # Système de traduction
├── tests/                       # Tests unitaires et d'intégration
│   ├── README.md               # Documentation des tests
│   ├── unit/                   # Tests unitaires
│   ├── integration/            # Tests d'intégration
│   └── fixtures/               # Données de test
├── ezqt_app/                   # Code source principal
├── modules/                    # Modules externes
└── pyproject.toml             # Configuration du projet
```

## Customization

- Edit the theme in `bin/themes/main_theme.qss` or use the toggle in the UI.
- Add your own icons/images in the corresponding folders.

## FAQ

- **main.py already exists?**: The CLI will ask for confirmation before overwriting.
- **pyside6-rcc error?**: Make sure PySide6 is installed and available in your PATH.

## Contribution

Contributions are welcome! Submit your ideas, fixes, or extensions via issues or pull requests.

## License & Credits

MIT License

This project is inspired by the template of Wanderson M. Pimenta. See the LICENSE file for details.
