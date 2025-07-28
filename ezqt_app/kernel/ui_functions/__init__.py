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

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..globals import GLOBAL_STATE, GLOBAL_TITLE_BAR
from .window_manager import WindowManager
from .panel_manager import PanelManager
from .menu_manager import MenuManager
from .theme_manager import ThemeManager
from .ui_definitions import UIDefinitions

# Classe principale qui combine tous les managers
from .ui_functions import UIFunctions

# HELPERS
from .helpers import (
    maximize_window,
    restore_window,
    toggle_window_state,
    load_theme,
    apply_theme,
    animate_panel,
    select_menu_item,
    refresh_menu_style,
    setup_custom_grips,
    connect_window_events,
    get_ui_functions_instance,
    is_window_maximized,
    get_window_status,
    apply_default_theme,
    setup_window_title_bar,
)

## ==> EXPORTS
# ///////////////////////////////////////////////////////////////
__all__ = [
    "WindowManager",
    "PanelManager",
    "MenuManager",
    "ThemeManager",
    "UIDefinitions",
    "GLOBAL_STATE",
    "GLOBAL_TITLE_BAR",
    "UIFunctions",
    # Helpers
    "maximize_window",
    "restore_window",
    "toggle_window_state",
    "load_theme",
    "apply_theme",
    "animate_panel",
    "select_menu_item",
    "refresh_menu_style",
    "setup_custom_grips",
    "connect_window_events",
    "get_ui_functions_instance",
    "is_window_maximized",
    "get_window_status",
    "apply_default_theme",
    "setup_window_title_bar",
]
