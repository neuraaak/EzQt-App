# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
"""
Initialization Package for EzQt_App
===================================

This package handles application initialization, resource generation,
and startup configuration.

Components:
- Initializer: Main initialization class
- FileMaker: File and resource generation
- StartupConfig: Startup configuration management
"""

# ///////////////////////////////////////////////////////////////
# IMPORTS
# ///////////////////////////////////////////////////////////////

from typing import Dict, Any

from .initializer import Initializer
from .startup_config import StartupConfig
from .sequence import InitializationSequence, InitStep, StepStatus

# ///////////////////////////////////////////////////////////////
# MAIN INTERFACE
# ///////////////////////////////////////////////////////////////

def init(mk_theme: bool = True, verbose: bool = True) -> Dict[str, Any]:
    """
    Initialize the EzQt_App application.
    
    This function configures UTF-8 encoding at system level,
    loads required resources, and generates necessary files.
    
    Parameters
    ----------
    mk_theme : bool, optional
        Generate theme file (default: True).
    verbose : bool, optional
        Whether to show detailed progress (default: True).
        
    Returns
    -------
    Dict[str, Any]
        Summary of the initialization process.
    """
    initializer = Initializer()
    return initializer.initialize(mk_theme, verbose)


def setup_project(base_path: str = None) -> bool:
    """
    Setup a new EzQt_App project.
    
    Parameters
    ----------
    base_path : str, optional
        Base path for the project (default: current directory).
        
    Returns
    -------
    bool
        True if setup was successful.
    """
    file_maker = FileMaker(base_path)
    return file_maker.setup_project()


def generate_assets() -> bool:
    """
    Generate all required assets.
    
    Returns
    -------
    bool
        True if generation was successful.
    """
    file_maker = FileMaker()
    return file_maker.generate_all_assets()


def configure_startup() -> None:
    """
    Configure startup settings.
    """
    config = StartupConfig()
    config.configure()


## ==> EXPORTS
# ///////////////////////////////////////////////////////////////
__all__ = [
    "Initializer",
    "StartupConfig",
    "InitializationSequence",
    "InitStep",
    "StepStatus",
    "init",
    "setup_project",
    "generate_assets",
    "configure_startup",
] 