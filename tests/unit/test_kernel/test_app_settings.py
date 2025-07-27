# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour les paramètres de l'application.
"""

import pytest
from PySide6.QtCore import QSize

from ezqt_app.kernel.app_settings import Settings


class TestSettings:
    """Tests pour la classe Settings."""

    def test_app_settings(self):
        """Test des paramètres de l'application."""
        # Vérifier les paramètres de base
        assert Settings.App.NAME == "MyApplication"
        assert Settings.App.DESCRIPTION == "MyDescription"
        assert Settings.App.ENABLE_CUSTOM_TITLE_BAR == True
        
        # Vérifier les dimensions
        assert isinstance(Settings.App.APP_MIN_SIZE, QSize)
        assert Settings.App.APP_WIDTH == 1280
        assert Settings.App.APP_HEIGHT == 720

    def test_gui_settings(self):
        """Test des paramètres de l'interface graphique."""
        # Vérifier le thème par défaut
        assert Settings.Gui.THEME == "dark"
        
        # Vérifier les paramètres du menu
        assert Settings.Gui.MENU_PANEL_SHRINKED_WIDTH == 60
        assert Settings.Gui.MENU_PANEL_EXTENDED_WIDTH == 240
        
        # Vérifier les paramètres du panneau
        assert Settings.Gui.SETTINGS_PANEL_WIDTH == 240
        assert Settings.Gui.TIME_ANIMATION == 400

    def test_theme_settings(self):
        """Test des paramètres de thème."""
        # Vérifier que la classe Theme peut être instanciée
        theme_settings = Settings.Theme()
        assert theme_settings is not None

    def test_kernel_settings(self):
        """Test des paramètres du kernel."""
        # Vérifier que la classe Kernel existe
        kernel_settings = Settings.Kernel()
        assert kernel_settings is not None

    def test_settings_mutability(self):
        """Test que les paramètres peuvent être modifiés (comportement attendu)."""
        # Sauvegarder les valeurs originales
        original_name = Settings.App.NAME
        original_theme = Settings.Gui.THEME
        original_width = Settings.Gui.MENU_PANEL_SHRINKED_WIDTH
        
        # Modifier les paramètres (c'est le comportement attendu)
        Settings.App.NAME = "ModifiedName"
        Settings.Gui.THEME = "light"
        Settings.Gui.MENU_PANEL_SHRINKED_WIDTH = 100
        
        # Vérifier que les valeurs ont été modifiées
        assert Settings.App.NAME == "ModifiedName"
        assert Settings.Gui.THEME == "light"
        assert Settings.Gui.MENU_PANEL_SHRINKED_WIDTH == 100
        
        # Restaurer les valeurs originales
        Settings.App.NAME = original_name
        Settings.Gui.THEME = original_theme
        Settings.Gui.MENU_PANEL_SHRINKED_WIDTH = original_width
        
        # Vérifier que les valeurs ont été restaurées
        assert Settings.App.NAME == original_name
        assert Settings.Gui.THEME == original_theme
        assert Settings.Gui.MENU_PANEL_SHRINKED_WIDTH == original_width

    def test_qsize_consistency(self):
        """Test de la cohérence des objets QSize."""
        min_size = Settings.App.APP_MIN_SIZE
        assert min_size.width() == 940
        assert min_size.height() == 560

    def test_boolean_settings(self):
        """Test des paramètres booléens."""
        assert isinstance(Settings.App.ENABLE_CUSTOM_TITLE_BAR, bool)
        assert Settings.App.ENABLE_CUSTOM_TITLE_BAR == True

    def test_integer_settings(self):
        """Test des paramètres entiers."""
        assert isinstance(Settings.App.APP_WIDTH, int)
        assert isinstance(Settings.App.APP_HEIGHT, int)
        assert isinstance(Settings.Gui.MENU_PANEL_SHRINKED_WIDTH, int)
        assert isinstance(Settings.Gui.MENU_PANEL_EXTENDED_WIDTH, int)
        assert isinstance(Settings.Gui.SETTINGS_PANEL_WIDTH, int)
        assert isinstance(Settings.Gui.TIME_ANIMATION, int)

    def test_string_settings(self):
        """Test des paramètres chaînes de caractères."""
        assert isinstance(Settings.App.NAME, str)
        assert isinstance(Settings.App.DESCRIPTION, str)
        assert isinstance(Settings.Gui.THEME, str)

    def test_settings_structure(self):
        """Test de la structure générale des paramètres."""
        # Vérifier que toutes les classes de paramètres existent
        assert hasattr(Settings, 'App')
        assert hasattr(Settings, 'Gui')
        assert hasattr(Settings, 'Theme')
        assert hasattr(Settings, 'Kernel')
        
        # Vérifier que les classes sont des types
        assert isinstance(Settings.App, type)
        assert isinstance(Settings.Gui, type)
        assert isinstance(Settings.Theme, type)
        assert isinstance(Settings.Kernel, type) 