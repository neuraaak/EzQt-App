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
from PySide6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..app_settings import Settings

# TYPE HINTS IMPROVEMENTS

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class PanelManager:
    """
    Interface panel manager.

    This class manages the animation and behavior of menu
    and settings panels in the application.
    """

    # PANEL MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    @staticmethod
    def toggleMenuPanel(self, enable) -> None:
        """
        Toggle menu panel display.

        Parameters
        ----------
        enable : bool
            Enable or disable menu panel.
        """
        if enable:
            # GET WIDTH
            width = self.ui.menuContainer.width()
            maxExtend = self.ui.menuContainer.get_extended_width()
            standard = self.ui.menuContainer.get_shrink_width()

            # SET MAX WIDTH
            if width == self.ui.menuContainer.get_shrink_width():
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.menu_animation = QPropertyAnimation(
                self.ui.menuContainer, b"minimumWidth"
            )
            self.menu_animation.setDuration(Settings.Gui.TIME_ANIMATION)
            self.menu_animation.setStartValue(width)
            self.menu_animation.setEndValue(widthExtended)
            self.menu_animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.menu_animation.start()

    @staticmethod
    def toggleSettingsPanel(self, enable) -> None:
        """
        Toggle settings panel display.

        Parameters
        ----------
        enable : bool
            Enable or disable settings panel.
        """
        if enable:
            # GET WIDTH
            width = self.ui.settingsPanel.width()
            maxExtend = Settings.Gui.SETTINGS_PANEL_WIDTH
            standard = 0

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.settings_animation = QPropertyAnimation(
                self.ui.settingsPanel, b"minimumWidth"
            )
            self.settings_animation.setDuration(Settings.Gui.TIME_ANIMATION)
            self.settings_animation.setStartValue(width)
            self.settings_animation.setEndValue(widthExtended)
            self.settings_animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.settings_animation.start()

            # Synchronize toggle with current theme
            current_theme = Settings.Gui.THEME
            theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
            if theme_toggle and hasattr(theme_toggle, "initialize_selector"):
                try:
                    # Convert theme to ID: 0 = Light, 1 = Dark
                    theme_id = 0 if current_theme.lower() == "light" else 1
                    theme_toggle.initialize_selector(theme_id)
                except Exception as e:
                    # Ignore initialization errors
                    pass
