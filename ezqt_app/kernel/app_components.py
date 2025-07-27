# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtGui import (
    QFont,
)
from PySide6.QtWidgets import (
    QSizePolicy,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Optional

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class Fonts:
    """
    Classe de gestion des polices de caractères.

    Cette classe fournit des polices Segoe UI prédéfinies
    avec différentes tailles et styles (Regular, Semibold).
    """

    # ////// REGULAR FONTS
    SEGOE_UI_8_REG: Optional[QFont] = None
    SEGOE_UI_10_REG: Optional[QFont] = None
    SEGOE_UI_12_REG: Optional[QFont] = None

    # ////// SEMIBOLD FONTS
    SEGOE_UI_8_SB: Optional[QFont] = None
    SEGOE_UI_10_SB: Optional[QFont] = None
    SEGOE_UI_12_SB: Optional[QFont] = None

    def __init__(self) -> None:
        """Initialise la classe Fonts."""
        pass

    @classmethod
    def initFonts(cls) -> None:
        """
        Initialise toutes les polices de caractères.

        Cette méthode doit être appelée au démarrage de l'application
        pour configurer toutes les polices Segoe UI.
        """
        # ////// SEGOE UI REGULAR - 8
        cls.SEGOE_UI_8_REG = QFont()
        cls.SEGOE_UI_8_REG.setFamily("Segoe UI")
        cls.SEGOE_UI_8_REG.setPointSize(8)
        cls.SEGOE_UI_8_REG.setBold(False)
        cls.SEGOE_UI_8_REG.setItalic(False)

        # ////// SEGOE UI REGULAR - 10
        cls.SEGOE_UI_10_REG = QFont()
        cls.SEGOE_UI_10_REG.setFamily("Segoe UI")
        cls.SEGOE_UI_10_REG.setPointSize(10)
        cls.SEGOE_UI_10_REG.setBold(False)
        cls.SEGOE_UI_10_REG.setItalic(False)

        # ////// SEGOE UI REGULAR - 12
        cls.SEGOE_UI_12_REG = QFont()
        cls.SEGOE_UI_12_REG.setFamily("Segoe UI")
        cls.SEGOE_UI_12_REG.setPointSize(12)
        cls.SEGOE_UI_12_REG.setBold(False)
        cls.SEGOE_UI_12_REG.setItalic(False)

        # ////// SEGOE UI SEMIBOLD - 8
        cls.SEGOE_UI_8_SB = QFont()
        cls.SEGOE_UI_8_SB.setFamily("Segoe UI Semibold")
        cls.SEGOE_UI_8_SB.setPointSize(8)
        cls.SEGOE_UI_8_SB.setBold(False)
        cls.SEGOE_UI_8_SB.setItalic(False)

        # ////// SEGOE UI SEMIBOLD - 10
        cls.SEGOE_UI_10_SB = QFont()
        cls.SEGOE_UI_10_SB.setFamily("Segoe UI Semibold")
        cls.SEGOE_UI_10_SB.setPointSize(10)
        cls.SEGOE_UI_10_SB.setBold(False)
        cls.SEGOE_UI_10_SB.setItalic(False)

        # ////// SEGOE UI SEMIBOLD - 12
        cls.SEGOE_UI_12_SB = QFont()
        cls.SEGOE_UI_12_SB.setFamily("Segoe UI Semibold")
        cls.SEGOE_UI_12_SB.setPointSize(12)
        cls.SEGOE_UI_12_SB.setBold(False)
        cls.SEGOE_UI_12_SB.setItalic(False)


class SizePolicy:
    """
    Classe de gestion des politiques de taille.

    Cette classe fournit des politiques de taille prédéfinies
    pour différents types de widgets Qt.
    """

    # ////// HORIZONTAL PRIORITY
    H_EXPANDING_V_FIXED: Optional[QSizePolicy] = None
    H_EXPANDING_V_PREFERRED: Optional[QSizePolicy] = None

    # ////// VERTICAL PRIORITY
    H_PREFERRED_V_EXPANDING: Optional[QSizePolicy] = None

    # ////// NO PRIORITY
    H_EXPANDING_V_EXPANDING: Optional[QSizePolicy] = None

    def __init__(self) -> None:
        """Initialise la classe SizePolicy."""
        pass

    @classmethod
    def initSizePolicy(cls) -> None:
        """
        Initialise toutes les politiques de taille.

        Cette méthode doit être appelée au démarrage de l'application
        pour configurer toutes les politiques de taille prédéfinies.
        """
        # ////// HORIZONTAL EXPANDING - VERTICAL FIXED
        cls.H_EXPANDING_V_FIXED = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cls.H_EXPANDING_V_FIXED.setHorizontalStretch(0)
        cls.H_EXPANDING_V_FIXED.setVerticalStretch(0)

        # ////// HORIZONTAL EXPANDING - VERTICAL PREFERRED
        cls.H_EXPANDING_V_PREFERRED = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )
        cls.H_EXPANDING_V_PREFERRED.setHorizontalStretch(0)
        cls.H_EXPANDING_V_PREFERRED.setVerticalStretch(0)

        # ////// HORIZONTAL PREFERRED - VERTICAL EXPANDING
        cls.H_PREFERRED_V_EXPANDING = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding
        )
        cls.H_PREFERRED_V_EXPANDING.setHorizontalStretch(0)
        cls.H_PREFERRED_V_EXPANDING.setVerticalStretch(0)

        # ////// HORIZONTAL EXPANDING - VERTICAL EXPANDING
        cls.H_EXPANDING_V_EXPANDING = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        cls.H_EXPANDING_V_EXPANDING.setHorizontalStretch(0)
        cls.H_EXPANDING_V_EXPANDING.setVerticalStretch(0)
