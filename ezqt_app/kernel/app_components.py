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

# TYPE HINTS IMPROVEMENTS
from typing import Optional

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class Fonts:
    """
    Font management class.

    This class provides predefined Segoe UI fonts
    with different sizes and styles (Regular, Semibold).
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
        """Initialize the Fonts class."""
        pass

    @classmethod
    def initFonts(cls) -> None:
        """
        Initialize all fonts.

        This method must be called at application startup
        to configure all Segoe UI fonts.
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
    Size policy management class.

    This class provides predefined size policies
    for different types of Qt widgets.
    """

    # ////// HORIZONTAL PRIORITY
    H_EXPANDING_V_FIXED: Optional[QSizePolicy] = None
    H_EXPANDING_V_PREFERRED: Optional[QSizePolicy] = None

    # ////// VERTICAL PRIORITY
    H_PREFERRED_V_EXPANDING: Optional[QSizePolicy] = None

    # ////// NO PRIORITY
    H_EXPANDING_V_EXPANDING: Optional[QSizePolicy] = None

    def __init__(self) -> None:
        """Initialize the SizePolicy class."""
        pass

    @classmethod
    def initSizePolicy(cls) -> None:
        """
        Initialize all size policies.

        This method must be called at application startup
        to configure all predefined size policies.
        """
        # ////// HORIZONTAL EXPANDING - VERTICAL FIXED
        cls.H_EXPANDING_V_FIXED = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        cls.H_EXPANDING_V_FIXED.setHorizontalStretch(0)
        cls.H_EXPANDING_V_FIXED.setVerticalStretch(0)

        # ////// HORIZONTAL EXPANDING - VERTICAL PREFERRED
        cls.H_EXPANDING_V_PREFERRED = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        cls.H_EXPANDING_V_PREFERRED.setHorizontalStretch(0)
        cls.H_EXPANDING_V_PREFERRED.setVerticalStretch(0)

        # ////// HORIZONTAL PREFERRED - VERTICAL EXPANDING
        cls.H_PREFERRED_V_EXPANDING = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        cls.H_PREFERRED_V_EXPANDING.setHorizontalStretch(0)
        cls.H_PREFERRED_V_EXPANDING.setVerticalStretch(0)

        # ////// HORIZONTAL EXPANDING - VERTICAL EXPANDING
        cls.H_EXPANDING_V_EXPANDING = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        cls.H_EXPANDING_V_EXPANDING.setHorizontalStretch(0)
        cls.H_EXPANDING_V_EXPANDING.setVerticalStretch(0)
