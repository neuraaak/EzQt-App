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
import yaml
from .printer import get_printer

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import QSize

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import Path
from ..app_settings import Settings

# TYPE HINTS IMPROVEMENTS
from typing import Dict, Optional

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class SettingsManager:
    """
    Application settings manager.

    This class manages the loading and configuration of application
    settings from configuration files.
    """

    # SETTINGS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def load_app_settings(yaml_file: Optional[Path] = None) -> Dict[str, str]:
        """
        Load application settings.

        Parameters
        ----------
        yaml_file : Optional[Path], optional
            YAML file to use (default: uses default file).

        Returns
        -------
        Dict[str, str]
            Loaded settings.
        """
        from .config_manager import get_package_resource

        # LOAD APP DATA
        if not yaml_file:
            yaml_file = get_package_resource("app.yaml")

        with open(yaml_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            app_data = data.get("app", {})

        # SET APP SETTINGS
        Settings.App.NAME = app_data["name"]
        Settings.App.DESCRIPTION = app_data["description"]
        Settings.App.ENABLE_CUSTOM_TITLE_BAR = True

        # SET DIMENSIONS
        Settings.App.APP_MIN_SIZE = QSize(
            app_data["app_min_width"], app_data["app_min_height"]
        )
        Settings.App.APP_WIDTH = app_data["app_width"]
        Settings.App.APP_HEIGHT = app_data["app_height"]

        # SET GUI SETTINGS
        # Load theme from settings_panel if it exists, otherwise from app
        try:
            settings_panel = data.get("settings_panel", {})
            Settings.Gui.THEME = settings_panel.get("theme", {}).get(
                "default", app_data["theme"]
            )
        except KeyError:
            Settings.Gui.THEME = app_data["theme"]

        Settings.Gui.MENU_PANEL_EXTENDED_WIDTH = app_data["menu_panel_extended_width"]
        Settings.Gui.MENU_PANEL_SHRINKED_WIDTH = app_data["menu_panel_shrinked_width"]
        Settings.Gui.SETTINGS_PANEL_WIDTH = app_data["settings_panel_width"]
        Settings.Gui.TIME_ANIMATION = app_data["time_animation"]

        # PRINT STATUS AND CONFIGURATION
        from .printer import Printer

        printer = Printer(verbose=True)  # Force verbose mode to display ASCII frame
        printer.config_display(app_data)

        return app_data
