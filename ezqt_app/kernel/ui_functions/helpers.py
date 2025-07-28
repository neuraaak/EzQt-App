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

"""
Helpers pour ui_functions
==========================

Ce module contient des fonctions utilitaires pour simplifier l'utilisation
des ui_functions dans le code client.

Fonctions disponibles:
- maximize_window: Maximise la fenêtre
- restore_window: Restaure la fenêtre
- toggle_window_state: Bascule l'état de la fenêtre
- load_theme: Charge un thème QSS
- apply_theme: Applique un thème à un widget
- animate_panel: Anime un panneau
- select_menu_item: Sélectionne un élément de menu
- refresh_menu_style: Rafraîchit le style du menu
- setup_custom_grips: Configure les grips personnalisés
- connect_window_events: Connecte les événements de fenêtre
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QFrame,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .window_manager import WindowManager
from .theme_manager import ThemeManager
from .panel_manager import PanelManager
from .menu_manager import MenuManager
from .ui_definitions import UIDefinitions
from .ui_functions import UIFunctions

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Optional

# ///////////////////////////////////////////////////////////////
# HELPERS FUNCTIONS
# ///////////////////////////////////////////////////////////////


def maximize_window(window: QMainWindow) -> bool:
    """
    Maximise la fenêtre principale.

    Args:
        window: Fenêtre principale à maximiser

    Returns:
        True si la maximisation a réussi

    Example:
        >>> success = maximize_window(main_window)
    """
    try:
        window_manager = WindowManager()
        return window_manager.maximizeMainWindow(window)
    except Exception:
        return False


def restore_window(window: QMainWindow) -> bool:
    """
    Restaure la fenêtre principale.

    Args:
        window: Fenêtre principale à restaurer

    Returns:
        True si la restauration a réussi

    Example:
        >>> success = restore_window(main_window)
    """
    try:
        window_manager = WindowManager()
        return window_manager.restoreMainWindow(window)
    except Exception:
        return False


def toggle_window_state(window: QMainWindow) -> bool:
    """
    Bascule l'état de la fenêtre (maximisé/restauré).

    Args:
        window: Fenêtre principale

    Returns:
        True si le basculement a réussi

    Example:
        >>> success = toggle_window_state(main_window)
    """
    try:
        window_manager = WindowManager()
        return window_manager.toggleMainWindowState(window)
    except Exception:
        return False


def load_theme(theme_name: str) -> Optional[str]:
    """
    Charge un thème QSS depuis les ressources.

    Args:
        theme_name: Nom du thème à charger

    Returns:
        Contenu du thème QSS ou None si échec

    Example:
        >>> theme_content = load_theme("dark_theme")
        >>> if theme_content:
        >>>     apply_theme(widget, theme_content)
    """
    try:
        theme_manager = ThemeManager()
        return theme_manager.loadTheme(theme_name)
    except Exception:
        return None


def apply_theme(widget: QWidget, theme_content: str) -> bool:
    """
    Applique un thème QSS à un widget.

    Args:
        widget: Widget à styliser
        theme_content: Contenu du thème QSS

    Returns:
        True si l'application a réussi

    Example:
        >>> success = apply_theme(widget, theme_content)
    """
    try:
        theme_manager = ThemeManager()
        return theme_manager.applyTheme(widget, theme_content)
    except Exception:
        return False


def animate_panel(panel: QFrame, direction: str = "left", duration: int = 300) -> bool:
    """
    Anime un panneau (menu ou paramètres).

    Args:
        panel: Panneau à animer
        direction: Direction de l'animation ("left", "right", "top", "bottom")
        duration: Durée de l'animation en ms

    Returns:
        True si l'animation a réussi

    Example:
        >>> success = animate_panel(menu_panel, "left", 500)
    """
    try:
        panel_manager = PanelManager()
        if direction == "left":
            return panel_manager.animateLeftMenu(panel, duration)
        elif direction == "right":
            return panel_manager.animateRightMenu(panel, duration)
        elif direction == "top":
            return panel_manager.animateTopMenu(panel, duration)
        elif direction == "bottom":
            return panel_manager.animateBottomMenu(panel, duration)
        return False
    except Exception:
        return False


def select_menu_item(button: QWidget, enable: bool = True) -> bool:
    """
    Sélectionne un élément de menu.

    Args:
        button: Bouton de menu à sélectionner
        enable: True pour sélectionner, False pour désélectionner

    Returns:
        True si la sélection a réussi

    Example:
        >>> success = select_menu_item(menu_button, True)
    """
    try:
        menu_manager = MenuManager()
        return menu_manager.selectMenu(button, enable)
    except Exception:
        return False


def refresh_menu_style() -> bool:
    """
    Rafraîchit le style du menu.

    Returns:
        True si le rafraîchissement a réussi

    Example:
        >>> success = refresh_menu_style()
    """
    try:
        menu_manager = MenuManager()
        return menu_manager.refreshStyle()
    except Exception:
        return False


def setup_custom_grips(window: QMainWindow) -> bool:
    """
    Configure les grips personnalisés pour une fenêtre.

    Args:
        window: Fenêtre principale

    Returns:
        True si la configuration a réussi

    Example:
        >>> success = setup_custom_grips(main_window)
    """
    try:
        ui_definitions = UIDefinitions()
        return ui_definitions.setupCustomGrips(window)
    except Exception:
        return False


def connect_window_events(window: QMainWindow) -> bool:
    """
    Connecte les événements de fenêtre.

    Args:
        window: Fenêtre principale

    Returns:
        True si la connexion a réussi

    Example:
        >>> success = connect_window_events(main_window)
    """
    try:
        ui_definitions = UIDefinitions()
        return ui_definitions.connectWindowEvents(window)
    except Exception:
        return False


def get_ui_functions_instance() -> UIFunctions:
    """
    Obtient une instance des UIFunctions.

    Returns:
        Instance des UIFunctions

    Example:
        >>> ui = get_ui_functions_instance()
        >>> ui.maximizeMainWindow(window)
    """
    return UIFunctions()


def is_window_maximized(window: QMainWindow) -> bool:
    """
    Vérifie si une fenêtre est maximisée.

    Args:
        window: Fenêtre à vérifier

    Returns:
        True si la fenêtre est maximisée

    Example:
        >>> if is_window_maximized(main_window):
        >>>     restore_window(main_window)
    """
    try:
        window_manager = WindowManager()
        return window_manager.isWindowMaximized(window)
    except Exception:
        return False


def get_window_status(window: QMainWindow) -> str:
    """
    Obtient le statut d'une fenêtre.

    Args:
        window: Fenêtre à vérifier

    Returns:
        Statut de la fenêtre ("maximized", "normal", "minimized")

    Example:
        >>> status = get_window_status(main_window)
        >>> print(f"Statut: {status}")
    """
    try:
        window_manager = WindowManager()
        return window_manager.getWindowStatus(window)
    except Exception:
        return "normal"


def apply_default_theme(widget: QWidget) -> bool:
    """
    Applique le thème par défaut à un widget.

    Args:
        widget: Widget à styliser

    Returns:
        True si l'application a réussi

    Example:
        >>> success = apply_default_theme(widget)
    """
    try:
        theme_manager = ThemeManager()
        return theme_manager.applyDefaultTheme(widget)
    except Exception:
        return False


def setup_window_title_bar(window: QMainWindow, title_bar: QWidget) -> bool:
    """
    Configure la barre de titre personnalisée.

    Args:
        window: Fenêtre principale
        title_bar: Widget de la barre de titre

    Returns:
        True si la configuration a réussi

    Example:
        >>> success = setup_window_title_bar(main_window, title_bar)
    """
    try:
        ui_definitions = UIDefinitions()
        return ui_definitions.setupTitleBar(window, title_bar)
    except Exception:
        return False
