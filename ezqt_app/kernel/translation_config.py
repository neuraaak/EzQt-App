# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import Dict, Any

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Dict

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////

# SUPPORTED LANGUAGES
# ///////////////////////////////////////////////////////////////

# Langues supportées
SUPPORTED_LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {"name": "English", "native_name": "English", "file": "ezqt_app_en.ts"},
    "fr": {"name": "Français", "native_name": "Français", "file": "ezqt_app_fr.ts"},
    "es": {"name": "Español", "native_name": "Español", "file": "ezqt_app_es.ts"},
    "de": {"name": "Deutsch", "native_name": "Deutsch", "file": "ezqt_app_de.ts"},
}

# DEFAULT SETTINGS
# ///////////////////////////////////////////////////////////////

# Langue par défaut
DEFAULT_LANGUAGE: str = "en"

# Dossier des traductions
TRANSLATIONS_DIR: str = "resources/translations"
