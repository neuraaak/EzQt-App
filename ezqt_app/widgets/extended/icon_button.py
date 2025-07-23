# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QIcon,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QToolButton,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ...kernel.app_components import SizePolicy

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> FUNCTIONS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class IconButton(QToolButton):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.setProperty("type", "IconButton")
        self.setContentsMargins(10, 0, 0, 0)

        self.icon_label = QLabel()
        self.text_label = QLabel()

        # Appliquer des styles au QLabel pour gérer l'alignement du texte
        self.text_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        # Configuration de la disposition
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)  # Espace entre l'icône et le texte
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)

        # Configurer le bouton pour s'étendre
        self.setSizePolicy(SizePolicy.H_EXPANDING_V_EXPANDING)

        # //////
        self.text_label.hide()

    # ///////////////////////////////////////////////////////////////

    def setIcon(self, icon_path) -> None:
        icon = icon_path if isinstance(icon_path, QIcon) else QIcon(icon_path)
        self.icon_label.setPixmap(
            icon.pixmap(QSize(24, 24))
        )  # Ajuster la taille de l'icône
        self.icon_label.setFixedSize(24, 24)  # Fixer la taille du QLabel de l'icône
        self.icon_label.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

    # ///////////////////////////////////////////////////////////////

    def setText(self, text) -> None:
        self.text_label.setText(text)

    # ///////////////////////////////////////////////////////////////

    def setTextAlignment(self, alignment) -> None:
        self.text_label.setAlignment(alignment)

    # ///////////////////////////////////////////////////////////////

    def setSpacing(self, spacing) -> None:
        layout = self.layout()
        layout.setSpacing(spacing)

    # ///////////////////////////////////////////////////////////////

    def sizeHint(self) -> QSize:
        return QSize(100, 40)  # Taille suggérée du bouton

    # ///////////////////////////////////////////////////////////////

    def toggleTextVisibility(self) -> None:
        if self.text_label.isHidden():
            self.text_label.show()
        # //////
        else:
            self.text_label.hide()
