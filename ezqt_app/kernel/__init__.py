# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# COMMON
from .common import APP_PATH

# GLOBALS
from .globals import GLOBAL_STATE, GLOBAL_TITLE_BAR

# MAINWINDOW
from .ui_main import Ui_MainWindow

# UI FUNCTIONS
from .ui_functions import (
    UIFunctions,
    # Helpers
    maximize_window,
    restore_window,
    toggle_window_state,
    load_theme,
    apply_theme,
    animate_panel,
    select_menu_item,
    refresh_menu_style,
    setup_custom_grips,
    connect_window_events,
    get_ui_functions_instance,
    is_window_maximized,
    get_window_status,
    apply_default_theme,
    setup_window_title_bar,
)

# APP FUNCTIONS
from .app_functions import (
    Kernel,
    # Helpers
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

# APP SETTINGS
from .app_settings import Settings

# APP RESOURCES
from .app_components import Fonts, SizePolicy
from .app_resources import *

# INITIALIZATION
from .initialization import (
    Initializer,
    StartupConfig,
    InitializationSequence,
    InitStep,
    StepStatus,
    init,
    setup_project,
    generate_assets,
    configure_startup,
)

# TRANSLATION
from .translation import (
    TranslationManager,
    get_translation_manager,
    translation_manager,
    tr,
    set_tr,
    register_tr,
    unregister_tr,
    change_language,
    get_available_languages,
    get_current_language,
)
