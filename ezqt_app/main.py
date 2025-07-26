# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ezqt_app.helper import Helper
from ezqt_app.kernel import Kernel

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


def init(mkTheme: bool = True) -> None:
    # //////
    # Configure UTF-8 encoding at system level
    import sys
    import locale
    import os
    
    # Set UTF-8 encoding for stdout/stderr
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    
    # Set environment variables for UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['QT_FONT_DPI'] = '96'
    
    # Set locale to UTF-8
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        # Fallback for systems without proper locale support
        pass
    
    # //////
    Kernel.checkAssetsRequirements()
    Kernel.makeRequiredFiles(mkTheme=mkTheme)
