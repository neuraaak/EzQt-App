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
from ..common import Path
from .printer import get_printer
from .file_maker import FileMaker

# TYPE HINTS IMPROVEMENTS

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class AssetsManager:
    """
    Application assets manager.

    This class manages the generation and verification of resources
    required for the EzQt_App application.
    """

    # ASSETS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def check_assets_requirements() -> None:
        """
        Check and generate required resources for the application.

        This method generates asset binaries, QRC files,
        Python RC files and the application resources module.
        """
        maker = FileMaker()  # Uses APP_PATH by default
        maker.make_assets_binaries()
        res = maker.make_qrc()
        maker.make_rc_py() if res else maker.purge_rc_py()
        maker.make_app_resources_module()

    @staticmethod
    def make_app_resources_module() -> None:
        """
        Generate the application resources module.
        """
        maker = FileMaker()  # Uses APP_PATH by default
        maker.make_app_resources_module()

    @staticmethod
    def make_required_files(mk_theme: bool = True) -> None:
        """
        Generate required files for the application.

        Parameters
        ----------
        mk_theme : bool, optional
            Generate theme file (default: True).
        """
        from .config_manager import get_package_resource

        # GENERATE YAML FILE
        yaml_package = get_package_resource("app.yaml")
        yaml_application = FileMaker(Path.cwd()).make_yaml_from_package(yaml_package)

        # GENERATE THEME FILE
        res = None
        if mk_theme:
            theme_package = get_package_resource("resources/themes/main_theme.qss")
            res = FileMaker(Path.cwd()).make_qss_from_package(theme_package)

        # COPY TRANSLATION FILES
        translations_package = get_package_resource("resources/translations")
        translations_res = FileMaker(Path.cwd()).make_translations_from_package(
            translations_package
        )
