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
    Gestionnaire des thèmes de l'interface.

    Cette classe gère le chargement et l'application des thèmes
    QSS/CSS de l'application.
    """

    # THEME MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def theme(self, customThemeFile: str = None) -> None:
        """
        Charge et applique un thème à l'interface.

        Parameters
        ----------
        customThemeFile : str, optional
            Fichier de thème personnalisé à utiliser.
        """
        _style = ""
        # Utiliser Settings.Gui.THEME qui a été mis à jour par loadAppSettings
        _theme = Settings.Gui.THEME
        _colors = Kernel.loadKernelConfig("theme_palette")[_theme]

        # Main Theme
        # ///////////////////////////////////////////////////////////////
        if customThemeFile:
            # Utiliser Path pour gérer les chemins Windows correctement
            main_qss = APP_PATH / "bin" / "themes" / customThemeFile
            try:
                if main_qss.exists():
                    with open(main_qss, "r", encoding="utf-8") as f:
                        main_style = f.read()
                    get_printer().verbose_msg(
                        f"Fichier de thème personnalisé chargé: {main_qss}"
                    )
                else:
                    get_printer().warning(
                        f"Fichier de thème personnalisé non trouvé: {main_qss}"
                    )
                    return
            except Exception as e:
                get_printer().error(
                    f"Erreur lors de la lecture du fichier de thème personnalisé {main_qss}: {e}"
                )
                return
        else:
            # Essayer d'abord le répertoire local, puis le package
            local_qss = APP_PATH / "bin" / "themes" / "main_theme.qss"

            get_printer().verbose_msg(f"Recherche du fichier de thème:")
            get_printer().verbose_msg(f"  - Local: {local_qss}")

            if local_qss.exists():
                # Utiliser le fichier local
                try:
                    with open(local_qss, "r", encoding="utf-8") as f:
                        main_style = f.read()
                    get_printer().verbose_msg(
                        f"Fichier de thème local chargé: {local_qss}"
                    )
                except Exception as e:
                    get_printer().error(
                        f"Erreur lors de la lecture du fichier local {local_qss}: {e}"
                    )
                    return
            else:
                # Utiliser la ressource embarquée du package
                try:
                    main_style = Kernel.getPackageResourceContent(
                        "resources/themes/main_theme.qss"
                    )
                    get_printer().verbose_msg(
                        "Fichier de thème package chargé depuis les ressources embarquées"
                    )
                except Exception as e:
                    get_printer().error(
                        f"Erreur lors de la lecture de la ressource embarquée: {e}"
                    )
                    return

        # //////
        for key, color in _colors.items():
            main_style = main_style.replace(key, color)
        # //////
        _style += f"{main_style}\n"

        # //////
        self.ui.styleSheet.setStyleSheet(_style)
