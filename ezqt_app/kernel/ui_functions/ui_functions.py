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

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .window_manager import WindowManager
from .panel_manager import PanelManager
from .menu_manager import MenuManager
from .theme_manager import ThemeManager
from .ui_definitions import UIDefinitions

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class UIFunctions:
    """
    Main UI functions class.

    This class combines all specialized managers to provide
    a unified interface for user interface management.
    """

    def __init__(self) -> None:
        from ..ui_main import Ui_MainWindow

        self.ui: Ui_MainWindow

    # WINDOW MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def maximize_restore(self) -> None:
        """
        Maximize or restore window based on current state.
        """
        WindowManager.maximize_restore(self)

    def returnStatus(self):
        """
        Return current window state.

        Returns
        -------
        bool
            True if window is maximized, False otherwise.
        """
        return WindowManager.returnStatus(self)

    def setStatus(self, status) -> None:
        """
        Set window state.

        Parameters
        ----------
        status : bool
            New window state.
        """
        WindowManager.setStatus(self, status)

    # PANEL MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def toggleMenuPanel(self, enable) -> None:
        """
        Toggle menu panel display.

        Parameters
        ----------
        enable : bool
            Enable or disable menu panel.
        """
        PanelManager.toggleMenuPanel(self, enable)

    def toggleSettingsPanel(self, enable) -> None:
        """
        Toggle settings panel display.

        Parameters
        ----------
        enable : bool
            Enable or disable settings panel.
        """
        PanelManager.toggleSettingsPanel(self, enable)

    # MENU MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def selectMenu(self, widget) -> None:
        """
        Select a menu item.

        Parameters
        ----------
        widget : str
            Name of menu item to select.
        """
        MenuManager.selectMenu(self, widget)

    def deselectMenu(self, widget) -> None:
        """
        Deselect a menu item.

        Parameters
        ----------
        widget : str
            Name of menu item to deselect.
        """
        MenuManager.deselectMenu(self, widget)

    def refreshStyle(self, w):
        """
        Refresh widget style.

        Parameters
        ----------
        w : QWidget
            Widget whose style should be refreshed.
        """
        MenuManager.refreshStyle(w)

    # THEME MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def theme(self, customThemeFile: str = None) -> None:
        """
        Load and apply theme to interface.

        Parameters
        ----------
        customThemeFile : str, optional
            Custom theme file to use.
        """
        ThemeManager.theme(self, customThemeFile)

    # UI DEFINITIONS
    # ///////////////////////////////////////////////////////////////

    def uiDefinitions(self) -> None:
        """
        Configure and initialize all user interface elements.
        """
        UIDefinitions.uiDefinitions(self)

    def resize_grips(self) -> None:
        """
        Resize window resize grips.
        """
        UIDefinitions.resize_grips(self)
