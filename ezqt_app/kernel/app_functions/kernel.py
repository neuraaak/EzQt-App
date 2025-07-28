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
from .assets_manager import AssetsManager
from .config_manager import ConfigManager
from .resource_manager import ResourceManager
from .settings_manager import SettingsManager

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class Kernel:
    """
    Classe principale du noyau de l'application.

    Cette classe gère les ressources, la configuration et l'initialisation
    de l'application EzQt_App en utilisant des gestionnaires spécialisés.
    """

    # ASSETS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def checkAssetsRequirements() -> None:
        """
        Vérifie et génère les ressources requises pour l'application.

        Cette méthode génère les binaires des assets, les fichiers QRC,
        les fichiers RC Python et le module de ressources de l'application.
        """
        AssetsManager.check_assets_requirements()

    @staticmethod
    def makeAppResourcesModule() -> None:
        """
        Génère le module de ressources de l'application.
        """
        AssetsManager.make_app_resources_module()

    @staticmethod
    def makeRequiredFiles(mkTheme: bool = True) -> None:
        """
        Génère les fichiers requis pour l'application.

        Parameters
        ----------
        mkTheme : bool, optional
            Génère le fichier de thème (défaut: True).
        """
        AssetsManager.make_required_files(mkTheme)

    # CONFIGURATION MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @classmethod
    def yamlFile(cls, yamlFile) -> None:
        """
        Définit le fichier YAML de configuration.

        Parameters
        ----------
        yamlFile : Path
            Chemin vers le fichier YAML.
        """
        ConfigManager.set_yaml_file(yamlFile)

    @classmethod
    def getConfigPath(cls, config_name: str):
        """
        Obtient le chemin du fichier de configuration.

        Parameters
        ----------
        config_name : str
            Nom de la configuration.

        Returns
        -------
        Path
            Chemin vers le fichier de configuration.
        """
        return ConfigManager.get_config_path(config_name)

    @classmethod
    def loadKernelConfig(cls, config_name: str):
        """
        Charge la configuration du noyau depuis le fichier YAML.

        Parameters
        ----------
        config_name : str
            Nom de la configuration à charger.

        Returns
        -------
        Dict[str, Union[str, int]]
            Configuration chargée.
        """
        return ConfigManager.load_kernel_config(config_name)

    @classmethod
    def saveKernelConfig(cls, config_name: str, data):
        """
        Sauvegarde une configuration dans un fichier YAML.

        Parameters
        ----------
        config_name : str
            Nom de la configuration.
        data : Dict[str, Any]
            Données à sauvegarder.
        """
        ConfigManager.save_kernel_config(config_name, data)

    @classmethod
    def writeYamlConfig(cls, keys, val):
        """
        Écrit une configuration dans le fichier YAML.

        Parameters
        ----------
        keys : List[str]
            Liste des clés pour accéder à la valeur.
        val : Union[str, int, Dict[str, str]]
            Valeur à écrire.
        """
        ConfigManager.write_yaml_config(keys, val)

    # RESOURCE MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def getPackageResource(resource_path: str):
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
        return ConfigManager.get_package_resource(resource_path)

    @staticmethod
    def getPackageResourceContent(resource_path: str) -> str:
        """
        Obtient le contenu d'une ressource du package.

        Parameters
        ----------
        resource_path : str
            Chemin de la ressource dans le package.

        Returns
        -------
        str
            Contenu de la ressource.
        """
        return ConfigManager.get_package_resource_content(resource_path)

    @staticmethod
    def loadFontsResources(app: bool = False) -> None:
        """
        Charge les ressources de polices de caractères.

        Parameters
        ----------
        app : bool, optional
            Charge depuis l'application si True, sinon depuis le package (défaut: False).
        """
        ResourceManager.load_fonts_resources(app)

    # SETTINGS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def loadAppSettings():
        """
        Charge les paramètres de l'application.

        Returns
        -------
        Dict[str, str]
            Paramètres chargés.
        """
        return SettingsManager.load_app_settings()
