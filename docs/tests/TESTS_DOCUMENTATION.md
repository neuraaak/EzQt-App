# Complete Test Documentation - EzQt_App

## Overview

This document presents all available tests for the EzQt_App framework, organized by functional modules. Each component has a complete test suite to ensure code quality and reliability.

## Table of Contents

- [🧠 Kernel Tests](#-kernel-tests)
  - [TranslationManager](#translationmanager)
  - [Settings](#settings)
  - [Helper.Maker](#helpermaker)
  - [AppFunctions](#appfunctions)
- [🎨 Widget Tests](#-widget-tests)
  - [Core Widgets](#core-widgets)
  - [Extended Widgets](#extended-widgets)
- [🔧 Utility Tests](#-utility-tests)
  - [CLI](#cli)
- [🔗 Integration Tests](#-integration-tests)
  - [AppFlow](#appflow)
  - [Translations](#translations)

## Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── unit/                          # Unit tests
│   ├── test_kernel/              # Kernel component tests
│   ├── test_utils/               # Utility tests
│   └── test_widgets/             # Widget tests
└── integration/                   # Integration tests
    ├── test_app_flow.py          # Application flow tests
    └── test_translations.py      # Translation system tests
```

## 🧠 Kernel Tests

### TranslationManager
**File :** `test_kernel/test_translation_manager.py`  
**Tests :** 25+ tests

Multilingual translation management system.

**Covered tests :**
- ✅ Initialization with default and custom languages
- ✅ Language loading by code and name
- ✅ Widget registration and unregistration
- ✅ Text translation and retranslation
- ✅ Language change signals
- ✅ Language mapping (name ↔ code)
- ✅ Error handling for invalid languages
- ✅ Singleton behavior and persistence

**Statistics :**
- **Tests :** 25+
- **Pass :** 25+
- **Skip :** 0
- **Coverage :** ~95%

### Settings
**File :** `test_kernel/test_app_settings.py`  
**Tests :** 15+ tests

Application configuration and settings management.

**Covered tests :**
- ✅ Application base settings
- ✅ Window dimensions and sizes
- ✅ Theme and interface parameters
- ✅ Data type validation
- ✅ Configuration constants

**Statistics :**
- **Tests :** 15+
- **Pass :** 15+
- **Skip :** 0
- **Coverage :** ~95%

### Helper.Maker
**File :** `test_kernel/test_helper_maker.py`  
**Tests :** 20+ tests

File and resource generation utility.

**Covered tests :**
- ✅ Directory and file creation
- ✅ Python file generation
- ✅ Resource management (QRC)
- ✅ File copying operations
- ✅ Error handling for creation failures

**Statistics :**
- **Tests :** 20+
- **Pass :** 20+
- **Skip :** 0
- **Coverage :** ~95%

### AppFunctions
**File :** `test_kernel/test_app_functions.py`  
**Tests :** 20+ tests

Application utility functions.

**Covered tests :**
- ✅ YAML configuration loading
- ✅ Configuration saving
- ✅ File path management
- ✅ Data validation
- ✅ Unicode support

**Statistics :**
- **Tests :** 20+
- **Pass :** 20+
- **Skip :** 0
- **Coverage :** ~95%

## 🎨 Widget Tests

### Core Widgets

#### EzApplication
**File :** `test_widgets/test_core/test_ez_app.py`  
**Tests :** 7 tests (with 7 skipped)

Main Qt application with specific configurations.

**Covered tests :**
- ✅ Basic inheritance and class definition
- ✅ Documentation of classes and methods
- ⏸️ Instance tests requiring QApplication (SKIP)
  - Locale configuration
  - Environment variables setup
  - High DPI scaling configuration
  - Application properties
  - Theme changed signal

**Statistics :**
- **Tests :** 7
- **Pass :** 0
- **Skip :** 7
- **Coverage :** ~30%

#### Header
**File :** `test_widgets/test_core/test_header.py`  
**Tests :** Multiple tests

Application header with control buttons.

**Covered tests :**
- ✅ Header creation with title and description
- ✅ Button management (settings, minimize, maximize, close)
- ✅ Horizontal and vertical layouts
- ✅ Fixed size properties
- ✅ Button signals

#### Menu
**File :** `test_widgets/test_core/test_menu.py`  
**Tests :** Multiple tests

Side menu with expand/collapse functionality.

**Covered tests :**
- ✅ Initialization with custom widths
- ✅ Collapsed/expanded menu state
- ✅ Toggle button functionality
- ✅ Menu button management
- ✅ Animations and transitions

#### PageContainer
**File :** `test_widgets/test_core/test_page_container.py`  
**Tests :** Multiple tests

Page container with navigation between pages.

**Covered tests :**
- ✅ Page addition and removal
- ✅ Navigation between pages
- ✅ Page dictionary management
- ✅ Layout with margins
- ✅ Stacked widget functionality

#### SettingsPanel
**File :** `test_widgets/test_core/test_settings_panel.py`  
**Tests :** Multiple tests

Settings panel with configurable widgets.

**Covered tests :**
- ✅ Panel creation with custom width
- ✅ Scroll area functionality
- ✅ Theme settings container
- ✅ Settings change signals
- ✅ YAML loading

### Extended Widgets

#### SettingWidgets
**File :** `test_widgets/test_extended/test_setting_widgets.py`  
**Tests :** Multiple tests

Specialized settings widgets.

**Covered tests :**
- ✅ BaseSettingWidget initialization
- ✅ Label and description management
- ✅ Parameter key handling
- ✅ Common base interface

## 🔧 Utility Tests

### CLI
**File :** `test_utils/test_cli.py`  
**Tests :** 6 tests

Command line interface and generation tools.

**Covered tests :**
- ✅ Main function execution
- ✅ Command line argument handling
- ✅ File generation from templates
- ✅ Error handling and exceptions
- ✅ User interaction (input/output)
- ✅ File path validation

**Statistics :**
- **Tests :** 6
- **Pass :** 6
- **Skip :** 0
- **Coverage :** ~95%

## 🔗 Integration Tests

### AppFlow
**File :** `integration/test_app_flow.py`  
**Tests :** 12 tests

Complete application workflow testing.

**Covered tests :**
- ✅ Complete application initialization
- ✅ Application with custom theme
- ✅ Window properties
- ✅ Menu functionality
- ✅ Header functionality
- ✅ Pages container
- ✅ Settings panel
- ✅ Signal connections
- ✅ Theme loading
- ✅ Window sizing
- ✅ Application cleanup
- ✅ Application without theme

**Statistics :**
- **Tests :** 12
- **Pass :** 12
- **Skip :** 0
- **Coverage :** ~90%

### Translations
**File :** `integration/test_translations.py`  
**Tests :** 15 tests

Integrated translation system testing.

**Covered tests :**
- ✅ Translation manager initialization
- ✅ Translation file loading
- ✅ Language switching
- ✅ Translation helpers
- ✅ Translation file loading workflow
- ✅ Translation error handling
- ✅ Translation manager singleton behavior
- ✅ Translation manager persistence
- ✅ Translation manager language mapping
- ✅ Translation manager available languages
- ✅ Translation manager current language
- ✅ Translation manager load language by code
- ✅ Translation manager load language by name
- ✅ Translation manager register widget
- ✅ Translation manager unregister widget

**Statistics :**
- **Tests :** 15
- **Pass :** 15
- **Skip :** 0
- **Coverage :** ~90%

## 🚀 Execution of Tests

### Installation of Dependencies

```bash
pip install -e ".[dev]"
```

### Quick Launch

```bash
# All tests
python tests/run_tests.py

# Only unit tests
python tests/run_tests.py --type unit

# Tests with coverage
python tests/run_tests.py --coverage

# Verbose mode
python tests/run_tests.py --verbose

# Exclude slow tests
python tests/run_tests.py --fast
```

### With pytest directly

```bash
# Unit tests
pytest -m unit

# Integration tests
pytest -m integration

# With coverage
pytest --cov=ezqt_app --cov-report=html

# Specific tests
pytest tests/unit/test_kernel/test_translation_manager.py
```

## 🧪 Types of Tests

### Unit Tests (`@pytest.mark.unit`)

- **Objective** : Test each component individually
- **Scope** : Functions, classes, methods
- **Isolation** : Use of mocks and fixtures
- **Speed** : Fast (< 1 second per test)

### Integration Tests (`@pytest.mark.integration`)

- **Objective** : Test interaction between components
- **Scope** : Complete application workflows
- **Isolation** : Complete application environment
- **Speed** : Slower (1-5 seconds per test)

### Slow Tests (`@pytest.mark.slow`)

- **Objective** : Tests requiring time (network, files)
- **Exclusion** : `pytest -m "not slow"`

## 🔧 Available Fixtures

### `qt_application`
Shared QApplication instance for all tests.

### `qt_widget_cleanup`
Automatically cleans up widgets after each test.

### `wait_for_signal`
Waits for a Qt signal to be emitted with a timeout.

### `tmp_path`
Temporary directory for file operations.

### `mock_yaml_config`
Temporary YAML configuration file.

## 📊 Code Coverage

Coverage is generated automatically with:
- Terminal report: `--cov-report=term-missing`
- HTML report: `--cov-report=html:htmlcov`
- XML report: `--cov-report=xml`

## 🎯 Best Practices

### 1. Test Naming
```python
def test_component_creation_default():
    """Test of creation with default parameters."""
    pass

def test_component_property_setter():
    """Test of property setter."""
    pass
```

### 2. Organization of Test Classes
```python
class TestComponentName:
    """Tests for the ComponentName class."""
    
    def test_method_name_scenario(self):
        """Test of the method in a specific scenario."""
        pass
```

### 3. Use of Fixtures
```python
def test_component_creation(self, qt_widget_cleanup, tmp_path):
    """Test with fixtures."""
    component = Component(path=tmp_path)
    assert component.path == tmp_path
```

### 4. Signal Tests
```python
def test_signal_emission(self, qt_widget_cleanup, wait_for_signal):
    """Test of signal emission."""
    widget = Widget()
    assert wait_for_signal(widget.someSignal)
```

## 🐛 Debugging

### Debug Mode
```bash
pytest --pdb
```

### Displaying Prints
```bash
pytest -s
```

### Specific Tests
```bash
pytest -k "test_translation_manager"
```

## 📈 Metrics

- **Target Coverage** : > 90%
- **Execution Time** : < 30 seconds for all tests
- **Reliability** : 0% flaky tests

## 🔄 Continuous Integration

Tests are automatically executed:
- On each commit
- Before each merge
- Before each release

## 📝 Adding New Tests

1. Create the test file in the correct directory
2. Follow the naming convention
3. Use appropriate fixtures
4. Add necessary markers
5. Check coverage

## 🚨 Common Issues

### QApplication already created
```python
# Use the qt_application fixture
def test_widget(qt_application):
    pass
```

### Tests failing randomly
- Add delays with `QTimer`
- Use `wait_for_signal`
- Check test isolation

### Memory leaks
- Use `qt_widget_cleanup`
- Explicitly delete widgets
- Check signal connections

## 📊 Global Statistics

| Category | Components | Tests | Coverage |
|-----------|------------|-------|------------|
| Kernel | 4 | 80+ | ~95% |
| Widgets | 5 | 20+ | ~80% |
| Utils | 1 | 6 | ~95% |
| Integration | 2 | 27 | ~90% |
| **Total** | **12** | **~133** | **~90%** |

---

**Documentation of EzQt_App Tests** - Complete guide for running and maintaining tests. 