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

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class AssetsManager:
    """
    Gestionnaire des assets de l'application.

    Cette classe gère la génération et la vérification des ressources
    requises pour l'application EzQt_App.
    """

    # ASSETS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def check_assets_requirements() -> None:
        """
        Vérifie et génère les ressources requises pour l'application.

        Cette méthode génère les binaires des assets, les fichiers QRC,
        les fichiers RC Python et le module de ressources de l'application.
        """
        maker = FileMaker()  # Utilise APP_PATH par défaut
        maker.make_assets_binaries()
        res = maker.make_qrc()
        maker.make_rc_py() if res else maker.purge_rc_py()
        maker.make_app_resources_module()
        printer = get_printer()
        printer.verbose_msg("...")

    @staticmethod
    def make_app_resources_module() -> None:
        """
        Génère le module de ressources de l'application.
        """
        maker = FileMaker()  # Utilise APP_PATH par défaut
        maker.make_app_resources_module()

    @staticmethod
    def make_required_files(mk_theme: bool = True) -> None:
        """
        Génère les fichiers requis pour l'application.

        Parameters
        ----------
        mk_theme : bool, optional
            Génère le fichier de thème (défaut: True).
        """
        from .config_manager import ConfigManager

        # GENERATE YAML FILE
        yaml_package = ConfigManager.get_package_resource("app.yaml")
        yaml_application = FileMaker(Path.cwd()).make_yaml_from_package(yaml_package)
        ConfigManager.set_yaml_file(yaml_application)

        # GENERATE THEME FILE
        res = None
        if mk_theme:
            theme_package = ConfigManager.get_package_resource(
                "resources/themes/main_theme.qss"
            )
            res = FileMaker(Path.cwd()).make_qss_from_package(theme_package)

        # COPY TRANSLATION FILES
        translations_package = ConfigManager.get_package_resource(
            "resources/translations"
        )
        translations_res = FileMaker(Path.cwd()).make_translations_from_package(
            translations_package
        )

        # PRINT STATUS
        if yaml_application or res is True or translations_res is True:
            printer = get_printer()
            printer.verbose_msg("...")
