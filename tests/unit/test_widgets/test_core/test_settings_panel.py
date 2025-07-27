# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour la classe SettingsPanel.
"""

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QFrame

from ezqt_app.widgets.core.settings_panel import SettingsPanel


class TestSettingsPanel:
    """Tests pour la classe SettingsPanel."""

    def test_init_default_parameters(self, qt_application):
        """Test de l'initialisation avec des paramètres par défaut."""
        panel = SettingsPanel()

        # Vérifier les propriétés de base
        assert panel.objectName() == "settingsPanel"
        assert panel.frameShape() == QFrame.NoFrame
        assert panel.frameShadow() == QFrame.Raised

    def test_init_with_custom_width(self, qt_application):
        """Test de l'initialisation avec une largeur personnalisée."""
        custom_width = 300
        panel = SettingsPanel(width=custom_width)

        # Vérifier que la largeur personnalisée est stockée
        assert panel._width == custom_width

    def test_init_with_parent(self, qt_application):
        """Test de l'initialisation avec un parent."""
        parent = QWidget()
        panel = SettingsPanel(parent=parent)

        # Vérifier que le parent est correctement défini
        assert panel.parent() == parent

    def test_layout_structure(self, qt_application):
        """Test de la structure du layout."""
        panel = SettingsPanel()

        # Vérifier que le layout principal existe
        assert hasattr(panel, "VL_settingsPanel")
        assert panel.VL_settingsPanel is not None

        # Vérifier les propriétés du layout
        assert panel.VL_settingsPanel.spacing() == 0
        margins = panel.VL_settingsPanel.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_top_border(self, qt_application):
        """Test de la bordure supérieure."""
        panel = SettingsPanel()

        # Vérifier que la bordure supérieure existe
        assert hasattr(panel, "settingsTopBorder")
        assert panel.settingsTopBorder is not None

        # Vérifier les propriétés de la bordure
        assert panel.settingsTopBorder.objectName() == "settingsTopBorder"
        assert panel.settingsTopBorder.frameShape() == QFrame.NoFrame
        assert panel.settingsTopBorder.frameShadow() == QFrame.Raised
        assert panel.settingsTopBorder.maximumSize().height() == 3

    def test_scroll_area(self, qt_application):
        """Test de la zone de défilement."""
        panel = SettingsPanel()

        # Vérifier que la zone de défilement existe
        assert hasattr(panel, "settingsScrollArea")
        assert panel.settingsScrollArea is not None
        assert isinstance(panel.settingsScrollArea, QScrollArea)

        # Vérifier les propriétés de la zone de défilement
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
        """Test du contenu des paramètres."""
        panel = SettingsPanel()

        # Vérifier que le contenu des paramètres existe
        assert hasattr(panel, "contentSettings")
        assert panel.contentSettings is not None

        # Vérifier les propriétés du contenu
        assert panel.contentSettings.objectName() == "contentSettings"
        assert panel.contentSettings.frameShape() == QFrame.NoFrame
        assert panel.contentSettings.frameShadow() == QFrame.Raised

    def test_content_layout(self, qt_application):
        """Test du layout du contenu."""
        panel = SettingsPanel()

        # Vérifier que le layout du contenu existe
        assert hasattr(panel, "VL_contentSettings")
        assert panel.VL_contentSettings is not None

        # Vérifier les propriétés du layout
        assert panel.VL_contentSettings.spacing() == 0
        margins = panel.VL_contentSettings.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0
        assert panel.VL_contentSettings.alignment() == Qt.AlignTop

    def test_theme_settings_container(self, qt_application):
        """Test du conteneur des paramètres de thème."""
        panel = SettingsPanel()

        # Vérifier que le conteneur des paramètres de thème existe
        assert hasattr(panel, "themeSettingsContainer")
        assert panel.themeSettingsContainer is not None

        # Vérifier les propriétés du conteneur
        assert panel.themeSettingsContainer.objectName() == "themeSettingsContainer"
        assert panel.themeSettingsContainer.frameShape() == QFrame.NoFrame
        assert panel.themeSettingsContainer.frameShadow() == QFrame.Raised

    def test_theme_layout(self, qt_application):
        """Test du layout des paramètres de thème."""
        panel = SettingsPanel()

        # Vérifier que le layout des paramètres de thème existe
        assert hasattr(panel, "VL_themeSettingsContainer")
        assert panel.VL_themeSettingsContainer is not None

        # Vérifier les propriétés du layout
        assert panel.VL_themeSettingsContainer.spacing() == 8
        margins = panel.VL_themeSettingsContainer.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_theme_label(self, qt_application):
        """Test du label de thème."""
        panel = SettingsPanel()

        # Vérifier que le label de thème existe
        assert hasattr(panel, "themeLabel")
        assert panel.themeLabel is not None

        # Vérifier les propriétés du label
        assert panel.themeLabel.objectName() == "themeLabel"
        assert panel.themeLabel.text() == "Theme actif"
        assert panel.themeLabel.alignment() == (
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

    def test_signals(self, qt_application):
        """Test des signaux."""
        panel = SettingsPanel()

        # Vérifier que les signaux existent
        assert hasattr(panel, "settingChanged")
        assert hasattr(panel, "languageChanged")
        assert isinstance(panel.settingChanged, Signal)
        assert isinstance(panel.languageChanged, Signal)

    def test_widgets_list(self, qt_application):
        """Test de la liste des widgets."""
        panel = SettingsPanel()

        # Vérifier que la liste des widgets existe
        assert hasattr(SettingsPanel, "_widgets")
        assert isinstance(SettingsPanel._widgets, list)

    def test_settings_dictionary(self, qt_application):
        """Test du dictionnaire des paramètres."""
        panel = SettingsPanel()

        # Vérifier que le dictionnaire des paramètres existe
        assert hasattr(SettingsPanel, "_settings")
        assert isinstance(SettingsPanel._settings, dict)

    def test_size_constraints(self, qt_application):
        """Test des contraintes de taille."""
        panel = SettingsPanel()

        # Vérifier les contraintes de taille
        min_size = panel.minimumSize()
        max_size = panel.maximumSize()

        assert min_size.width() == 0
        assert min_size.height() == 0
        assert max_size.width() == 0
        assert max_size.height() == 16777215  # Qt maximum height

    def test_get_width(self, qt_application):
        """Test de récupération de la largeur."""
        panel = SettingsPanel(width=250)

        # Vérifier que la largeur est correctement récupérée
        assert panel.get_width() == 250

    def test_set_width(self, qt_application):
        """Test de définition de la largeur."""
        panel = SettingsPanel()

        # Définir une nouvelle largeur
        new_width = 350
        panel.set_width(new_width)

        # Vérifier que la largeur a été mise à jour
        assert panel._width == new_width

    def test_settings_panel_without_yaml_loading(self, qt_application):
        """Test du panneau sans chargement YAML."""
        panel = SettingsPanel(load_from_yaml=False)

        # Vérifier que le panneau a été créé sans chargement YAML
        assert panel is not None
        assert hasattr(panel, "VL_settingsPanel")

    @patch("ezqt_app.widgets.core.settings_panel.SettingsPanel.load_settings_from_yaml")
    def test_settings_panel_with_yaml_loading(self, mock_load_yaml, qt_application):
        """Test du panneau avec chargement YAML."""
        panel = SettingsPanel(load_from_yaml=True)

        # Vérifier que la méthode de chargement YAML a été appelée
        mock_load_yaml.assert_called_once()

    def test_settings_panel_object_names(self, qt_application):
        """Test des noms d'objets du panneau."""
        panel = SettingsPanel()

        # Vérifier que tous les objets ont les bons noms
        assert panel.objectName() == "settingsPanel"
        assert panel.settingsTopBorder.objectName() == "settingsTopBorder"
        assert panel.settingsScrollArea.objectName() == "settingsScrollArea"
        assert panel.contentSettings.objectName() == "contentSettings"
        assert panel.themeSettingsContainer.objectName() == "themeSettingsContainer"
        assert panel.themeLabel.objectName() == "themeLabel"

    def test_settings_panel_frame_properties(self, qt_application):
        """Test des propriétés des frames du panneau."""
        panel = SettingsPanel()

        # Vérifier que tous les frames ont les bonnes propriétés
        frames = [
            panel,
            panel.settingsTopBorder,
            panel.contentSettings,
            panel.themeSettingsContainer,
        ]

        for frame in frames:
            assert frame.frameShape() == QFrame.NoFrame
            assert frame.frameShadow() == QFrame.Raised

    def test_settings_panel_layout_properties(self, qt_application):
        """Test des propriétés des layouts du panneau."""
        panel = SettingsPanel()

        # Vérifier que tous les layouts ont les bonnes propriétés
        layouts = [
            panel.VL_settingsPanel,
            panel.VL_contentSettings,
            panel.VL_themeSettingsContainer,
        ]

        for layout in layouts:
            assert layout.spacing() >= 0
            margins = layout.contentsMargins()
            assert margins.left() >= 0
            assert margins.top() >= 0
            assert margins.right() >= 0
            assert margins.bottom() >= 0

    def test_settings_panel_inheritance(self, qt_application):
        """Test de l'héritage du panneau."""
        panel = SettingsPanel()

        # Vérifier l'héritage
        from PySide6.QtWidgets import QFrame

        assert isinstance(panel, QFrame)

    def test_settings_panel_size_policy(self, qt_application):
        """Test de la politique de taille du panneau."""
        panel = SettingsPanel()

        # Vérifier que la politique de taille est configurée
        size_policy = panel.sizePolicy()
        assert size_policy.hasHeightForWidth() == False
