# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import locale
import os

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Signal,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Any

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class EzApplication(QApplication):
    """
    Application principale étendue avec support des thèmes et encodage UTF-8.

    Cette classe hérite de QApplication et ajoute des fonctionnalités
    pour la gestion des thèmes et l'encodage UTF-8.
    """

    themeChanged = Signal()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialise l'application avec support UTF-8 et haute résolution.

        Parameters
        ----------
        *args : Any
            Arguments positionnels passés à QApplication.
        **kwargs : Any
            Arguments nommés passés à QApplication.
        """
        super().__init__(*args, **kwargs)

        # ////// CONFIGURE HIGH DPI SCALING
        self.setAttribute(Qt.AA_EnableHighDpiScaling, True)

        # ////// CONFIGURE UTF-8 ENCODING
        try:
            locale.setlocale(locale.LC_ALL, "")
        except locale.Error:
            pass

        # ////// SET ENVIRONMENT VARIABLES
        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["QT_FONT_DPI"] = "96"
