# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import Dict

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QStackedWidget,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from ...kernel.app_resources import *

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class PageContainer(QFrame):
    # //////
    pages: Dict[str, QWidget] = {}

    # ///////////////////////////////////////////////////////////////

    def __init__(self, parent: QWidget = None) -> None:
        super(PageContainer, self).__init__(parent)

        # ///////////////////////////////////////////////////////////////

        self.setObjectName("pagesContainer")
        self.setStyleSheet("")
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        # //////
        self.VL_pagesContainer = QVBoxLayout(self)
        self.VL_pagesContainer.setSpacing(0)
        self.VL_pagesContainer.setObjectName("VL_pagesContainer")
        self.VL_pagesContainer.setContentsMargins(10, 10, 10, 10)

        # ///////////////////////////////////////////////////////////////

        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setStyleSheet("background: transparent;")
        #
        self.VL_pagesContainer.addWidget(self.stackedWidget)

    # ///////////////////////////////////////////////////////////////

    def add_page(self, name: str) -> QWidget:
        page = QWidget()
        page.setObjectName(f"page_{name}")
        #
        self.stackedWidget.addWidget(page)
        PageContainer.pages[name] = page

        # //////
        return page
