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

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtGui import QIcon

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .. import globals

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Any

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class WindowManager:
    """
    Gestionnaire de l'état de la fenêtre.

    Cette classe gère la maximisation, restauration et l'état
    de la fenêtre principale de l'application.
    """

    # WINDOW STATE MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def maximize_restore(self) -> None:
        """
        Maximise ou restaure la fenêtre selon son état actuel.
        """
        status = globals.get_global_state()
        if status == False:
            self.showMaximized()
            globals.set_global_state(True)
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.headerContainer.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.headerContainer.maximizeRestoreAppBtn.setIcon(
                QIcon(":/icons/icons/icon_restore.png")
            )
            self.ui.bottomBar.appSizeGrip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            globals.set_global_state(False)
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.headerContainer.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.headerContainer.maximizeRestoreAppBtn.setIcon(
                QIcon(":/icons/icons/icon_maximize.png")
            )
            self.ui.bottomBar.appSizeGrip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    @staticmethod
    def returnStatus(self) -> Any | bool:
        """
        Retourne l'état actuel de la fenêtre.

        Returns
        -------
        bool
            True si la fenêtre est maximisée, False sinon.
        """
        return globals.get_global_state()

    @staticmethod
    def setStatus(self, status) -> None:
        """
        Définit l'état de la fenêtre.

        Parameters
        ----------
        status : bool
            Nouvel état de la fenêtre.
        """
        globals.set_global_state(status)
