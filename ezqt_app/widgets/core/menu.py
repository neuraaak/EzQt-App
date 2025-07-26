# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import Dict, List

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QCursor,
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QPushButton,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from ...kernel.app_components import *
from ...kernel.app_resources import *
from ...kernel.app_settings import Settings

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class Menu(QFrame):
    """
    This class is used to create a menu container.
    It contains a main menu frame and a toggle box.
    The main menu frame contains a top menu and a bottom menu.
    The toggle box contains a toggle button.
    The menu container is used to display the menu.
    """

    menus: Dict[str, QPushButton] = {}
    _buttons: List = []  # Type hint removed to avoid circular import
    _icons: List = []  # Type hint removed to avoid circular import

    # ///////////////////////////////////////////////////////////////

    def __init__(
        self, parent: QWidget = None, shrink_width: int = 60, extended_width: int = 240
    ) -> None:
        super(Menu, self).__init__(parent)

        # ///////////////////////////////////////////////////////////////
        # Store configuration
        self._shrink_width = shrink_width
        self._extended_width = extended_width

        self.setObjectName("menuContainer")
        self.setMinimumSize(QSize(self._shrink_width, 0))
        self.setMaximumSize(QSize(self._shrink_width, 16777215))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        # //////
        self.VL_menuContainer = QVBoxLayout(self)
        self.VL_menuContainer.setSpacing(0)
        self.VL_menuContainer.setObjectName("VL_menuContainer")
        self.VL_menuContainer.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////

        self.mainMenuFrame = QFrame(self)
        self.mainMenuFrame.setObjectName("mainMenuFrame")
        self.mainMenuFrame.setFrameShape(QFrame.NoFrame)
        self.mainMenuFrame.setFrameShadow(QFrame.Raised)
        #
        self.VL_menuContainer.addWidget(self.mainMenuFrame)
        # //////
        self.VL_mainMenuFrame = QVBoxLayout(self.mainMenuFrame)
        self.VL_mainMenuFrame.setSpacing(0)
        self.VL_mainMenuFrame.setObjectName("VL_mainMenuFrame")
        self.VL_mainMenuFrame.setContentsMargins(0, 0, 0, 0)

        # ToggleContainer for expand button
        # ///////////////////////////////////////////////////////////////

        self.toggleBox = QFrame(self.mainMenuFrame)
        self.toggleBox.setObjectName("toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        #
        self.VL_mainMenuFrame.addWidget(self.toggleBox)
        # //////
        self.VL_toggleBox = QVBoxLayout(self.toggleBox)
        self.VL_toggleBox.setSpacing(0)
        self.VL_toggleBox.setObjectName("VL_toggleBox")
        self.VL_toggleBox.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////

        # Lazy import to avoid circular imports
        from ...widgets.extended.menu_button import MenuButton
        from ...widgets.extended.theme_icon import ThemeIcon

        self.toggleButton = MenuButton(
            parent=self.toggleBox,
            icon=Icons.icon_menu,
            text="Hide",
            shrink_size=self._shrink_width,
            spacing=35,
            duration=Settings.Gui.TIME_ANIMATION,
        )
        self.toggleButton.setObjectName("toggleButton")
        self.toggleButton.setSizePolicy(SizePolicy.H_EXPANDING_V_FIXED)
        SizePolicy.H_EXPANDING_V_FIXED.setHeightForWidth(
            self.toggleButton.sizePolicy().hasHeightForWidth()
        )
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(Fonts.SEGOE_UI_10_REG)
        self.toggleButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        # Don't set contents margins here - MenuButton handles its own positioning
        # self.toggleButton.setContentsMargins(20, 0, 0, 0)
        #
        icon_menu = ThemeIcon(Icons.icon_menu)
        self._buttons.append(self.toggleButton)
        self._icons.append(icon_menu)
        # Connect to the new toggle_state method
        self.toggleButton.clicked.connect(self.toggleButton.toggle_state)
        #
        self.VL_toggleBox.addWidget(self.toggleButton)

        # The Menu itself
        # ///////////////////////////////////////////////////////////////

        self.topMenu = QFrame(self.mainMenuFrame)
        self.topMenu.setObjectName("topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        #
        self.VL_mainMenuFrame.addWidget(self.topMenu, 0, Qt.AlignTop)
        # //////
        self.VL_topMenu = QVBoxLayout(self.topMenu)
        self.VL_topMenu.setSpacing(0)
        self.VL_topMenu.setObjectName("VL_topMenu")
        self.VL_topMenu.setContentsMargins(0, 0, 0, 0)

        # ////// SYNC INITIAL STATE
        # Menu container starts shrinked (60px width), so sync toggle button state
        self._sync_initial_state()

    # ///////////////////////////////////////////////////////////////

    def _sync_initial_state(self):
        """Sync the initial state of all buttons with the menu container state."""
        # Menu container starts shrinked (configured width)
        # So all buttons should start in shrink state
        if hasattr(self, "toggleButton"):
            # Force toggle button to shrink state
            self.toggleButton.set_state(False)  # False = shrink state
            # Sync all existing menu buttons
            self.sync_all_menu_states(False)

    # ///////////////////////////////////////////////////////////////

    def add_menu(self, name: str, icon: str | Icons = None):
        # Lazy import to avoid circular imports
        from ...widgets.extended.menu_button import MenuButton
        from ...widgets.extended.theme_icon import ThemeIcon

        menu = MenuButton(
            parent=self.topMenu,
            icon=icon,
            text=name,
            shrink_size=self._shrink_width,
            spacing=35,
            duration=Settings.Gui.TIME_ANIMATION,
        )
        menu.setObjectName(f"menu_{name}")
        menu.setProperty("class", "inactive")
        menu.setSizePolicy(SizePolicy.H_EXPANDING_V_FIXED)
        SizePolicy.H_EXPANDING_V_FIXED.setHeightForWidth(
            menu.sizePolicy().hasHeightForWidth()
        )
        menu.setMinimumSize(QSize(0, 45))
        menu.setFont(Fonts.SEGOE_UI_10_REG)
        menu.setCursor(QCursor(Qt.PointingHandCursor))
        menu.setLayoutDirection(Qt.LeftToRight)
        # Don't set contents margins here - MenuButton handles its own positioning
        # menu.setContentsMargins(20, 0, 0, 0)
        #
        theme_icon = ThemeIcon(icon)
        self._buttons.append(menu)
        self._icons.append(theme_icon)
        # Connect to the toggle button to sync state
        self.toggleButton.stateChanged.connect(menu.set_state)
        #
        self.VL_topMenu.addWidget(menu)
        Menu.menus[name] = menu

        # //////
        return menu

    # ///////////////////////////////////////////////////////////////

    def update_all_theme_icons(self) -> None:
        """Update theme icons for all buttons."""
        for i, btn in enumerate(self._buttons):
            if hasattr(btn, "update_theme_icon") and self._icons[i]:
                # Use the dedicated method for theme icon updates
                btn.update_theme_icon(self._icons[i])

    def sync_all_menu_states(self, extended: bool) -> None:
        """Sync all menu buttons with the given state."""
        for btn in self._buttons:
            if btn != self.toggleButton:  # Don't sync the toggle button itself
                btn.set_state(extended)

    def get_menu_state(self) -> bool:
        """Get the current menu state (True for extended, False for shrink)."""
        if hasattr(self, "toggleButton"):
            return self.toggleButton.is_extended
        return False

    def get_shrink_width(self) -> int:
        """Get the configured shrink width."""
        return self._shrink_width

    def get_extended_width(self) -> int:
        """Get the configured extended width."""
        return self._extended_width
