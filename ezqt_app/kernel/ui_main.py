# -*- coding: utf-8 -*-
# /////////////////////////////////////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# /////////////////////////////////////////////////////////////////////////////////////////////

# IMPORT BASE
# /////////////////////////////////////////////////////////////////////////////////////////////

# IMPORT SPECS
# /////////////////////////////////////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QSize,
    QMetaObject,
)
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from .app_components import *
from .app_resources import *
from ..widgets.core import *
from ..kernel.app_settings import Settings

## ==> GLOBALS
# /////////////////////////////////////////////////////////////////////////////////////////////

## ==> VARIABLES
# /////////////////////////////////////////////////////////////////////////////////////////////

## ==> CLASSES
# /////////////////////////////////////////////////////////////////////////////////////////////


class Ui_MainWindow(object):
    def __init__(self) -> None:
        pass

    # ///////////////////////////////////////////////////////////////

    def setupUi(self, MainWindow: QMainWindow) -> None:
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QSize(940, 560))

        # ///////////////////////////////////////////////////////////////

        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName("styleSheet")
        self.styleSheet.setFont(Fonts.SEGOE_UI_10_REG)
        # //////
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName("appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)

        # ///////////////////////////////////////////////////////////////

        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName("bgApp")
        self.bgApp.setStyleSheet("")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        #
        self.appMargins.addWidget(self.bgApp)
        # //////
        self.appLayout = QVBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName("appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////
        # BALISE HEADER
        # ///////////////////////////////////////////////////////////////

        self.headerContainer = Header(parent=self.bgApp)
        #
        self.appLayout.addWidget(self.headerContainer)

        # ///////////////////////////////////////////////////////////////
        # END HEADER
        # ///////////////////////////////////////////////////////////////

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName("contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        #
        self.appLayout.addWidget(self.contentBox)
        # //////
        self.HL_contentBox = QHBoxLayout(self.contentBox)
        self.HL_contentBox.setSpacing(0)
        self.HL_contentBox.setObjectName("HL_contentBox")
        self.HL_contentBox.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////
        # BALISE MENU
        # ///////////////////////////////////////////////////////////////

        self.menuContainer = Menu(
            parent=self.contentBox,
            shrink_width=Settings.Gui.MENU_PANEL_SHRINKED_WIDTH,
            extended_width=Settings.Gui.MENU_PANEL_EXTENDED_WIDTH,
        )
        #
        self.HL_contentBox.addWidget(self.menuContainer)

        # ///////////////////////////////////////////////////////////////
        # END MENU
        # ///////////////////////////////////////////////////////////////

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName("contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        #
        self.HL_contentBox.addWidget(self.contentBottom)
        # //////
        self.VL_contentBottom = QVBoxLayout(self.contentBottom)
        self.VL_contentBottom.setSpacing(0)
        self.VL_contentBottom.setObjectName("VL_contentBottom")
        self.VL_contentBottom.setContentsMargins(0, 0, 0, 0)

        self.content = QFrame(self.contentBottom)
        self.content.setObjectName("content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        #
        self.VL_contentBottom.addWidget(self.content)
        # //////
        self.HL_content = QHBoxLayout(self.content)
        self.HL_content.setSpacing(0)
        self.HL_content.setObjectName("HL_content")
        self.HL_content.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////
        # BALISE PAGE CONTAINER
        # ///////////////////////////////////////////////////////////////

        self.pagesContainer = PageContainer(self.contentBottom)
        #
        self.HL_content.addWidget(self.pagesContainer)

        # ///////////////////////////////////////////////////////////////
        # END PAGE CONTAINER
        # ///////////////////////////////////////////////////////////////

        # ///////////////////////////////////////////////////////////////
        # BALISE SETTINGS PANEL
        # ///////////////////////////////////////////////////////////////

        self.settingsPanel = SettingsPanel(
            parent=self.content,
            width=Settings.Gui.SETTINGS_PANEL_WIDTH,
        )
        #
        self.HL_content.addWidget(self.settingsPanel)

        # ///////////////////////////////////////////////////////////////
        # END SETTINGS PANEL
        # ///////////////////////////////////////////////////////////////

        # ///////////////////////////////////////////////////////////////
        # BALISE BOTTOM BAR
        # ///////////////////////////////////////////////////////////////

        self.bottomBar = BottomBar(parent=self.contentBottom)
        #
        self.VL_contentBottom.addWidget(self.bottomBar)

        # ///////////////////////////////////////////////////////////////
        # END BOTTOM BAR
        # ///////////////////////////////////////////////////////////////

        MainWindow.setCentralWidget(self.styleSheet)
        QMetaObject.connectSlotsByName(MainWindow)
