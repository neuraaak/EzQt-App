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
Main Initializer for EzQt_App
==============================

This module handles the main initialization process for EzQt_App,
coordinating startup configuration, resource generation, and kernel setup.
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from .startup_config import StartupConfig
from .sequence import InitializationSequence
from ..app_functions import FileMaker, Kernel

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# TYPE HINTS IMPROVEMENTS
from typing import Optional, Dict, Any


## ==> CLASSES
# ///////////////////////////////////////////////////////////////
class Initializer:
    """
    Main initializer for EzQt_App applications.

    This class coordinates the complete initialization process:
    - Startup configuration (encoding, locale, environment)
    - Resource generation and asset setup
    - Kernel initialization
    - Application readiness checks
    """

    def __init__(self) -> None:
        """Initialize the main initializer."""
        self._startup_config = StartupConfig()
        self._file_maker = FileMaker()
        self._sequence = InitializationSequence()
        self._initialized = False

    def initialize(self, mk_theme: bool = True, verbose: bool = True) -> Dict[str, Any]:
        """
        Perform complete application initialization using the sequence.

        Parameters
        ----------
        mk_theme : bool, optional
            Generate theme files (default: True).
        verbose : bool, optional
            Whether to show detailed progress (default: True).

        Returns
        -------
        Dict[str, Any]
            Summary of the initialization process.
        """
        if self._initialized:
            return {"success": True, "message": "Already initialized"}

        # Execute the initialization sequence
        summary = self._sequence.execute(verbose=verbose)

        if summary["success"]:
            self._initialized = True

        return summary

    def setup_project(self, base_path: Optional[str] = None) -> bool:
        """
        Setup a complete EzQt_App project.

        Parameters
        ----------
        base_path : str, optional
            Base path for the project.

        Returns
        -------
        bool
            True if setup was successful.
        """
        # Configure startup first
        self._startup_config.configure()

        # Setup project with FileMaker
        file_maker = FileMaker(base_path)
        return file_maker.setup_project()

    def configure_startup(self) -> None:
        """Configure startup settings only."""
        self._startup_config.configure()

    def generate_assets(self) -> bool:
        """
        Generate all required assets.

        Returns
        -------
        bool
            True if generation was successful.
        """
        return self._file_maker.generate_all_assets()

    def check_requirements(self) -> bool:
        """
        Check if all requirements are met.

        Returns
        -------
        bool
            True if all requirements are met.
        """
        try:
            Kernel.checkAssetsRequirements()
            return True
        except Exception:
            return False

    def make_required_files(self, mk_theme: bool = True) -> None:
        """
        Generate required files.

        Parameters
        ----------
        mk_theme : bool, optional
            Generate theme files (default: True).
        """
        Kernel.makeRequiredFiles(mkTheme=mk_theme)

    def is_initialized(self) -> bool:
        """
        Check if initialization is complete.

        Returns
        -------
        bool
            True if initialization is complete.
        """
        return self._initialized

    def get_startup_config(self) -> StartupConfig:
        """Get the startup configuration instance."""
        return self._startup_config

    def get_file_maker(self) -> FileMaker:
        """Get the file maker instance."""
        return self._file_maker

    def get_sequence(self) -> InitializationSequence:
        """Get the initialization sequence instance."""
        return self._sequence

    def reset(self) -> None:
        """Reset initialization state."""
        self._initialized = False
        self._startup_config.reset()
        self._sequence.reset()
