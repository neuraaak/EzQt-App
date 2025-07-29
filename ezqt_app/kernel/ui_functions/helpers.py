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
UI Functions Helpers
====================

This module contains utility functions to simplify the use
of ui_functions in client code.

Available functions:
- maximize_window: Maximize window
- restore_window: Restore window
- toggle_window_state: Toggle window state
- load_theme: Load QSS theme
- apply_theme: Apply theme to widget
- animate_panel: Animate panel
- select_menu_item: Select menu item
- refresh_menu_style: Refresh menu style
- setup_custom_grips: Setup custom grips
- connect_window_events: Connect window events
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

# TYPE HINTS IMPROVEMENTS
from typing import Optional

# ///////////////////////////////////////////////////////////////
# HELPERS FUNCTIONS
# ///////////////////////////////////////////////////////////////


def maximize_window(window: QMainWindow) -> bool:
    """
    Maximize the main window.

    Args:
        window: Main window to maximize

    Returns:
        True if maximization succeeded

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
    Restore the main window.

    Args:
        window: Main window to restore

    Returns:
        True if restoration succeeded

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
    Toggle window state (maximized/restored).

    Args:
        window: Main window

    Returns:
        True if toggle succeeded

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
    Load a QSS theme from resources.

    Args:
        theme_name: Theme name to load

    Returns:
        QSS theme content or None if failed

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
    Apply a QSS theme to a widget.

    Args:
        widget: Widget to style
        theme_content: QSS theme content

    Returns:
        True if application succeeded

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
    Animate a panel (menu or settings).

    Args:
        panel: Panel to animate
        direction: Animation direction ("left", "right", "top", "bottom")
        duration: Animation duration in ms

    Returns:
        True if animation succeeded

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
    Select a menu item.

    Args:
        button: Menu button to select
        enable: True to select, False to deselect

    Returns:
        True if selection succeeded

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
    Refresh menu style.

    Returns:
        True if refresh succeeded

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
    Setup custom grips for a window.

    Args:
        window: Main window

    Returns:
        True if setup succeeded

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
    Connect window events.

    Args:
        window: Main window

    Returns:
        True if connection succeeded

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
    Get a UIFunctions instance.

    Returns:
        UIFunctions instance

    Example:
        >>> ui = get_ui_functions_instance()
        >>> ui.maximizeMainWindow(window)
    """
    return UIFunctions()


def is_window_maximized(window: QMainWindow) -> bool:
    """
    Check if a window is maximized.

    Args:
        window: Window to check

    Returns:
        True if window is maximized

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
    Get window status.

    Args:
        window: Window to check

    Returns:
        Window status ("maximized", "normal", "minimized")

    Example:
        >>> status = get_window_status(main_window)
        >>> print(f"Status: {status}")
    """
    try:
        window_manager = WindowManager()
        return window_manager.getWindowStatus(window)
    except Exception:
        return "normal"


def apply_default_theme(widget: QWidget) -> bool:
    """
    Apply default theme to a widget.

    Args:
        widget: Widget to style

    Returns:
        True if application succeeded

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
    Setup custom title bar.

    Args:
        window: Main window
        title_bar: Title bar widget

    Returns:
        True if setup succeeded

    Example:
        >>> success = setup_window_title_bar(main_window, title_bar)
    """
    try:
        ui_definitions = UIDefinitions()
        return ui_definitions.setupTitleBar(window, title_bar)
    except Exception:
        return False
