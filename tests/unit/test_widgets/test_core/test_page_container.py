# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour la classe PageContainer.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Ajouter le chemin du projet au sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QStackedWidget, QFrame

# Import direct du module sans passer par le package principal
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "..", "ezqt_app", "widgets", "core"
    ),
)
from ezqt_app.widgets.core.page_container import PageContainer


class TestPageContainer:
    """Tests pour la classe PageContainer."""

    def setup_method(self):
        """Réinitialise le dictionnaire des pages avant chaque test."""
        PageContainer.pages.clear()

    def test_init_default_parameters(self, qt_application):
        """Test de l'initialisation avec des paramètres par défaut."""
        container = PageContainer()

        # Vérifier les propriétés de base
        assert container.objectName() == "pagesContainer"
        assert container.frameShape() == QFrame.NoFrame
        assert container.frameShadow() == QFrame.Raised

    def test_init_with_parent(self, qt_application):
        """Test de l'initialisation avec un parent."""
        parent = QWidget()
        container = PageContainer(parent=parent)

        # Vérifier que le parent est correctement défini
        assert container.parent() == parent

    def test_layout_structure(self, qt_application):
        """Test de la structure du layout."""
        container = PageContainer()

        # Vérifier que le layout principal existe
        assert hasattr(container, "VL_pagesContainer")
        assert container.VL_pagesContainer is not None

        # Vérifier les propriétés du layout
        assert container.VL_pagesContainer.spacing() == 0
        margins = container.VL_pagesContainer.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_stacked_widget(self, qt_application):
        """Test du widget empilé."""
        container = PageContainer()

        # Vérifier que le widget empilé existe
        assert hasattr(container, "stackedWidget")
        assert container.stackedWidget is not None
        assert isinstance(container.stackedWidget, QStackedWidget)

        # Vérifier les propriétés du widget empilé
        assert container.stackedWidget.objectName() == "stackedWidget"
        assert container.stackedWidget.styleSheet() == "background: transparent;"

    def test_pages_dictionary(self, qt_application):
        """Test du dictionnaire des pages."""
        container = PageContainer()

        # Vérifier que le dictionnaire des pages existe
        assert hasattr(PageContainer, "pages")
        assert isinstance(PageContainer.pages, dict)

    def test_add_page(self, qt_application):
        """Test d'ajout d'une page."""
        container = PageContainer()

        # Ajouter une page
        page_name = "test_page"
        page = container.add_page(page_name)

        # Vérifier que la page a été créée
        assert page is not None
        assert isinstance(page, QWidget)
        assert page.objectName() == f"page_{page_name}"

        # Vérifier que la page a été ajoutée au widget empilé
        assert container.stackedWidget.indexOf(page) >= 0

        # Vérifier que la page a été ajoutée au dictionnaire
        assert page_name in PageContainer.pages
        assert PageContainer.pages[page_name] == page

    def test_add_multiple_pages(self, qt_application):
        """Test d'ajout de plusieurs pages."""
        container = PageContainer()

        # Ajouter plusieurs pages
        page_names = ["page1", "page2", "page3"]
        pages = []

        for name in page_names:
            page = container.add_page(name)
            pages.append(page)

        # Vérifier que toutes les pages ont été créées
        assert len(pages) == 3

        # Vérifier que toutes les pages sont dans le widget empilé
        for page in pages:
            assert container.stackedWidget.indexOf(page) >= 0

        # Vérifier que toutes les pages sont dans le dictionnaire
        for name in page_names:
            assert name in PageContainer.pages

    def test_page_object_names(self, qt_application):
        """Test des noms d'objets des pages."""
        container = PageContainer()

        # Ajouter une page
        page_name = "test_page"
        page = container.add_page(page_name)

        # Vérifier que le nom d'objet est correct
        expected_object_name = f"page_{page_name}"
        assert page.objectName() == expected_object_name

    def test_page_container_initial_state(self, qt_application):
        """Test de l'état initial du conteneur de pages."""
        container = PageContainer()

        # Vérifier que le conteneur commence vide
        assert container.stackedWidget.count() == 0
        assert len(PageContainer.pages) == 0

    def test_page_container_with_existing_pages(self, qt_application):
        """Test du conteneur avec des pages existantes."""
        container1 = PageContainer()
        container2 = PageContainer()

        # Ajouter des pages au premier conteneur
        page1 = container1.add_page("page1")
        page2 = container1.add_page("page2")

        # Vérifier que les pages sont partagées dans le dictionnaire de classe
        assert "page1" in PageContainer.pages
        assert "page2" in PageContainer.pages
        assert PageContainer.pages["page1"] == page1
        assert PageContainer.pages["page2"] == page2

        # Vérifier que chaque conteneur a ses propres pages dans son stackedWidget
        assert container1.stackedWidget.indexOf(page1) >= 0
        assert container1.stackedWidget.indexOf(page2) >= 0
        assert (
            container2.stackedWidget.indexOf(page1) == -1
        )  # Le deuxième conteneur n'a pas ces pages
        assert (
            container2.stackedWidget.indexOf(page2) == -1
        )  # Le deuxième conteneur n'a pas ces pages

        # Ajouter des pages au deuxième conteneur
        page3 = container2.add_page("page3")
        assert container2.stackedWidget.indexOf(page3) >= 0
        assert (
            container1.stackedWidget.indexOf(page3) == -1
        )  # Le premier conteneur n'a pas cette page

    def test_add_page_with_special_characters(self, qt_application):
        """Test d'ajout de page avec des caractères spéciaux."""
        container = PageContainer()

        # Ajouter une page avec des caractères spéciaux
        page_name = "test-page_with_underscores"
        page = container.add_page(page_name)

        # Vérifier que la page a été créée
        assert page is not None
        assert page.objectName() == f"page_{page_name}"
        assert page_name in PageContainer.pages

    def test_add_page_with_empty_name(self, qt_application):
        """Test d'ajout de page avec un nom vide."""
        container = PageContainer()

        # Ajouter une page avec un nom vide
        page_name = ""
        page = container.add_page(page_name)

        # Vérifier que la page a été créée
        assert page is not None
        assert page.objectName() == "page_"
        assert page_name in PageContainer.pages

    def test_add_page_with_numeric_name(self, qt_application):
        """Test d'ajout de page avec un nom numérique."""
        container = PageContainer()

        # Ajouter une page avec un nom numérique
        page_name = "123"
        page = container.add_page(page_name)

        # Vérifier que la page a été créée
        assert page is not None
        assert page.objectName() == f"page_{page_name}"
        assert page_name in PageContainer.pages

    def test_page_container_layout_margins(self, qt_application):
        """Test des marges du layout du conteneur."""
        container = PageContainer()

        # Vérifier que les marges sont correctes
        margins = container.VL_pagesContainer.contentsMargins()
        assert margins.left() == 10
        assert margins.top() == 10
        assert margins.right() == 10
        assert margins.bottom() == 10

    def test_page_container_layout_spacing(self, qt_application):
        """Test de l'espacement du layout du conteneur."""
        container = PageContainer()

        # Vérifier que l'espacement est correct
        assert container.VL_pagesContainer.spacing() == 0

    def test_stacked_widget_style(self, qt_application):
        """Test du style du widget empilé."""
        container = PageContainer()

        # Vérifier que le style est transparent
        assert container.stackedWidget.styleSheet() == "background: transparent;"

    def test_page_container_frame_properties(self, qt_application):
        """Test des propriétés du frame du conteneur."""
        container = PageContainer()

        # Vérifier les propriétés du frame
        assert container.frameShape() == QFrame.NoFrame
        assert container.frameShadow() == QFrame.Raised

    def test_page_container_object_name(self, qt_application):
        """Test du nom d'objet du conteneur."""
        container = PageContainer()

        # Vérifier le nom d'objet
        assert container.objectName() == "pagesContainer"

    def test_page_container_inheritance(self, qt_application):
        """Test de l'héritage du conteneur."""
        container = PageContainer()

        # Vérifier l'héritage
        from PySide6.QtWidgets import QFrame

        assert isinstance(container, QFrame)

    def test_page_container_size_policy(self, qt_application):
        """Test de la politique de taille du conteneur."""
        container = PageContainer()

        # Vérifier que la politique de taille est configurée
        size_policy = container.sizePolicy()
        assert size_policy.hasHeightForWidth() == False
