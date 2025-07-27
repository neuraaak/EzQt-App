# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    QSize,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Any

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class Settings:
    """
    Classe de configuration principale pour l'application.

    Cette classe contient toutes les configurations de l'application
    organisées en sous-classes thématiques.
    """

    # KERNEL SETTINGS
    # ///////////////////////////////////////////////////////////////
    class Kernel:
        """Configuration du noyau de l'application."""

        pass

    # APP SETTINGS
    # ///////////////////////////////////////////////////////////////
    class App:
        """Configuration générale de l'application."""

        # ////// APP INFO
        NAME: str = "MyApplication"
        DESCRIPTION: str = "MyDescription"

        # ////// WINDOW SETTINGS
        ENABLE_CUSTOM_TITLE_BAR: bool = True

        # ////// APP DIMENSIONS
        APP_MIN_SIZE: QSize = QSize(940, 560)
        APP_WIDTH: int = 1280
        APP_HEIGHT: int = 720

    # GUI SETTINGS
    # ///////////////////////////////////////////////////////////////
    class Gui:
        """Configuration de l'interface graphique."""

        # ////// THEME SETTINGS
        THEME: str = "dark"

        # ////// MENU SETTINGS
        MENU_PANEL_SHRINKED_WIDTH: int = 60
        MENU_PANEL_EXTENDED_WIDTH: int = 240

        # ////// PANEL SETTINGS
        SETTINGS_PANEL_WIDTH: int = 240
        TIME_ANIMATION: int = 400

    # THEME SETTINGS
    # ///////////////////////////////////////////////////////////////
    class Theme:
        """Configuration des thèmes."""

        def __init__(self) -> None:
            """Initialise la configuration des thèmes."""
            pass
