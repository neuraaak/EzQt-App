# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QSize,
)
from PySide6.QtGui import (
    QCursor,
    QPixmap,
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QPushButton,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ...kernel.app_components import *
from ...kernel.app_resources import *
from ...kernel.app_settings import Settings

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Dict, List, Optional, Union

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class Menu(QFrame):
    """
    Menu container with expansion/reduction support.

    This class provides a menu container with a toggle button
    to expand or reduce the menu width. The menu contains an upper
    section for menu items and a lower section for the toggle button.
    """

    # ////// CLASS VARIABLES
    menus: Dict[str, QPushButton] = {}
    _buttons: List = []  # Type hint removed to avoid circular import
    _icons: List = []  # Type hint removed to avoid circular import

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        shrink_width: int = 60,
        extended_width: int = 240,
    ) -> None:
        """
        Initialize the menu container.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget (default: None).
        shrink_width : int, optional
            Width when menu is shrunk (default: 60).
        extended_width : int, optional
            Width when menu is extended (default: 240).
        """
        super().__init__(parent)

        # ////// STORE CONFIGURATION
        self._shrink_width = shrink_width
        self._extended_width = extended_width

        # ////// SETUP WIDGET PROPERTIES
        self.setObjectName("menuContainer")
        self.setMinimumSize(QSize(self._shrink_width, 0))
        self.setMaximumSize(QSize(self._shrink_width, 16777215))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        # ////// SETUP MAIN LAYOUT
        self.VL_menuContainer = QVBoxLayout(self)
        self.VL_menuContainer.setSpacing(0)
        self.VL_menuContainer.setObjectName("VL_menuContainer")
        self.VL_menuContainer.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP MAIN MENU FRAME
        self.mainMenuFrame = QFrame(self)
        self.mainMenuFrame.setObjectName("mainMenuFrame")
        self.mainMenuFrame.setFrameShape(QFrame.NoFrame)
        self.mainMenuFrame.setFrameShadow(QFrame.Raised)
        self.VL_menuContainer.addWidget(self.mainMenuFrame)

        # ////// SETUP MAIN MENU LAYOUT
        self.VL_mainMenuFrame = QVBoxLayout(self.mainMenuFrame)
        self.VL_mainMenuFrame.setSpacing(0)
        self.VL_mainMenuFrame.setObjectName("VL_mainMenuFrame")
        self.VL_mainMenuFrame.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP TOGGLE CONTAINER
        self.toggleBox = QFrame(self.mainMenuFrame)
        self.toggleBox.setObjectName("toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.VL_mainMenuFrame.addWidget(self.toggleBox)

        # ////// SETUP TOGGLE LAYOUT
        self.VL_toggleBox = QVBoxLayout(self.toggleBox)
        self.VL_toggleBox.setSpacing(0)
        self.VL_toggleBox.setObjectName("VL_toggleBox")
        self.VL_toggleBox.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP TOGGLE BUTTON
        # Lazy import to avoid circular imports
        from ...widgets.extended.menu_button import MenuButton
        from ...widgets.extended.theme_icon import ThemeIcon

        self.toggleButton = MenuButton(
            parent=self.toggleBox,
            icon=Icons.icon_menu,
            text="Hide",
            shrink_size=self._shrink_width,
            spacing=15,  # Reduced from 35 to 15 for better alignment
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

        # ////// SETUP TOP MENU
        self.topMenu = QFrame(self.mainMenuFrame)
        self.topMenu.setObjectName("topMenu")
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.VL_mainMenuFrame.addWidget(self.topMenu, 0, Qt.AlignTop)

        # ////// SETUP TOP MENU LAYOUT
        self.VL_topMenu = QVBoxLayout(self.topMenu)
        self.VL_topMenu.setSpacing(0)
        self.VL_topMenu.setObjectName("VL_topMenu")
        self.VL_topMenu.setContentsMargins(0, 0, 0, 0)

        # ////// SYNC INITIAL STATE
        self._sync_initial_state()

    # ////// UTILITY FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def _sync_initial_state(self) -> None:
        """
        Sync the initial state of all buttons with the container state.

        The menu container starts shrunk, so all buttons
        must start in the shrunk state.
        """
        if hasattr(self, "toggleButton"):
            # Force toggle button to shrink state
            self.toggleButton.set_state(False)  # False = shrink state
            # Sync all existing menu buttons
            self.sync_all_menu_states(False)

    def add_menu(self, name: str, icon: Optional[Union[str, QPixmap]] = None):
        """
        Add a menu item to the container.

        Parameters
        ----------
        name : str
            The name of the menu item.
        icon : str or Icons, optional
            The icon for the menu item (default: None).

        Returns
        -------
        MenuButton
            The created menu button.
        """
        # Lazy import to avoid circular imports
        from ...widgets.extended.menu_button import MenuButton
        from ...widgets.extended.theme_icon import ThemeIcon

        menu = MenuButton(
            parent=self.topMenu,
            icon=icon,
            text=name,
            shrink_size=self._shrink_width,
            spacing=15,  # Reduced from 35 to 15 for better alignment
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

        # ////// SETUP THEME ICON
        theme_icon = ThemeIcon(icon)
        self._buttons.append(menu)
        self._icons.append(theme_icon)

        # Connect to the toggle button to sync state
        self.toggleButton.stateChanged.connect(menu.set_state)

        self.VL_topMenu.addWidget(menu)
        Menu.menus[name] = menu

        return menu

    def update_all_theme_icons(self) -> None:
        """Update theme icons for all buttons."""
        for i, btn in enumerate(self._buttons):
            if hasattr(btn, "update_theme_icon") and self._icons[i]:
                btn.update_theme_icon(self._icons[i])

    def sync_all_menu_states(self, extended: bool) -> None:
        """
        Sync all menu buttons to the given state.

        Parameters
        ----------
        extended : bool
            True for extended, False for shrunk.
        """
        for btn in self._buttons:
            if btn != self.toggleButton:  # Don't sync the toggle button itself
                btn.set_state(extended)

    def get_menu_state(self) -> bool:
        """
        Get the current menu state.

        Returns
        -------
        bool
            True if extended, False if shrunk.
        """
        if hasattr(self, "toggleButton"):
            return self.toggleButton.is_extended
        return False

    def get_shrink_width(self) -> int:
        """
        Get the configured shrink width.

        Returns
        -------
        int
            The shrink width.
        """
        return self._shrink_width

    def get_extended_width(self) -> int:
        """
        Get the configured extended width.

        Returns
        -------
        int
            The extended width.
        """
        return self._extended_width
