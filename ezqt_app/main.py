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
New Main Module for EzQt_App
============================

This module provides the new initialization system for EzQt_App,
using the modular initialization package.
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from typing import Optional, TYPE_CHECKING

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .kernel.initialization import init as init_app
from .kernel.app_functions.printer import get_printer

if TYPE_CHECKING:
    from ezqt_app.kernel.initialization import Initializer, StartupConfig
    from ezqt_app.kernel.app_functions import FileMaker

# ///////////////////////////////////////////////////////////////
# MAIN FUNCTIONS
# ///////////////////////////////////////////////////////////////


def init(mk_theme: bool = True) -> None:
    """
    Initialize the EzQt_App application using the new modular system.

    This function uses the new initialization package to:
    - Configure UTF-8 encoding at system level
    - Load required resources and generate necessary files
    - Setup the complete application environment

    Parameters
    ----------
    mk_theme : bool, optional
        Generate theme file (default: True).
    """
    init_app(mk_theme)


def setup_project(base_path: Optional[str] = None) -> bool:
    """
    Setup a new EzQt_App project using the new modular system.

    Parameters
    ----------
    base_path : str, optional
        Base path for the project (default: current directory).

    Returns
    -------
    bool
        True if setup was successful.
    """
    from ezqt_app.kernel.initialization import setup_project as setup_project_app

    return setup_project_app(base_path)


def generate_assets() -> bool:
    """
    Generate all required assets using the new modular system.

    Returns
    -------
    bool
        True if generation was successful.
    """
    from ezqt_app.kernel.initialization import generate_assets as generate_assets_app

    return generate_assets_app()


def configure_startup() -> None:
    """
    Configure startup settings using the new modular system.
    """
    from ezqt_app.kernel.initialization import (
        configure_startup as configure_startup_app,
    )

    configure_startup_app()


# ///////////////////////////////////////////////////////////////
# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////


def get_initializer() -> "Initializer":
    """
    Get the main initializer instance.

    Returns
    -------
    Initializer
        The main initializer instance.
    """
    from ezqt_app.kernel.initialization import Initializer

    return Initializer()


def get_file_maker(verbose: bool = False) -> "FileMaker":
    """
    Get the file maker instance.

    Parameters
    ----------
    verbose : bool, optional
        Enable verbose output mode, default False

    Returns
    -------
    FileMaker
        The file maker instance.
    """
    from ezqt_app.kernel.app_functions import FileMaker

    return FileMaker(verbose=verbose)


def get_startup_config() -> "StartupConfig":
    """
    Get the startup configuration instance.

    Returns
    -------
    StartupConfig
        The startup configuration instance.
    """
    from ezqt_app.kernel.initialization import StartupConfig

    return StartupConfig()


# ///////////////////////////////////////////////////////////////
# MAIN ENTRY POINT
# ///////////////////////////////////////////////////////////////

if __name__ == "__main__":
    # Example usage of the new initialization system
    printer = get_printer()
    printer.section("EzQt_App - New Initialization System")

    # Initialize the application
    init(mk_theme=True)

    printer.success("Application initialized successfully!")
    printer.info("Ready to create your EzQt_App application!")
