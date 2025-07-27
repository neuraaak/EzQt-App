# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import sys
import locale
import os

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ezqt_app.kernel import Kernel

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


def init(mkTheme: bool = True) -> None:
    """
    Initialise l'application EzQt_App.

    Cette fonction configure l'encodage UTF-8 au niveau système,
    charge les ressources requises et génère les fichiers nécessaires.

    Parameters
    ----------
    mkTheme : bool, optional
        Génère le fichier de thème (défaut: True).
    """
    # ////// CONFIGURE UTF-8 ENCODING
    # Configure UTF-8 encoding at system level
    # Set UTF-8 encoding for stdout/stderr
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    # ////// SET ENVIRONMENT VARIABLES
    # Set environment variables for UTF-8
    os.environ["PYTHONIOENCODING"] = "utf-8"
    os.environ["QT_FONT_DPI"] = "96"

    # ////// SET LOCALE
    # Set locale to UTF-8
    try:
        locale.setlocale(locale.LC_ALL, "")
    except locale.Error:
        # Fallback for systems without proper locale support
        pass

    # ////// INITIALIZE KERNEL
    Kernel.checkAssetsRequirements()
    Kernel.makeRequiredFiles(mkTheme=mkTheme)
