# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.1] - 2025-01-27

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

## [3.1.0] - 2025-01-27

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

## [3.0.1] - 2025-01-27

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

## [3.0.0] - 2025-01-27

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

## [2.3.3] - 2025-01-26

### 🔧 **Changed**
- Updated PySide6 from 6.7.3 to 6.9.1
- Stability and performance improvements
- Support for new typing features

### 🐛 **Fixed**
- Fixed memory leaks related to QVariant
- Improved QtAsyncio error handling
- Fixed crashes during signal connections

---

## [2.3.1] - 2025-01-26

### 🔧 **Changed**
- Version update and various improvements

---

## [2.3.0] - 2025-01-26

### 🚀 **Added**
- Bottom bar for user interface

---

## [2.2.1] - 2025-01-26

### 🚀 **Added**
- Global translation system with multi-language support
- Support for English, French, Spanish and German
- Simple translation API: `tr()`, `set_tr()`, `change_language()`
- Automatic widget retranslation when changing language

---

## [2.1.0] - 2025-01-26

### 🚀 **Added**
- Settings panel improvements
- New configuration features

---

## [2.0.5] - 2025-01-25

### 🚀 **Added**
- MenuButton widget with animation support
- Improved user experience

---

## [2.0.4] - 2025-01-24

### 🚀 **Added**
- Build/upload script to automate deployment process

### 🔧 **Changed**
- Excluded .bat file from package in MANIFEST.in

---

## [2.0.3] - 2025-01-24

### 🔧 **Changed**
- General version update to 2.0.3

---

## [2.0.2] - 2025-01-23

### 🔧 **Changed**
- Updated version in pyproject.toml and ezqt_app/__init__.py
- Improved project configuration

---

## [2.0.0] - 2025-01-23

### 🚀 **Added**
- Initial project files
- Complete configuration with .gitignore, LICENSE, MANIFEST.in, pyproject.toml
- Resources and icons for ezqt_app application
- Base structure of EzQt_App framework

### 🔧 **Changed**
- Updated pyproject.toml with initial configuration

---

## [1.0.0] - 2025-01-23

### 🚀 **Added**
- First project commit
- Base structure of EzQt_App framework
- PySide6 support for modern Qt applications
- Light/dark theme system
- Automatic resource management
- `ezqt_init` CLI for project initialization

---

## Change Types

| Type | Description | Icon |
|------|-------------|------|
| **🚀 Added** | New features | 🚀 |
| **🔧 Changed** | Changes in existing functionality | 🔧 |
| **🐛 Fixed** | Bug fixes | 🐛 |
| **🧹 Cleaned** | Removal of obsolete or unnecessary code | 🧹 |
| **📝 Documentation** | Documentation updates | 📝 |
| **🔄 Refactored** | Code restructuring without functional changes | 🔄 |
| **📦 Updated** | Package and dependency updates | 📦 |
| **🔧 Technical Improvements** | Optimizations and technical enhancements | 🔧 |
| **📋 Migration** | Migration instructions and notes | 📋 | 