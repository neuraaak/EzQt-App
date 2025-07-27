# Quick Start Tests - EzQt_App

## Quick Verification

### Essential Commands

```bash
# Quick verification
python tests/run_tests.py --type unit

# With coverage
python tests/run_tests.py --coverage

# Verbose mode
python tests/run_tests.py --verbose
```

### Direct pytest Execution

```bash
# Unit tests only
pytest -m unit

# With coverage
pytest --cov=ezqt_app --cov-report=html

# Specific test file
pytest tests/unit/test_kernel/test_translation_manager.py -v
```

## Expected Results

### Quick Verification
- **Status** : 🟢 All tests passing
- **Total** : ~68 tests
- **Coverage** : ~90%
- **Duration** : < 30 seconds

### Common Issues

#### QApplication Already Created
```python
# Use the qt_application fixture
def test_widget(qt_application):
    pass
```

#### Random Test Failures
- Add delays with `QTimer`
- Use `wait_for_signal`
- Check test isolation

#### Memory Leaks
- Use `qt_widget_cleanup`
- Delete widgets explicitly
- Check signal connections

## Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── run_tests.py                   # Test execution script
├── unit/                          # Unit tests
│   ├── test_kernel/              # Kernel component tests
│   ├── test_utils/               # Utility tests
│   └── test_widgets/             # Widget tests
└── integration/                   # Integration tests
    ├── test_app_flow.py          # Application flow tests
    └── test_translations.py      # Translation system tests
```

## Troubleshooting

### Installation Issues
```bash
# Install in development mode
pip install -e ".[dev]"

# Install test dependencies
pip install pytest pytest-qt pytest-cov
```

### Test Execution Issues
```bash
# Debug mode
pytest --pdb

# Show prints
pytest -s

# Specific test
pytest -k "test_translation_manager"
```

---

**Quick Start Tests** - Essential commands and troubleshooting for EzQt_App testing. 