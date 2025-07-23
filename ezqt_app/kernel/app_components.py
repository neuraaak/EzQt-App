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
# /////////////////////////////////////////////////////////////////////////////////////////////

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class Fonts:
    # Regular
    SEGOE_UI_8_REG = None
    SEGOE_UI_10_REG = None
    SEGOE_UI_12_REG = None

    # Semibold
    SEGOE_UI_8_SB = None
    SEGOE_UI_10_SB = None
    SEGOE_UI_12_SB = None

    # ///////////////////////////////////////////////////////////////
    def __init__(self) -> None:
        pass

    # ///////////////////////////////////////////////////////////////
    @classmethod
    def initFonts(cls) -> None:

        # Segoe UI - 8
        # ///////////////////////////////////////////////////////////////
        cls.SEGOE_UI_8_REG = QFont()
        cls.SEGOE_UI_8_REG.setFamily("Segoe UI")
        cls.SEGOE_UI_8_REG.setPointSize(8)
        cls.SEGOE_UI_8_REG.setBold(False)
        cls.SEGOE_UI_8_REG.setItalic(False)

        # Segoe UI - 10
        # ///////////////////////////////////////////////////////////////
        cls.SEGOE_UI_10_REG = QFont()
        cls.SEGOE_UI_10_REG.setFamily("Segoe UI")
        cls.SEGOE_UI_10_REG.setPointSize(10)
        cls.SEGOE_UI_10_REG.setBold(False)
        cls.SEGOE_UI_10_REG.setItalic(False)

        # Segoe UI - 12
        # ///////////////////////////////////////////////////////////////
        cls.SEGOE_UI_12_REG = QFont()
        cls.SEGOE_UI_12_REG.setFamily("Segoe UI")
        cls.SEGOE_UI_12_REG.setPointSize(12)
        cls.SEGOE_UI_12_REG.setBold(False)
        cls.SEGOE_UI_12_REG.setItalic(False)

        # Segoe UI Semibold - 8
        # ///////////////////////////////////////////////////////////////
        cls.SEGOE_UI_8_SB = QFont()
        cls.SEGOE_UI_8_SB.setFamily("Segoe UI Semibold")
        cls.SEGOE_UI_8_SB.setPointSize(8)
        cls.SEGOE_UI_8_SB.setBold(False)
        cls.SEGOE_UI_8_SB.setItalic(False)

        # Segoe UI Semibold - 10
        # ///////////////////////////////////////////////////////////////
        cls.SEGOE_UI_10_SB = QFont()
        cls.SEGOE_UI_10_SB.setFamily("Segoe UI Semibold")
        cls.SEGOE_UI_10_SB.setPointSize(10)
        cls.SEGOE_UI_10_SB.setBold(False)
        cls.SEGOE_UI_10_SB.setItalic(False)

        # Segoe UI Semibold - 12
        # ///////////////////////////////////////////////////////////////
        cls.SEGOE_UI_12_SB = QFont()
        cls.SEGOE_UI_12_SB.setFamily("Segoe UI Semibold")
        cls.SEGOE_UI_12_SB.setPointSize(12)
        cls.SEGOE_UI_12_SB.setBold(False)
        cls.SEGOE_UI_12_SB.setItalic(False)


# ///////////////////////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////


class SizePolicy:
    # Horizontal priority
    H_EXPANDING_V_FIXED = None
    H_EXPANDING_V_PREFERRED = None

    # Vertical priority
    H_PREFERRED_V_EXPANDING = None

    # No priority
    H_EXPANDING_V_EXPANDING = None

    # ///////////////////////////////////////////////////////////////
    def __init__(self) -> None:
        pass

    # ///////////////////////////////////////////////////////////////
    @classmethod
    def initSizePolicy(cls) -> None:

        # Horizontal Expanding - Vertical Fixed
        # ///////////////////////////////////////////////////////////////
        cls.H_EXPANDING_V_FIXED = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cls.H_EXPANDING_V_FIXED.setHorizontalStretch(0)
        cls.H_EXPANDING_V_FIXED.setVerticalStretch(0)

        # Horizontal Expanding - Vertical Preferred
        # ///////////////////////////////////////////////////////////////
        cls.H_EXPANDING_V_PREFERRED = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Preferred
        )
        cls.H_EXPANDING_V_PREFERRED.setHorizontalStretch(0)
        cls.H_EXPANDING_V_PREFERRED.setVerticalStretch(0)

        # Horizontal Preferred - Vertical Expanding
        # ///////////////////////////////////////////////////////////////
        cls.H_PREFERRED_V_EXPANDING = QSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding
        )
        cls.H_PREFERRED_V_EXPANDING.setHorizontalStretch(0)
        cls.H_PREFERRED_V_EXPANDING.setVerticalStretch(0)

        # Horizontal Expanding - Vertical Expanding
        # ///////////////////////////////////////////////////////////////
        cls.H_EXPANDING_V_EXPANDING = QSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        cls.H_EXPANDING_V_EXPANDING.setHorizontalStretch(0)
        cls.H_EXPANDING_V_EXPANDING.setVerticalStretch(0)
