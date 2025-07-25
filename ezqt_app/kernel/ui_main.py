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
from ezqt_widgets import OptionSelector

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

        self.settingsPanel = QFrame(self.content)
        self.settingsPanel.setObjectName("settingsPanel")
        self.settingsPanel.setMinimumSize(QSize(0, 0))
        self.settingsPanel.setMaximumSize(QSize(0, 16777215))
        self.settingsPanel.setFrameShape(QFrame.NoFrame)
        self.settingsPanel.setFrameShadow(QFrame.Raised)
        #
        self.HL_content.addWidget(self.settingsPanel)
        # //////
        self.VL_settingsPanel = QVBoxLayout(self.settingsPanel)
        self.VL_settingsPanel.setSpacing(0)
        self.VL_settingsPanel.setObjectName("VL_settingsPanel")
        self.VL_settingsPanel.setContentsMargins(0, 0, 0, 0)

        # //////
        self.settingsTopBorder = QFrame(self.settingsPanel)
        self.settingsTopBorder.setObjectName("settingsTopBorder")
        self.settingsTopBorder.setMaximumSize(QSize(16777215, 3))
        self.settingsTopBorder.setFrameShape(QFrame.NoFrame)
        self.settingsTopBorder.setFrameShadow(QFrame.Raised)
        #
        self.VL_settingsPanel.addWidget(self.settingsTopBorder)

        # //////
        self.contentSettings = QFrame(self.settingsPanel)
        self.contentSettings.setObjectName("contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        #
        self.VL_settingsPanel.addWidget(self.contentSettings)
        # //////
        self.VL_contentSettings = QVBoxLayout(self.contentSettings)
        self.VL_contentSettings.setObjectName("VL_contentSettings")
        self.VL_contentSettings.setSpacing(0)
        self.VL_contentSettings.setContentsMargins(0, 0, 0, 0)
        self.VL_contentSettings.setAlignment(Qt.AlignmentFlag.AlignTop)

        # //////
        self.themeSettingsContainer = QFrame(self.contentSettings)
        self.themeSettingsContainer.setObjectName("themeSettingsContainer")
        self.themeSettingsContainer.setFrameShape(QFrame.NoFrame)
        self.themeSettingsContainer.setFrameShadow(QFrame.Raised)
        #
        self.VL_contentSettings.addWidget(self.themeSettingsContainer, 0, Qt.AlignTop)
        # //////
        self.VL_themeSettingsContainer = QVBoxLayout(self.themeSettingsContainer)
        self.VL_themeSettingsContainer.setSpacing(8)
        self.VL_themeSettingsContainer.setObjectName("VL_themeSettingsContainer")
        self.VL_themeSettingsContainer.setContentsMargins(10, 10, 10, 10)

        # //////
        self.themeLabel = QLabel("Theme actif", self.themeSettingsContainer)
        self.themeLabel.setObjectName("themeLabel")
        self.themeLabel.setFont(Fonts.SEGOE_UI_10_REG)
        self.themeLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        #
        self.VL_themeSettingsContainer.addWidget(self.themeLabel)

        # //////
        self.themeToggleButton = OptionSelector(
            items=["Light", "Dark"],
            parent=self.themeSettingsContainer,
            animation_duration=Settings.Gui.TIME_ANIMATION,
        )
        self.themeToggleButton.setObjectName("themeToggleButton")
        self.themeToggleButton.setSizePolicy(SizePolicy.H_EXPANDING_V_FIXED)
        self.themeToggleButton.setFixedHeight(40)

        self.VL_themeSettingsContainer.addWidget(self.themeToggleButton)

        # ///////////////////////////////////////////////////////////////
        # END SETTINGS PANEL
        # ///////////////////////////////////////////////////////////////

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName("bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        #
        self.VL_contentBottom.addWidget(self.bottomBar)
        # //////
        self.HL_bottomBar = QHBoxLayout(self.bottomBar)
        self.HL_bottomBar.setSpacing(0)
        self.HL_bottomBar.setObjectName("HL_bottomBar")
        self.HL_bottomBar.setContentsMargins(0, 0, 0, 0)

        # //////
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName("creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        self.creditsLabel.setFont(Fonts.SEGOE_UI_10_REG)
        self.creditsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        #
        self.HL_bottomBar.addWidget(self.creditsLabel)

        # //////
        self.version = QLabel(self.bottomBar)
        self.version.setObjectName("version")
        self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        #
        self.HL_bottomBar.addWidget(self.version)

        # //////
        self.appSizeGrip = QFrame(self.bottomBar)
        self.appSizeGrip.setObjectName("appSizeGrip")
        self.appSizeGrip.setMinimumSize(QSize(20, 0))
        self.appSizeGrip.setMaximumSize(QSize(20, 16777215))
        self.appSizeGrip.setFrameShape(QFrame.NoFrame)
        self.appSizeGrip.setFrameShadow(QFrame.Raised)
        #
        self.HL_bottomBar.addWidget(self.appSizeGrip)

        # ///////////////////////////////////////////////////////////////
        # ///////////////////////////////////////////////////////////////

        MainWindow.setCentralWidget(self.styleSheet)
        QMetaObject.connectSlotsByName(MainWindow)
