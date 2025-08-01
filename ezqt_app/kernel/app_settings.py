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
    QSize,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# TYPE HINTS IMPROVEMENTS

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class Settings:
    """
    Main configuration class for the application.

    This class contains all application configurations
    organized in thematic subclasses.
    """

    # KERNEL SETTINGS
    # ///////////////////////////////////////////////////////////////
    class Kernel:
        """Application kernel configuration."""

        pass

    # APP SETTINGS
    # ///////////////////////////////////////////////////////////////
    class App:
        """General application configuration."""

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
        """Graphical interface configuration."""

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
        """Theme configuration."""

        def __init__(self) -> None:
            """Initialize theme configuration."""
            pass
