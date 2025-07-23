# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QPainter,
    QPixmap,
    QIcon,
    QColor,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from .ez_app import EzApplication
from ...kernel.app_settings import Settings
from ...kernel.app_resources import *

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class ThemeIcon(QIcon):
    def __init__(self, original_icon: QIcon) -> None:
        super().__init__()
        self.original_icon = (
            QIcon(original_icon) if isinstance(original_icon, str) else original_icon
        )
        self.updateIcon()
        # //////
        EzApplication.instance().themeChanged.connect(self.updateIcon)

    # ///////////////////////////////////////////////////////////////

    def updateIcon(self) -> None:
        icon_color = "light" if Settings.Gui.THEME == "dark" else "dark"

        # Get the QPixmap from the original QIcon
        pixmap = self.original_icon.pixmap(self.original_icon.availableSizes()[0])

        # Create an image for manipulation
        image = pixmap.toImage()

        # Determine the new color
        new_color = QColor(
            Qt.GlobalColor.white if icon_color == "light" else Qt.GlobalColor.black
        )

        # Create a new QPixmap to draw the colored icon
        new_pixmap = QPixmap(image.size())
        new_pixmap.fill(Qt.transparent)

        # Draw the new colored icon
        painter = QPainter(new_pixmap)
        painter.drawImage(0, 0, image)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), new_color)
        painter.end()

        self.addPixmap(new_pixmap)
