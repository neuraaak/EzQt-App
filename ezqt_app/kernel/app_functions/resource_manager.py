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
from PySide6.QtGui import QFontDatabase

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import APP_PATH
from .printer import get_printer

# TYPE HINTS IMPROVEMENTS

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class ResourceManager:
    """
    System resource manager.

    This class manages the loading of fonts and other
    system resources required by the application.
    """

    # RESOURCE MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def load_fonts_resources(app: bool = False) -> None:
        """
        Load font resources.

        Parameters
        ----------
        app : bool, optional
            Load from application if True, otherwise from package (default: False).
        """
        from .config_manager import get_package_resource

        # DETERMINE FONT SOURCE
        if not app:
            fonts = get_package_resource("resources/fonts")
            source = "Package"
        else:
            fonts = APP_PATH / r"bin\fonts"
            source = "Application"

        # LOAD FONTS
        for font in fonts.iterdir():
            if font.suffix == ".ttf":
                font_id = QFontDatabase.addApplicationFont(str(font))

                printer = get_printer()
                if font_id == -1:
                    printer.error(
                        f"[AppKernel] Failed to load from {source} : {font.stem}."
                    )
                else:
                    printer.info(
                        f"[AppKernel] Font loaded from {source} : {font.stem}."
                    )

        # RECURSIVE LOAD
        if not app:
            ResourceManager.load_fonts_resources(app=True)
