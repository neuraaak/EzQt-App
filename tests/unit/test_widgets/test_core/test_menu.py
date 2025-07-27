# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour la classe Menu.
"""

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QPushButton, QFrame
from ezqt_app.widgets.extended.menu_button import MenuButton

from ezqt_app.widgets.core.menu import Menu


class TestMenu:
    """Tests pour la classe Menu."""

    def test_init_default_parameters(self, qt_application):
        """Test de l'initialisation avec des paramètres par défaut."""
        menu = Menu()

        # Vérifier les propriétés de base
        assert menu.objectName() == "menuContainer"
        assert menu.frameShape() == QFrame.NoFrame
        assert menu.frameShadow() == QFrame.Raised

        # Vérifier les largeurs par défaut
        assert menu._shrink_width == 60
        assert menu._extended_width == 240

    def test_init_with_custom_widths(self, qt_application):
        """Test de l'initialisation avec des largeurs personnalisées."""
        shrink_width = 80
        extended_width = 300

        menu = Menu(shrink_width=shrink_width, extended_width=extended_width)

        # Vérifier que les largeurs personnalisées sont utilisées
        assert menu._shrink_width == shrink_width
        assert menu._extended_width == extended_width

        # Vérifier que la largeur minimale est définie
        assert menu.minimumSize().width() == shrink_width

    def test_layout_structure(self, qt_application):
        """Test de la structure du layout."""
        menu = Menu()

        # Vérifier que le layout principal existe
        assert hasattr(menu, "VL_menuContainer")
        assert menu.VL_menuContainer is not None

        # Vérifier les propriétés du layout
        assert menu.VL_menuContainer.spacing() == 0
        margins = menu.VL_menuContainer.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_main_menu_frame(self, qt_application):
        """Test du frame principal du menu."""
        menu = Menu()

        # Vérifier que le frame principal existe
        assert hasattr(menu, "mainMenuFrame")
        assert menu.mainMenuFrame is not None

        # Vérifier les propriétés du frame
        assert menu.mainMenuFrame.objectName() == "mainMenuFrame"
        assert menu.mainMenuFrame.frameShape() == QFrame.NoFrame
        assert menu.mainMenuFrame.frameShadow() == QFrame.Raised

    def test_main_menu_layout(self, qt_application):
        """Test du layout principal du menu."""
        menu = Menu()

        # Vérifier que le layout principal existe
        assert hasattr(menu, "VL_mainMenuFrame")
        assert menu.VL_mainMenuFrame is not None

        # Vérifier les propriétés du layout
        assert menu.VL_mainMenuFrame.spacing() == 0
        margins = menu.VL_mainMenuFrame.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_toggle_container(self, qt_application):
        """Test du conteneur de basculement."""
        menu = Menu()

        # Vérifier que le conteneur de basculement existe
        assert hasattr(menu, "toggleBox")
        assert menu.toggleBox is not None

        # Vérifier les propriétés du conteneur
        assert menu.toggleBox.objectName() == "toggleBox"
        assert menu.toggleBox.frameShape() == QFrame.NoFrame
        assert menu.toggleBox.frameShadow() == QFrame.Raised
        assert menu.toggleBox.maximumSize().height() == 45

    def test_toggle_layout(self, qt_application):
        """Test du layout de basculement."""
        menu = Menu()

        # Vérifier que le layout de basculement existe
        assert hasattr(menu, "VL_toggleBox")
        assert menu.VL_toggleBox is not None

        # Vérifier les propriétés du layout
        assert menu.VL_toggleBox.spacing() == 0
        margins = menu.VL_toggleBox.contentsMargins()
        assert margins.left() == 0
        assert margins.top() == 0
        assert margins.right() == 0
        assert margins.bottom() == 0

    def test_toggle_button(self, qt_application):
        """Test du bouton de basculement."""
        menu = Menu()

        # Vérifier que le bouton de basculement existe
        assert hasattr(menu, "toggleButton")
        assert menu.toggleButton is not None

        # Vérifier les propriétés du bouton
        assert menu.toggleButton.objectName() == "toggleButton"
        assert isinstance(menu.toggleButton, MenuButton)

    def test_menu_dictionary(self, qt_application):
        """Test du dictionnaire des menus."""
        menu = Menu()

        # Vérifier que le dictionnaire des menus existe
        assert hasattr(Menu, "menus")
        assert isinstance(Menu.menus, dict)

    def test_button_list_management(self, qt_application):
        """Test de la gestion de la liste des boutons."""
        menu = Menu()

        # Vérifier que la liste des boutons est initialisée
        assert hasattr(Menu, "_buttons")
        assert isinstance(Menu._buttons, list)

    def test_icon_list_management(self, qt_application):
        """Test de la gestion de la liste des icônes."""
        menu = Menu()

        # Vérifier que la liste des icônes est initialisée
        assert hasattr(Menu, "_icons")
        assert isinstance(Menu._icons, list)

    def test_size_constraints(self, qt_application):
        """Test des contraintes de taille."""
        menu = Menu()

        # Vérifier les contraintes de taille
        min_size = menu.minimumSize()
        max_size = menu.maximumSize()

        assert min_size.width() == menu._shrink_width
        assert max_size.width() == menu._shrink_width
        assert max_size.height() == 16777215  # Qt maximum height

    def test_toggle_button_properties(self, qt_application):
        """Test des propriétés du bouton de basculement."""
        menu = Menu()

        # Vérifier que le bouton a les bonnes propriétés
        toggle_button = menu.toggleButton
        # Vérifier le texte (peut être un attribut ou une méthode)
        if hasattr(toggle_button, "text") and callable(toggle_button.text):
            assert toggle_button.text() == "Hide"
        else:
            assert toggle_button.text == "Hide"
        # Vérifier que les attributs existent (ils peuvent être des propriétés)
        assert hasattr(toggle_button, "shrink_size")
        assert hasattr(toggle_button, "spacing")
        assert hasattr(toggle_button, "duration")

    def test_toggle_button_signal(self, qt_application):
        """Test que le bouton de basculement émet des signaux."""
        menu = Menu()

        # Vérifier que le bouton a un signal clicked
        assert hasattr(menu.toggleButton, "clicked")
        assert hasattr(menu.toggleButton.clicked, "connect")

    def test_menu_expansion_capability(self, qt_application):
        """Test de la capacité d'expansion du menu."""
        menu = Menu()

        # Vérifier que le menu peut s'étendre
        assert menu._extended_width > menu._shrink_width
        assert menu._extended_width == 240
        assert menu._shrink_width == 60

    def test_menu_initial_state(self, qt_application):
        """Test de l'état initial du menu."""
        menu = Menu()

        # Vérifier que le menu commence en état réduit
        assert menu.width() == menu._shrink_width
        assert menu.minimumSize().width() == menu._shrink_width
        assert menu.maximumSize().width() == menu._shrink_width

    def test_menu_with_different_widths(self, qt_application):
        """Test du menu avec différentes largeurs."""
        shrink_width = 100
        extended_width = 400

        menu = Menu(shrink_width=shrink_width, extended_width=extended_width)

        # Vérifier que les nouvelles largeurs sont utilisées
        assert menu._shrink_width == shrink_width
        assert menu._extended_width == extended_width
        assert menu.minimumSize().width() == shrink_width
        assert menu.maximumSize().width() == shrink_width

    def test_menu_frame_properties(self, qt_application):
        """Test des propriétés des frames du menu."""
        menu = Menu()

        # Vérifier que tous les frames ont les bonnes propriétés
        frames = [menu.mainMenuFrame, menu.toggleBox]

        for frame in frames:
            assert frame.frameShape() == QFrame.NoFrame
            assert frame.frameShadow() == QFrame.Raised

    def test_menu_layout_properties(self, qt_application):
        """Test des propriétés des layouts du menu."""
        menu = Menu()

        # Vérifier que tous les layouts ont les bonnes propriétés
        layouts = [menu.VL_menuContainer, menu.VL_mainMenuFrame, menu.VL_toggleBox]

        for layout in layouts:
            assert layout.spacing() == 0
            margins = layout.contentsMargins()
            assert margins.left() == 0
            assert margins.top() == 0
            assert margins.right() == 0
            assert margins.bottom() == 0

    def test_menu_object_names(self, qt_application):
        """Test des noms d'objets du menu."""
        menu = Menu()

        # Vérifier que tous les objets ont les bons noms
        assert menu.objectName() == "menuContainer"
        assert menu.mainMenuFrame.objectName() == "mainMenuFrame"
        assert menu.toggleBox.objectName() == "toggleBox"
        assert menu.toggleButton.objectName() == "toggleButton"

    def test_menu_size_policy(self, qt_application):
        """Test de la politique de taille du menu."""
        menu = Menu()

        # Vérifier que la politique de taille est configurée
        size_policy = menu.sizePolicy()
        assert size_policy.hasHeightForWidth() == False
