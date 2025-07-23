# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import Dict, List

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    Signal,
    QPropertyAnimation,
    QEasingCurve,
)
from PySide6.QtWidgets import (
    QFrame,
    QSizePolicy,
    QGridLayout,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .framed_label import FramedLabel
from ...kernel.app_settings import Settings

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> FUNCTIONS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class ToggleRadio(QFrame):
    clicked = Signal()

    # ///////////////////////////////////////////////////////////////
    def __init__(
        self, items: List[str], default: str = "", parent=None, *args, **kwargs
    ) -> None:
        super().__init__(parent, *args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # //////
        self._value = ""
        self._options_list = items
        self._default = default
        self._options: Dict[str, FramedLabel] = {}
        # //////
        self.initUI()

    # ///////////////////////////////////////////////////////////////

    def initUI(self) -> None:
        self.grid = QGridLayout(self)
        self.grid.setObjectName("grid")
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(4, 4, 4, 4)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # //////
        self.selector = QFrame(self)
        self.selector.setObjectName("selector")

        # //////
        for option in self._options_list:  # Exemple avec trois labels
            self.add_option(option_text=option)

    # ///////////////////////////////////////////////////////////////

    def initialize_selector(self, default: str = "") -> None:
        self._default = default
        # //////
        if self._options:
            # //////
            first_option_key = next(iter(self._options_list), None)
            selected_option = self._options.get(
                self._default.capitalize(), self._options.get(first_option_key)
            )
            default_pos = self.grid.indexOf(selected_option)

            # //////
            self.grid.addWidget(self.selector, 0, default_pos)
            self.selector.lower()  # S'assure que le selector reste en dessous
            self.selector.update()  # Force le rafraîchissement si nécessaire

    # ///////////////////////////////////////////////////////////////

    def add_option(self, option_text: str) -> None:
        option = FramedLabel(option_text, self)
        option.setObjectName(f"opt_{option_text}")
        option.setFrameShape(QFrame.NoFrame)
        option.setFrameShadow(QFrame.Raised)
        option.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # //////
        self.grid.addWidget(option, 0, len(self._options.items()))

        # //////
        option.mousePressEvent = lambda event, option=option: self.toggle_selection(
            option
        )
        self._options[option_text] = option

    # ///////////////////////////////////////////////////////////////

    def get_value_option(self) -> FramedLabel | None:
        return self._options.get(self._value)

    # ///////////////////////////////////////////////////////////////

    def toggle_selection(self, option: FramedLabel) -> None:
        self._value = option.text()
        # //////
        self.clicked.emit()
        self.move_selector(option)

    # ///////////////////////////////////////////////////////////////

    def move_selector(self, option: FramedLabel) -> None:

        # Variables d'animation
        start_pos = self.selector.pos()
        end_pos = option.pos()
        # //////
        self.selector.setGeometry(option.geometry())
        self.selector.lower()  # S'assure que le selector reste en dessous
        self.selector.update()  # Force le rafraîchissement si nécessaire

        # ANIMATION
        self.selector_animation = QPropertyAnimation(self.selector, b"pos")
        self.selector_animation.setDuration(Settings.Gui.TIME_ANIMATION)
        self.selector_animation.setStartValue(start_pos)
        self.selector_animation.setEndValue(end_pos)
        self.selector_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.selector_animation.start()
