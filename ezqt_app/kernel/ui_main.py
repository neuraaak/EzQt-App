# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
# EzQt_App - A Modern Qt Application Framework
# ///////////////////////////////////////////////////////////////
#
# Author: EzQt_App Team
# Website: https://github.com/ezqt-app/ezqt_app
#
# This file is part of EzQt_App.
#
# EzQt_App is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EzQt_App is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EzQt_App.  If not, see <https://www.gnu.org/licenses/>.
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    QSize,
    QMetaObject,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .app_components import *
from .app_resources import *
from ..widgets.core import *
from ..kernel.app_settings import Settings

# TYPE HINTS IMPROVEMENTS

#  UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

#  CLASS
# ///////////////////////////////////////////////////////////////


class Ui_MainWindow:
    """
    Main application user interface.

    This class defines the structure of the main user interface
    with all its components (header, menu, content, etc.).
    """

    def __init__(self) -> None:
        """Initialize the main user interface."""
        pass

    def setupUi(self, MainWindow: QMainWindow) -> None:
        """
        Configure the main user interface.

        Parameters
        ----------
        MainWindow : QMainWindow
            The main window to configure.
        """
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QSize(940, 560))

        # ////// SETUP MAIN STYLESHEET WIDGET
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName("styleSheet")
        self.styleSheet.setFont(Fonts.SEGOE_UI_10_REG)

        # ////// SETUP MAIN MARGINS
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName("appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)

        # ////// SETUP BACKGROUND APP
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName("bgApp")
        self.bgApp.setStyleSheet("")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appMargins.addWidget(self.bgApp)

        # ////// SETUP APP LAYOUT
        self.appLayout = QVBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName("appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP HEADER
        self.headerContainer = Header(parent=self.bgApp)
        self.appLayout.addWidget(self.headerContainer)

        # ////// SETUP CONTENT BOX
        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName("contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.appLayout.addWidget(self.contentBox)

        # ////// SETUP CONTENT BOX LAYOUT
        self.HL_contentBox = QHBoxLayout(self.contentBox)
        self.HL_contentBox.setSpacing(0)
        self.HL_contentBox.setObjectName("HL_contentBox")
        self.HL_contentBox.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP MENU
        self.menuContainer = Menu(
            parent=self.contentBox,
            shrink_width=Settings.Gui.MENU_PANEL_SHRINKED_WIDTH,
            extended_width=Settings.Gui.MENU_PANEL_EXTENDED_WIDTH,
        )
        self.HL_contentBox.addWidget(self.menuContainer)

        # ////// SETUP CONTENT BOTTOM
        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName("contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.HL_contentBox.addWidget(self.contentBottom)

        # ////// SETUP CONTENT BOTTOM LAYOUT
        self.VL_contentBottom = QVBoxLayout(self.contentBottom)
        self.VL_contentBottom.setSpacing(0)
        self.VL_contentBottom.setObjectName("VL_contentBottom")
        self.VL_contentBottom.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP CONTENT
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName("content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.VL_contentBottom.addWidget(self.content)

        # ////// SETUP CONTENT LAYOUT
        self.HL_content = QHBoxLayout(self.content)
        self.HL_content.setSpacing(0)
        self.HL_content.setObjectName("HL_content")
        self.HL_content.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP PAGE CONTAINER
        self.pagesContainer = PageContainer(self.contentBottom)
        self.HL_content.addWidget(self.pagesContainer)

        # ////// SETUP SETTINGS PANEL
        self.settingsPanel = SettingsPanel(
            parent=self.content,
            width=Settings.Gui.SETTINGS_PANEL_WIDTH,
        )
        self.HL_content.addWidget(self.settingsPanel)

        # ////// SETUP BOTTOM BAR
        self.bottomBar = BottomBar(parent=self.contentBottom)
        self.VL_contentBottom.addWidget(self.bottomBar)

        # ////// FINAL SETUP
        MainWindow.setCentralWidget(self.styleSheet)
        QMetaObject.connectSlotsByName(MainWindow)
