# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import sys
import platform
from pathlib import Path
from colorama import Fore, Style

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .kernel.app_functions.printer import get_printer
from .kernel import *
from .widgets.core.ez_app import EzApplication

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Optional, Any, Union

# ////// GLOBALS
# ///////////////////////////////////////////////////////////////
os_name: str = platform.system()
widgets: Optional[Any] = None

# ////// VARIABLES
# ///////////////////////////////////////////////////////////////
APP_PATH: Path = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))
_dev: bool = True if not hasattr(sys, "frozen") else False

# ////// UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# ////// CLASS
# ///////////////////////////////////////////////////////////////


class EzQt_App(QMainWindow):
    """
    Main EzQt_App application.

    This class represents the main application window
    with all its components (menu, pages, settings, etc.).
    """

    def __init__(
        self,
        themeFileName: Optional[str] = None,
    ) -> None:
        """
        Initialize the EzQt_App application.

        Parameters
        ----------
        themeFileName : str, optional
            Name of the theme file to use (default: None).
        """
        QMainWindow.__init__(self)

        # ////// KERNEL LOADER
        # ///////////////////////////////////////////////////////////////
        Kernel.loadFontsResources()
        Kernel.loadAppSettings()

        # ////// LOAD TRANSLATIONS
        # ///////////////////////////////////////////////////////////////
        from .kernel.translation import get_translation_manager

        # Load language from settings
        try:
            # Try to load settings_panel from app.yaml
            app_config = Kernel.loadKernelConfig("app")
            if "settings_panel" in app_config:
                settings_panel = app_config["settings_panel"]
                language = settings_panel.get("language", {}).get("default", "English")
            else:
                language = "English"
            translation_manager = get_translation_manager()
            translation_manager.load_language(language)
        except Exception:
            translation_manager = get_translation_manager()
            translation_manager.load_language("English")

        # ////// INITIALIZE COMPONENTS
        # ///////////////////////////////////////////////////////////////
        Fonts.initFonts()
        SizePolicy.initSizePolicy()

        # ////// SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # ////// USE CUSTOM TITLE BAR
        # ///////////////////////////////////////////////////////////////
        Settings.App.ENABLE_CUSTOM_TITLE_BAR = True if os_name == "Windows" else False

        # ////// APP DATA
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(Settings.App.NAME)
        (
            self.setAppIcon(Images.logo_placeholder, yShrink=0)
            if Settings.Gui.THEME == "dark"
            else self.setAppIcon(Images.logo_placeholder, yShrink=0)
        )

        # ==> TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.menuContainer.toggleButton.clicked.connect(
            lambda: UIFunctions.toggleMenuPanel(self, True)
        )

        # ==> TOGGLE SETTINGS
        # ///////////////////////////////////////////////////////////////
        widgets.headerContainer.settingsTopBtn.clicked.connect(
            lambda: UIFunctions.toggleSettingsPanel(self, True)
        )

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # SET THEME
        # ///////////////////////////////////////////////////////////////
        self._themeFileName = themeFileName
        UIFunctions.theme(self, self._themeFileName)
        # //////
        # Load theme from settings_panel if it exists, otherwise from app
        try:
            # Try to load settings_panel from app.yaml
            app_config = Kernel.loadKernelConfig("app")
            if "settings_panel" in app_config:
                settings_panel = app_config["settings_panel"]
                _theme = settings_panel.get("theme", {}).get("default", "dark")
            else:
                # Fallback to default value
                _theme = "dark"
            # Force conversion to lowercase
            _theme = _theme.lower()
        except Exception:
            # Fallback to default value
            _theme = "dark"

        # Update Settings.Gui.THEME with lowercase value
        Settings.Gui.THEME = _theme

        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle and hasattr(theme_toggle, "initialize_selector"):
            try:
                # Convert theme value to ID
                theme_id = 0 if _theme == "light" else 1  # 0 = Light, 1 = Dark
                theme_toggle.initialize_selector(theme_id)
            except Exception as e:
                # Ignore initialization errors
                pass
        self.ui.headerContainer.update_all_theme_icons()
        self.ui.menuContainer.update_all_theme_icons()
        # //////
        if theme_toggle:
            # Connect valueChanged signal instead of clicked for new version
            if hasattr(theme_toggle, "valueChanged"):
                theme_toggle.valueChanged.connect(self.setAppTheme)
            elif hasattr(theme_toggle, "clicked"):
                theme_toggle.clicked.connect(self.setAppTheme)

        # ==> REGISTER ALL WIDGETS FOR TRANSLATION
        # ///////////////////////////////////////////////////////////////
        # TODO: Réactiver la traduction automatique - DÉSACTIVÉ TEMPORAIREMENT
        # self._register_all_widgets_for_translation()

        # ==> COLLECT STRINGS FOR TRANSLATION
        # ///////////////////////////////////////////////////////////////
        # TODO: Réactiver la collecte de chaînes - DÉSACTIVÉ TEMPORAIREMENT
        # self._collect_strings_for_translation()

    # SET APP THEME
    # ///////////////////////////////////////////////////////////////
    def setAppTheme(self) -> None:
        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle:
            # Handle both cases: valueChanged (string) and clicked (no parameter)
            if hasattr(theme_toggle, "value_id"):
                # Use value_id to get current ID
                theme_id = theme_toggle.value_id
                # Convert ID to theme value
                theme = "light" if theme_id == 0 else "dark"
            elif hasattr(theme_toggle, "value"):
                # Use value to get text value
                theme = theme_toggle.value.lower()
            else:
                # Fallback: use current Settings value
                theme = Settings.Gui.THEME

            # Update Settings.Gui.THEME
            Settings.Gui.THEME = theme

            # Save directly to app.settings_panel.theme.default
            Kernel.writeYamlConfig(
                keys=["app", "settings_panel", "theme", "default"], val=theme
            )

            # Force immediate update
            self.updateUI()

    # UPDATE UI
    # ///////////////////////////////////////////////////////////////
    def updateUI(self) -> None:
        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle and hasattr(theme_toggle, "get_value_option"):
            # New OptionSelector version handles positioning automatically
            # No need for manual move_selector
            pass

        # //////
        UIFunctions.theme(self, self._themeFileName)
        # //////
        EzApplication.instance().themeChanged.emit()
        self.ui.headerContainer.update_all_theme_icons()
        self.ui.menuContainer.update_all_theme_icons()
        self.ui.settingsPanel.update_all_theme_icons()

        # //////
        QApplication.processEvents()

        # Force refresh of all widgets
        for widget in QApplication.instance().allWidgets():
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    # SET APP ICON
    # ///////////////////////////////////////////////////////////////
    def setAppIcon(
        self, icon: Union[str, QPixmap], yShrink: int = 0, yOffset: int = 0
    ) -> None:
        return self.ui.headerContainer.set_app_logo(
            logo=icon, y_shrink=yShrink, y_offset=yOffset
        )

    # ADD MENU & PAGE
    # ///////////////////////////////////////////////////////////////
    def addMenu(self, name: str, icon: str) -> QWidget:
        page = self.ui.pagesContainer.add_page(name)
        # //////
        menu = self.ui.menuContainer.add_menu(name, icon)
        menu.setProperty("page", page)
        if len(self.ui.menuContainer.menus) == 1:
            menu.setProperty("class", "active")
        # //////
        menu.clicked.connect(
            lambda: widgets.pagesContainer.stackedWidget.setCurrentWidget(page)
        )
        menu.clicked.connect(self.switchMenu)

        # //////
        return page

    # MENU SWITCH
    # ///////////////////////////////////////////////////////////////
    def switchMenu(self) -> None:
        # GET BUTTON CLICKED
        sender = self.sender()
        senderName = sender.objectName()

        # SHOW HOME PAGE
        for btnName, btnWidget in self.ui.menuContainer.menus.items():
            if senderName == f"menu_{btnName}":
                UIFunctions.deselectMenu(self, senderName)
                UIFunctions.selectMenu(self, senderName)

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event: QResizeEvent) -> None:
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # REGISTER ALL WIDGETS FOR TRANSLATION
    # ///////////////////////////////////////////////////////////////
    def _register_all_widgets_for_translation(self) -> None:
        """Automatically register all widgets with text for translation."""
        try:
            # Safe import of translation functions
            try:
                from .kernel.translation import set_tr, tr as translate_text
            except ImportError as import_error:
                get_printer().warning(
                    f"Could not import translation helpers: {import_error}"
                )
                return

            registered_count = 0
            registered_widgets = set()  # To avoid duplicates

            def register_widget_recursive(widget):
                """Recursive function to register all widgets."""
                nonlocal registered_count

                try:
                    # Avoid already registered widgets
                    if widget in registered_widgets:
                        return

                    # Check if widget has text
                    if hasattr(widget, "text") and callable(
                        getattr(widget, "text", None)
                    ):
                        try:
                            text = widget.text().strip()
                            # Avoid widgets with technical text, numeric values, or too short
                            if (
                                text
                                and not text.isdigit()
                                and len(text) > 1
                                and not text.startswith("_")
                                and not text.startswith("menu_")
                                and not text.startswith("btn_")
                                and not text.startswith("setting")
                            ):

                                # Register widget for translation
                                set_tr(widget, text)
                                registered_widgets.add(widget)
                                registered_count += 1
                        except Exception as text_error:
                            # Ignore text reading errors
                            pass

                    # Check tooltips
                    if hasattr(widget, "toolTip") and callable(
                        getattr(widget, "toolTip", None)
                    ):
                        try:
                            tooltip = widget.toolTip().strip()
                            if (
                                tooltip
                                and not tooltip.isdigit()
                                and len(tooltip) > 1
                                and not tooltip.startswith("_")
                            ):
                                # For tooltips, we can use setToolTip with tr()
                                widget.setToolTip(translate_text(tooltip))
                        except Exception as tooltip_error:
                            # Ignore tooltip errors
                            pass

                    # Check placeholders
                    if hasattr(widget, "placeholderText") and callable(
                        getattr(widget, "placeholderText", None)
                    ):
                        try:
                            placeholder = widget.placeholderText().strip()
                            if (
                                placeholder
                                and not placeholder.isdigit()
                                and len(placeholder) > 1
                                and not placeholder.startswith("_")
                            ):
                                widget.setPlaceholderText(translate_text(placeholder))
                        except Exception as placeholder_error:
                            # Ignore placeholder errors
                            pass

                    # Iterate through all children
                    try:
                        for child in widget.findChildren(QWidget):
                            register_widget_recursive(child)
                    except Exception as children_error:
                        # Ignore child search errors
                        pass

                except Exception as widget_error:
                    # Ignore individual widget errors
                    pass

            # Start with main window
            register_widget_recursive(self)

            # Manually register specific widgets with fixed text
            self._register_specific_widgets_for_translation()
            get_printer().action(
                f"[AppKernel] {registered_count} widgets registered for translation."
            )

        except Exception as e:
            get_printer().warning(f"Could not register widgets for translation: {e}")

    def _register_specific_widgets_for_translation(self) -> None:
        """Manually register specific widgets with fixed text."""
        try:
            from .kernel.translation import set_tr

            # Widgets in ui_main.py with fixed text

            # Widgets in settings_panel with fixed text
            if hasattr(self.ui, "settingsPanel"):
                settings_panel = self.ui.settingsPanel

                # Register dynamically created settings widgets
                for widget in getattr(settings_panel, "_widgets", []):
                    if hasattr(widget, "label") and widget.label:
                        try:
                            text = widget.label.text()
                            if text and len(text) > 1:
                                set_tr(widget.label, text)
                        except:
                            pass

                # Register theme label
                if hasattr(settings_panel, "themeLabel"):
                    set_tr(settings_panel.themeLabel, "Theme")

                # Register theme selector options
                if hasattr(settings_panel, "themeToggleButton"):
                    theme_button = settings_panel.themeToggleButton
                    try:
                        # New OptionSelector version handles translations automatically
                        # No need to manually register items
                        pass
                    except:
                        pass

            # Widgets in menu with fixed text
            if hasattr(self.ui, "menuContainer"):
                menu_container = self.ui.menuContainer

                # Register dynamically created menu buttons
                for button in getattr(menu_container, "_buttons", []):
                    if hasattr(button, "text_label") and button.text_label:
                        try:
                            text = button.text_label.text()
                            if text and len(text) > 1:
                                set_tr(button.text_label, text)
                        except:
                            pass

            # Widgets in header with fixed text
            if hasattr(self.ui, "headerContainer"):
                header_container = self.ui.headerContainer

                # Register header labels
                if hasattr(header_container, "headerAppName"):
                    try:
                        text = header_container.headerAppName.text()
                        if text and len(text) > 1:
                            set_tr(header_container.headerAppName, text)
                    except:
                        pass

                if hasattr(header_container, "headerAppDescription"):
                    try:
                        text = header_container.headerAppDescription.text()
                        if text and len(text) > 1:
                            set_tr(header_container.headerAppDescription, text)
                    except:
                        pass

            # ezqt_widgets widgets with text
            # Note: These widgets generally handle their own translations
            # but we can register their text for automatic retranslation

            # ToggleSwitch widgets (in setting_widgets)
            # OptionSelector widgets (in settings_panel)
            # These widgets are already handled by automatic registration

        except Exception as e:
            # Ignore errors for this function
            pass

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event: QMouseEvent) -> None:
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()

        # //////
        if _dev:
            # PRINT OBJECT NAME
            # //////
            child_widget = self.childAt(event.position().toPoint())
            if child_widget:
                child_name = child_widget.objectName()
                get_printer().verbose_msg(f"Mouse click on widget: {child_name}")

            # PRINT MOUSE EVENTS
            # //////
            elif event.buttons() == Qt.LeftButton:
                get_printer().verbose_msg("Mouse click: LEFT CLICK")
            elif event.buttons() == Qt.RightButton:
                get_printer().verbose_msg("Mouse click: RIGHT CLICK")

    def set_credits(self, credits):
        """
        Set the credits text in the bottom bar.
        Can be a simple string, a dict {"name": ..., "email": ...}, or a JSON string.
        """
        if hasattr(self.ui, "bottomBar") and self.ui.bottomBar:
            self.ui.bottomBar.set_credits(credits)

    def set_version(self, version):
        """
        Set the version text in the bottom bar.
        Can be a string ("1.0.0", "v1.0.0", etc).
        """
        if hasattr(self.ui, "bottomBar") and self.ui.bottomBar:
            self.ui.bottomBar.set_version(version)

    # TRANSLATION MANAGEMENT METHODS
    # ///////////////////////////////////////////////////////////////

    def scan_widgets_for_translation(self, widget=None, recursive=True):
        """
        Scan a widget to find translatable text.

        Parameters
        ----------
        widget : QWidget, optional
            Widget to scan (default: main window)
        recursive : bool
            If True, also scan child widgets

        Returns
        -------
        List[Tuple[QWidget, str]]
            List of tuples (widget, text) found
        """
        from .kernel.translation import scan_widgets_for_translation

        if widget is None:
            widget = self

        return scan_widgets_for_translation(widget, recursive)

    def register_widgets_manually(self, widgets_list):
        """
        Manually register a list of widgets for translation.

        Parameters
        ----------
        widgets_list : List[Tuple[QWidget, str]]
            List of tuples (widget, text) to register

        Returns
        -------
        int
            Number of widgets registered
        """
        from .kernel.translation import register_widgets_manually

        return register_widgets_manually(widgets_list)

    def scan_and_register_widgets(self, widget=None, recursive=True):
        """
        Scan a widget and automatically register all found widgets.

        Parameters
        ----------
        widget : QWidget, optional
            Widget to scan (default: main window)
        recursive : bool
            If True, also scan child widgets

        Returns
        -------
        int
            Number of widgets registered
        """
        from .kernel.translation import scan_and_register_widgets

        if widget is None:
            widget = self

        return scan_and_register_widgets(widget, recursive)

    def get_translation_stats(self):
        """
        Return complete translation system statistics.

        Returns
        -------
        dict
            Detailed statistics
        """
        from .kernel.translation import get_translation_stats

        return get_translation_stats()

    def enable_auto_translation(self, enabled=True):
        """
        Enable or disable automatic translation.

        Parameters
        ----------
        enabled : bool
            True to enable, False to disable
        """
        from .kernel.translation import enable_auto_translation

        enable_auto_translation(enabled)

    def clear_translation_cache(self):
        """Clear the automatic translation cache."""
        from .kernel.translation import clear_auto_translation_cache

        clear_auto_translation_cache()

    def _collect_strings_for_translation(self):
        """Automatically collect strings for translation."""
        try:
            from .kernel.translation import collect_and_compare_strings

            # Collect strings from entire application
            stats = collect_and_compare_strings(self, recursive=True)

            get_printer().info(
                f"[AppKernel] Automatic collection completed: {stats['new_strings']} new strings found"
            )

        except Exception as e:
            get_printer().warning(f"Error during automatic string collection: {e}")

    def collect_strings_for_translation(self, widget=None, recursive=True):
        """
        Collect character strings for translation.

        Parameters
        ----------
        widget : QWidget, optional
            Widget to scan (default: main window)
        recursive : bool
            If True, also scan child widgets

        Returns
        -------
        dict
            Collection statistics
        """
        from .kernel.translation import collect_and_compare_strings

        if widget is None:
            widget = self

        return collect_and_compare_strings(widget, recursive)

    def get_new_strings(self):
        """
        Return newly found strings.

        Returns
        -------
        set
            Set of new strings
        """
        from .kernel.translation import get_new_strings

        return get_new_strings()

    def mark_strings_as_registered(self, strings=None):
        """
        Mark strings as registered.

        Parameters
        ----------
        strings : set, optional
            Strings to mark (default: all new strings)
        """
        from .kernel.translation import mark_strings_as_registered

        mark_strings_as_registered(strings)

    def get_string_collector_stats(self):
        """
        Return string collector statistics.

        Returns
        -------
        dict
            Detailed statistics
        """
        from .kernel.translation import get_string_collector_stats

        return get_string_collector_stats()
