# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import sys
import pkg_resources
from pathlib import Path
from typing import Dict, List
from colorama import Fore, Style
import yaml
import ruamel.yaml

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import (
    QSize,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .app_settings import Settings
from ..helper import Helper

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////
APP_PATH = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class Kernel:
    _yamlFile: None | Path = None

    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def checkAssetsRequirements() -> None:
        # //////
        maker = Helper.Maker()  # Utilise APP_PATH par défaut
        maker.make_assets_binaries()
        res = maker.make_qrc()
        maker.make_rc_py() if res else maker.purge_rc_py()
        maker.make_app_resources_module()
        # //////
        print(Fore.LIGHTBLACK_EX + "..." + Style.RESET_ALL)

    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def makeAppResourcesModule() -> None:
        # //////
        maker = Helper.Maker()  # Utilise APP_PATH par défaut
        maker.make_app_resources_module()

    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def makeRequiredFiles(mkTheme: bool = True) -> None:
        # //////
        yaml_package = Kernel.getPackageResource("app.yaml")
        yaml_application = Helper.Maker(Path.cwd()).make_yaml(yaml_package)
        Kernel.yamlFile(yaml_application)
        # //////
        if mkTheme:
            theme_package = Kernel.getPackageResource("resources/themes/main_theme.qss")
            res = Helper.Maker(Path.cwd()).make_qss(theme_package)

        # //////
        # Copier les fichiers de traduction
        translations_package = Kernel.getPackageResource("resources/translations")
        translations_res = Helper.Maker(Path.cwd()).make_translations(translations_package)

        # //////
        if yaml_application or res is True or translations_res is True:
            print(Fore.LIGHTBLACK_EX + "..." + Style.RESET_ALL)

    # ///////////////////////////////////////////////////////////////

    @classmethod
    def yamlFile(cls, yamlFile: Path) -> None:
        # //////
        cls._yamlFile = yamlFile

    # ///////////////////////////////////////////////////////////////

    @classmethod
    def loadKernelConfig(cls, key: str) -> Dict[str, str | int]:
        # //////
        if not cls._yamlFile:
            cls._yamlFile = Kernel.getPackageResource("app.yaml")

        # //////
        with open(cls._yamlFile, "r", encoding='utf-8') as file:
            data = yaml.safe_load(file)
            # //////
            return data[key]

    # ///////////////////////////////////////////////////////////////

    @classmethod
    def writeYamlConfig(cls, keys: List[str], val: str | int | Dict[str, str]) -> None:
        # Protection contre la récursion
        if not hasattr(cls, '_writing_yaml'):
            cls._writing_yaml = False
        
        if cls._writing_yaml:
            return  # Éviter la récursion
        
        cls._writing_yaml = True
        
        try:
            yaml = ruamel.yaml.YAML()

            # //////
            with open(cls._yamlFile, "r", encoding='utf-8') as file:
                data = yaml.load(file)

            # //////
            d = data
            for key in keys[:-1]:
                d = d.setdefault(
                    key, ruamel.yaml.comments.CommentedMap()
                )  # Aller au niveau de la clé ou créer un nouveau dict
            d[keys[-1]] = val  # Mettre à jour la valeur de la dernière clé

            # //////
            with open(cls._yamlFile, "w", encoding='utf-8') as file:
                yaml.dump(data, file)
        finally:
            cls._writing_yaml = False

    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def getPackageResource(resource_path: str) -> Path:
        resource = Path(pkg_resources.resource_filename("ezqt_app", resource_path))
        return resource

    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def loadFontsResources(app: bool = False) -> None:
        # //////
        if not app:
            fonts = Kernel.getPackageResource("resources/fonts")
            source = "Package"
        else:
            fonts = APP_PATH / r"bin\fonts"
            source = "Application"

        # //////
        for font in fonts.iterdir():
            # //////
            if font.suffix == ".ttf":
                font_id = QFontDatabase.addApplicationFont(str(font))
                # //////
                if font_id == -1:
                    print(
                        Fore.LIGHTRED_EX
                        + f"! [AppKernel] | Failed to load from {source} : {font.stem}."
                        + Style.RESET_ALL
                    )
                # //////
                else:
                    print(
                        Fore.LIGHTBLUE_EX
                        + f"+ [AppKernel] | Font loaded from {source} : {font.stem}."
                        + Style.RESET_ALL
                    )

        # //////
        if not app:
            Kernel.loadFontsResources(app=True)
            # //////
            print(Fore.LIGHTBLACK_EX + "..." + Style.RESET_ALL)

    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def loadAppSettings() -> Dict[str, str] | Dict[str, str]:
        # //////
        app_data = Kernel.loadKernelConfig("app")

        # //////
        Settings.App.NAME = app_data["name"]
        Settings.App.DESCRIPTION = app_data["description"]
        # //////
        Settings.App.ENABLE_CUSTOM_TITLE_BAR = True
        # //////
        Settings.App.APP_MIN_SIZE = QSize(
            app_data["app_min_width"], app_data["app_min_height"]
        )
        Settings.App.APP_WIDTH = app_data["app_width"]
        Settings.App.APP_HEIGHT = app_data["app_height"]

        # //////
        # Charger le thème depuis settings_panel s'il existe, sinon depuis app
        try:
            settings_panel = Kernel.loadKernelConfig("settings_panel")
            Settings.Gui.THEME = settings_panel.get("theme", {}).get("default", app_data["theme"])
        except KeyError:
            Settings.Gui.THEME = app_data["theme"]
            
        Settings.Gui.MENU_PANEL_EXTENDED_WIDTH = app_data["menu_panel_extended_width"]
        Settings.Gui.MENU_PANEL_SHRINKED_WIDTH = app_data["menu_panel_shrinked_width"]
        Settings.Gui.SETTINGS_PANEL_WIDTH = app_data["settings_panel_width"]
        Settings.Gui.TIME_ANIMATION = app_data["time_animation"]

        # //////
        print(
            Fore.LIGHTBLUE_EX
            + f"+ [AppKernel] | Loaded Application settings."
            + Style.RESET_ALL
        )
        # //////
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

        # //////
        print(Fore.LIGHTBLACK_EX + "..." + Style.RESET_ALL)
