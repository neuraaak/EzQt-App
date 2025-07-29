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
from PySide6.QtWidgets import (
    QWidget,
    QToolButton,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# TYPE HINTS IMPROVEMENTS

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class MenuManager:
    """
    Interface menu manager.

    This class manages the selection and deselection of menu
    items in the application.
    """

    # MENU MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def selectMenu(self, widget) -> None:
        """
        Select a menu item.

        Parameters
        ----------
        widget : str
            Name of menu item to select.
        """
        for w in self.ui.menuContainer.topMenu.findChildren(QToolButton):
            if w.objectName() == widget and isinstance(w, QToolButton):
                w.setProperty("class", "active")
                MenuManager.refreshStyle(w)

    @staticmethod
    def deselectMenu(self, widget) -> None:
        """
        Deselect a menu item.

        Parameters
        ----------
        widget : str
            Name of menu item to deselect.
        """
        for w in self.ui.menuContainer.topMenu.findChildren(QToolButton):
            if w.objectName() != widget and isinstance(w, QToolButton):
                w.setProperty("class", "inactive")
                MenuManager.refreshStyle(w)

    @staticmethod
    def refreshStyle(w: QWidget) -> None:
        """
        Refresh widget style.

        Parameters
        ----------
        w : QWidget
            Widget whose style should be refreshed.
        """
        w.style().unpolish(w)
        w.style().polish(w)
