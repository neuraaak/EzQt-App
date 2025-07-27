# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

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
# ///////////////////////////////////////////////////////////////
from ...kernel.app_components import *
from ...kernel.app_resources import *

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import List, Optional, Union, Any

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class Header(QFrame):
    """
    En-tête de l'application avec logo, nom et boutons de contrôle.

    Cette classe fournit une barre d'en-tête personnalisable avec
    le logo de l'application, son nom, sa description et les boutons
    de contrôle de fenêtre (minimiser, maximiser, fermer).
    """

    # ////// CLASS VARIABLES
    _buttons: List[QPushButton] = []
    _icons: List = []  # Type hint removed to avoid circular import

    def __init__(
        self,
        app_name: str = "",
        description: str = "",
        parent: Optional[QWidget] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Initialise l'en-tête de l'application.

        Parameters
        ----------
        app_name : str, optional
            Nom de l'application (défaut: "").
        description : str, optional
            Description de l'application (défaut: "").
        parent : QWidget, optional
            Le widget parent (défaut: None).
        *args : Any
            Arguments positionnels supplémentaires.
        **kwargs : Any
            Arguments nommés supplémentaires.
        """
        super().__init__(parent, *args, **kwargs)

        # ////// SETUP WIDGET PROPERTIES
        self.setObjectName("headerContainer")
        self.setFixedHeight(50)
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        # Vérifier si SizePolicy est initialisé, sinon utiliser une politique par défaut
        if (
            hasattr(SizePolicy, "H_EXPANDING_V_PREFERRED")
            and SizePolicy.H_EXPANDING_V_PREFERRED is not None
        ):
            self.setSizePolicy(SizePolicy.H_EXPANDING_V_PREFERRED)
            SizePolicy.H_EXPANDING_V_PREFERRED.setHeightForWidth(
                self.sizePolicy().hasHeightForWidth()
            )
        else:
            # Utiliser une politique de taille par défaut si SizePolicy n'est pas initialisé
            default_policy = QSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
            )
            default_policy.setHorizontalStretch(0)
            default_policy.setVerticalStretch(0)
            self.setSizePolicy(default_policy)

        # ////// SETUP MAIN LAYOUT
        self.HL_headerContainer = QHBoxLayout(self)
        self.HL_headerContainer.setSpacing(0)
        self.HL_headerContainer.setObjectName("HL_headerContainer")
        self.HL_headerContainer.setContentsMargins(0, 0, 10, 0)

        # ////// SETUP META INFO SECTION
        self.headerMetaInfo = QFrame(self)
        self.headerMetaInfo.setObjectName("headerMetaInfo")
        self.headerMetaInfo.setMinimumSize(QSize(0, 50))
        self.headerMetaInfo.setMaximumSize(QSize(16777215, 50))
        self.headerMetaInfo.setFrameShape(QFrame.NoFrame)
        self.headerMetaInfo.setFrameShadow(QFrame.Raised)
        self.HL_headerContainer.addWidget(self.headerMetaInfo)

        # ////// SETUP APP LOGO
        self.headerAppLogo = QLabel(self.headerMetaInfo)
        self.headerAppLogo.setObjectName("headerAppLogo")
        self.headerAppLogo.setGeometry(QRect(10, 4, 40, 40))
        self.headerAppLogo.setMinimumSize(QSize(40, 40))
        self.headerAppLogo.setMaximumSize(QSize(40, 40))
        self.headerAppLogo.setFrameShape(QFrame.NoFrame)
        self.headerAppLogo.setFrameShadow(QFrame.Raised)

        # ////// SETUP APP NAME
        self.headerAppName = QLabel(app_name, self.headerMetaInfo)
        self.headerAppName.setObjectName("headerAppName")
        self.headerAppName.setGeometry(QRect(65, 6, 160, 20))

        # Vérifier si Fonts est initialisé, sinon utiliser une police par défaut
        if hasattr(Fonts, "SEGOE_UI_12_SB") and Fonts.SEGOE_UI_12_SB is not None:
            self.headerAppName.setFont(Fonts.SEGOE_UI_12_SB)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(12)
                self.headerAppName.setFont(default_font)
            except ImportError:
                # Si QFont n'est pas disponible, ignorer la police
                pass

        self.headerAppName.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        # //////
        self.headerAppDescription = QLabel(description, self.headerMetaInfo)
        self.headerAppDescription.setObjectName("headerAppDescription")
        self.headerAppDescription.setGeometry(QRect(65, 26, 240, 16))
        self.headerAppDescription.setMaximumSize(QSize(16777215, 16))

        # Vérifier si Fonts est initialisé, sinon utiliser une police par défaut
        if hasattr(Fonts, "SEGOE_UI_8_REG") and Fonts.SEGOE_UI_8_REG is not None:
            self.headerAppDescription.setFont(Fonts.SEGOE_UI_8_REG)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(8)
                self.headerAppDescription.setFont(default_font)
            except ImportError:
                # Si QFont n'est pas disponible, ignorer la police
                pass

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

        # Vérifier si Fonts est initialisé, sinon utiliser une police par défaut
        if hasattr(Fonts, "SEGOE_UI_10_REG") and Fonts.SEGOE_UI_10_REG is not None:
            self.maximizeRestoreAppBtn.setFont(Fonts.SEGOE_UI_10_REG)
        else:
            try:
                from PySide6.QtGui import QFont

                default_font = QFont()
                default_font.setFamily("Segoe UI")
                default_font.setPointSize(10)
                self.maximizeRestoreAppBtn.setFont(default_font)
            except ImportError:
                # Si QFont n'est pas disponible, ignorer la police
                pass

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

    # ////// UTILITY FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def set_app_name(self, app_name: str) -> None:
        """
        Définit le nom de l'application dans l'en-tête.

        Parameters
        ----------
        app_name : str
            Le nouveau nom de l'application.
        """
        self.headerAppName.setText(app_name)

    def set_app_description(self, description: str) -> None:
        """
        Définit la description de l'application dans l'en-tête.

        Parameters
        ----------
        description : str
            La nouvelle description de l'application.
        """
        self.headerAppDescription.setText(description)

    def set_app_logo(
        self, logo: Union[str, QPixmap], y_shrink: int = 0, y_offset: int = 0
    ) -> None:
        """
        Définit le logo de l'application dans l'en-tête.

        Parameters
        ----------
        logo : str or QPixmap
            Le logo à afficher (chemin de fichier ou QPixmap).
        y_shrink : int, optional
            Réduction verticale du logo (défaut: 0).
        y_offset : int, optional
            Décalage vertical du logo (défaut: 0).
        """

        def offsetY(y_offset: int = 0, x_offset: int = 0) -> None:
            """Applique un décalage au logo."""
            current_rect = self.headerAppLogo.geometry()
            new_rect = QRect(
                current_rect.x() + x_offset,
                current_rect.y() + y_offset,
                current_rect.width(),
                current_rect.height(),
            )
            self.headerAppLogo.setGeometry(new_rect)

        # ////// PROCESS LOGO
        pixmap_logo = QPixmap(logo) if isinstance(logo, str) else logo
        if pixmap_logo.size() != self.headerAppLogo.minimumSize():
            pixmap_logo = pixmap_logo.scaled(
                self.headerAppLogo.minimumSize().shrunkBy(
                    QMargins(0, y_shrink, 0, y_shrink)
                ),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

        self.headerAppLogo.setPixmap(pixmap_logo)
        offsetY(y_offset, y_shrink)

    def update_all_theme_icons(self) -> None:
        """Met à jour tous les icônes des boutons selon le thème actuel."""
        for i, btn in enumerate(self._buttons):
            btn.setIcon(self._icons[i])
