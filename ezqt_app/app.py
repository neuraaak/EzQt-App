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
    Application principale EzQt_App.

    Cette classe représente la fenêtre principale de l'application
    avec tous ses composants (menu, pages, paramètres, etc.).
    """

    def __init__(
        self,
        themeFileName: Optional[str] = None,
    ) -> None:
        """
        Initialise l'application EzQt_App.

        Parameters
        ----------
        themeFileName : str, optional
            Nom du fichier de thème à utiliser (défaut: None).
        """
        QMainWindow.__init__(self)

        # ////// KERNEL LOADER
        # ///////////////////////////////////////////////////////////////
        Kernel.loadFontsResources()
        Kernel.loadAppSettings()

        # ////// LOAD TRANSLATIONS
        # ///////////////////////////////////////////////////////////////
        from .kernel.translation import get_translation_manager

        # Charger la langue depuis les paramètres
        try:
            settings_panel = Kernel.loadKernelConfig("settings_panel")
            language = settings_panel.get("language", {}).get("default", "English")
            translation_manager = get_translation_manager()
            translation_manager.load_language(language)
        except KeyError:
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
        # Charger le thème depuis settings_panel s'il existe, sinon depuis app
        try:
            settings_panel = Kernel.loadKernelConfig("settings_panel")
            _theme = settings_panel.get("theme", {}).get(
                "default", Kernel.loadKernelConfig("app")["theme"]
            )
            # Forcer la conversion en minuscules
            _theme = _theme.lower()
        except KeyError:
            _theme = Kernel.loadKernelConfig("app")["theme"]
            # Forcer la conversion en minuscules
            _theme = _theme.lower()

        # Mettre à jour Settings.Gui.THEME avec la valeur en minuscules
        Settings.Gui.THEME = _theme

        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle and hasattr(theme_toggle, "initialize_selector"):
            try:
                # Convertir la valeur de thème en ID
                theme_id = 0 if _theme == "light" else 1  # 0 = Light, 1 = Dark
                theme_toggle.initialize_selector(theme_id)
            except Exception as e:
                # Ignorer les erreurs d'initialisation
                pass
        self.ui.headerContainer.update_all_theme_icons()
        self.ui.menuContainer.update_all_theme_icons()
        # //////
        if theme_toggle:
            # Connecter le signal valueChanged au lieu de clicked pour la nouvelle version
            if hasattr(theme_toggle, "valueChanged"):
                theme_toggle.valueChanged.connect(self.setAppTheme)
            elif hasattr(theme_toggle, "clicked"):
                theme_toggle.clicked.connect(self.setAppTheme)

        # ==> REGISTER ALL WIDGETS FOR TRANSLATION
        # ///////////////////////////////////////////////////////////////
        self._register_all_widgets_for_translation()

    # SET APP THEME
    # ///////////////////////////////////////////////////////////////
    def setAppTheme(self) -> None:
        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle:
            # Gérer les deux cas : valueChanged (chaîne) et clicked (pas de paramètre)
            if hasattr(theme_toggle, "value_id"):
                # Utiliser value_id pour obtenir l'ID actuel
                theme_id = theme_toggle.value_id
                # Convertir l'ID en valeur de thème
                theme = "light" if theme_id == 0 else "dark"
            elif hasattr(theme_toggle, "value"):
                # Utiliser value pour obtenir la valeur textuelle
                theme = theme_toggle.value.lower()
            else:
                # Fallback : utiliser la valeur actuelle de Settings
                theme = Settings.Gui.THEME

            # Mettre à jour Settings.Gui.THEME
            Settings.Gui.THEME = theme

            # Sauvegarder directement dans settings_panel.theme.default
            Kernel.writeYamlConfig(
                keys=["settings_panel", "theme", "default"], val=theme
            )

            # Forcer la mise à jour immédiate
            self.updateUI()

    # UPDATE UI
    # ///////////////////////////////////////////////////////////////
    def updateUI(self) -> None:
        theme_toggle = self.ui.settingsPanel.get_theme_toggle_button()
        if theme_toggle and hasattr(theme_toggle, "get_value_option"):
            # La nouvelle version d'OptionSelector gère automatiquement le positionnement
            # Pas besoin de move_selector manuel
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

        # Forcer le rafraîchissement de tous les widgets
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
        """Enregistre automatiquement tous les widgets avec du texte pour la traduction."""
        try:
            # Import sécurisé des fonctions de traduction
            try:
                from .kernel.translation import set_tr, tr as translate_text
            except ImportError as import_error:
                get_printer().warning(
                    f"Could not import translation helpers: {import_error}"
                )
                return

            registered_count = 0
            registered_widgets = set()  # Pour éviter les doublons

            def register_widget_recursive(widget):
                """Fonction récursive pour enregistrer tous les widgets."""
                nonlocal registered_count

                try:
                    # Éviter les widgets déjà enregistrés
                    if widget in registered_widgets:
                        return

                    # Vérifier si le widget a du texte
                    if hasattr(widget, "text") and callable(
                        getattr(widget, "text", None)
                    ):
                        try:
                            text = widget.text().strip()
                            # Éviter les widgets avec du texte technique, valeurs numériques, ou trop courts
                            if (
                                text
                                and not text.isdigit()
                                and len(text) > 1
                                and not text.startswith("_")
                                and not text.startswith("menu_")
                                and not text.startswith("btn_")
                                and not text.startswith("setting")
                            ):

                                # Enregistrer le widget pour la traduction
                                set_tr(widget, text)
                                registered_widgets.add(widget)
                                registered_count += 1
                        except Exception as text_error:
                            # Ignorer les erreurs de lecture de texte
                            pass

                    # Vérifier les tooltips
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
                                # Pour les tooltips, on peut utiliser setToolTip avec tr()
                                widget.setToolTip(translate_text(tooltip))
                        except Exception as tooltip_error:
                            # Ignorer les erreurs de tooltip
                            pass

                    # Vérifier les placeholders
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
                            # Ignorer les erreurs de placeholder
                            pass

                    # Parcourir tous les enfants
                    try:
                        for child in widget.findChildren(QWidget):
                            register_widget_recursive(child)
                    except Exception as children_error:
                        # Ignorer les erreurs de recherche d'enfants
                        pass

                except Exception as widget_error:
                    # Ignorer les erreurs individuelles de widgets
                    pass

            # Commencer par la fenêtre principale
            register_widget_recursive(self)

            # Enregistrer manuellement les widgets spécifiques avec du texte fixe
            self._register_specific_widgets_for_translation()
            get_printer().action(
                f"[AppKernel] {registered_count} widgets registered for translation."
            )

        except Exception as e:
            get_printer().warning(f"Could not register widgets for translation: {e}")

    def _register_specific_widgets_for_translation(self) -> None:
        """Enregistre manuellement les widgets spécifiques avec du texte fixe."""
        try:
            from .kernel.translation import set_tr

            # Widgets dans ui_main.py avec du texte fixe

            # Widgets dans settings_panel avec du texte fixe
            if hasattr(self.ui, "settingsPanel"):
                settings_panel = self.ui.settingsPanel

                # Enregistrer les widgets de paramètres créés dynamiquement
                for widget in getattr(settings_panel, "_widgets", []):
                    if hasattr(widget, "label") and widget.label:
                        try:
                            text = widget.label.text()
                            if text and len(text) > 1:
                                set_tr(widget.label, text)
                        except:
                            pass

                # Enregistrer le label de thème
                if hasattr(settings_panel, "themeLabel"):
                    set_tr(settings_panel.themeLabel, "Theme")

                # Enregistrer les options du sélecteur de thème
                if hasattr(settings_panel, "themeToggleButton"):
                    theme_button = settings_panel.themeToggleButton
                    try:
                        # La nouvelle version d'OptionSelector gère automatiquement les traductions
                        # Pas besoin d'enregistrer manuellement les items
                        pass
                    except:
                        pass

            # Widgets dans menu avec du texte fixe
            if hasattr(self.ui, "menuContainer"):
                menu_container = self.ui.menuContainer

                # Enregistrer les boutons de menu créés dynamiquement
                for button in getattr(menu_container, "_buttons", []):
                    if hasattr(button, "text_label") and button.text_label:
                        try:
                            text = button.text_label.text()
                            if text and len(text) > 1:
                                set_tr(button.text_label, text)
                        except:
                            pass

            # Widgets dans header avec du texte fixe
            if hasattr(self.ui, "headerContainer"):
                header_container = self.ui.headerContainer

                # Enregistrer les labels du header
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

            # Widgets de ezqt_widgets avec du texte
            # Note: Ces widgets gèrent généralement leurs propres traductions
            # mais on peut enregistrer leurs textes pour la retraduction automatique

            # ToggleSwitch widgets (dans setting_widgets)
            # OptionSelector widgets (dans settings_panel)
            # Ces widgets sont déjà gérés par l'enregistrement automatique

        except Exception as e:
            # Ignorer les erreurs pour cette fonction
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
        Définit le texte des crédits dans la barre du bas.
        Peut être une chaîne simple, un dict {"name": ..., "email": ...}, ou une chaîne JSON.
        """
        if hasattr(self.ui, "bottomBar") and self.ui.bottomBar:
            self.ui.bottomBar.set_credits(credits)

    def set_version(self, version):
        """
        Définit le texte de version dans la barre du bas.
        Peut être une chaîne ("1.0.0", "v1.0.0", etc).
        """
        if hasattr(self.ui, "bottomBar") and self.ui.bottomBar:
            self.ui.bottomBar.set_version(version)
