# API Documentation - EzQt_App

## Overview

This directory contains the complete API documentation for the EzQt_App framework. The documentation is organized in a modular way to facilitate navigation and usage.

## Documentation Structure

### 📋 Main Documentation
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete documentation of all components
  - Overview of all modules
  - Detailed documentation of each component
  - Parameters, properties, signals and examples
  - Usage guide and best practices

### 🎨 Style Guide
- **[STYLE_GUIDE.md](STYLE_GUIDE.md)** - Style guide and QSS customization
  - QSS styles for custom widgets
  - Theme customization
  - Color schemes and styling best practices
  - Integration with existing themes

### 🔧 Helper Functions
- **[HELPERS_GUIDE.md](HELPERS_GUIDE.md)** - Helper functions guide
  - Simplified API for common operations
  - Configuration management helpers
  - UI operation helpers
  - Translation helpers with automatic translation
  - Usage examples and best practices

## Quick Navigation

### 🧠 Core Components (`ezqt_app.kernel`)
- **Kernel Architecture** : Modular design with specialized packages
- **App Functions Package** : Asset, config, resource, and settings management
- **UI Functions Package** : Window, panel, menu, and theme management
- **Initialization Package** : Structured initialization sequence
- **Qt Configuration** : High DPI support and cross-platform configuration
- **Resource Definitions** : Image and icon resource definitions
- **Translation Package** : Complete internationalization system with automatic translation
- **Helper Functions** : Simplified API for common operations

### 🎨 Widget Components (`ezqt_app.widgets`)
- **EzApplication** : Extended QApplication with theme support
- **EzQt_App** : Main application window with modern UI
- **Core Widgets** : Header, Menu, PageContainer, SettingsPanel
- **Extended Widgets** : SettingWidgets with validation

### 🔧 Utility Components (`ezqt_app.cli`)
- **CLI** : Command line interface for project management
- **ProjectRunner** : Project creation and template management
- **Create QM Files** : Translation file conversion utilities

### 🌍 Translation System (`ezqt_app.kernel.translation`)
- **TranslationManager** : Complete translation management with .ts support
- **Auto-Translator** : Multi-provider automatic translation system
- **String Collector** : Automatic string collection for translations
- **Translation Helpers** : Utility functions for translations
- **Translation Config** : Language configuration and setup

## Usage

### 🔍 How to Navigate
1. **Start with** `API_DOCUMENTATION.md` for a complete overview
2. **Use** the table of contents to access components directly
3. **Consult** `STYLE_GUIDE.md` for QSS customization and theming

### 📚 Recommended Reading Order
- **Beginners** : Overview → Basic setup → Simple examples
- **Experienced users** : Specific component → Integration → Advanced features
- **Developers** : Complete documentation → Advanced examples → Style guide
- **Translation** : Translation system → Auto-translation → String collection

## Useful Links

### 📖 General Documentation
- **[../README.md](../README.md)** - Main documentation guide

### 🖥️ CLI Documentation
- **[../cli/README.md](../cli/README.md)** - Command-line interface guide

### 🧪 Tests and Examples
- **[../tests/](../tests/)** - Test documentation
- **[../../tests/](../../tests/)** - Unit and integration tests

### 🔗 External Resources
- **Source code** : `../../ezqt_app/` - Framework implementation
- **Examples** : `../../examples/` - Usage examples

---

**EzQt_App API Documentation** - Complete and consolidated guide for using the EzQt_App framework. 