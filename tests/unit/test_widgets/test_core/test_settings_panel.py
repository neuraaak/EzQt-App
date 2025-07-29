# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Unit tests for the SettingsPanel class.
"""

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QFrame

from ezqt_app.widgets.core.settings_panel import SettingsPanel


class TestSettingsPanel:
    """Tests for the SettingsPanel class."""

    def test_init_default_parameters(self, qt_application):
        """Test initialization with default parameters."""
        panel = SettingsPanel()

        # Check basic properties
        assert panel.objectName() == "settingsPanel"
        assert panel.frameShape() == QFrame.NoFrame
        assert panel.frameShadow() == QFrame.Raised

    def test_init_with_custom_width(self, qt_application):
        """Test initialization with custom width."""
        custom_width = 300
        panel = SettingsPanel(width=custom_width)

        # Check that custom width is stored
        assert panel._width == custom_width

    def test_init_with_parent(self, qt_application):
        """Test initialization with parent."""
        parent = QWidget()
        panel = SettingsPanel(parent=parent)

        # Check that parent is correctly defined
        assert panel.parent() == parent

    def test_layout_structure(self, qt_application):
        """Test layout structure."""
        panel = SettingsPanel()

        # Check that main layout exists
        assert hasattr(panel, "VL_settingsPanel")
        assert panel.VL_settingsPanel is not None

        # Check layout properties
        assert panel.VL_settingsPanel.spacing() == 0
        margins = panel.VL_settingsPanel.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_top_border(self, qt_application):
        """Test top border."""
        panel = SettingsPanel()

        # Check that top border exists
        assert hasattr(panel, "settingsTopBorder")
        assert panel.settingsTopBorder is not None

        # Check border properties
        assert panel.settingsTopBorder.objectName() == "settingsTopBorder"
        assert panel.settingsTopBorder.frameShape() == QFrame.NoFrame
        assert panel.settingsTopBorder.frameShadow() == QFrame.Raised
        assert panel.settingsTopBorder.maximumSize().height() == 3

    def test_scroll_area(self, qt_application):
        """Test scroll area."""
        panel = SettingsPanel()

        # Check that scroll area exists
        assert hasattr(panel, "settingsScrollArea")
        assert panel.settingsScrollArea is not None
        assert isinstance(panel.settingsScrollArea, QScrollArea)

        # Check scroll area properties
        assert panel.settingsScrollArea.objectName() == "settingsScrollArea"
        assert panel.settingsScrollArea.widgetResizable() == True
        assert (
            panel.settingsScrollArea.horizontalScrollBarPolicy()
            == Qt.ScrollBarAlwaysOff
        )
        assert (
            panel.settingsScrollArea.verticalScrollBarPolicy() == Qt.ScrollBarAsNeeded
        )
        assert panel.settingsScrollArea.frameShape() == QFrame.NoFrame
        assert panel.settingsScrollArea.frameShadow() == QFrame.Raised

    def test_content_settings(self, qt_application):
        """Test settings content."""
        panel = SettingsPanel()

        # Check that settings content exists
        assert hasattr(panel, "settingsContent")
        assert panel.settingsContent is not None

        # Check content properties
        assert panel.settingsContent.objectName() == "settingsContent"
        assert panel.settingsContent.frameShape() == QFrame.NoFrame
        assert panel.settingsContent.frameShadow() == QFrame.Raised

    def test_content_layout(self, qt_application):
        """Test content layout."""
        panel = SettingsPanel()

        # Check that content layout exists
        assert hasattr(panel, "VL_settingsContent")
        assert panel.VL_settingsContent is not None

        # Check layout properties
        assert panel.VL_settingsContent.spacing() == 0
        margins = panel.VL_settingsContent.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_theme_settings_container(self, qt_application):
        """Test theme settings container."""
        panel = SettingsPanel()

        # Check that theme settings container exists
        assert hasattr(panel, "themeSettingsContainer")
        assert panel.themeSettingsContainer is not None

        # Check container properties
        assert panel.themeSettingsContainer.objectName() == "themeSettingsContainer"
        assert panel.themeSettingsContainer.frameShape() == QFrame.NoFrame
        assert panel.themeSettingsContainer.frameShadow() == QFrame.Raised

    def test_theme_layout(self, qt_application):
        """Test theme layout."""
        panel = SettingsPanel()

        # Check that theme layout exists
        assert hasattr(panel, "VL_themeSettings")
        assert panel.VL_themeSettings is not None

        # Check layout properties
        assert panel.VL_themeSettings.spacing() == 0
        margins = panel.VL_themeSettings.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_theme_label(self, qt_application):
        """Test theme label."""
        panel = SettingsPanel()

        # Check that theme label exists
        assert hasattr(panel, "themeLabel")
        assert panel.themeLabel is not None
        assert isinstance(panel.themeLabel, QLabel)

        # Check label properties
        assert panel.themeLabel.objectName() == "themeLabel"
        assert panel.themeLabel.text() == "Theme Settings"

    def test_signals(self, qt_application):
        """Test signals."""
        panel = SettingsPanel()

        # Check that signals exist
        assert hasattr(panel, "themeChanged")
        assert isinstance(panel.themeChanged, Signal)

    def test_widgets_list(self, qt_application):
        """Test widgets list."""
        panel = SettingsPanel()

        # Check that widgets list exists
        assert hasattr(panel, "widgets")
        assert isinstance(panel.widgets, list)

    def test_settings_dictionary(self, qt_application):
        """Test settings dictionary."""
        panel = SettingsPanel()

        # Check that settings dictionary exists
        assert hasattr(panel, "settings")
        assert isinstance(panel.settings, dict)

    def test_size_constraints(self, qt_application):
        """Test size constraints."""
        panel = SettingsPanel()

        # Check size constraints
        assert panel.minimumSize().width() == 200
        assert panel.maximumSize().width() == 400
        assert panel.sizePolicy().horizontalPolicy() == Qt.PreferredSize

    def test_get_width(self, qt_application):
        """Test width retrieval."""
        panel = SettingsPanel(width=250)

        # Check that width is correctly retrieved
        assert panel.get_width() == 250

    def test_set_width(self, qt_application):
        """Test width definition."""
        panel = SettingsPanel()

        # Define a new width
        panel.set_width(350)

        # Check that width has been updated
        assert panel._width == 350

    def test_settings_panel_without_yaml_loading(self, qt_application):
        """Test settings panel without YAML loading."""
        panel = SettingsPanel()

        # Check that panel was created without YAML loading
        assert panel.settings == {}

    @patch("ezqt_app.widgets.core.settings_panel.SettingsPanel.load_settings_from_yaml")
    def test_settings_panel_with_yaml_loading(self, mock_load_yaml, qt_application):
        """Test settings panel with YAML loading."""
        panel = SettingsPanel()

        # Check that YAML loading method was called
        mock_load_yaml.assert_called_once()

    def test_settings_panel_object_names(self, qt_application):
        """Test settings panel object names."""
        panel = SettingsPanel()

        # Check that all objects have correct names
        assert panel.objectName() == "settingsPanel"
        assert panel.settingsTopBorder.objectName() == "settingsTopBorder"
        assert panel.settingsScrollArea.objectName() == "settingsScrollArea"
        assert panel.settingsContent.objectName() == "settingsContent"
        assert panel.themeSettingsContainer.objectName() == "themeSettingsContainer"
        assert panel.themeLabel.objectName() == "themeLabel"

    def test_settings_panel_frame_properties(self, qt_application):
        """Test settings panel frame properties."""
        panel = SettingsPanel()

        # Check that all frames have correct properties
        assert panel.frameShape() == QFrame.NoFrame
        assert panel.frameShadow() == QFrame.Raised
        assert panel.settingsTopBorder.frameShape() == QFrame.NoFrame
        assert panel.settingsTopBorder.frameShadow() == QFrame.Raised
        assert panel.settingsScrollArea.frameShape() == QFrame.NoFrame
        assert panel.settingsScrollArea.frameShadow() == QFrame.Raised
        assert panel.settingsContent.frameShape() == QFrame.NoFrame
        assert panel.settingsContent.frameShadow() == QFrame.Raised
        assert panel.themeSettingsContainer.frameShape() == QFrame.NoFrame
        assert panel.themeSettingsContainer.frameShadow() == QFrame.Raised

    def test_settings_panel_layout_properties(self, qt_application):
        """Test settings panel layout properties."""
        panel = SettingsPanel()

        # Check that all layouts have correct properties
        assert panel.VL_settingsPanel.spacing() == 0
        assert panel.VL_settingsContent.spacing() == 0
        assert panel.VL_themeSettings.spacing() == 0

        margins = panel.VL_settingsPanel.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

        margins = panel.VL_settingsContent.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

        margins = panel.VL_themeSettings.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_settings_panel_inheritance(self, qt_application):
        """Test settings panel inheritance."""
        panel = SettingsPanel()

        # Check inheritance
        assert isinstance(panel, QFrame)

    def test_settings_panel_size_policy(self, qt_application):
        """Test settings panel size policy."""
        panel = SettingsPanel()

        # Check that size policy is configured
        assert panel.sizePolicy().horizontalPolicy() == Qt.PreferredSize
