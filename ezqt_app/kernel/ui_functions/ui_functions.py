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
    Classe principale des fonctions UI.

    Cette classe combine tous les gestionnaires spécialisés pour fournir
    une interface unifiée pour la gestion de l'interface utilisateur.
    """

    def __init__(self) -> None:
        from ..ui_main import Ui_MainWindow

        self.ui: Ui_MainWindow

    # WINDOW MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def maximize_restore(self) -> None:
        """
        Maximise ou restaure la fenêtre selon son état actuel.
        """
        WindowManager.maximize_restore(self)

    def returnStatus(self):
        """
        Retourne l'état actuel de la fenêtre.

        Returns
        -------
        bool
            True si la fenêtre est maximisée, False sinon.
        """
        return WindowManager.returnStatus(self)

    def setStatus(self, status) -> None:
        """
        Définit l'état de la fenêtre.

        Parameters
        ----------
        status : bool
            Nouvel état de la fenêtre.
        """
        WindowManager.setStatus(self, status)

    # PANEL MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def toggleMenuPanel(self, enable) -> None:
        """
        Bascule l'affichage du panneau de menu.

        Parameters
        ----------
        enable : bool
            Active ou désactive le panneau de menu.
        """
        PanelManager.toggleMenuPanel(self, enable)

    def toggleSettingsPanel(self, enable) -> None:
        """
        Bascule l'affichage du panneau de paramètres.

        Parameters
        ----------
        enable : bool
            Active ou désactive le panneau de paramètres.
        """
        PanelManager.toggleSettingsPanel(self, enable)

    # MENU MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def selectMenu(self, widget) -> None:
        """
        Sélectionne un élément de menu.

        Parameters
        ----------
        widget : str
            Nom de l'élément de menu à sélectionner.
        """
        MenuManager.selectMenu(self, widget)

    def deselectMenu(self, widget) -> None:
        """
        Désélectionne un élément de menu.

        Parameters
        ----------
        widget : str
            Nom de l'élément de menu à désélectionner.
        """
        MenuManager.deselectMenu(self, widget)

    def refreshStyle(self, w):
        """
        Rafraîchit le style d'un widget.

        Parameters
        ----------
        w : QWidget
            Widget dont le style doit être rafraîchi.
        """
        MenuManager.refreshStyle(w)

    # THEME MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def theme(self, customThemeFile: str = None) -> None:
        """
        Charge et applique un thème à l'interface.

        Parameters
        ----------
        customThemeFile : str, optional
            Fichier de thème personnalisé à utiliser.
        """
        ThemeManager.theme(self, customThemeFile)

    # UI DEFINITIONS
    # ///////////////////////////////////////////////////////////////

    def uiDefinitions(self) -> None:
        """
        Configure et initialise tous les éléments de l'interface utilisateur.
        """
        UIDefinitions.uiDefinitions(self)

    def resize_grips(self) -> None:
        """
        Redimensionne les grips de redimensionnement de la fenêtre.
        """
        UIDefinitions.resize_grips(self)
