# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
EzQt_App package initialization.
"""
__version__ = "3.2.0"

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
