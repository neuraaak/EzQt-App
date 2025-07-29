# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import APP_PATH
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

# Classe principale qui combine tous les managers
from .kernel import Kernel

# FILE MAKER
from .file_maker import FileMaker

# HELPERS
from .helpers import (
    load_config_section,
    save_config_section,
    get_setting,
    set_setting,
    load_fonts,
    verify_assets,
    get_resource_path,
    get_kernel_instance,
    is_development_mode,
    get_app_version,
    get_app_name,
)

## ==> EXPORTS
# ///////////////////////////////////////////////////////////////
__all__ = [
    "AssetsManager",
    "ResourceManager",
    "SettingsManager",
    "FileMaker",
    "APP_PATH",
    "Kernel",
    # Config functions
    "get_config_manager",
    "load_config",
    "get_config_value",
    "save_config",
    "get_package_resource",
    "get_package_resource_content",
    # Helpers
    "load_config_section",
    "save_config_section",
    "get_setting",
    "set_setting",
    "load_fonts",
    "verify_assets",
    "get_resource_path",
    "get_kernel_instance",
    "is_development_mode",
    "get_app_version",
    "get_app_name",
]
