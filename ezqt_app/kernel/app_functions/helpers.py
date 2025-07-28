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
Helpers pour app_functions
==========================

Ce module contient des fonctions utilitaires pour simplifier l'utilisation
des app_functions dans le code client.

Fonctions disponibles:
- load_config_section: Charge une section de configuration
- save_config_section: Sauvegarde une section de configuration
- get_setting: Récupère un paramètre avec fallback
- set_setting: Définit un paramètre
- load_fonts: Charge les polices système
- verify_assets: Vérifie l'intégrité des assets
- get_resource_path: Obtient le chemin d'une ressource
- get_kernel_instance: Obtient une instance du Kernel principal
- is_development_mode: Vérifie si l'application est en mode développement
- get_app_version: Obtient la version de l'application
- get_app_name: Obtient le nom de l'application
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import Path
from .kernel import Kernel
from .config_manager import ConfigManager
from .assets_manager import AssetsManager
from .resource_manager import ResourceManager

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Any, Dict, Optional

# ///////////////////////////////////////////////////////////////
# HELPERS FUNCTIONS
# ///////////////////////////////////////////////////////////////


def load_config_section(section: str) -> Dict[str, Any]:
    """
    Charge une section de configuration depuis le YAML.

    Args:
        section: Nom de la section à charger

    Returns:
        Dict contenant la configuration de la section

    Example:
        >>> config = load_config_section("settings_panel")
        >>> theme_config = config.get("theme", {})
    """
    return ConfigManager.loadKernelConfig(section)


def save_config_section(section: str, data: Dict[str, Any]) -> bool:
    """
    Sauvegarde une section de configuration dans le YAML.

    Args:
        section: Nom de la section à sauvegarder
        data: Données à sauvegarder

    Returns:
        True si la sauvegarde a réussi

    Example:
        >>> success = save_config_section("settings_panel", {"theme": {"default": "dark"}})
    """
    try:
        ConfigManager.writeKernelConfig(section, data)
        return True
    except Exception:
        return False


def get_setting(section: str, key: str, default: Any = None) -> Any:
    """
    Récupère un paramètre de configuration avec valeur par défaut.

    Args:
        section: Section de configuration
        key: Clé du paramètre
        default: Valeur par défaut si non trouvée

    Returns:
        Valeur du paramètre ou valeur par défaut

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
    Définit un paramètre de configuration.

    Args:
        section: Section de configuration
        key: Clé du paramètre (peut utiliser la notation pointée)
        value: Valeur à définir

    Returns:
        True si la définition a réussi

    Example:
        >>> success = set_setting("settings_panel", "theme.default", "light")
        >>> success = set_setting("ui", "window.width", 1024)
    """
    try:
        ConfigManager.writeYamlConfig([section] + key.split("."), value)
        return True
    except Exception:
        return False


def load_fonts() -> bool:
    """
    Charge les polices système.

    Returns:
        True si le chargement a réussi

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
    Vérifie l'intégrité des assets.

    Returns:
        Dict avec le statut de chaque asset

    Example:
        >>> status = verify_assets()
        >>> if status.get("fonts", False):
        >>>     print("Polices OK")
    """
    try:
        return AssetsManager.verifyAssets()
    except Exception:
        return {}


def get_resource_path(resource_type: str, name: str) -> Optional[Path]:
    """
    Obtient le chemin d'une ressource.

    Args:
        resource_type: Type de ressource ("fonts", "icons", "images", "themes")
        name: Nom de la ressource

    Returns:
        Chemin vers la ressource ou None si non trouvée

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
    Obtient une instance du Kernel principal.

    Returns:
        Instance du Kernel

    Example:
        >>> kernel = get_kernel_instance()
        >>> config = kernel.loadKernelConfig("app")
    """
    return Kernel()


def is_development_mode() -> bool:
    """
    Vérifie si l'application est en mode développement.

    Returns:
        True si en mode développement

    Example:
        >>> if is_development_mode():
        >>>     print("Mode debug activé")
    """
    try:
        return get_setting("app", "development_mode", False)
    except Exception:
        return False


def get_app_version() -> str:
    """
    Obtient la version de l'application.

    Returns:
        Version de l'application

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
    Obtient le nom de l'application.

    Returns:
        Nom de l'application

    Example:
        >>> name = get_app_name()
        >>> print(f"Application: {name}")
    """
    try:
        return get_setting("app", "name", "EzQt App")
    except Exception:
        return "EzQt App"
