# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# MAINWINDOW
from .ui_main import Ui_MainWindow

# UI FUNCTIONS
from .ui_functions import UIFunctions

# APP FUNCTIONS
from .app_functions import Kernel

# APP SETTINGS
from .app_settings import Settings

# APP RESOURCES
from .app_components import Fonts, SizePolicy
from .app_resources import *
from .translation_manager import get_translation_manager, translation_manager
from .translation_helpers import tr, set_tr, register_tr, unregister_tr, change_language, get_available_languages, get_current_language