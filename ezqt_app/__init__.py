# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
EzQt_App package initialization.
"""
__version__ = "4.0.3.post1"

# IMPORT QT CONFIG FIRST - This ensures Qt environment is configured before any Qt imports
from .kernel import qt_config

# IMPORT GLOBALS SECOND - This ensures High DPI configuration is applied early
from .kernel import globals

# CLI
from .cli.main import cli

# MAIN
from .main import init

# APP
from .app import EzQt_App, EzApplication

# KERNEL
from .kernel import Kernel, Settings, UIFunctions, Ui_MainWindow

# WIDGETS - Import specific classes to avoid circular imports
from .widgets.core.header import Header
from .widgets.core.menu import Menu
from .widgets.core.page_container import PageContainer
from .widgets.core.settings_panel import SettingsPanel
