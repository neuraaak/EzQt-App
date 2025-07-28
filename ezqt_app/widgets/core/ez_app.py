# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import locale
import os

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# Configure High DPI using the centralized configuration
try:
    from ...kernel.qt_config import configure_qt_high_dpi
    configure_qt_high_dpi()
except (ImportError, RuntimeError, Exception):
    # If we can't configure it, continue anyway
    pass

from PySide6.QtCore import (
    Signal,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
)
from PySide6.QtGui import QGuiApplication

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
        # Configure High DPI JUST BEFORE creating QApplication
        # This is the critical moment when QGuiApplication is created
        try:
            from PySide6.QtCore import Qt
            from PySide6.QtGui import QGuiApplication
            
            # Check if QGuiApplication instance already exists
            if QGuiApplication.instance() is None:
                # Set High DPI scale factor rounding policy
                # This must be called before any QApplication instance is created
                QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
                    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
                )
        except (ImportError, RuntimeError, Exception):
            # If we can't configure it, continue anyway
            pass

        # Vérifier s'il y a déjà une instance QApplication
        existing_app = QApplication.instance()
        if existing_app and not isinstance(existing_app, EzApplication):
            raise RuntimeError(
                "Please destroy the QApplication singleton before creating a new EzApplication instance."
            )

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

    @classmethod
    def create_for_testing(cls, *args: Any, **kwargs: Any) -> "EzApplication":
        """
        Méthode de classe pour créer une instance EzApplication pour les tests.
        Cette méthode contourne la vérification de singleton pour les tests.
        """
        # Configure High DPI JUST BEFORE creating QApplication
        # This is the critical moment when QGuiApplication is created
        try:
            from PySide6.QtCore import Qt
            from PySide6.QtGui import QGuiApplication
            
            # Check if QGuiApplication instance already exists
            if QGuiApplication.instance() is None:
                # Set High DPI scale factor rounding policy
                # This must be called before any QApplication instance is created
                QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
                    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
                )
        except (ImportError, RuntimeError, Exception):
            # If we can't configure it, continue anyway
            pass

        # Vérifier s'il y a déjà une instance
        existing_app = QApplication.instance()
        if existing_app:
            # Si c'est déjà une EzApplication, la retourner
            if isinstance(existing_app, cls):
                return existing_app
            # Sinon, la détruire proprement
            existing_app.quit()
            existing_app.deleteLater()
            import time

            time.sleep(0.2)  # Plus de temps pour s'assurer que l'instance est détruite

            # Vérifier que l'instance a bien été détruite
            if QApplication.instance():
                # Si l'instance existe encore, forcer la destruction
                QApplication.instance().quit()
                QApplication.instance().deleteLater()
                time.sleep(0.2)

        # Créer une nouvelle instance directement avec QApplication
        # pour éviter les vérifications du constructeur EzApplication
        try:
            instance = QApplication(*args, **kwargs)
        except RuntimeError as e:
            # Si on a encore une erreur, essayer de forcer la destruction
            if "QApplication singleton" in str(e):
                # Forcer la destruction de toute instance existante
                app = QApplication.instance()
                if app:
                    app.quit()
                    app.deleteLater()
                    import time

                    time.sleep(0.3)

                # Réessayer de créer l'instance
                instance = QApplication(*args, **kwargs)
            else:
                raise

        # Ajouter les attributs d'EzApplication
        instance.themeChanged = Signal()

        # Configurer l'instance comme dans le constructeur EzApplication
        instance.setAttribute(Qt.AA_EnableHighDpiScaling, True)

        try:
            locale.setlocale(locale.LC_ALL, "")
        except locale.Error:
            pass

        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["QT_FONT_DPI"] = "96"

        return instance
