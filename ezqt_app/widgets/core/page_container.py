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

# TYPE HINTS IMPROVEMENTS
from typing import Dict, Optional

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class PageContainer(QFrame):
    """
    Page container with stacked widget management.

    This class provides a container to manage multiple pages
    with a tab-based navigation system.
    """

    # ////// CLASS VARIABLES
    pages: Dict[str, QWidget] = {}

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the page container.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget (default: None).
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
        Add a new page to the container.

        Parameters
        ----------
        name : str
            The name of the page to add.

        Returns
        -------
        QWidget
            The created page widget.
        """
        page = QWidget()
        page.setObjectName(f"page_{name}")

        self.stackedWidget.addWidget(page)
        PageContainer.pages[name] = page

        return page
