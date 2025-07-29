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

"""
Helper functions for app_functions.

This module contains utility functions to simplify the use
of app_functions in client code.

Available functions:
- load_config_section: Load a configuration section
- save_config_section: Save a configuration section
- get_setting: Get a setting with fallback
- set_setting: Set a setting
- load_fonts: Load system fonts
- verify_assets: Verify asset integrity
- get_resource_path: Get a resource path
- get_kernel_instance: Get a main Kernel instance
- is_development_mode: Check if application is in development mode
- get_app_version: Get application version
- get_app_name: Get application name
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import Path
from .kernel import Kernel

# Import removed - using Kernel methods instead
from .assets_manager import AssetsManager
from .resource_manager import ResourceManager

# TYPE HINTS IMPROVEMENTS
from typing import Any, Dict, Optional

# ///////////////////////////////////////////////////////////////
# HELPERS FUNCTIONS
# ///////////////////////////////////////////////////////////////


def load_config_section(section: str) -> Dict[str, Any]:
    """
    Load a configuration section from YAML.

    Args:
        section: Name of the section to load

    Returns:
        Dict containing the section configuration

    Example:
        >>> config = load_config_section("settings_panel")
        >>> theme_config = config.get("theme", {})
    """
    from .kernel import Kernel

    return Kernel.loadKernelConfig(section)


def save_config_section(section: str, data: Dict[str, Any]) -> bool:
    """
    Save a configuration section to YAML.

    Args:
        section: Name of the section to save
        data: Data to save

    Returns:
        True if save was successful

    Example:
        >>> success = save_config_section("settings_panel", {"theme": {"default": "dark"}})
    """
    try:
        from .kernel import Kernel

        Kernel.saveKernelConfig(section, data)
        return True
    except Exception:
        return False


def get_setting(section: str, key: str, default: Any = None) -> Any:
    """
    Get a configuration setting with default value.

    Args:
        section: Configuration section
        key: Setting key
        default: Default value if not found

    Returns:
        Setting value or default value

    Example:
        >>> theme = get_setting("settings_panel", "theme.default", "dark")
        >>> width = get_setting("ui", "window.width", 800)
    """
    try:
        config = load_config_section(section)
        keys = key.split(".")
        value = config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value
    except Exception:
        return default


def set_setting(section: str, key: str, value: Any) -> bool:
    """
    Set a configuration setting.

    Args:
        section: Configuration section
        key: Setting key (can use dot notation)
        value: Value to set

    Returns:
        True if setting was successful

    Example:
        >>> success = set_setting("settings_panel", "theme.default", "light")
        >>> success = set_setting("ui", "window.width", 1024)
    """
    try:
        from .kernel import Kernel

        Kernel.writeYamlConfig([section] + key.split("."), value)
        return True
    except Exception:
        return False


def load_fonts() -> bool:
    """
    Load system fonts.

    Returns:
        True if loading was successful

    Example:
        >>> success = load_fonts()
    """
    try:
        ResourceManager.loadFontsResources()
        return True
    except Exception:
        return False


def verify_assets() -> Dict[str, bool]:
    """
    Verify asset integrity.

    Returns:
        Dict with status of each asset

    Example:
        >>> status = verify_assets()
        >>> if status.get("fonts", False):
        >>>     print("Fonts OK")
    """
    try:
        return AssetsManager.verifyAssets()
    except Exception:
        return {}


def get_resource_path(resource_type: str, name: str) -> Optional[Path]:
    """
    Get the path of a resource.

    Args:
        resource_type: Resource type ("fonts", "icons", "images", "themes")
        name: Resource name

    Returns:
        Path to the resource or None if not found

    Example:
        >>> font_path = get_resource_path("fonts", "Segoe UI.ttf")
        >>> icon_path = get_resource_path("icons", "cil-home.png")
    """
    try:
        return ResourceManager.getResourcePath(resource_type, name)
    except Exception:
        return None


def get_kernel_instance() -> Kernel:
    """
    Get a main Kernel instance.

    Returns:
        Kernel instance

    Example:
        >>> kernel = get_kernel_instance()
        >>> config = kernel.loadKernelConfig("app")
    """
    return Kernel()


def is_development_mode() -> bool:
    """
    Check if application is in development mode.

    Returns:
        True if in development mode

    Example:
        >>> if is_development_mode():
        >>>     print("Debug mode activated")
    """
    try:
        return get_setting("app", "development_mode", False)
    except Exception:
        return False


def get_app_version() -> str:
    """
    Get application version.

    Returns:
        Application version

    Example:
        >>> version = get_app_version()
        >>> print(f"Version: {version}")
    """
    try:
        return get_setting("app", "version", "1.0.0")
    except Exception:
        return "1.0.0"


def get_app_name() -> str:
    """
    Get application name.

    Returns:
        Application name

    Example:
        >>> name = get_app_name()
        >>> print(f"Application: {name}")
    """
    try:
        return get_setting("app", "name", "EzQt App")
    except Exception:
        return "EzQt App"
