# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import Optional

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import QObject, QMessageLogger, QLoggingCategory

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////

class QtLogger:
    """
    Wrapper pour QMessageLogger de PySide6 6.9.1
    """

    def __init__(self, category: Optional[str] = None):
        """
        Initialise le logger Qt.

        Parameters
        ----------
        category : str, optional
            Catégorie de logging (défaut: None)
        """
        if category:
            self.logging_category = QLoggingCategory(category)
            self.logger = QMessageLogger(category)
        else:
            self.logging_category = None
            self.logger = QMessageLogger()

    def debug(self, message: str) -> None:
        """Log un message de debug."""
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """Log un message d'information."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Log un message d'avertissement."""
        self.logger.warning(message)

    def critical(self, message: str) -> None:
        """Log un message critique."""
        self.logger.critical(message)

    def fatal(self, message: str) -> None:
        """Log un message fatal."""
        self.logger.fatal(message)

## ==> MAIN
# ///////////////////////////////////////////////////////////////

# Exemple d'utilisation
if __name__ == "__main__":
    logger = QtLogger("EzQt_App")
    logger.info("Application démarrée")
    logger.debug("Mode debug activé")
    logger.warning("Attention: fonctionnalité expérimentale")
