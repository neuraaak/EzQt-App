# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
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
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import sys
import platform
from pathlib import Path

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .kernel import *
from .widgets import *

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////
os_name = platform.system()
widgets = None

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////
APP_PATH = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))
# //////
_dev = True if not hasattr(sys, "frozen") else False

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class EzQt_App(QMainWindow):
    def __init__(
        self,
        themeFileName: str = None,
    ) -> None:
        QMainWindow.__init__(self)

        # ==> KERNEL LOADER
        # ///////////////////////////////////////////////////////////////.
        Kernel.loadFontsResources()
        Kernel.loadAppSettings()

        # ==> INITIALIZE COMPONENTS
        # ///////////////////////////////////////////////////////////////.
        Fonts.initFonts()
        SizePolicy.initSizePolicy()

        # ==> SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # ==> USE CUSTOM TITLE BAR | "True" for Windows
        # ///////////////////////////////////////////////////////////////
        Settings.App.ENABLE_CUSTOM_TITLE_BAR = True if os_name == "Windows" else False

        # ==> APP DATA
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(Settings.App.NAME)
        (
            self.setAppIcon(Images.logo_placeholder, yShrink=0)
            if Settings.Gui.THEME == "dark"
            else self.setAppIcon(Images.logo_placeholder, yShrink=0)
        )

        # ==> TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.menuContainer.toggleButton.clicked.connect(
            lambda: UIFunctions.toggleMenuPanel(self, True)
        )

        # ==> TOGGLE SETTINGS
        # ///////////////////////////////////////////////////////////////
        widgets.headerContainer.settingsTopBtn.clicked.connect(
            lambda: UIFunctions.toggleSettingsPanel(self, True)
        )

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # SET THEME
        # ///////////////////////////////////////////////////////////////
        self._themeFileName = themeFileName
        UIFunctions.theme(self, self._themeFileName)
        # //////
        _theme = Kernel.loadKernelConfig("app")["theme"]
        self.ui.themeToggleButton.initialize_selector(_theme)
        self.ui.headerContainer.update_all_theme_icons()
        self.ui.menuContainer.update_all_theme_icons()
        # //////
        self.ui.themeToggleButton.clicked.connect(self.setAppTheme)

    # SET APP THEME
    # ///////////////////////////////////////////////////////////////
    def setAppTheme(self) -> None:
        theme = self.ui.themeToggleButton._value
        Settings.Gui.THEME = theme.lower()
        Kernel.writeYamlConfig(keys=["app", "theme"], val=theme.lower())
        # //////
        QTimer.singleShot(100, self.updateUI)

    # UPDATE UI
    # ///////////////////////////////////////////////////////////////
    def updateUI(self) -> None:
        new_pos = self.ui.themeToggleButton.get_value_option()
        self.ui.themeToggleButton.move_selector(new_pos)

        # //////
        UIFunctions.theme(self, self._themeFileName)
        # //////
        EzApplication.instance().themeChanged.emit()
        self.ui.headerContainer.update_all_theme_icons()
        self.ui.menuContainer.update_all_theme_icons()

        # //////
        QApplication.processEvents()

    # SET APP ICON
    # ///////////////////////////////////////////////////////////////
    def setAppIcon(
        self, icon: str | QPixmap, yShrink: int = 0, yOffset: int = 0
    ) -> None:
        return self.ui.headerContainer.set_app_logo(
            logo=icon, y_shrink=yShrink, y_offset=yOffset
        )

    # ADD MENU & PAGE
    # ///////////////////////////////////////////////////////////////
    def addMenu(self, name: str, icon: str) -> QWidget:
        page = self.ui.pagesContainer.add_page(name)
        # //////
        menu = self.ui.menuContainer.add_menu(name, icon)
        menu.setProperty("page", page)
        if len(self.ui.menuContainer.menus) == 1:
            menu.setProperty("class", "active")
        # //////
        menu.clicked.connect(
            lambda: widgets.pagesContainer.stackedWidget.setCurrentWidget(page)
        )
        menu.clicked.connect(self.switchMenu)

        # //////
        return page

    # MENU SWITCH
    # ///////////////////////////////////////////////////////////////
    def switchMenu(self) -> None:
        # GET BUTTON CLICKED
        sender = self.sender()
        senderName = sender.objectName()

        # SHOW HOME PAGE
        for btnName, btnWidget in self.ui.menuContainer.menus.items():
            if senderName == f"menu_{btnName}":
                UIFunctions.deselectMenu(self, senderName)
                UIFunctions.selectMenu(self, senderName)

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event) -> None:
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event) -> None:
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()

        # //////
        if _dev:
            # PRINT OBJECT NAME
            # //////
            child_widget = self.childAt(event.position().toPoint())
            if child_widget:
                child_name = child_widget.objectName()
                print(child_name)

            # PRINT MOUSE EVENTS
            # //////
            elif event.buttons() == Qt.LeftButton:
                print(f"Mouse click: LEFT CLICK")
            elif event.buttons() == Qt.RightButton:
                print("Mouse click: RIGHT CLICK")
