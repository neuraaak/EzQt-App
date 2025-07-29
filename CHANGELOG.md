# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.3] - 2025-01-27

### 🌐 **Automatic Translation System**

| Feature | Description | Impact |
|---------|-------------|---------|
| **Auto-Translator Module** | New `auto_translator.py` module with multi-provider support | Advanced automatic translation |
| **String Collector** | New `string_collector.py` module for automatic string collection | Automatic translation management |
| **Translation Providers** | Support for LibreTranslate, MyMemory and Google Translate | Translation service flexibility |
| **Configuration Languages** | New `languages.yaml` file for language configuration | Centralized language management |
| **Translation Manager** | Enhanced translation manager with auto-translation | Seamless integration |

### 🔧 **Technical Improvements**

| Component | Change | Impact |
|-----------|--------|---------|
| **App Structure** | Complete reorganization of application structure | Better architecture |
| **Resource Management** | Enhanced resource and asset management | Optimized performance |
| **UI Functions** | Complete refactoring of UI functions with new features | More modern interface |
| **Configuration System** | New configuration system with YAML files | More flexible configuration |
| **CLI Tools** | Enhanced CLI tools for project creation | Better developer experience |

### 🧹 **Cleanup and Reorganization**

| Change | Description | Impact |
|--------|-------------|---------|
| **File Structure** | Reorganization of configuration files in `resources/config/` | Clearer structure |
| **Widgets Module** | Removal of `widgets.py` and reorganization into specialized modules | More modular code |
| **TODO Management** | Moving TODO files to `todo/` directory | Better organization |
| **Test Structure** | Updated test structure for new features | More comprehensive tests |

### 📝 **Documentation and Configuration**

| Documentation | Update | Impact |
|---------------|--------|---------|
| **Translation System** | Complete documentation of automatic translation system | User guide |
| **Configuration Files** | New configuration files for languages and palette | Advanced configuration |
| **Project Structure** | Updated project structure documentation | Up-to-date documentation |

### ⚠️ **Important Note**

The automatic translation system has been **temporarily disabled** to simplify development.
See `todo/TODO_TRANSLATION_DISABLED.md` for reactivation details.

---

## [4.0.2] - 2025-01-27

### 🔄 **Major Project Reorganization and Qt Configuration**

| Feature | Description | Impact |
|---------|-------------|---------|
| **Qt Configuration Module** | Added qt_config.py with comprehensive High DPI support and cross-platform configuration | Enhanced Qt compatibility |
| **Project Structure Cleanup** | Reorganized project structure by removing obsolete files from bin/ directory | Cleaner codebase |
| **Resource Management** | Removed modules/app_resources.py and consolidated resource management | Better resource handling |
| **Enhanced Configuration** | Significantly improved globals.py with enhanced configuration management (+245 lines) | More robust configuration |
| **File Management** | Enhanced file_maker.py with better file handling capabilities (+221 lines) | Improved file operations |

### 🧹 **Code Cleanup**

| Component | Change | Impact |
|-----------|--------|---------|
| **Test Files** | Removed deprecated test files (test_libretranslate.py, test_translation_apis.py) | Reduced test complexity |
| **Initialization** | Updated initialization sequence and startup configuration | Better startup process |
| **Translation System** | Improved translation manager and UI functions | Enhanced i18n support |
| **Project Configuration** | Cleaned up project configuration in pyproject.toml | Better packaging |

### 📝 **Documentation**

| Documentation | Update | Impact |
|---------------|--------|---------|
| **CHANGELOG.md** | Updated with latest changes | Better change tracking |

### 🧹 **Repository Management**

| Component | Change | Impact |
|-----------|--------|---------|
| **Git Exclusions** | Added exclusion of bin/ and modules/ directories in .gitignore | Cleaner repository |
| **Repository Cleanup** | Enhanced .gitignore configuration to exclude unnecessary directories | Reduced repository size |

---

## [4.0.1] - 2025-07-28

### 🔧 **Development Status Update**

| Change | Description | Impact |
|--------|-------------|---------|
| **Development Status** | Changed from "Alpha" to "Beta" in pyproject.toml | Project maturity milestone |

---

## [4.0.0] - 2025-07-28

### 🎨 **Standardized Logging System**

| Feature | Description | Impact |
|---------|-------------|---------|
| **Consistent Message Formatting** | All messages follow `[Subsystem] Message` pattern | Professional output |
| **Color-Coded Messages** | 6 message types with distinct colors (info, action, success, warning, error, init) | Visual clarity |
| **Subsystem Identification** | Clear identification with prefixes like `[TranslationManager]`, `[FileMaker]`, etc. | Easy debugging |
| **Verbose Mode** | Optional detailed output for development and debugging | Flexible logging |
| **Configuration Display** | ASCII art boxes for configuration data in verbose mode | Visual configuration |

### 🔧 **System Integration**

| Component | Change | Impact |
|-----------|--------|---------|
| **Printer Class** | New centralized logging system with 6 message types | Unified logging |
| **Initialization Sequence** | Standardized format with `[InitializationSequence]` prefix | Consistent output |
| **FileMaker** | Uses `[FileMaker]` prefix for file generation messages | Clear identification |
| **TranslationManager** | Uses `[TranslationManager]` prefix for translation messages | Consistent formatting |
| **SettingsManager** | Uses `[AppKernel]` prefix with configuration display | Professional output |
| **ThemeManager** | Uses `[ThemeManager]` prefix for theme-related messages | Standardized logging |

### 📚 **Documentation Updates**

| Documentation | Update | Impact |
|---------------|--------|---------|
| **API Documentation** | Added comprehensive logging system section | Complete reference |
| **LOGGING_SYSTEM.md** | New dedicated documentation file | Detailed guide |
| **README.md** | Updated to mention standardized logging | Feature visibility |
| **CHANGELOG.md** | Documented all logging improvements | Change tracking |

### 🎯 **Message Types and Colors**

| Type | Prefix | Color | Usage |
|------|--------|-------|-------|
| **Info** | `~` | White | General information messages |
| **Action** | `+` | Blue | Actions being performed |
| **Success** | `✓` | Green | Successful operations |
| **Warning** | `!` | Orange | Warning messages |
| **Error** | `✗` | Red | Error messages |
| **Init** | `🚀` | Magenta | Initialization messages |

### 📊 **Example Output**

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
~ [InitializationSequence] Starting EzQt_App Initialization Sequence
+ [InitializationSequence] [ 1/10] Configure Startup
✓ [InitializationSequence] Step completed successfully (0.00s)
```

### 🐛 **Bug Fixes**

| Issue | Fix | Impact |
|-------|-----|---------|
| **Inconsistent print() statements** | Replaced all non-standard print() with Printer system | Consistent output |
| **Missing subsystem identification** | Added subsystem prefixes to all messages | Clear message sources |
| **Verbose mode issues** | Fixed verbose mode handling in SettingsManager | Proper configuration display |

---

## [3.2.0] - 2025-07-27

### 🚀 **Major Framework Restructuring**

| Feature | Description | Impact |
|---------|-------------|---------|
| **Modular Architecture** | Complete reorganization of kernel modules into specialized packages | Better maintainability |
| **FileMaker Integration** | Replaced Helper.Maker with dedicated FileMaker class | Improved file management |
| **Resource Management** | Enhanced resource detection and loading system | Better performance |
| **Translation System** | Improved translation management with dedicated modules | Professional i18n |

### 🔧 **System Integration**

| Component | Change | Impact |
|-----------|--------|---------|
| **Kernel Structure** | Reorganized into `app_functions/`, `initialization/`, `resource_definitions/`, `translation/`, `ui_functions/` | Modular architecture |
| **FileMaker Class** | New dedicated class for file generation and management | Centralized file operations |
| **Resource Definitions** | Separated icons and images into dedicated modules | Better organization |
| **UI Functions** | Modularized UI management into specialized packages | Cleaner code structure |

### 📚 **Documentation Updates**

| Documentation | Update | Impact |
|---------------|--------|---------|
| **API Documentation** | Added comprehensive helpers guide and style guide | Complete reference |
| **Test Documentation** | Updated with new test structure and guidelines | Better testing practices |
| **README.md** | Enhanced with new features and structure | Improved user guidance |

### 🧪 **Testing Infrastructure**

| Component | Change | Impact |
|-----------|--------|---------|
| **Translation APIs** | Added comprehensive tests for translation APIs | Better reliability |
| **LibreTranslate Integration** | Added tests for LibreTranslate API integration | Enhanced testing coverage |
| **Test Structure** | Reorganized test files for better organization | Improved test management |

### 📦 **Dependencies**

| Dependency | Version | Purpose |
|------------|---------|---------|
| **Enhanced pyproject.toml** | Updated with new module structure | Modern packaging |
| **Test Dependencies** | Added comprehensive test requirements | Better testing |

---

## [3.1.0] - 2025-07-27

### 🚀 **CLI Modernization**

| Feature | Description | Impact |
|---------|-------------|---------|
| **Modern CLI Framework** | Migrated from simple scripts to Click-based CLI with `ezqt` command | Enhanced developer experience |
| **Unified Command Interface** | `ezqt init`, `ezqt convert`, `ezqt mkqm`, `ezqt test`, `ezqt docs`, `ezqt info`, `ezqt create` | Streamlined workflow |
| **Project Templates** | Basic and advanced project templates with `ezqt create --template <type> --name <name>` | Quick project setup |
| **Legacy Command Removal** | Removed `ezqt_init` and `ezqt_qm_convert` direct commands | Cleaner interface |

### 📚 **Documentation Restructuring**

| Component | Change | Impact |
|-----------|--------|---------|
| **API Documentation** | Created comprehensive `docs/api/` structure with `API_DOCUMENTATION.md` and `STYLE_GUIDE.md` | Better organization |
| **Test Documentation** | Consolidated test docs into `QUICK_START_TESTS.md` and `TESTS_DOCUMENTATION.md` | Reduced redundancy |
| **CLI Documentation** | New `docs/cli/README.md` with complete command reference | Professional CLI docs |
| **Translation System** | Integrated `TRANSLATION_SYSTEM.md` into API documentation | Unified documentation |

### 🏗️ **Project Structure Improvements**

| Change | Description | Benefits |
|--------|-------------|----------|
| **Utils → CLI Rename** | Renamed `ezqt_app/utils/` to `ezqt_app/cli/` | Better organization |
| **CLI Package Creation** | New `ezqt_app/cli/` package with `main.py` and `runner.py` | Modular architecture |
| **File Consolidation** | Moved `create_qm_files.py` to CLI package, removed unused `qmessage_logger.py` | Cleaner codebase |
| **Entry Points Update** | Updated `pyproject.toml` with new CLI entry points | Modern packaging |

### 🔧 **Technical Enhancements**

| Enhancement | Details | Impact |
|-------------|---------|---------|
| **Click Framework** | Added `click>=8.0.0` dependency for modern CLI | Professional CLI |
| **ProjectRunner Class** | New class for project management and template generation | Extensible architecture |
| **Template System** | Basic and advanced project templates | Quick development |
| **Error Handling** | Improved CLI error handling with verbose mode | Better debugging |

### 🐛 **Bug Fixes**

| Issue | Fix | Impact |
|-------|-----|---------|
| **Import Paths** | Fixed incorrect import paths in CLI modules | Proper functionality |
| **Entry Point Configuration** | Corrected `pyproject.toml` script definitions | Working CLI installation |
| **Documentation Links** | Updated all documentation links to reflect new structure | Consistent navigation |
| **Legacy Commands** | Removed deprecated CLI commands from package configuration | Clean installation |

### 📦 **Dependencies**

| Dependency | Version | Purpose |
|------------|---------|---------|
| **click** | `>=8.0.0` | Modern CLI framework |
| **Enhanced pyproject.toml** | Updated with new entry points | Professional packaging |

### 🎯 **Benefits**

| Benefit | Description |
|---------|-------------|
| **Developer Experience** | Single `ezqt` command for all operations |
| **Project Management** | Quick project creation with templates |
| **Documentation** | Professional, organized documentation structure |
| **Maintainability** | Cleaner, more modular codebase |

---

## [3.0.1] - 2025-07-27

### 🧪 **Test Infrastructure Stabilization**

| Component | Change | Impact |
|-----------|--------|---------|
| **EzApplication Tests** | Fixed QApplication singleton conflicts with proper test isolation | Stable test execution |
| **Test Documentation** | Updated unit test documentation with known issues section | Better transparency |
| **TODO Management** | Created comprehensive TODO.md for test improvements | Clear development roadmap |

### 🔧 **Technical Improvements**

| Improvement | Details | Benefits |
|-------------|---------|----------|
| **Test Isolation** | Implemented proper QApplication mocking strategies | Reliable test execution |
| **Error Handling** | Enhanced error handling for Qt component tests | Better debugging |
| **Documentation** | Added "Known Issues and TODO" section in test docs | Clear status reporting |

### 📊 **Test Statistics**

| Metric | Value | Status |
|--------|-------|--------|
| **Total Tests** | 214/221 passing | ✅ Stable |
| **Skipped Tests** | 7 tests (documented) | ✅ Managed |
| **Coverage** | Maintained across modules | ✅ Good |
| **Execution Time** | ~2.17s | ✅ Fast |

---

## [3.0.0] - 2025-07-27

### 🚀 **PySide6 6.9.1 Migration**

| Feature | Description | Impact |
|---------|-------------|---------|
| **Complete Migration** | Full migration to PySide6 6.9.1 with all new features | Latest Qt framework |
| **Type Annotations** | Complete type hint support with PySide6 6.9.1 improvements | Better code quality |
| **Windows ARM64** | Extended compatibility with new architectures | Broader platform support |
| **QMessageLogger** | Integrated logging system using PySide6 6.9.1 APIs | Enhanced debugging |

### 🔧 **Framework Enhancements**

| Enhancement | Details | Benefits |
|-------------|---------|----------|
| **Resource Management** | Improved resource detection and loading | Better performance |
| **Translation System** | Enhanced support for .ts and .qm files | Professional i18n |
| **User Interface** | UI experience improvements with new widgets | Better UX |
| **Code Structure** | Standardized code structure across all modules | Maintainability |

### 🐛 **Bug Fixes**

| Issue | Fix | Impact |
|-------|-----|---------|
| **QVariant Memory Leaks** | Fixed memory leaks related to QVariant usage | Better performance |
| **QtAsyncio Errors** | Improved asynchronous error handling | Enhanced stability |
| **Signal Connections** | Fixed crashes during signal connections | Reliable operation |
| **Circular Imports** | Resolved circular import issues with TYPE_CHECKING | Clean architecture |

### 📦 **Dependencies**

| Dependency | Version | Purpose |
|------------|---------|---------|
| **PySide6** | `6.9.1` | Modern Qt framework |
| **PyYaml** | `6.0.2` | YAML configuration |
| **colorama** | `0.4.6` | Terminal colors |
| **requests** | `2.32.3` | HTTP requests |
| **ezqt-widgets** | `>=2.0.0` | Custom widgets |

### 🎯 **Migration Benefits**

| Benefit | Description |
|---------|-------------|
| **Performance** | Improved performance with PySide6 6.9.1 optimizations |
| **Maintainability** | More maintainable code with complete type annotations |
| **Compatibility** | Extended support with Windows ARM64 |
| **Stability** | Enhanced stability with bug fixes |
| **Features** | Enriched features with new APIs |

---

## [2.3.3] - 2025-07-26

### 🔧 **Changed**
- Updated PySide6 from 6.7.3 to 6.9.1
- Stability and performance improvements
- Support for new typing features

### 🐛 **Fixed**
- Fixed memory leaks related to QVariant
- Improved QtAsyncio error handling
- Fixed crashes during signal connections

---

## [2.3.1] - 2025-07-26

### 🔧 **Changed**
- Version update and various improvements

---

## [2.3.0] - 2025-07-26

### 🚀 **Added**
- Bottom bar for user interface

---

## [2.2.1] - 2025-07-26

### 🚀 **Added**
- Global translation system with multi-language support
- Support for English, French, Spanish and German
- Simple translation API: `tr()`, `set_tr()`, `change_language()`
- Automatic widget retranslation when changing language

---

## [2.1.0] - 2025-07-26

### 🚀 **Added**
- Settings panel improvements
- New configuration features

---

## [2.0.5] - 2025-07-25

### 🚀 **Added**
- MenuButton widget with animation support
- Improved user experience

---

## [2.0.4] - 2025-07-24

### 🚀 **Added**
- Build/upload script to automate deployment process

### 🔧 **Changed**
- Excluded .bat file from package in MANIFEST.in

---

## [2.0.3] - 2025-07-24

### 🔧 **Changed**
- General version update to 2.0.3

---

## [2.0.2] - 2025-07-23

### 🔧 **Changed**
- Updated version in pyproject.toml and ezqt_app/__init__.py
- Improved project configuration

---

## [2.0.0] - 2025-07-23

### 🚀 **Added**
- Initial project files
- Complete configuration with .gitignore, LICENSE, MANIFEST.in, pyproject.toml
- Resources and icons for ezqt_app application
- Base structure of EzQt_App framework

### 🔧 **Changed**
- Updated pyproject.toml with initial configuration

---

## [1.0.0] - 2025-07-23

### 🚀 **Added**
- First project commit
- Base structure of EzQt_App framework
- PySide6 support for modern Qt applications
- Light/dark theme system
- Automatic resource management
- `ezqt_init` CLI for project initialization

---

## Change Types Reference

| Type | Description | Icon | Usage |
|------|-------------|------|-------|
| **🚀 Added** | New features | 🚀 | New functionality, features, capabilities |
| **🔧 Changed** | Changes in existing functionality | 🔧 | Modifications to existing features |
| **🐛 Fixed** | Bug fixes | 🐛 | Bug corrections and fixes |
| **🧹 Cleaned** | Removal of obsolete or unnecessary code | 🧹 | Code cleanup and removal |
| **📝 Documentation** | Documentation updates | 📝 | Documentation changes and improvements |
| **🔄 Refactored** | Code restructuring without functional changes | 🔄 | Code reorganization and refactoring |
| **📦 Updated** | Package and dependency updates | 📦 | Dependency and package updates |
| **🔧 Technical Improvements** | Optimizations and technical enhancements | 🔧 | Performance and technical improvements |
| **📋 Migration** | Migration instructions and notes | 📋 | Framework or system migrations |
| **🧪 Test Infrastructure** | Testing improvements and changes | 🧪 | Test-related changes |
| **🎨 UI/UX Improvements** | User interface and experience changes | 🎨 | Visual and interaction improvements |
| **📊 Performance** | Performance-related changes | 📊 | Speed and efficiency improvements |
| **🔒 Security** | Security-related changes | 🔒 | Security improvements and fixes |
| **🌐 Internationalization** | Multi-language and localization changes | 🌐 | Translation and i18n updates | 