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
from pathlib import Path

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QEvent,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
)
from PySide6.QtGui import (
    QIcon,
    QColor,
)
from PySide6.QtWidgets import (
    QWidget,
    QToolButton,
    QSizeGrip,
    QGraphicsDropShadowEffect,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .app_settings import Settings
from .app_functions import Kernel
from ..widgets.custom_grips.custom_grips import CustomGrip

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Any

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////
APP_PATH = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class UIFunctions:
    def __init__(self) -> None:
        from .ui_main import Ui_MainWindow

        self.ui: Ui_MainWindow

    # MAXIMIZE/RESTORE
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self) -> None:
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False:
            self.showMaximized()
            GLOBAL_STATE = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.headerContainer.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.headerContainer.maximizeRestoreAppBtn.setIcon(
                QIcon(":/icons/icons/icon_restore.png")
            )
            self.ui.bottomBar.appSizeGrip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.headerContainer.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.headerContainer.maximizeRestoreAppBtn.setIcon(
                QIcon(":/icons/icons/icon_maximize.png")
            )
            self.ui.bottomBar.appSizeGrip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    # RETURN STATUS
    # ///////////////////////////////////////////////////////////////
    def returnStatus(self) -> Any | bool:
        return GLOBAL_STATE

    # SET STATUS
    # ///////////////////////////////////////////////////////////////
    def setStatus(self, status) -> None:
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU PANEL
    # ///////////////////////////////////////////////////////////////
    def toggleMenuPanel(self, enable) -> None:
        if enable:
            # GET WIDTH
            width = self.ui.menuContainer.width()
            maxExtend = self.ui.menuContainer.get_extended_width()
            standard = self.ui.menuContainer.get_shrink_width()

            # SET MAX WIDTH
            if width == self.ui.menuContainer.get_shrink_width():
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.menu_animation = QPropertyAnimation(
                self.ui.menuContainer, b"minimumWidth"
            )
            self.menu_animation.setDuration(Settings.Gui.TIME_ANIMATION)
            self.menu_animation.setStartValue(width)
            self.menu_animation.setEndValue(widthExtended)
            self.menu_animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.menu_animation.start()

    # TOGGLE SETTINGS PANEL
    # ///////////////////////////////////////////////////////////////
    def toggleSettingsPanel(self, enable) -> None:
        if enable:
            # GET WIDTH
            width = self.ui.settingsPanel.width()
            maxExtend = Settings.Gui.SETTINGS_PANEL_WIDTH
            standard = 0

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.settings_animation = QPropertyAnimation(
                self.ui.settingsPanel, b"minimumWidth"
            )
            self.settings_animation.setDuration(Settings.Gui.TIME_ANIMATION)
            self.settings_animation.setStartValue(width)
            self.settings_animation.setEndValue(widthExtended)
            self.settings_animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.settings_animation.start()

            # Synchronisation du toggle avec le thème courant
            current_theme = Settings.Gui.THEME
            theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
            if theme_toggle and hasattr(theme_toggle, "initialize_selector"):
                try:
                    # Convertir le thème en ID : 0 = Light, 1 = Dark
                    theme_id = 0 if current_theme.lower() == "light" else 1
                    theme_toggle.initialize_selector(theme_id)
                except Exception as e:
                    # Ignorer les erreurs d'initialisation
                    pass

    # SELECT/DESELECT MENU
    # ///////////////////////////////////////////////////////////////
    # START SELECTION
    def selectMenu(self, widget) -> None:
        for w in self.ui.menuContainer.topMenu.findChildren(QToolButton):
            if w.objectName() == widget and isinstance(w, QToolButton):
                w.setProperty("class", "active")
                UIFunctions.refreshStyle(w)

    # RESET SELECTION
    def deselectMenu(self, widget) -> None:
        for w in self.ui.menuContainer.topMenu.findChildren(QToolButton):
            if w.objectName() != widget and isinstance(w, QToolButton):
                w.setProperty("class", "inactive")
                UIFunctions.refreshStyle(w)

    # REFRESH STYLE
    @staticmethod
    def refreshStyle(w: QWidget) -> None:
        w.style().unpolish(w)
        w.style().polish(w)

    # IMPORT THEMES FILES QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def theme(self, customThemeFile: str = None) -> None:
        _style = ""
        # Utiliser Settings.Gui.THEME qui a été mis à jour par loadAppSettings
        _theme = Settings.Gui.THEME
        _colors = Kernel.loadKernelConfig("theme_palette")[_theme]

        # Main Theme
        # ///////////////////////////////////////////////////////////////
        if customThemeFile:
            main_qss = APP_PATH / rf"bin\themes\{customThemeFile}"
        else:
            main_qss = Kernel.getPackageResource("resources/themes/main_theme.qss")

        main_style = open(main_qss, "r").read()
        # //////
        for key, color in _colors.items():
            main_style = main_style.replace(key, color)
        # //////
        _style += f"{main_style}\n"

        # QtStrap
        # ///////////////////////////////////////////////////////////////
        qtstrap_qss = Kernel.getPackageResource("resources/themes/qtstrap.qss")
        qtstrap_style = open(qtstrap_qss, "r").read()
        # //////
        _style += f"{qtstrap_style}\n"

        # //////
        self.ui.styleSheet.setStyleSheet(_style)

    # START - GUI DEFINITIONS
    # ///////////////////////////////////////////////////////////////
    def uiDefinitions(self) -> None:
        def doubleClickMaximizeRestore(event) -> None:
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        self.ui.headerContainer.mouseDoubleClickEvent = doubleClickMaximizeRestore

        # //////
        if Settings.App.NAME:
            self.ui.headerContainer.set_app_name(Settings.App.NAME)
        # //////
        if Settings.App.DESCRIPTION:
            self.ui.headerContainer.set_app_description(Settings.App.DESCRIPTION)
        # //////
        if Settings.App.APP_WIDTH and Settings.App.APP_HEIGHT:
            self.resize(Settings.App.APP_WIDTH, Settings.App.APP_HEIGHT)
        # //////
        if Settings.App.APP_MIN_SIZE:
            self.setMinimumSize(Settings.App.APP_MIN_SIZE)
        # //////
        if Settings.App.ENABLE_CUSTOM_TITLE_BAR:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event) -> None:
                # IF MAXIMIZED CHANGE TO NORMAL
                if UIFunctions.returnStatus(self):
                    UIFunctions.maximize_restore(self)
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()

            self.ui.headerContainer.mouseMoveEvent = moveWindow

            # CUSTOM GRIPS
            self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
            self.right_grip = CustomGrip(self, Qt.RightEdge, True)
            self.top_grip = CustomGrip(self, Qt.TopEdge, True)
            self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.headerContainer.minimizeAppBtn.hide()
            self.ui.headerContainer.maximizeRestoreAppBtn.hide()
            self.ui.headerContainer.closeAppBtn.hide()
            self.ui.bottomBar.appSizeGrip.hide()

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.bottomBar.appSizeGrip)
        self.sizegrip.setStyleSheet(
            "width: 20px; height: 20px; margin 0px; padding: 0px;"
        )

        # MINIMIZE
        self.ui.headerContainer.minimizeAppBtn.clicked.connect(
            lambda: self.showMinimized()
        )

        # MAXIMIZE/RESTORE
        self.ui.headerContainer.maximizeRestoreAppBtn.clicked.connect(
            lambda: UIFunctions.maximize_restore(self)
        )

        # CLOSE APPLICATION
        self.ui.headerContainer.closeAppBtn.clicked.connect(lambda: self.close())

    def resize_grips(self) -> None:
        if Settings.App.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    # ///////////////////////////////////////////////////////////////
    # END - GUI DEFINITIONS
