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

# TYPE HINTS IMPROVEMENTS
from typing import Any

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class EzApplication(QApplication):
    """
    Extended main application with theme and UTF-8 encoding support.

    This class inherits from QApplication and adds functionality
    for theme management and UTF-8 encoding.
    """

    themeChanged = Signal()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the application with UTF-8 and high resolution support.

        Parameters
        ----------
        *args : Any
            Positional arguments passed to QApplication.
        **kwargs : Any
            Keyword arguments passed to QApplication.
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

        # Check if there's already a QApplication instance
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
        Class method to create an EzApplication instance for testing.
        This method bypasses singleton checking for tests.
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

        # Check if there's already an instance
        existing_app = QApplication.instance()
        if existing_app:
            # If it's already an EzApplication, return it
            if isinstance(existing_app, cls):
                return existing_app
            # Otherwise, destroy it properly
            existing_app.quit()
            existing_app.deleteLater()
            import time

            time.sleep(0.2)  # More time to ensure instance is destroyed

            # Check that instance has been properly destroyed
            if QApplication.instance():
                # If instance still exists, force destruction
                QApplication.instance().quit()
                QApplication.instance().deleteLater()
                time.sleep(0.2)

        # Create new instance directly with QApplication
        # to avoid EzApplication constructor checks
        try:
            instance = QApplication(*args, **kwargs)
        except RuntimeError as e:
            # If we still have an error, try to force destruction
            if "QApplication singleton" in str(e):
                # Force destruction of any existing instance
                app = QApplication.instance()
                if app:
                    app.quit()
                    app.deleteLater()
                    import time

                    time.sleep(0.3)

                # Retry creating instance
                instance = QApplication(*args, **kwargs)
            else:
                raise

        # Add EzApplication attributes
        instance.themeChanged = Signal()

        # Configure instance as in EzApplication constructor
        instance.setAttribute(Qt.AA_EnableHighDpiScaling, True)

        try:
            locale.setlocale(locale.LC_ALL, "")
        except locale.Error:
            pass

        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["QT_FONT_DPI"] = "96"

        return instance
