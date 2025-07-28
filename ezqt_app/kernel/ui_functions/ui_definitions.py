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
    Qt,
    QEvent,
    QTimer,
)
from PySide6.QtGui import (
    QColor,
)
from PySide6.QtWidgets import (
    QSizeGrip,
    QGraphicsDropShadowEffect,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..app_settings import Settings
from .window_manager import WindowManager
from ...widgets.custom_grips.custom_grips import CustomGrip

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class UIDefinitions:
    """
    Définitions de l'interface utilisateur.

    Cette classe gère la configuration et l'initialisation
    des éléments UI de l'application.
    """

    # UI DEFINITIONS
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def uiDefinitions(self) -> None:
        """
        Configure et initialise tous les éléments de l'interface utilisateur.
        """

        def doubleClickMaximizeRestore(event) -> None:
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: WindowManager.maximize_restore(self))

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
                if WindowManager.returnStatus(self):
                    WindowManager.maximize_restore(self)
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
            lambda: WindowManager.maximize_restore(self)
        )

        # CLOSE APPLICATION
        self.ui.headerContainer.closeAppBtn.clicked.connect(lambda: self.close())

    @staticmethod
    def resize_grips(self) -> None:
        """
        Redimensionne les grips de redimensionnement de la fenêtre.
        """
        if Settings.App.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)
