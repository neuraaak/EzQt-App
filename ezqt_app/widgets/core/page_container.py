# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QStackedWidget,
)

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Dict, Optional

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class PageContainer(QFrame):
    """
    Conteneur de pages avec gestion des widgets empilés.

    Cette classe fournit un conteneur pour gérer plusieurs pages
    avec un système de navigation par onglets.
    """

    # ////// CLASS VARIABLES
    pages: Dict[str, QWidget] = {}

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialise le conteneur de pages.

        Parameters
        ----------
        parent : QWidget, optional
            Le widget parent (défaut: None).
        """
        super().__init__(parent)

        # ////// SETUP WIDGET PROPERTIES
        self.setObjectName("pagesContainer")
        self.setStyleSheet("")
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        # ////// SETUP MAIN LAYOUT
        self.VL_pagesContainer = QVBoxLayout(self)
        self.VL_pagesContainer.setSpacing(0)
        self.VL_pagesContainer.setObjectName("VL_pagesContainer")
        self.VL_pagesContainer.setContentsMargins(10, 10, 10, 10)

        # ////// SETUP STACKED WIDGET
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setStyleSheet("background: transparent;")
        self.VL_pagesContainer.addWidget(self.stackedWidget)

    # ////// UTILITY FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def add_page(self, name: str) -> QWidget:
        """
        Ajoute une nouvelle page au conteneur.

        Parameters
        ----------
        name : str
            Nom de la page à ajouter.

        Returns
        -------
        QWidget
            La page créée.
        """
        page = QWidget()
        page.setObjectName(f"page_{name}")

        self.stackedWidget.addWidget(page)
        PageContainer.pages[name] = page

        return page
