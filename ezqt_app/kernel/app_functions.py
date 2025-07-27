# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import sys
import pkg_resources
from pathlib import Path
from colorama import Fore, Style
import yaml

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    QSize,
)
from PySide6.QtGui import (
    QFontDatabase,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .app_settings import Settings
from ..helper import Helper

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Dict, List, Union, Optional, Any

# VARIABLES
# ///////////////////////////////////////////////////////////////
APP_PATH: Path = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class Kernel:
    """
    Classe principale du noyau de l'application.

    Cette classe gère les ressources, la configuration et l'initialisation
    de l'application EzQt_App.
    """

    _yamlFile: Optional[Path] = None

    # ASSETS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def checkAssetsRequirements() -> None:
        """
        Vérifie et génère les ressources requises pour l'application.

        Cette méthode génère les binaires des assets, les fichiers QRC,
        les fichiers RC Python et le module de ressources de l'application.
        """
        maker = Helper.Maker()  # Utilise APP_PATH par défaut
        maker.make_assets_binaries()
        res = maker.make_qrc()
        maker.make_rc_py() if res else maker.purge_rc_py()
        maker.make_app_resources_module()
        print(Fore.LIGHTBLACK_EX + "..." + Style.RESET_ALL)

    @staticmethod
    def makeAppResourcesModule() -> None:
        """
        Génère le module de ressources de l'application.
        """
        maker = Helper.Maker()  # Utilise APP_PATH par défaut
        maker.make_app_resources_module()

    @staticmethod
    def makeRequiredFiles(mkTheme: bool = True) -> None:
        """
        Génère les fichiers requis pour l'application.

        Parameters
        ----------
        mkTheme : bool, optional
            Génère le fichier de thème (défaut: True).
        """
        # GENERATE YAML FILE
        yaml_package = Kernel.getPackageResource("app.yaml")
        yaml_application = Helper.Maker(Path.cwd()).make_yaml(yaml_package)
        Kernel.yamlFile(yaml_application)

        # GENERATE THEME FILE
        if mkTheme:
            theme_package = Kernel.getPackageResource("resources/themes/main_theme.qss")
            res = Helper.Maker(Path.cwd()).make_qss(theme_package)

        # COPY TRANSLATION FILES
        translations_package = Kernel.getPackageResource("resources/translations")
        translations_res = Helper.Maker(Path.cwd()).make_translations(
            translations_package
        )

        # PRINT STATUS
        if yaml_application or res is True or translations_res is True:
            print(Fore.LIGHTBLACK_EX + "..." + Style.RESET_ALL)

    # CONFIGURATION MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @classmethod
    def yamlFile(cls, yamlFile: Path) -> None:
        """
        Définit le fichier YAML de configuration.

        Parameters
        ----------
        yamlFile : Path
            Chemin vers le fichier YAML.
        """
        cls._yamlFile = yamlFile

    @classmethod
    def loadKernelConfig(cls, key: str) -> Dict[str, Union[str, int]]:
        """
        Charge la configuration du noyau depuis le fichier YAML.

        Parameters
        ----------
        key : str
            Clé de configuration à charger.

        Returns
        -------
        Dict[str, Union[str, int]]
            Configuration chargée.
        """
        if not cls._yamlFile:
            cls._yamlFile = Kernel.getPackageResource("app.yaml")

        with open(cls._yamlFile, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
            return data.get(key, {})

    @classmethod
    def writeYamlConfig(
        cls, keys: List[str], val: Union[str, int, Dict[str, str]]
    ) -> None:
        """
        Écrit une configuration dans le fichier YAML.

        Parameters
        ----------
        keys : List[str]
            Liste des clés pour accéder à la valeur.
        val : Union[str, int, Dict[str, str]]
            Valeur à écrire.
        """
        # Protection contre la récursion
        if not cls._yamlFile:
            cls._yamlFile = Kernel.getPackageResource("app.yaml")

        with open(cls._yamlFile, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        # Naviguer dans la structure de données
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Écrire la valeur
        current[keys[-1]] = val

        with open(cls._yamlFile, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

    # RESOURCE MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def getPackageResource(resource_path: str) -> Path:
        """
        Obtient le chemin d'une ressource du package.

        Parameters
        ----------
        resource_path : str
            Chemin de la ressource dans le package.

        Returns
        -------
        Path
            Chemin vers la ressource.
        """
        resource = Path(pkg_resources.resource_filename("ezqt_app", resource_path))
        return resource

    @staticmethod
    def loadFontsResources(app: bool = False) -> None:
        """
        Charge les ressources de polices de caractères.

        Parameters
        ----------
        app : bool, optional
            Charge depuis l'application si True, sinon depuis le package (défaut: False).
        """
        # DETERMINE FONT SOURCE
        if not app:
            fonts = Kernel.getPackageResource("resources/fonts")
            source = "Package"
        else:
            fonts = APP_PATH / r"bin\fonts"
            source = "Application"

        # LOAD FONTS
        for font in fonts.iterdir():
            if font.suffix == ".ttf":
                font_id = QFontDatabase.addApplicationFont(str(font))

                if font_id == -1:
                    print(
                        Fore.LIGHTRED_EX
                        + f"! [AppKernel] | Failed to load from {source} : {font.stem}."
                        + Style.RESET_ALL
                    )
                else:
                    print(
                        Fore.LIGHTBLUE_EX
                        + f"+ [AppKernel] | Font loaded from {source} : {font.stem}."
                        + Style.RESET_ALL
                    )

        # RECURSIVE LOAD
        if not app:
            Kernel.loadFontsResources(app=True)
            print(Fore.LIGHTBLACK_EX + "..." + Style.RESET_ALL)

    # SETTINGS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def loadAppSettings() -> Dict[str, str]:
        """
        Charge les paramètres de l'application.

        Returns
        -------
        Dict[str, str]
            Paramètres chargés.
        """
        # LOAD APP DATA
        app_data = Kernel.loadKernelConfig("app")

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
        # Charger le thème depuis settings_panel s'il existe, sinon depuis app
        try:
            settings_panel = Kernel.loadKernelConfig("settings_panel")
            Settings.Gui.THEME = settings_panel.get("theme", {}).get(
                "default", app_data["theme"]
            )
        except KeyError:
            Settings.Gui.THEME = app_data["theme"]

        Settings.Gui.MENU_PANEL_EXTENDED_WIDTH = app_data["menu_panel_extended_width"]
        Settings.Gui.MENU_PANEL_SHRINKED_WIDTH = app_data["menu_panel_shrinked_width"]
        Settings.Gui.SETTINGS_PANEL_WIDTH = app_data["settings_panel_width"]
        Settings.Gui.TIME_ANIMATION = app_data["time_animation"]

        # PRINT STATUS
        print(
            Fore.LIGHTBLUE_EX
            + f"+ [AppKernel] | Loaded Application settings."
            + Style.RESET_ALL
        )

        # PRINT CONFIGURATION
        print(
            Fore.LIGHTBLACK_EX
            + "   ┌───────────────────────────────────────────────┐"
            + Style.RESET_ALL
        )
        for key, val in app_data.items():
            print(
                Fore.LIGHTBLACK_EX
                + f"   |- {key}: "
                + Fore.LIGHTWHITE_EX
                + f"{val}"
                + Style.RESET_ALL
            )
        print(
            Fore.LIGHTBLACK_EX
            + "   └───────────────────────────────────────────────┘"
            + Style.RESET_ALL
        )

        print(Fore.LIGHTBLACK_EX + "..." + Style.RESET_ALL)
