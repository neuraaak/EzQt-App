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
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import APP_PATH
from .printer import get_printer

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class ConfigManager:
    """Modular configuration manager for EzQt_App"""

    def __init__(self):
        self._config_cache: Dict[str, Any] = {}
        self._config_files: Dict[str, Path] = {}
        self._project_root: Optional[Path] = None

    def set_project_root(self, project_root: Path):
        """Set the project root directory"""
        self._project_root = project_root

    def get_config_paths(self, config_name: str) -> List[Path]:
        """
        Return the list of possible paths for a configuration file.

        Parameters
        ----------
        config_name : str
            Configuration file name (e.g., "app", "palette", "languages")

        Returns
        -------
        List[Path]
            List of possible paths in priority order
        """
        config_file = f"{config_name}.yaml"

        paths = []

        # 1. Child project (bin/config/)
        if self._project_root:
            project_config = self._project_root / "bin" / "config" / config_file
            paths.append(project_config)

        # 2. Current directory (bin/config/)
        current_config = Path.cwd() / "bin" / "config" / config_file
        paths.append(current_config)

        # 3. Package (resources/config/) - from current directory
        package_config = Path.cwd() / "ezqt_app" / "resources" / "config" / config_file
        paths.append(package_config)

        # 4. Package (resources/config/) - from APP_PATH
        package_config_app = APP_PATH / "resources" / "config" / config_file
        paths.append(package_config_app)

        return paths

    def load_config(
        self, config_name: str, force_reload: bool = False
    ) -> Dict[str, Any]:
        """
        Load a configuration from the appropriate file.

        Parameters
        ----------
        config_name : str
            Configuration file name
        force_reload : bool
            Force reload even if cached

        Returns
        -------
        Dict[str, Any]
            Loaded configuration
        """
        # Check cache
        if not force_reload and config_name in self._config_cache:
            return self._config_cache[config_name]

        # Get possible paths
        config_paths = self.get_config_paths(config_name)

        # Find the first existing file
        config_file = None
        for path in config_paths:
            if path.exists():
                config_file = path
                break

        if not config_file:
            get_printer().warning(f"No configuration file found for '{config_name}'")
            get_printer().verbose_msg(f"Searched paths: {config_paths}")
            return {}

        # Load configuration
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

            # Cache
            self._config_cache[config_name] = config_data
            self._config_files[config_name] = config_file

            get_printer().verbose_msg(
                f"Configuration '{config_name}' loaded from: {config_file}"
            )

            return config_data

        except Exception as e:
            get_printer().error(f"Error loading '{config_name}': {e}")
            return {}

    def get_config_value(
        self, config_name: str, key_path: str, default: Any = None
    ) -> Any:
        """
        Get a specific value from a configuration.

        Parameters
        ----------
        config_name : str
            Configuration file name
        key_path : str
            Key path (e.g., "app.name", "theme_palette.dark")
        default : Any
            Default value if key doesn't exist

        Returns
        -------
        Any
            Found value or default value
        """
        config = self.load_config(config_name)

        # Navigate structure
        keys = key_path.split(".")
        current = config

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default

        return current

    def save_config(self, config_name: str, config_data: Dict[str, Any]) -> bool:
        """
        Save a configuration to the project file.

        Parameters
        ----------
        config_name : str
            Configuration file name
        config_data : Dict[str, Any]
            Data to save

        Returns
        -------
        bool
            True if save successful
        """
        if not self._project_root:
            get_printer().error("No project root defined")
            return False

        # Create config directory if it doesn't exist
        config_dir = self._project_root / "bin" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = config_dir / f"{config_name}.yaml"

        try:
            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)

            # Update cache
            self._config_cache[config_name] = config_data
            self._config_files[config_name] = config_file

            get_printer().verbose_msg(
                f"Configuration '{config_name}' saved: {config_file}"
            )
            return True

        except Exception as e:
            get_printer().error(f"Error saving '{config_name}': {e}")
            return False

    def copy_package_configs_to_project(self) -> bool:
        """
        Copy package configurations to child project.

        Returns
        -------
        bool
            True if copy successful
        """
        if not self._project_root:
            get_printer().error("No project root defined")
            return False

        # Find package configuration directory
        package_config_dir = None

        # Function to find EzQt_App package
        def find_ezqt_package():
            # 1. Search in current directory and parents
            current = Path.cwd()
            while current.parent != current:  # As long as we're not at system root
                ezqt_path = current / "ezqt_app"
                if ezqt_path.exists() and (ezqt_path / "resources" / "config").exists():
                    return ezqt_path
                current = current.parent

            # 2. Search in Python paths
            import sys

            for path in sys.path:
                ezqt_path = Path(path) / "ezqt_app"
                if ezqt_path.exists() and (ezqt_path / "resources" / "config").exists():
                    return ezqt_path

            return None

        # Find EzQt_App package
        ezqt_package = find_ezqt_package()
        if ezqt_package:
            package_config_dir = ezqt_package / "resources" / "config"
            get_printer().verbose_msg(f"EzQt_App package found: {ezqt_package}")
            get_printer().verbose_msg(f"Configuration directory: {package_config_dir}")
        else:
            # Fallback to old paths
            possible_paths = [
                Path.cwd() / "ezqt_app" / "resources" / "config",
                APP_PATH / "resources" / "config",
                APP_PATH / "ezqt_app" / "resources" / "config",
            ]

            for path in possible_paths:
                if path.exists():
                    package_config_dir = path
                    get_printer().verbose_msg(
                        f"Configuration directory found (fallback): {path}"
                    )
                    break

        if not package_config_dir:
            get_printer().error(
                f"EzQt_App package not found. Tested paths: {[str(p) for p in [Path.cwd(), APP_PATH]]}"
            )
            return False

        project_config_dir = self._project_root / "bin" / "config"

        # Create destination directory
        project_config_dir.mkdir(parents=True, exist_ok=True)

        copied_files = []

        try:
            for config_file in package_config_dir.glob("*.yaml"):
                target_file = project_config_dir / config_file.name

                # Don't overwrite if file already exists
                if target_file.exists():
                    get_printer().verbose_msg(f"Existing file, ignored: {target_file}")
                    continue

                # Copy file
                import shutil

                shutil.copy2(config_file, target_file)
                copied_files.append(config_file.name)
                get_printer().info(f"Configuration copied: {config_file.name}")

            if copied_files:
                get_printer().info(
                    f"✅ {len(copied_files)} configurations copied to project"
                )

            return True

        except Exception as e:
            get_printer().error(f"Error copying configurations: {e}")
            return False

    def clear_cache(self):
        """Clear configuration cache"""
        self._config_cache.clear()
        self._config_files.clear()
        get_printer().verbose_msg("Configuration cache cleared")

    def get_loaded_configs(self) -> Dict[str, Path]:
        """Return list of loaded configurations"""
        return self._config_files.copy()


# Global configuration manager instance
_config_manager = None


def get_config_manager() -> ConfigManager:
    """Return global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


def load_config(config_name: str) -> Dict[str, Any]:
    """Load a configuration"""
    return get_config_manager().load_config(config_name)


def get_config_value(config_name: str, key_path: str, default: Any = None) -> Any:
    """Get a configuration value"""
    return get_config_manager().get_config_value(config_name, key_path, default)


def save_config(config_name: str, config_data: Dict[str, Any]) -> bool:
    """Save a configuration"""
    return get_config_manager().save_config(config_name, config_data)


def get_package_resource(resource_path: str) -> Path:
    """
    Get the path of a package resource.

    Parameters
    ----------
    resource_path : str
        Resource path in package.

    Returns
    -------
    Path
        Path to resource.
    """
    try:
        import pkg_resources

        resource = Path(pkg_resources.resource_filename("ezqt_app", resource_path))
        return resource
    except Exception as e:
        # Fallback to relative path
        fallback_path = APP_PATH / "ezqt_app" / resource_path
        return fallback_path


def get_package_resource_content(resource_path: str) -> str:
    """
    Get the content of a package resource.

    Parameters
    ----------
    resource_path : str
        Resource path in package.

    Returns
    -------
    str
        Resource content.
    """
    try:
        import pkg_resources

        content = pkg_resources.resource_string("ezqt_app", resource_path)
        return content.decode("utf-8")
    except Exception as e:
        # Fallback to file reading
        file_path = get_package_resource(resource_path)
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            raise FileNotFoundError(f"Resource not found: {resource_path}")
