# runner.py

"""
Project runner module for EzQt_App CLI.

Handles project creation, template management, and example generation.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import click

from ..kernel.app_functions.printer import get_printer


class ProjectRunner:
    """Handles EzQt_App project operations and template management."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = Path.cwd()

    def get_project_info(self) -> Dict[str, Any]:
        """Get information about the current project structure."""
        info = {
            "status": "unknown",
            "has_assets": False,
            "has_qrc": False,
            "has_main": False,
            "has_tests": False,
        }

        # Check for EzQt_App project structure
        assets_dir = self.project_root / "assets"
        qrc_file = self.project_root / "base_resources.qrc"
        main_file = self.project_root / "main.py"
        tests_dir = self.project_root / "tests"

        if assets_dir.exists():
            info["has_assets"] = True
        if qrc_file.exists():
            info["has_qrc"] = True
        if main_file.exists():
            info["has_main"] = True
        if tests_dir.exists():
            info["has_tests"] = True

        # Determine project status
        if all([info["has_assets"], info["has_qrc"], info["has_main"]]):
            info["status"] = "initialized"
        elif any([info["has_assets"], info["has_qrc"], info["has_main"]]):
            info["status"] = "partial"
        else:
            info["status"] = "not_initialized"

        return info

    def create_project_template(
        self, template_type: Optional[str], project_name: Optional[str]
    ) -> bool:
        """Create a new project with a predefined template."""

        if not template_type:
            template_type = "basic"

        if not project_name:
            project_name = "my_ezqt_app"

        if self.verbose:
            click.echo(f"🎯 Creating {template_type} template: {project_name}")

        try:
            # Create project directory
            project_dir = self.project_root / project_name
            if project_dir.exists():
                if not click.confirm(
                    f"Directory {project_name} already exists. Overwrite?"
                ):
                    return False
                # Remove existing directory
                import shutil

                shutil.rmtree(project_dir)

            project_dir.mkdir(parents=True)

            # Change to project directory
            original_cwd = os.getcwd()
            os.chdir(project_dir)

            try:
                # Initialize basic EzQt_App structure
                self._create_basic_template(project_name)

                if template_type == "advanced":
                    self._create_advanced_template(project_name)

                click.echo(f"✅ Project '{project_name}' created successfully!")
                click.echo(f"📁 Location: {project_dir.absolute()}")
                click.echo("\n🚀 Next steps:")
                click.echo(f"  cd {project_name}")
                click.echo("  python main.py")

                return True

            finally:
                # Restore original working directory
                os.chdir(original_cwd)

        except Exception as e:
            if self.verbose:
                click.echo(f"❌ Error creating template: {e}")
            return False

    def _create_basic_template(self, project_name: str) -> None:
        """Create basic project template."""
        if self.verbose:
            click.echo("📦 Creating basic template...")

        # Create basic directory structure
        (Path.cwd() / "assets").mkdir(exist_ok=True)
        (Path.cwd() / "assets" / "icons").mkdir(exist_ok=True)
        (Path.cwd() / "assets" / "images").mkdir(exist_ok=True)
        (Path.cwd() / "assets" / "themes").mkdir(exist_ok=True)

        # Create basic main.py
        main_content = f'''# -*- coding: utf-8 -*-
"""
{project_name} - Basic EzQt_App Application

A simple application using the EzQt_App framework.
"""

import sys
import ezqt_app.main as ezqt
from ezqt_app.app import EzQt_App, EzApplication

def main():
    """Main application entry point."""
    # Initialize the framework
    ezqt.init()
    
    # Create application
    app = EzApplication(sys.argv)
    
    # Create main window
    window = EzQt_App(themeFileName="main_theme.qss")
    
    # Add some basic menus
    home_page = window.addMenu("Home", "🏠")
    settings_page = window.addMenu("Settings", "⚙️")
    
    # Show application
    window.show()
    
    # Start event loop
    app.exec()

if __name__ == "__main__":
    main()
'''

        with open("main.py", "w", encoding="utf-8") as f:
            f.write(main_content)

        # Create basic theme file
        theme_content = """/* Basic Theme for EzQt_App */

QMainWindow {
    background-color: #2d2d2d;
    color: #ffffff;
}

QMenuBar {
    background-color: #3d3d3d;
    border-bottom: 1px solid #555555;
}

QPushButton {
    background-color: #0078d4;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    color: white;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QLabel {
    color: #ffffff;
    font-size: 14px;
}
"""

        with open("assets/themes/main_theme.qss", "w", encoding="utf-8") as f:
            f.write(theme_content)

        # Create README
        readme_content = f"""# {project_name}

A basic EzQt_App application.

## Quick Start

```bash
# Run the application
python main.py
```

## Features

- Modern Qt application with PySide6
- Dynamic theming support
- Translation system ready
- Modular architecture

## Structure

```
{project_name}/
├── main.py              # Application entry point
├── assets/              # Application assets
│   ├── icons/          # Icon files
│   ├── images/         # Image files
│   └── themes/         # QSS theme files
└── README.md           # This file
```

## Customization

1. Modify `main.py` to add your own functionality
2. Add icons to `assets/icons/`
3. Add images to `assets/images/`
4. Customize themes in `assets/themes/`

## Documentation

For more information, visit the [EzQt_App documentation](https://github.com/neuraaak/ezqt_app).
"""

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

    def _create_advanced_template(self, project_name: str) -> None:
        """Create advanced project template with additional features."""
        if self.verbose:
            click.echo("🚀 Creating advanced template...")

        # Create additional directories
        (Path.cwd() / "src").mkdir(exist_ok=True)
        (Path.cwd() / "src" / "widgets").mkdir(exist_ok=True)
        (Path.cwd() / "src" / "utils").mkdir(exist_ok=True)
        (Path.cwd() / "tests").mkdir(exist_ok=True)
        (Path.cwd() / "docs").mkdir(exist_ok=True)

        # Create advanced main.py
        advanced_main_content = f'''# -*- coding: utf-8 -*-
"""
{project_name} - Advanced EzQt_App Application

An advanced application using the EzQt_App framework with custom widgets
and advanced features.
"""

import sys
import ezqt_app.main as ezqt
from ezqt_app.app import EzQt_App, EzApplication
from ezqt_app.kernel import tr, set_tr

# Import custom modules
from src.widgets.custom_widget import CustomWidget
from src.utils.app_utils import AppUtils

class AdvancedApplication:
    """Advanced application class with custom functionality."""
    
    def __init__(self):
        """Initialize the advanced application."""
        # Initialize the framework
        ezqt.init()
        
        # Create application
        self.app = EzApplication(sys.argv)
        
        # Create main window
        self.window = EzQt_App(themeFileName="main_theme.qss")
        
        # Setup application
        self.setup_application()
        
    def setup_application(self):
        """Setup the application with custom features."""
        # Add custom menus
        self.home_page = self.window.addMenu("Home", "🏠")
        self.dashboard_page = self.window.addMenu("Dashboard", "📊")
        self.settings_page = self.window.addMenu("Settings", "⚙️")
        self.help_page = self.window.addMenu("Help", "❓")
        
        # Add custom widgets to pages
        self.setup_home_page()
        self.setup_dashboard_page()
        self.setup_settings_page()
        
        # Set application properties
        self.window.set_credits("Made with EzQt_App")
        self.window.set_version("1.0.0")
        
    def setup_home_page(self):
        """Setup the home page with custom widgets."""
        # Add custom widget to home page
        custom_widget = CustomWidget()
        set_tr(custom_widget, "Welcome to {project_name}")
        self.home_page.layout().addWidget(custom_widget)
        
    def setup_dashboard_page(self):
        """Setup the dashboard page."""
        # Add dashboard widgets here
        pass
        
    def setup_settings_page(self):
        """Setup the settings page."""
        # Add settings widgets here
        pass
        
    def run(self):
        """Run the application."""
        self.window.show()
        return self.app.exec()

def main():
    """Main application entry point."""
    app = AdvancedApplication()
    return app.run()

if __name__ == "__main__":
    main()
'''

        with open("main.py", "w", encoding="utf-8") as f:
            f.write(advanced_main_content)

        # Create custom widget
        custom_widget_content = '''# -*- coding: utf-8 -*-
"""
Custom Widget Module

Example custom widget for the advanced template.
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from ezqt_app.kernel import set_tr

class CustomWidget(QFrame):
    """Example custom widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)
        
        layout = QVBoxLayout(self)
        
        # Title label
        self.title_label = QLabel()
        set_tr(self.title_label, "Custom Widget Title")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.title_label)
        
        # Description label
        self.desc_label = QLabel()
        set_tr(self.desc_label, "This is a custom widget example")
        self.desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.desc_label)
        
        # Action button
        self.action_button = QPushButton()
        set_tr(self.action_button, "Click Me")
        self.action_button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.action_button)
        
    def on_button_clicked(self):
        """Handle button click event."""
        printer = get_printer()
        printer.info("Custom widget button clicked!")
'''

        with open("src/widgets/custom_widget.py", "w", encoding="utf-8") as f:
            f.write(custom_widget_content)

        # Create utils module
        utils_content = '''# -*- coding: utf-8 -*-
"""
Application Utilities

Utility functions for the advanced application.
"""

import os
from pathlib import Path

class AppUtils:
    """Utility class for application functions."""
    
    @staticmethod
    def get_app_data_dir():
        """Get the application data directory."""
        return Path.home() / ".ezqt_app" / "data"
    
    @staticmethod
    def ensure_data_dir():
        """Ensure the data directory exists."""
        data_dir = AppUtils.get_app_data_dir()
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    @staticmethod
    def get_config_file():
        """Get the configuration file path."""
        data_dir = AppUtils.ensure_data_dir()
        return data_dir / "config.yaml"
'''

        with open("src/utils/app_utils.py", "w", encoding="utf-8") as f:
            f.write(utils_content)

        # Create test file
        test_content = '''# -*- coding: utf-8 -*-
"""
Test module for the advanced application.

Run with: python -m pytest tests/
"""

import pytest
from src.widgets.custom_widget import CustomWidget

def test_custom_widget_creation():
    """Test that custom widget can be created."""
    widget = CustomWidget()
    assert widget is not None
    assert widget.title_label is not None
    assert widget.action_button is not None

def test_custom_widget_button_click():
    """Test button click functionality."""
    widget = CustomWidget()
    # This is a basic test - in a real application you might want to
    # mock the print function or test actual functionality
    assert widget.action_button is not None
'''

        with open("tests/test_custom_widget.py", "w", encoding="utf-8") as f:
            f.write(test_content)

    def list_available_templates(self) -> None:
        """List all available project templates."""
        templates = {
            "basic": "Simple EzQt_App project with basic structure",
            "advanced": "Advanced project with custom widgets and utilities",
        }

        click.echo("📋 Available project templates:")
        click.echo("=" * 50)

        for template, description in templates.items():
            click.echo(f"  {template:<12} - {description}")

        click.echo(
            "\n💡 Usage: ezqt create --template <template> --name <project_name>"
        )


def create_project_template(
    template_type: str, project_name: str, verbose: bool = False
) -> bool:
    """Create a project template."""
    runner = ProjectRunner(verbose)
    return runner.create_project_template(template_type, project_name)


def get_project_info() -> Dict[str, Any]:
    """Get current project information."""
    runner = ProjectRunner()
    return runner.get_project_info()


def list_available_templates() -> None:
    """List available templates."""
    runner = ProjectRunner()
    runner.list_available_templates()
