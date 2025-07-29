# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
# EzQt_App - A Modern Qt Application Framework
# ///////////////////////////////////////////////////////////////
#
# Author: EzQt_App Team
# Website: https://github.com/ezqt-app/ezqt_app
#
# This file is part of EzQt_App.
#
# EzQt_App is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EzQt_App is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EzQt_App.  If not, see <https://www.gnu.org/licenses/>.
# ///////////////////////////////////////////////////////////////

"""
Global Configuration for EzQt_App
=================================

This module contains global configurations and settings that should be
applied as early as possible in the application lifecycle.
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import os
import sys

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# TYPE HINTS IMPROVEMENTS
from typing import Optional, Any

# ////// GLOBAL HIGH DPI CONFIGURATION
# ///////////////////////////////////////////////////////////////
# IMPORTANT: This configuration must be done BEFORE any QApplication creation
# to avoid the warning: "setHighDpiScaleFactorRoundingPolicy must be called before creating the QGuiApplication instance"


def _configure_high_dpi_globally():
    """
    Configure High DPI settings globally before any Qt application creation.

    This function sets up:
    - High DPI scale factor rounding policy
    - Environment variables for High DPI
    - Platform-specific High DPI settings
    """
    # Set environment variables for High DPI FIRST
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

    # Now try to configure Qt High DPI policy
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
            # This is expected in some cases, so we just continue
            return False
            
    except ImportError:
        # PySide6 not available, skip High DPI configuration
        return False
    except RuntimeError as e:
        # QGuiApplication already initialized, this is expected in some cases
        if "QGuiApplication instance" in str(e):
            # This is the specific error we're trying to avoid
            return False
        else:
            # Re-raise unexpected RuntimeError
            raise
    except Exception:
        # Any other error, continue without High DPI configuration
        return False


# Apply High DPI configuration immediately when this module is imported
# This must be done before any Qt modules are imported
_configure_high_dpi_globally()

# ////// GLOBAL VARIABLES
# ///////////////////////////////////////////////////////////////

# Application state
APP_INITIALIZED = False
APP_RUNNING = False

# Configuration flags
DEBUG_MODE = False
VERBOSE_MODE = False

# ////// UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////


def set_debug_mode(enabled: bool = True) -> None:
    """
    Enable or disable debug mode globally.

    Parameters
    ----------
    enabled : bool
        Whether to enable debug mode (default: True).
    """
    global DEBUG_MODE
    DEBUG_MODE = enabled


def set_verbose_mode(enabled: bool = True) -> None:
    """
    Enable or disable verbose mode globally.

    Parameters
    ----------
    enabled : bool
        Whether to enable verbose mode (default: True).
    """
    global VERBOSE_MODE
    VERBOSE_MODE = enabled


def is_debug_mode() -> bool:
    """
    Check if debug mode is enabled.

    Returns
    -------
    bool
        True if debug mode is enabled.
    """
    return DEBUG_MODE


def is_verbose_mode() -> bool:
    """
    Check if verbose mode is enabled.

    Returns
    -------
    bool
        True if verbose mode is enabled.
    """
    return VERBOSE_MODE


def mark_app_initialized() -> None:
    """Mark the application as initialized."""
    global APP_INITIALIZED
    APP_INITIALIZED = True


def mark_app_running() -> None:
    """Mark the application as running."""
    global APP_RUNNING
    APP_RUNNING = True


def is_app_initialized() -> bool:
    """
    Check if the application is initialized.

    Returns
    -------
    bool
        True if the application is initialized.
    """
    return APP_INITIALIZED


def is_app_running() -> bool:
    """
    Check if the application is running.

    Returns
    -------
    bool
        True if the application is running.
    """
    return APP_RUNNING


# Legacy compatibility - for backward compatibility with existing code
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True


def get_global_state() -> bool:
    """
    Get the global window state (legacy compatibility).

    Returns
    -------
    bool
        The global window state.
    """
    return GLOBAL_STATE


def set_global_state(state: bool) -> None:
    """
    Set the global window state (legacy compatibility).

    Parameters
    ----------
    state : bool
        The new global window state.
    """
    global GLOBAL_STATE
    GLOBAL_STATE = state


def get_global_title_bar() -> bool:
    """
    Get the global title bar setting (legacy compatibility).

    Returns
    -------
    bool
        The global title bar setting.
    """
    return GLOBAL_TITLE_BAR


def set_global_title_bar(enabled: bool) -> None:
    """
    Set the global title bar setting (legacy compatibility).

    Parameters
    ----------
    enabled : bool
        Whether to enable the title bar.
    """
    global GLOBAL_TITLE_BAR
    GLOBAL_TITLE_BAR = enabled
