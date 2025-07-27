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
# ///////////////////////////////////////////////////////////////
from ...kernel.app_settings import Settings
from ...kernel.app_resources import *

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Union

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class ThemeIcon(QIcon):
    """
    Icône avec support automatique des thèmes.

    Cette classe étend QIcon pour fournir une icône qui s'adapte
    automatiquement au thème actuel (clair/sombre). L'icône change
    de couleur en fonction du thème de l'application.
    """

    def __init__(self, original_icon: Union[QIcon, str]) -> None:
        """
        Initialise l'icône avec support de thème.

        Parameters
        ----------
        original_icon : QIcon or str
            L'icône originale ou le chemin vers l'icône.
        """
        super().__init__()
        self.original_icon = (
            QIcon(original_icon) if isinstance(original_icon, str) else original_icon
        )
        self.updateIcon()
        self._connect_theme_changed()

    # ////// UTILITY FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def _connect_theme_changed(self) -> None:
        """
        Connecte au signal de changement de thème.

        Utilise un import lazy pour éviter les imports circulaires.
        """
        try:
            # Import lazy pour éviter l'import circulaire
            from ...widgets.core.ez_app import EzApplication

            EzApplication.instance().themeChanged.connect(self.updateIcon)
        except ImportError:
            # Fallback si l'import échoue
            print("Warning: Could not connect to EzApplication theme signal")

    def updateIcon(self) -> None:
        """
        Met à jour l'icône selon le thème actuel.

        Change la couleur de l'icône en fonction du thème :
        - Thème sombre : icône claire
        - Thème clair : icône sombre
        """
        icon_color = "light" if Settings.Gui.THEME == "dark" else "dark"

        # ////// GET ORIGINAL PIXMAP
        pixmap = self.original_icon.pixmap(self.original_icon.availableSizes()[0])

        # ////// CREATE IMAGE FOR MANIPULATION
        image = pixmap.toImage()

        # ////// DETERMINE NEW COLOR
        new_color = QColor(Qt.white if icon_color == "light" else Qt.black)

        # ////// CREATE NEW PIXMAP
        new_pixmap = QPixmap(image.size())
        new_pixmap.fill(Qt.transparent)

        # ////// DRAW COLORED ICON
        painter = QPainter(new_pixmap)
        painter.drawImage(0, 0, image)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), new_color)
        painter.end()

        self.addPixmap(new_pixmap)
