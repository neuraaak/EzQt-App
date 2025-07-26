# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import List

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QSize,
    QRect,
    QMargins,
)
from PySide6.QtGui import (
    QPixmap,
    QCursor,
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
    QSpacerItem,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from ...kernel.app_components import *
from ...kernel.app_resources import *

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class Header(QFrame):
    _buttons: List[QPushButton] = []
    _icons: List = []  # Type hint removed to avoid circular import

    # ///////////////////////////////////////////////////////////////

    def __init__(
        self,
        app_name: str = "",
        description: str = "",
        parent: QWidget = None,
        *args,
        **kwargs
    ) -> None:
        super(Header, self).__init__(parent, *args, **kwargs)

        # ///////////////////////////////////////////////////////////////

        self.setObjectName("headerContainer")
        self.setFixedHeight(50)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        SizePolicy.H_EXPANDING_V_PREFERRED.setHeightForWidth(
            self.sizePolicy().hasHeightForWidth()
        )
        # //////
        self.HL_headerContainer = QHBoxLayout(self)
        self.HL_headerContainer.setSpacing(0)
        self.HL_headerContainer.setObjectName("HL_headerContainer")
        self.HL_headerContainer.setContentsMargins(0, 0, 10, 0)

        # /////////////////////////////////////////////////////////////////////

        self.headerMetaInfo = QFrame(self)
        self.headerMetaInfo.setObjectName("headerMetaInfo")
        self.headerMetaInfo.setMinimumSize(QSize(0, 50))
        self.headerMetaInfo.setMaximumSize(QSize(16777215, 50))
        self.headerMetaInfo.setFrameShape(QFrame.NoFrame)
        self.headerMetaInfo.setFrameShadow(QFrame.Raised)
        #
        self.HL_headerContainer.addWidget(self.headerMetaInfo)

        # /////////////////////////////////////////////////////////////////////

        self.headerAppLogo = QLabel(self.headerMetaInfo)
        self.headerAppLogo.setObjectName("headerAppLogo")
        self.headerAppLogo.setGeometry(QRect(10, 4, 40, 40))
        self.headerAppLogo.setMinimumSize(QSize(40, 40))
        self.headerAppLogo.setMaximumSize(QSize(40, 40))
        self.headerAppLogo.setFrameShape(QFrame.NoFrame)
        self.headerAppLogo.setFrameShadow(QFrame.Raised)
        # //////
        self.headerAppName = QLabel(app_name, self.headerMetaInfo)
        self.headerAppName.setObjectName("headerAppName")
        self.headerAppName.setGeometry(QRect(65, 6, 160, 20))
        self.headerAppName.setFont(Fonts.SEGOE_UI_12_SB)
        self.headerAppName.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        # //////
        self.headerAppDescription = QLabel(description, self.headerMetaInfo)
        self.headerAppDescription.setObjectName("headerAppDescription")
        self.headerAppDescription.setGeometry(QRect(65, 26, 160, 16))
        self.headerAppDescription.setMaximumSize(QSize(16777215, 16))
        self.headerAppDescription.setFont(Fonts.SEGOE_UI_8_REG)
        self.headerAppDescription.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop
        )

        # /////////////////////////////////////////////////////////////////////
        self.headerHSpacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        #
        self.HL_headerContainer.addItem(self.headerHSpacer)

        # /////////////////////////////////////////////////////////////////////

        self.headerButtons = QFrame(self)
        self.headerButtons.setObjectName("headerButtons")
        self.headerButtons.setMinimumSize(QSize(0, 28))
        self.headerButtons.setFrameShape(QFrame.NoFrame)
        self.headerButtons.setFrameShadow(QFrame.Raised)
        #
        self.HL_headerContainer.addWidget(self.headerButtons, 0, Qt.AlignRight)
        # //////
        self.HL_headerButtons = QHBoxLayout(self.headerButtons)
        self.HL_headerButtons.setSpacing(5)
        self.HL_headerButtons.setObjectName("HL_headerButtons")
        self.HL_headerButtons.setContentsMargins(0, 0, 0, 0)

        # /////////////////////////////////////////////////////////////////////

        # Lazy import to avoid circular imports
        from ...widgets.extended.theme_icon import ThemeIcon

        self.settingsTopBtn = QPushButton(self.headerButtons)
        self._buttons.append(self.settingsTopBtn)
        self.settingsTopBtn.setObjectName("settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.PointingHandCursor))
        #
        icon_settings = ThemeIcon(Icons.icon_settings)
        self._icons.append(icon_settings)
        self.settingsTopBtn.setIcon(icon_settings)
        self.settingsTopBtn.setIconSize(QSize(20, 20))
        #
        self.HL_headerButtons.addWidget(self.settingsTopBtn)
        # //////
        self.minimizeAppBtn = QPushButton(self.headerButtons)
        self._buttons.append(self.minimizeAppBtn)
        self.minimizeAppBtn.setObjectName("minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        #
        icon_minimize = ThemeIcon(Icons.icon_minimize)
        self._icons.append(icon_minimize)
        self.minimizeAppBtn.setIcon(icon_minimize)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))
        #
        self.HL_headerButtons.addWidget(self.minimizeAppBtn)
        # //////
        self.maximizeRestoreAppBtn = QPushButton(self.headerButtons)
        self._buttons.append(self.maximizeRestoreAppBtn)
        self.maximizeRestoreAppBtn.setObjectName("maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setFont(Fonts.SEGOE_UI_10_REG)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        #
        icon_maximize = ThemeIcon(Icons.icon_maximize)
        self._icons.append(icon_maximize)
        self.maximizeRestoreAppBtn.setIcon(icon_maximize)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))
        #
        self.HL_headerButtons.addWidget(self.maximizeRestoreAppBtn)
        # //////
        self.closeAppBtn = QPushButton(self.headerButtons)
        self._buttons.append(self.closeAppBtn)
        self.closeAppBtn.setObjectName("closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.PointingHandCursor))
        #
        icon_close = ThemeIcon(Icons.icon_close)
        self._icons.append(icon_close)
        self.closeAppBtn.setIcon(icon_close)
        self.closeAppBtn.setIconSize(QSize(20, 20))
        #
        self.HL_headerButtons.addWidget(self.closeAppBtn)

    # ///////////////////////////////////////////////////////////////

    def set_app_name(self, app_name: str) -> None:
        self.headerAppName.setText(app_name)

    # ///////////////////////////////////////////////////////////////

    def set_app_description(self, description: str) -> None:
        self.headerAppDescription.setText(description)

    # ///////////////////////////////////////////////////////////////

    def set_app_logo(
        self, logo: str | QPixmap, y_shrink: int = 0, y_offset: int = 0
    ) -> None:
        # ///////////////////////////////////////////////////////////////
        def offsetY(y_offset=0, x_offset=0) -> None:
            # Obtenir le QRect actuel du widget
            current_rect = self.headerAppLogo.geometry()

            # Créer un nouveau QRect avec l'offset Y appliqué
            new_rect = QRect(
                current_rect.x() + x_offset,
                current_rect.y() + y_offset,
                current_rect.width(),
                current_rect.height(),
            )

            # Appliquer le nouveau QRect au widget
            self.headerAppLogo.setGeometry(new_rect)

        # ///////////////////////////////////////////////////////////////
        pixmap_logo = QPixmap(logo) if isinstance(logo, str) else logo
        if pixmap_logo.size() != self.headerAppLogo.minimumSize():
            pixmap_logo = pixmap_logo.scaled(
                self.headerAppLogo.minimumSize().shrunkBy(
                    QMargins(0, y_shrink, 0, y_shrink)
                ),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        # //////
        self.headerAppLogo.setPixmap(pixmap_logo)
        offsetY(y_offset, y_shrink)

    # ///////////////////////////////////////////////////////////////

    def update_all_theme_icons(self) -> None:
        for i, btn in enumerate(self._buttons):
            btn.setIcon(self._icons[i])
