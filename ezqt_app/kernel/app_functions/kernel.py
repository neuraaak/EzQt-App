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
from .config_manager import (
    get_config_manager,
    load_config,
    get_config_value,
    save_config,
    get_package_resource,
    get_package_resource_content,
)
from .resource_manager import ResourceManager
from .settings_manager import SettingsManager

# TYPE HINTS IMPROVEMENTS

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class Kernel:
    """
    Main application kernel class.

    This class manages resources, configuration and initialization
    of the EzQt_App application using specialized managers.
    """

    # ASSETS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def checkAssetsRequirements() -> None:
        """
        Check and generate required resources for the application.

        This method generates asset binaries, QRC files,
        Python RC files and the application resources module.
        """
        AssetsManager.check_assets_requirements()

    @staticmethod
    def makeAppResourcesModule() -> None:
        """
        Generate the application resources module.
        """
        AssetsManager.make_app_resources_module()

    @staticmethod
    def makeRequiredFiles(mkTheme: bool = True) -> None:
        """
        Generate required files for the application.

        Parameters
        ----------
        mkTheme : bool, optional
            Generate theme file (default: True).
        """
        AssetsManager.make_required_files(mkTheme)

    # CONFIGURATION MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @classmethod
    def setProjectRoot(cls, project_root) -> None:
        """
        Set the project root directory.

        Parameters
        ----------
        project_root : Path
            Path to the project root directory.
        """
        get_config_manager().set_project_root(project_root)

    @classmethod
    def loadKernelConfig(cls, config_name: str):
        """
        Load kernel configuration from YAML file.

        Parameters
        ----------
        config_name : str
            Name of the configuration to load.

        Returns
        -------
        Dict[str, Any]
            Loaded configuration.
        """
        return load_config(config_name)

    @classmethod
    def getConfigValue(cls, config_name: str, key_path: str, default=None):
        """
        Get a specific value from a configuration.

        Parameters
        ----------
        config_name : str
            Configuration name.
        key_path : str
            Key path (e.g., "app.name", "theme_palette.dark").
        default : Any
            Default value if key doesn't exist.

        Returns
        -------
        Any
            Found value or default value.
        """
        return get_config_value(config_name, key_path, default)

    @classmethod
    def saveKernelConfig(cls, config_name: str, data):
        """
        Save a configuration to a YAML file.

        Parameters
        ----------
        config_name : str
            Configuration name.
        data : Dict[str, Any]
            Data to save.
        """
        return save_config(config_name, data)

    @classmethod
    def copyPackageConfigsToProject(cls):
        """
        Copy package configurations to child project.
        """
        return get_config_manager().copy_package_configs_to_project()

    @classmethod
    def writeYamlConfig(cls, keys, val):
        """
        Write configuration to YAML file (compatibility method).

        Parameters
        ----------
        keys : List[str]
            List of keys to access the value.
        val : Union[str, int, Dict[str, str]]
            Value to write.
        """
        # For compatibility, load current config and update
        if keys:
            config_name = keys[0]  # First element as config name
            config = load_config(config_name)

            # Navigate through structure
            current = config
            for key in keys[1:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]

            # Write the value
            current[keys[-1]] = val

            # Save
            save_config(config_name, config)

    # RESOURCE MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def getPackageResource(resource_path: str):
        """
        Get the path of a package resource.

        Parameters
        ----------
        resource_path : str
            Resource path in the package.

        Returns
        -------
        Path
            Path to the resource.
        """
        return get_package_resource(resource_path)

    @staticmethod
    def getPackageResourceContent(resource_path: str) -> str:
        """
        Get the content of a package resource.

        Parameters
        ----------
        resource_path : str
            Resource path in the package.

        Returns
        -------
        str
            Resource content.
        """
        return get_package_resource_content(resource_path)

    @staticmethod
    def loadFontsResources(app: bool = False) -> None:
        """
        Load font resources.

        Parameters
        ----------
        app : bool, optional
            Load from application if True, otherwise from package (default: False).
        """
        ResourceManager.load_fonts_resources(app)

    # SETTINGS MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def loadAppSettings():
        """
        Load application settings.

        Returns
        -------
        Dict[str, str]
            Loaded settings.
        """
        return SettingsManager.load_app_settings()
