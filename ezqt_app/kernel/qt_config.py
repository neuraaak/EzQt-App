# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
"""
Qt Configuration for EzQt_App
=============================

This module handles Qt-specific configuration that must be done
before any Qt modules are imported.
"""

import os
import sys

def configure_qt_environment():
    """
    Configure Qt environment variables before any Qt imports.
    """
    # Set environment variables for High DPI
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"
    os.environ["QT_FONT_DPI"] = "96"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    # Platform-specific configurations
    if sys.platform.startswith("win"):
        os.environ["QT_QPA_PLATFORM"] = "windows:dpiawareness=0"
    elif sys.platform.startswith("linux"):
        os.environ["QT_QPA_PLATFORM"] = "xcb"
    elif sys.platform.startswith("darwin"):
        os.environ["QT_QPA_PLATFORM"] = "cocoa"

def configure_qt_high_dpi():
    """
    Configure Qt High DPI policy after Qt modules are available.
    """
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
            return True
        else:
            # QGuiApplication already exists, we can't set the policy
            return False
            
    except ImportError:
        # PySide6 not available, skip High DPI configuration
        return False
    except RuntimeError as e:
        # QGuiApplication already initialized, this is expected in some cases
        if "QGuiApplication instance" in str(e):
            return False
        else:
            # Re-raise unexpected RuntimeError
            raise
    except Exception:
        # Any other error, continue without High DPI configuration
        return False

def configure_qt_high_dpi_early():
    """
    Configure Qt High DPI policy as early as possible.
    This function should be called before any Qt modules are imported.
    """
    # Set environment variables for High DPI
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"
    os.environ["QT_FONT_DPI"] = "96"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

    # Platform-specific configurations
    if sys.platform.startswith("win"):
        os.environ["QT_QPA_PLATFORM"] = "windows:dpiawareness=0"
    elif sys.platform.startswith("linux"):
        os.environ["QT_QPA_PLATFORM"] = "xcb"
    elif sys.platform.startswith("darwin"):
        os.environ["QT_QPA_PLATFORM"] = "cocoa"

    # Try to configure High DPI policy if Qt modules are available
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
            return True
        else:
            # QGuiApplication already exists, we can't set the policy
            return False
            
    except ImportError:
        # PySide6 not available, skip High DPI configuration
        return False
    except RuntimeError as e:
        # QGuiApplication already initialized, this is expected in some cases
        if "QGuiApplication instance" in str(e):
            return False
        else:
            # Re-raise unexpected RuntimeError
            raise
    except Exception:
        # Any other error, continue without High DPI configuration
        return False

# Configure environment immediately when this module is imported
configure_qt_environment()

# Export functions for later use
__all__ = ["configure_qt_environment", "configure_qt_high_dpi", "configure_qt_high_dpi_early"] 