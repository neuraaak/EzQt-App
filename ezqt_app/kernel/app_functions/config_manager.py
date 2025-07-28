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
import pkg_resources
import yaml

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import APP_PATH, Path

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Dict, List, Union, Optional, Any

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class ConfigManager:
    """
    Gestionnaire de configuration YAML.

    Cette classe gère le chargement, la sauvegarde et la manipulation
    des fichiers de configuration YAML de l'application.
    """

    _yaml_file: Optional[Path] = None

    # CONFIGURATION MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @classmethod
    def set_yaml_file(cls, yaml_file: Path) -> None:
        """
        Définit le fichier YAML de configuration.

        Parameters
        ----------
        yaml_file : Path
            Chemin vers le fichier YAML.
        """
        cls._yaml_file = yaml_file

    @classmethod
    def get_config_path(cls, config_name: str) -> Path:
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
        return APP_PATH / f"{config_name}.yaml"

    @classmethod
    def load_kernel_config(cls, config_name: str) -> Dict[str, Union[str, int]]:
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

        Raises
        ------
        FileNotFoundError
            Si le fichier de configuration n'existe pas.
        yaml.YAMLError
            Si le fichier YAML est invalide.
        KeyError
            Si la section demandée n'existe pas dans le fichier.
        """
        # Utiliser le fichier app.yaml unifié
        if not cls._yaml_file:
            cls._yaml_file = cls.get_package_resource("app.yaml")

        try:
            with open(cls._yaml_file, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                if data is None:
                    return {}
                return data.get(config_name, {})
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in {cls._yaml_file}: {e}")

    @classmethod
    def save_kernel_config(cls, config_name: str, data: Dict[str, Any]) -> None:
        """
        Sauvegarde une configuration dans un fichier YAML.

        Parameters
        ----------
        config_name : str
            Nom de la configuration.
        data : Dict[str, Any]
            Données à sauvegarder.
        """
        config_file = cls.get_config_path(config_name)

        # Créer le répertoire parent s'il n'existe pas
        config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(config_file, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

    @classmethod
    def write_yaml_config(
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
        if not cls._yaml_file:
            cls._yaml_file = cls.get_package_resource("app.yaml")

        with open(cls._yaml_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        # Naviguer dans la structure de données
        current = data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Écrire la valeur
        current[keys[-1]] = val

        with open(cls._yaml_file, "w", encoding="utf-8") as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

    # RESOURCE MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def get_package_resource(resource_path: str) -> Path:
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
        try:
            # Utiliser pkg_resources pour accéder aux ressources embarquées
            resource = Path(pkg_resources.resource_filename("ezqt_app", resource_path))
            return resource
        except Exception as e:
            # Fallback vers le chemin relatif si pkg_resources échoue
            from ..common import APP_PATH

            fallback_path = APP_PATH / "ezqt_app" / resource_path
            return fallback_path

    @staticmethod
    def get_package_resource_content(resource_path: str) -> str:
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
        try:
            # Utiliser pkg_resources pour lire directement le contenu
            content = pkg_resources.resource_string("ezqt_app", resource_path)
            return content.decode("utf-8")
        except Exception as e:
            # Fallback vers la lecture de fichier
            file_path = ConfigManager.get_package_resource(resource_path)
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                raise FileNotFoundError(f"Resource not found: {resource_path}")
