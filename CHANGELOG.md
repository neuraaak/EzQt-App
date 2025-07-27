# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/lang/en/).

## [3.0.0] - 2025-07-27

### Added
- **Complete migration to PySide6 6.9.1** with support for new features
- **QMessageLogger** - New integrated logging system using PySide6 6.9.1 APIs
- **Windows ARM64 support** - Compatibility with new architectures
- **Complete type annotations** - Improved code maintainability
- **Automated migration scripts** - Tools for future updates
- **Automated tests** - Complete migration validation
- **Complete documentation** - Detailed guides and migration reports

### Changed
- **Standardized code structure** - Uniform comment format across all modules
- **Import organization** - Optimization and specification of PySide6 imports
- **Enhanced translation system** - Support for .ts and .qm files with direct parsing
- **Resource management** - Improved resource detection and loading
- **User interface** - UI experience improvements with new widgets

### Fixed
- **QVariant memory leaks** - Fixed memory leaks related to QVariant
- **QtAsyncio error handling** - Improved asynchronous error handling
- **Signal connection crashes** - Fixed crashes during signal connections
- **Circular imports** - Resolved circular import issues with TYPE_CHECKING
- **Type compatibility** - Fixed type annotations for better robustness

### Security
- **Dependency updates** - Updated to latest and most secure versions

## [2.3.3] - 2025-07-27

### Changed
- Updated PySide6 from 6.7.3 to 6.9.1
- Stability and performance improvements
- Support for new typing features

### Fixed
- Fixed memory leaks related to QVariant
- Improved QtAsyncio error handling
- Fixed crashes during signal connections

## [2.3.1] - 2025-07-27

### Changed
- Version update and various improvements

## [2.3.0] - 2025-07-26

### Added
- Bottom bar for user interface

## [2.2.1] - 2025-07-26

### Added
- Global translation system with multi-language support
- Support for English, French, Spanish and German
- Simple translation API: `tr()`, `set_tr()`, `change_language()`
- Automatic widget retranslation when changing language

## [2.1.0] - 2025-07-26

### Added
- Settings panel improvements
- New configuration features

## [2.0.5] - 2025-07-25

### Added
- MenuButton widget with animation support
- Improved user experience

## [2.0.4] - 2025-07-24

### Added
- Build/upload script to automate deployment process

### Changed
- Excluded .bat file from package in MANIFEST.in

## [2.0.3] - 2025-07-24

### Changed
- General version update to 2.0.3

## [2.0.2] - 2025-07-23

### Changed
- Updated version in pyproject.toml and ezqt_app/__init__.py
- Improved project configuration

## [2.0.0] - 2025-07-23

### Added
- Initial project files
- Complete configuration with .gitignore, LICENSE, MANIFEST.in, pyproject.toml
- Resources and icons for ezqt_app application
- Base structure of EzQt_App framework

### Changed
- Updated pyproject.toml with initial configuration

## [1.0.0] - 2025-07-23

### Added
- First project commit
- Base structure of EzQt_App framework
- PySide6 support for modern Qt applications
- Light/dark theme system
- Automatic resource management
- `ezqt_init` CLI for project initialization

---

## Types of changes

- **Added** : for new features
- **Changed** : for changes in existing functionality
- **Deprecated** : for features that will be removed soon
- **Removed** : for removed features
- **Fixed** : for bug fixes
- **Security** : in case of vulnerabilities fixed 