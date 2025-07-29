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
from ..common import APP_PATH
from ..app_functions.printer import get_printer
from ..app_settings import Settings
from ..app_functions import Kernel

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class ThemeManager:
    """
    Interface theme manager.

    This class manages the loading and application of QSS/CSS
    themes in the application.
    """

    # THEME MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def theme(self, customThemeFile: str = None) -> None:
        """
        Load and apply theme to interface.

        Parameters
        ----------
        customThemeFile : str, optional
            Custom theme file to use.
        """
        _style = ""
        # Use Settings.Gui.THEME which has been updated by loadAppSettings
        _theme = Settings.Gui.THEME
        # Load palette from palette.yaml file
        palette_config = Kernel.loadKernelConfig("palette")
        _colors = palette_config.get("theme_palette", {}).get(_theme, {})

        # Main Theme
        # ///////////////////////////////////////////////////////////////
        if customThemeFile:
            # Use Path to handle Windows paths correctly
            main_qss = APP_PATH / "bin" / "themes" / customThemeFile
            try:
                if main_qss.exists():
                    with open(main_qss, "r", encoding="utf-8") as f:
                        main_style = f.read()
                    get_printer().verbose_msg(f"Custom theme file loaded: {main_qss}")
                else:
                    get_printer().warning(f"Custom theme file not found: {main_qss}")
                    return
            except Exception as e:
                get_printer().error(f"Error reading custom theme file {main_qss}: {e}")
                return
        else:
            # Try local directory first, then package
            local_qss = APP_PATH / "bin" / "themes" / "main_theme.qss"

            get_printer().verbose_msg(f"Searching for theme file:")
            get_printer().verbose_msg(f"  - Local: {local_qss}")

            if local_qss.exists():
                # Use local file
                try:
                    with open(local_qss, "r", encoding="utf-8") as f:
                        main_style = f.read()
                    get_printer().verbose_msg(f"Local theme file loaded: {local_qss}")
                except Exception as e:
                    get_printer().error(f"Error reading local file {local_qss}: {e}")
                    return
            else:
                # Use embedded package resource
                try:
                    main_style = Kernel.getPackageResourceContent(
                        "resources/themes/main_theme.qss"
                    )
                    get_printer().verbose_msg(
                        "Package theme file loaded from embedded resources"
                    )
                except Exception as e:
                    get_printer().error(f"Error reading embedded resource: {e}")
                    return

        # //////
        for key, color in _colors.items():
            main_style = main_style.replace(key, color)
        # //////
        _style += f"{main_style}\n"

        # //////
        self.ui.styleSheet.setStyleSheet(_style)
