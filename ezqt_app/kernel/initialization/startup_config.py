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
Startup Configuration for EzQt_App
==================================

This module handles system-level configuration for application startup,
including encoding, locale, and environment variables.
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import sys
import locale
import os

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Optional

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class StartupConfig:
    """
    Manages startup configuration for EzQt_App.

    This class handles system-level configuration including:
    - UTF-8 encoding setup
    - Locale configuration
    - Environment variables
    - System compatibility
    """

    def __init__(self) -> None:
        """Initialize the startup configuration."""
        self._configured = False

    def configure(self) -> None:
        """
        Configure all startup settings.

        This method sets up:
        - UTF-8 encoding for stdout/stderr
        - Environment variables
        - Locale settings
        - System compatibility
        """
        if self._configured:
            return

        self._configure_encoding()
        self._configure_environment()
        self._configure_locale()
        self._configure_system()

        self._configured = True

    def _configure_encoding(self) -> None:
        """Configure UTF-8 encoding for system I/O."""
        # Configure UTF-8 encoding at system level
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")

    def _configure_environment(self) -> None:
        """Configure environment variables."""
        # Set environment variables for UTF-8
        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["QT_FONT_DPI"] = "96"

        # Additional Qt environment variables
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"

        # High DPI configuration is handled globally in kernel.globals
        # No need to configure it here as it's already done at module import time

    def _configure_locale(self) -> None:
        """Configure locale settings."""
        try:
            # Set locale to UTF-8
            locale.setlocale(locale.LC_ALL, "")
        except locale.Error:
            # Fallback for systems without proper locale support
            pass

    def _configure_system(self) -> None:
        """Configure system-specific settings."""
        # Platform-specific configurations
        if sys.platform.startswith("win"):
            self._configure_windows()
        elif sys.platform.startswith("linux"):
            self._configure_linux()
        elif sys.platform.startswith("darwin"):
            self._configure_macos()

    def _configure_windows(self) -> None:
        """Configure Windows-specific settings."""
        # Windows-specific environment variables
        os.environ["QT_QPA_PLATFORM"] = "windows:dpiawareness=0"

    def _configure_linux(self) -> None:
        """Configure Linux-specific settings."""
        # Linux-specific environment variables
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    def _configure_macos(self) -> None:
        """Configure macOS-specific settings."""
        # macOS-specific environment variables
        os.environ["QT_QPA_PLATFORM"] = "cocoa"

    def get_encoding(self) -> str:
        """Get current encoding configuration."""
        return getattr(sys.stdout, "encoding", "utf-8")

    def get_locale(self) -> Optional[str]:
        """Get current locale configuration."""
        try:
            return locale.getlocale()[0]
        except (locale.Error, IndexError):
            return None

    def is_configured(self) -> bool:
        """Check if startup configuration is complete."""
        return self._configured

    def reset(self) -> None:
        """Reset configuration state."""
        self._configured = False
