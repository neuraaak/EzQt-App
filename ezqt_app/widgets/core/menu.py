# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import Dict, List

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QCursor,
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QPushButton,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from ...widgets.core.theme_icon import ThemeIcon
from ...widgets.extended.icon_button import IconButton
from ...kernel.app_components import *
from ...kernel.app_resources import *

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class Menu(QFrame):
    # //////
    menus: Dict[str, QPushButton] = {}
    _buttons: List[IconButton] = []
    _icons: List[ThemeIcon] = []

    # ///////////////////////////////////////////////////////////////

    def __init__(self, parent: QWidget = None) -> None:
        super(Menu, self).__init__(parent)

        # ///////////////////////////////////////////////////////////////

        self.setObjectName("menuContainer")
        self.setMinimumSize(QSize(60, 0))
        self.setMaximumSize(QSize(60, 16777215))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        # //////
        self.VL_menuContainer = QVBoxLayout(self)
        self.VL_menuContainer.setSpacing(0)
        self.VL_menuContainer.setObjectName("VL_menuContainer")
        self.VL_menuContainer.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////

        self.mainMenuFrame = QFrame(self)
        self.mainMenuFrame.setObjectName("mainMenuFrame")
        self.mainMenuFrame.setFrameShape(QFrame.NoFrame)
        self.mainMenuFrame.setFrameShadow(QFrame.Raised)
        #
        self.VL_menuContainer.addWidget(self.mainMenuFrame)
        # //////
        self.VL_mainMenuFrame = QVBoxLayout(self.mainMenuFrame)
        self.VL_mainMenuFrame.setSpacing(0)
        self.VL_mainMenuFrame.setObjectName("VL_mainMenuFrame")
        self.VL_mainMenuFrame.setContentsMargins(0, 0, 0, 0)

        # ToggleContainer for expand button
        # ///////////////////////////////////////////////////////////////

        self.toggleBox = QFrame(self.mainMenuFrame)
        self.toggleBox.setObjectName("toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        #
        self.VL_mainMenuFrame.addWidget(self.toggleBox)
        # //////
        self.VL_toggleBox = QVBoxLayout(self.toggleBox)
        self.VL_toggleBox.setSpacing(0)
        self.VL_toggleBox.setObjectName("VL_toggleBox")
        self.VL_toggleBox.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////

        self.toggleButton = IconButton(self.toggleBox)
        self.toggleButton.setObjectName("toggleButton")
        self.toggleButton.setSizePolicy(SizePolicy.H_EXPANDING_V_FIXED)
        SizePolicy.H_EXPANDING_V_FIXED.setHeightForWidth(
            self.toggleButton.sizePolicy().hasHeightForWidth()
        )
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(Fonts.SEGOE_UI_10_REG)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        #
        icon_menu = ThemeIcon(Icons.icon_menu)
        self.toggleButton.setIcon(Icons.icon_menu)
        self.toggleButton.setText("Hide")
        self.toggleButton.setSpacing(35)
        self.toggleButton.setContentsMargins(20, 0, 0, 0)
        #
        self._buttons.append(self.toggleButton)
        self._icons.append(icon_menu)
        self.toggleButton.clicked.connect(self.toggleButton.toggleTextVisibility)
        #
        self.VL_toggleBox.addWidget(self.toggleButton)

        # The Menu itself
        # ///////////////////////////////////////////////////////////////

        self.topMenu = QFrame(self.mainMenuFrame)
        self.topMenu.setObjectName("topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        #
        self.VL_mainMenuFrame.addWidget(self.topMenu, 0, Qt.AlignTop)
        # //////
        self.VL_topMenu = QVBoxLayout(self.topMenu)
        self.VL_topMenu.setSpacing(0)
        self.VL_topMenu.setObjectName("VL_topMenu")
        self.VL_topMenu.setContentsMargins(0, 0, 0, 0)

    # ///////////////////////////////////////////////////////////////

    def add_menu(self, name: str, icon: str | Icons = None) -> IconButton:
        menu = IconButton(self.topMenu)
        menu.setObjectName(f"menu_{name}")
        menu.setProperty("class", "inactive")
        menu.setSizePolicy(SizePolicy.H_EXPANDING_V_FIXED)
        SizePolicy.H_EXPANDING_V_FIXED.setHeightForWidth(
            menu.sizePolicy().hasHeightForWidth()
        )
        menu.setMinimumSize(QSize(0, 45))
        menu.setFont(Fonts.SEGOE_UI_10_REG)
        menu.setCursor(QCursor(Qt.PointingHandCursor))
        menu.setLayoutDirection(Qt.LeftToRight)
        #
        theme_icon = ThemeIcon(icon)
        menu.setIcon(theme_icon)
        menu.setText(name)
        menu.setSpacing(35)
        menu.setContentsMargins(20, 0, 0, 0)
        #
        self._buttons.append(menu)
        self._icons.append(theme_icon)
        self.toggleButton.clicked.connect(menu.toggleTextVisibility)
        #
        self.VL_topMenu.addWidget(menu)
        Menu.menus[name] = menu

        # //////
        return menu

    # ///////////////////////////////////////////////////////////////

    def update_all_theme_icons(self) -> None:
        for i, btn in enumerate(self._buttons):
            btn.setIcon(self._icons[i])
