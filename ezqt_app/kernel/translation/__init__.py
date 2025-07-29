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
from .config import (
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
    TRANSLATIONS_DIR,
)
from .manager import (
    TranslationManager,
    get_translation_manager,
    translation_manager,
)
from .helpers import (
    tr,
    set_tr,
    register_tr,
    unregister_tr,
    change_language,
    get_available_languages,
    get_current_language,
    enable_auto_translation,
    get_auto_translation_stats,
    clear_auto_translation_cache,
    translate_auto,
    scan_widgets_for_translation,
    register_widgets_manually,
    scan_and_register_widgets,
    get_translation_stats,
    collect_strings_from_widget,
    collect_and_compare_strings,
    get_new_strings,
    mark_strings_as_registered,
    get_string_collector_stats,
)

## ==> EXPORTS
# ///////////////////////////////////////////////////////////////
__all__ = [
    # Configuration
    "SUPPORTED_LANGUAGES",
    "DEFAULT_LANGUAGE",
    "TRANSLATIONS_DIR",
    # Manager
    "TranslationManager",
    "get_translation_manager",
    "translation_manager",
    # Helper functions
    "tr",
    "set_tr",
    "register_tr",
    "unregister_tr",
    "change_language",
    "get_available_languages",
    "get_current_language",
    "enable_auto_translation",
    "get_auto_translation_stats",
    "clear_auto_translation_cache",
    "translate_auto",
    "scan_widgets_for_translation",
    "register_widgets_manually",
    "scan_and_register_widgets",
    "get_translation_stats",
    "collect_strings_from_widget",
    "collect_and_compare_strings",
    "get_new_strings",
    "mark_strings_as_registered",
    "mark_strings_as_processed",
    "get_string_collector_stats",
]
