# EzQt_App CLI

Command-line interface for managing EzQt_App projects and framework utilities.

## 🚀 Quick Start

### Installation
```bash
# Install EzQt_App
pip install ezqt_app

# Verify installation
ezqt --version
```

### Basic Usage
```bash
# Initialize a new project
ezqt init

# Create project template
ezqt create --template basic --name my_app

# Convert translation files
ezqt mkqm

# Show package information
ezqt info
```

## 📋 Available Commands

### `ezqt init` - Initialize Project

Initialize a new EzQt_App project in the current directory.

#### Options
| Option | Short | Description |
|--------|-------|-------------|
| `--force` | `-f` | Force overwrite of existing files |
| `--verbose` | `-v` | Verbose output with detailed information |
| `--no-main` | | Skip main.py generation |

#### Examples
```bash
# Basic initialization
ezqt init

# Force overwrite existing files
ezqt init --force

# Verbose output
ezqt init --verbose

# Skip main.py generation
ezqt init --no-main
```

### `ezqt create` - Create Project Template

Create a new project with predefined templates.

#### Options
| Option | Short | Description |
|--------|-------|-------------|
| `--template` | `-t` | Template type (basic, advanced) |
| `--name` | `-n` | Project name |
| `--verbose` | `-v` | Verbose output |

#### Examples
```bash
# Create basic template
ezqt create --template basic --name my_app

# Create advanced template
ezqt create --template advanced --name my_project --verbose

# Interactive creation
ezqt create
```

### `ezqt mkqm` / `ezqt convert` - Convert Translation Files

Convert .ts files to .qm format for Qt applications.

#### Options
| Option | Short | Description |
|--------|-------|-------------|
| `--verbose` | `-v` | Verbose output |

#### Examples
```bash
# Convert translation files
ezqt mkqm

# Convert with verbose output
ezqt convert --verbose

# Both commands are equivalent
ezqt mkqm
ezqt convert
```

### `ezqt test` - Run Tests

Execute the test suite for EzQt_App framework.

#### Options
| Option | Short | Description |
|--------|-------|-------------|
| `--unit` | `-u` | Run unit tests |
| `--integration` | `-i` | Run integration tests |
| `--coverage` | `-c` | Run tests with coverage |
| `--verbose` | `-v` | Verbose output |

#### Examples
```bash
# Run unit tests
ezqt test --unit

# Run tests with coverage
ezqt test --coverage

# Run all tests with verbose output
ezqt test --unit --integration --coverage --verbose
```

### `ezqt docs` - Documentation Utilities

Access and manage EzQt_App documentation.

#### Options
| Option | Short | Description |
|--------|-------|-------------|
| `--serve` | `-s` | Serve documentation locally |
| `--port` | `-p` | Specify port (default: 8000) |

#### Examples
```bash
# Serve documentation on default port
ezqt docs --serve

# Serve documentation on custom port
ezqt docs --serve --port 8080

# Show documentation options
ezqt docs
```

### `ezqt info` - Package Information

Display information about EzQt_App installation and environment.

```bash
ezqt info
```

**Output:**
```
🚀 EzQt_App Information
========================================
Version: 3.1.0
Location: /path/to/ezqt_app/__init__.py
PySide6: 6.9.1
PyYaml: Available
Colorama: Available
Project structure: initialized
========================================
```

## 🎯 Use Cases

### For New Projects
```bash
# 1. Create new project
ezqt create --template basic --name my_app

# 2. Navigate to project
cd my_app

# 3. Initialize assets
ezqt init

# 4. Convert translations
ezqt mkqm

# 5. Run tests
ezqt test --unit
```

### For Development
```bash
# Quick project setup
ezqt init --verbose

# Test framework functionality
ezqt test --coverage

# Check environment
ezqt info
```

### For Documentation
```bash
# Serve documentation locally
ezqt docs --serve --port 8080

# Open browser to http://localhost:8080
```

## 🔧 Configuration

### Environment Variables
- `EZQT_VERBOSE` - Enable verbose mode by default
- `EZQT_PROJECT_ROOT` - Custom project root directory

### Project Structure
The CLI automatically detects and manages:
- `assets/` - Application assets (icons, images, themes)
- `base_resources.qrc` - Qt resource file
- `base_resources_rc.py` - Python resource module
- `app_resources.py` - Application resources
- `main.py` - Application entry point (optional)

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Command not found** | Install EzQt_App: `pip install ezqt_app` |
| **Permission errors** | Use `--force` flag or check file permissions |
| **Import errors** | Verify dependencies: `pip install PySide6 PyYaml` |
| **Template not found** | Check template name: `basic` or `advanced` |

### Debug Mode
```bash
# Enable verbose output
ezqt init --verbose

# Check package installation
ezqt info

# Test conversion
ezqt mkqm --verbose
```

## 📚 Integration

### With Development Workflow
```bash
# 1. Install EzQt_App
pip install ezqt_app

# 2. Create new project
ezqt create --template advanced --name my_project

# 3. Initialize project
cd my_project && ezqt init

# 4. Run tests
ezqt test --coverage

# 5. Serve documentation
ezqt docs --serve
```

### With CI/CD
```bash
# In CI pipeline
pip install ezqt_app
ezqt test --unit --coverage
```

## 🎨 Template System

### Available Templates

#### Basic Template
- Simple EzQt_App project structure
- Basic main.py with minimal setup
- Standard theme file
- README with usage instructions

**Structure:**
```
my_app/
├── main.py              # Application entry point
├── assets/              # Application assets
│   ├── icons/          # Icon files
│   ├── images/         # Image files
│   └── themes/         # QSS theme files
└── README.md           # Project documentation
```

#### Advanced Template
- Complete project structure with src/ directory
- Custom widgets and utilities
- Test files included
- Advanced main.py with class-based structure
- Documentation structure

**Structure:**
```
my_app/
├── main.py              # Advanced application entry point
├── assets/              # Application assets
├── src/                 # Source code
│   ├── widgets/        # Custom widgets
│   └── utils/          # Utility functions
├── tests/              # Test files
├── docs/               # Documentation
└── README.md           # Project documentation
```

## 🔗 Related Documentation

- **[📖 API Documentation](../api/API_DOCUMENTATION.md)** - Complete component reference
- **[🎨 Style Guide](../api/STYLE_GUIDE.md)** - QSS customization examples
- **[🧪 Test Documentation](../tests/TESTS_DOCUMENTATION.md)** - Testing patterns and fixtures
- **[📋 Framework Documentation](../README.md)** - Framework overview and features

---

**EzQt_App CLI** - Making project management and development easier with command-line tools. 