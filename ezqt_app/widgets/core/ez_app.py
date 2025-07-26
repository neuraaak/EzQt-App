# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Signal,
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class EzApplication(QApplication):
    themeChanged = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        # Configure UTF-8 encoding for the application
        self.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        
        # Set UTF-8 encoding for text handling
        import locale
        try:
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error:
            pass
        
        # Set environment variables for UTF-8
        import os
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        os.environ['QT_FONT_DPI'] = '96'
