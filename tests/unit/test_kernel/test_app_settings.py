# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Unit tests for application settings.
"""

import pytest
from PySide6.QtCore import QSize

from ezqt_app.kernel.app_settings import Settings


class TestSettings:
    """Tests for the Settings class."""

    def test_app_settings(self):
        """Test application settings."""
        # Check basic settings
        assert Settings.App.NAME == "MyApplication"
        assert Settings.App.DESCRIPTION == "MyDescription"
        assert Settings.App.ENABLE_CUSTOM_TITLE_BAR == True

        # Check dimensions
        assert isinstance(Settings.App.APP_MIN_SIZE, QSize)
        assert Settings.App.APP_WIDTH == 1280
        assert Settings.App.APP_HEIGHT == 720

    def test_gui_settings(self):
        """Test GUI settings."""
        # Check default theme
        assert Settings.Gui.THEME == "dark"

        # Check menu settings
        assert Settings.Gui.MENU_PANEL_SHRINKED_WIDTH == 60
        assert Settings.Gui.MENU_PANEL_EXTENDED_WIDTH == 240

        # Check panel settings
        assert Settings.Gui.SETTINGS_PANEL_WIDTH == 240
        assert Settings.Gui.TIME_ANIMATION == 400

    def test_theme_settings(self):
        """Test theme settings."""
        # Check that Theme class can be instantiated
        theme_settings = Settings.Theme()
        assert theme_settings is not None

    def test_kernel_settings(self):
        """Test kernel settings."""
        # Check that Kernel class exists
        kernel_settings = Settings.Kernel()
        assert kernel_settings is not None

    def test_settings_mutability(self):
        """Test that settings can be modified (expected behavior)."""
        # Save original values
        original_name = Settings.App.NAME
        original_theme = Settings.Gui.THEME
        original_width = Settings.Gui.MENU_PANEL_SHRINKED_WIDTH

        # Modify settings (this is expected behavior)
        Settings.App.NAME = "ModifiedName"
        Settings.Gui.THEME = "light"
        Settings.Gui.MENU_PANEL_SHRINKED_WIDTH = 100

        # Check that values were modified
        assert Settings.App.NAME == "ModifiedName"
        assert Settings.Gui.THEME == "light"
        assert Settings.Gui.MENU_PANEL_SHRINKED_WIDTH == 100

        # Restore original values
        Settings.App.NAME = original_name
        Settings.Gui.THEME = original_theme
        Settings.Gui.MENU_PANEL_SHRINKED_WIDTH = original_width

        # Check that values were restored
        assert Settings.App.NAME == original_name
        assert Settings.Gui.THEME == original_theme
        assert Settings.Gui.MENU_PANEL_SHRINKED_WIDTH == original_width

    def test_qsize_consistency(self):
        """Test QSize object consistency."""
        min_size = Settings.App.APP_MIN_SIZE
        assert min_size.width() == 940
        assert min_size.height() == 560

    def test_boolean_settings(self):
        """Test boolean settings."""
        assert isinstance(Settings.App.ENABLE_CUSTOM_TITLE_BAR, bool)
        assert Settings.App.ENABLE_CUSTOM_TITLE_BAR == True

    def test_integer_settings(self):
        """Test integer settings."""
        assert isinstance(Settings.App.APP_WIDTH, int)
        assert isinstance(Settings.App.APP_HEIGHT, int)
        assert isinstance(Settings.Gui.MENU_PANEL_SHRINKED_WIDTH, int)
        assert isinstance(Settings.Gui.MENU_PANEL_EXTENDED_WIDTH, int)
        assert isinstance(Settings.Gui.SETTINGS_PANEL_WIDTH, int)
        assert isinstance(Settings.Gui.TIME_ANIMATION, int)

    def test_string_settings(self):
        """Test string settings."""
        assert isinstance(Settings.App.NAME, str)
        assert isinstance(Settings.App.DESCRIPTION, str)
        assert isinstance(Settings.Gui.THEME, str)

    def test_settings_structure(self):
        """Test general settings structure."""
        # Check that all main sections exist
        assert hasattr(Settings, "App")
        assert hasattr(Settings, "Gui")
        assert hasattr(Settings, "Theme")
        assert hasattr(Settings, "Kernel")
