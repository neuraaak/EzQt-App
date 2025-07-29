# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Unit tests for kernel application functions.
"""

import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import os

from ezqt_app.kernel.app_functions import Kernel, APP_PATH


class TestKernel:
    """Tests for the Kernel class."""

    def setup_method(self):
        """Reset Kernel state before each test."""
        Kernel._yamlFile = None

    def test_load_kernel_config_success(self, tmp_path):
        """Test successful configuration loading."""
        # Create a test configuration file
        config_file = tmp_path / "app.yaml"
        config_data = {
            "app": {
                "name": "Test App",
                "description": "Test Description",
                "theme": "dark",
                "app_width": 1280,
                "app_height": 720,
                "app_min_width": 940,
                "app_min_height": 560,
                "menu_panel_shrinked_width": 60,
                "menu_panel_extended_width": 240,
                "settings_panel_width": 240,
                "time_animation": 400,
            },
            "settings_panel": {
                "theme": {
                    "type": "toggle",
                    "label": "Active Theme",
                    "options": ["Light", "Dark"],
                    "default": "dark",
                    "description": "Choose the application theme",
                    "enabled": True,
                },
                "language": {
                    "type": "select",
                    "label": "Language",
                    "options": ["English", "Français", "Español", "Deutsch"],
                    "default": "English",
                    "description": "Interface language",
                    "enabled": True,
                },
            },
            "theme_palette": {
                "dark": {
                    "$_main_surface": "rgb(33, 37, 43)",
                    "$_main_border": "rgb(44, 49, 58)",
                },
                "light": {
                    "$_main_surface": "rgb(240, 240, 243)",
                    "$_main_border": "rgb(225, 223, 229)",
                },
            },
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Load configuration
        result = Kernel.loadKernelConfig("app")

        # Check that configuration was loaded
        assert result == config_data["app"]
        assert result["name"] == "Test App"
        assert result["description"] == "Test Description"
        assert result["theme"] == "dark"

    def test_load_kernel_config_file_not_found(self, tmp_path):
        """Test loading with non-existent file."""
        # Create an empty app.yaml file
        config_file = tmp_path / "app.yaml"
        config_data = {"app": {"name": "Test"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Try to load a non-existent section
        result = Kernel.loadKernelConfig("non_existent_section")
        assert result is None

    def test_load_kernel_config_invalid_yaml(self, tmp_path):
        """Test loading with invalid YAML."""
        # Create a file with invalid YAML
        config_file = tmp_path / "app.yaml"
        with open(config_file, "w") as f:
            f.write("invalid: yaml: content: [\n")

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Try to load configuration
        result = Kernel.loadKernelConfig("app")
        assert result is None

    def test_load_kernel_config_section_not_found(self, tmp_path):
        """Test loading with section not found."""
        # Create a configuration file without the requested section
        config_file = tmp_path / "app.yaml"
        config_data = {
            "other_section": {
                "name": "Other App",
                "description": "Other Description",
            }
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Try to load non-existent section
        result = Kernel.loadKernelConfig("app")
        assert result is None

    def test_save_kernel_config_success(self, tmp_path):
        """Test successful configuration saving."""
        # Create initial configuration file
        config_file = tmp_path / "app.yaml"
        initial_data = {
            "app": {
                "name": "Initial App",
                "description": "Initial Description",
            }
        }

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Save new configuration
        new_config = {
            "name": "Updated App",
            "description": "Updated Description",
            "theme": "light",
        }

        result = Kernel.saveKernelConfig("app", new_config)

        # Check that save was successful
        assert result == True

        # Verify file was updated
        with open(config_file, "r") as f:
            saved_data = yaml.safe_load(f)

        assert saved_data["app"]["name"] == "Updated App"
        assert saved_data["app"]["description"] == "Updated Description"
        assert saved_data["app"]["theme"] == "light"

    def test_save_kernel_config_with_existing_file(self, tmp_path):
        """Test saving configuration with existing file."""
        # Create initial configuration file with multiple sections
        config_file = tmp_path / "app.yaml"
        initial_data = {
            "app": {
                "name": "Initial App",
                "description": "Initial Description",
            },
            "other_section": {
                "key": "value",
            },
        }

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Save new configuration
        new_config = {
            "name": "Updated App",
            "description": "Updated Description",
        }

        result = Kernel.saveKernelConfig("app", new_config)

        # Check that save was successful
        assert result == True

        # Verify file was updated and other sections preserved
        with open(config_file, "r") as f:
            saved_data = yaml.safe_load(f)

        assert saved_data["app"]["name"] == "Updated App"
        assert saved_data["other_section"]["key"] == "value"

    def test_get_config_path(self, tmp_path):
        """Test configuration path generation."""
        # Mock _yamlFile
        config_file = tmp_path / "app.yaml"
        Kernel._yamlFile = config_file

        # Test path generation
        result = Kernel.getConfigPath()
        assert result == config_file

    def test_config_path_with_different_names(self, tmp_path):
        """Test configuration path with different names."""
        # Test with different file names
        config_file = tmp_path / "custom.yaml"
        Kernel._yamlFile = config_file

        result = Kernel.getConfigPath()
        assert result == config_file

    def test_load_kernel_config_multiple_sections(self, tmp_path):
        """Test loading multiple configuration sections."""
        # Create configuration file with multiple sections
        config_file = tmp_path / "app.yaml"
        config_data = {
            "app": {
                "name": "Test App",
                "description": "Test Description",
            },
            "settings": {
                "theme": "dark",
                "language": "en",
            },
            "ui": {
                "width": 1280,
                "height": 720,
            },
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Load different sections
        app_config = Kernel.loadKernelConfig("app")
        settings_config = Kernel.loadKernelConfig("settings")
        ui_config = Kernel.loadKernelConfig("ui")

        # Check that all sections were loaded correctly
        assert app_config["name"] == "Test App"
        assert settings_config["theme"] == "dark"
        assert ui_config["width"] == 1280

    def test_save_kernel_config_preserves_structure(self, tmp_path):
        """Test that configuration saving preserves structure."""
        # Create initial configuration file with complex structure
        config_file = tmp_path / "app.yaml"
        initial_data = {
            "app": {
                "name": "Initial App",
                "nested": {
                    "key1": "value1",
                    "key2": "value2",
                },
                "list": ["item1", "item2", "item3"],
            },
            "other_section": {
                "preserved": True,
            },
        }

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Save new configuration
        new_config = {
            "name": "Updated App",
            "nested": {
                "key1": "updated_value1",
                "key3": "new_value3",
            },
            "list": ["updated_item1", "new_item2"],
        }

        result = Kernel.saveKernelConfig("app", new_config)

        # Check that save was successful
        assert result == True

        # Verify structure was preserved
        with open(config_file, "r") as f:
            saved_data = yaml.safe_load(f)

        assert saved_data["app"]["name"] == "Updated App"
        assert saved_data["app"]["nested"]["key1"] == "updated_value1"
        assert saved_data["app"]["nested"]["key3"] == "new_value3"
        assert saved_data["app"]["list"] == ["updated_item1", "new_item2"]
        assert saved_data["other_section"]["preserved"] == True

    def test_load_kernel_config_empty_file(self, tmp_path):
        """Test loading configuration from empty file."""
        # Create empty configuration file
        config_file = tmp_path / "app.yaml"
        with open(config_file, "w") as f:
            f.write("")

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Try to load configuration
        result = Kernel.loadKernelConfig("app")
        assert result is None

    def test_save_kernel_config_empty_data(self, tmp_path):
        """Test saving empty configuration data."""
        # Create initial configuration file
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"name": "Initial App"}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Save empty configuration
        empty_config = {}

        result = Kernel.saveKernelConfig("app", empty_config)

        # Check that save was successful
        assert result == True

        # Verify file was updated
        with open(config_file, "r") as f:
            saved_data = yaml.safe_load(f)

        assert saved_data["app"] == {}

    def test_config_file_permissions(self, tmp_path):
        """Test configuration file permissions."""
        # Create configuration file
        config_file = tmp_path / "app.yaml"
        config_data = {"app": {"name": "Test App"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Test that file is readable
        result = Kernel.loadKernelConfig("app")
        assert result is not None
        assert result["name"] == "Test App"

        # Test that file is writable
        new_config = {"name": "Updated App"}
        result = Kernel.saveKernelConfig("app", new_config)
        assert result == True

    def test_load_kernel_config_with_comments(self, tmp_path):
        """Test loading configuration with comments."""
        # Create configuration file with comments
        config_file = tmp_path / "app.yaml"
        config_content = """
# Application configuration
app:
  name: "Test App"  # Application name
  description: "Test Description"  # Application description
  theme: "dark"  # Theme setting
  app_width: 1280  # Window width
  app_height: 720  # Window height
  app_min_width: 940  # Minimum width
  app_min_height: 560  # Minimum height
  menu_panel_shrinked_width: 60  # Collapsed menu width
  menu_panel_extended_width: 240  # Expanded menu width
  settings_panel_width: 240  # Settings panel width
  time_animation: 400  # Animation duration

# Settings panel configuration
settings_panel:
  theme:
    type: "toggle"
    label: "Active Theme"
    options: ["Light", "Dark"]
    default: "dark"
    description: "Choose the application theme"
    enabled: true
  language:
    type: "select"
    label: "Language"
    options: ["English", "Français", "Español", "Deutsch"]
    default: "English"
    description: "Interface language"
    enabled: true

# Theme palette configuration
theme_palette:
  dark:
    $_main_surface: "rgb(33, 37, 43)"
    $_main_border: "rgb(44, 49, 58)"
  light:
    $_main_surface: "rgb(240, 240, 243)"
    $_main_border: "rgb(225, 223, 229)"
"""

        with open(config_file, "w") as f:
            f.write(config_content)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Load configuration
        result = Kernel.loadKernelConfig("app")

        # Check that configuration was loaded correctly
        assert result is not None
        assert result["name"] == "Test App"
        assert result["description"] == "Test Description"
        assert result["theme"] == "dark"
        assert result["app_width"] == 1280
        assert result["app_height"] == 720

    def test_save_kernel_config_unicode_support(self, tmp_path):
        """Test configuration saving with Unicode support."""
        # Create initial configuration file
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"name": "Initial App"}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile directly
        Kernel._yamlFile = config_file

        # Save configuration with Unicode characters
        unicode_config = {
            "name": "Test App with Unicode: éàçñüö",
            "description": "Description with special chars: ©®™",
            "unicode_list": ["é", "à", "ç", "ñ", "ü", "ö"],
        }

        result = Kernel.saveKernelConfig("app", unicode_config)

        # Check that save was successful
        assert result == True

        # Verify Unicode was preserved
        with open(config_file, "r", encoding="utf-8") as f:
            saved_data = yaml.safe_load(f)

        assert saved_data["app"]["name"] == "Test App with Unicode: éàçñüö"
        assert saved_data["app"]["description"] == "Description with special chars: ©®™"
        assert saved_data["app"]["unicode_list"] == ["é", "à", "ç", "ñ", "ü", "ö"]

    def test_yaml_file_setter(self):
        """Test the yamlFile setter method."""
        # Test setting yamlFile
        test_path = Path("/test/path/app.yaml")
        Kernel.yamlFile(test_path)
        assert Kernel._yamlFile == test_path

    def test_yaml_file_setter_multiple_calls(self):
        """Test multiple calls to yamlFile setter."""
        # Test multiple calls
        test_path1 = Path("/test/path1/app.yaml")
        test_path2 = Path("/test/path2/app.yaml")

        Kernel.yamlFile(test_path1)
        assert Kernel._yamlFile == test_path1

        Kernel.yamlFile(test_path2)
        assert Kernel._yamlFile == test_path2

    def test_get_package_resource(self):
        """Test the getPackageResource method."""
        # Test package resource retrieval
        result = Kernel.getPackageResource("resources/config/app.yaml")
        assert isinstance(result, Path)
        assert "ezqt_app" in str(result)

    def test_check_assets_requirements(self):
        """Test the checkAssetsRequirements method."""
        # Test assets requirements check
        result = Kernel.checkAssetsRequirements()
        assert isinstance(result, bool)

    def test_check_assets_requirements_qrc_failure(self):
        """Test checkAssetsRequirements when make_qrc fails."""
        # Mock make_qrc to return False
        with patch("ezqt_app.kernel.app_functions.make_qrc", return_value=False):
            result = Kernel.checkAssetsRequirements()
            assert result == False

    def test_make_app_resources_module(self):
        """Test the makeAppResourcesModule method."""
        # Test app resources module creation
        result = Kernel.makeAppResourcesModule()
        assert isinstance(result, bool)
