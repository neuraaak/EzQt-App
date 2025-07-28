# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    Qt,
    QSize,
    Signal,
)

from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QVBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from ...kernel.app_functions.printer import get_printer
from ...kernel.app_components import *
from ...kernel.app_resources import *
from ...kernel.app_settings import Settings

# Import lazy pour éviter l'import circulaire
# from ...kernel import Kernel

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import List, Dict, Any, Optional

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class SettingsPanel(QFrame):
    """
    This class is used to create a settings panel.
    It contains a top border, a content settings frame and a theme settings container.
    The settings panel is used to display the settings.
    """

    _widgets: List = []  # Type hint removed to avoid circular import
    _settings: Dict[str, Any] = {}  # Stockage des paramètres

    # Signal émis quand un paramètre change
    settingChanged = Signal(str, object)  # key, value
    # Signal émis quand la langue change
    languageChanged = Signal()

    # ///////////////////////////////////////////////////////////////

    def __init__(
        self, parent: QWidget = None, width: int = 240, load_from_yaml: bool = True
    ) -> None:
        super(SettingsPanel, self).__init__(parent)

        # ///////////////////////////////////////////////////////////////
        # Store configuration
        self._width = width

        self.setObjectName("settingsPanel")
        self.setMinimumSize(QSize(0, 0))
        self.setMaximumSize(QSize(0, 16777215))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)
        # //////
        self.VL_settingsPanel = QVBoxLayout(self)
        self.VL_settingsPanel.setSpacing(0)
        self.VL_settingsPanel.setObjectName("VL_settingsPanel")
        self.VL_settingsPanel.setContentsMargins(0, 0, 0, 0)

        # ///////////////////////////////////////////////////////////////

        self.settingsTopBorder = QFrame(self)
        self.settingsTopBorder.setObjectName("settingsTopBorder")
        self.settingsTopBorder.setMaximumSize(QSize(16777215, 3))
        self.settingsTopBorder.setFrameShape(QFrame.NoFrame)
        self.settingsTopBorder.setFrameShadow(QFrame.Raised)
        #
        self.VL_settingsPanel.addWidget(self.settingsTopBorder)

        # ///////////////////////////////////////////////////////////////

        # Créer le QScrollArea pour les paramètres
        self.settingsScrollArea = QScrollArea(self)
        self.settingsScrollArea.setObjectName("settingsScrollArea")
        self.settingsScrollArea.setWidgetResizable(True)
        self.settingsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.settingsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.settingsScrollArea.setFrameShape(QFrame.NoFrame)
        self.settingsScrollArea.setFrameShadow(QFrame.Raised)
        #
        self.VL_settingsPanel.addWidget(self.settingsScrollArea)

        # ///////////////////////////////////////////////////////////////

        # Widget conteneur pour tous les paramètres
        self.contentSettings = QFrame()
        self.contentSettings.setObjectName("contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.contentSettings.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        #
        self.settingsScrollArea.setWidget(self.contentSettings)
        # //////
        self.VL_contentSettings = QVBoxLayout(self.contentSettings)
        self.VL_contentSettings.setObjectName("VL_contentSettings")
        self.VL_contentSettings.setSpacing(0)
        self.VL_contentSettings.setContentsMargins(0, 0, 0, 0)
        self.VL_contentSettings.setAlignment(Qt.AlignTop)

        # ///////////////////////////////////////////////////////////////

        self.themeSettingsContainer = QFrame(self.contentSettings)
        self.themeSettingsContainer.setObjectName("themeSettingsContainer")
        self.themeSettingsContainer.setFrameShape(QFrame.NoFrame)
        self.themeSettingsContainer.setFrameShadow(QFrame.Raised)
        #
        self.VL_contentSettings.addWidget(self.themeSettingsContainer, 0, Qt.AlignTop)
        # //////
        self.VL_themeSettingsContainer = QVBoxLayout(self.themeSettingsContainer)
        self.VL_themeSettingsContainer.setSpacing(8)
        self.VL_themeSettingsContainer.setObjectName("VL_themeSettingsContainer")
        self.VL_themeSettingsContainer.setContentsMargins(10, 10, 10, 10)

        # ///////////////////////////////////////////////////////////////

        self.themeLabel = QLabel("Theme actif", self.themeSettingsContainer)
        self.themeLabel.setObjectName("themeLabel")
        self.themeLabel.setFont(Fonts.SEGOE_UI_10_SB)
        self.themeLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        #
        self.VL_themeSettingsContainer.addWidget(self.themeLabel)

        # ///////////////////////////////////////////////////////////////

        # Créer le sélecteur de thème si OptionSelector est disponible
        try:
            from ezqt_widgets import OptionSelector

            # Créer le sélecteur de thème avec la bonne signature
            # OptionSelector attend: items, default_id, min_width, min_height, orientation, animation_duration, parent
            self.themeToggleButton = OptionSelector(
                items=["Light", "Dark"],  # Liste des options
                default_id=1,  # 0 = Light, 1 = Dark (Dark par défaut)
                min_width=None,
                min_height=None,
                orientation="horizontal",
                animation_duration=Settings.Gui.TIME_ANIMATION,
                parent=self.themeSettingsContainer,
            )
            self.themeToggleButton.setObjectName("themeToggleButton")
            self.themeToggleButton.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
            )
            self.themeToggleButton.setFixedHeight(40)
            self._widgets.append(self.themeToggleButton)

            # Connecter le signal de changement du sélecteur de thème
            self._connect_theme_selector_signals()

            # Ajouter au layout
            self.VL_themeSettingsContainer.addWidget(self.themeToggleButton)

        except ImportError:
            get_printer().warning(
                "OptionSelector not available, theme toggle not created"
            )

        # ///////////////////////////////////////////////////////////////
        # Chargement automatique depuis YAML si demandé
        if load_from_yaml:
            self.load_settings_from_yaml()

        # Connecter les changements de paramètres
        self.settingChanged.connect(self._on_setting_changed)

    # ///////////////////////////////////////////////////////////////

    def load_settings_from_yaml(self) -> None:
        """Charge les paramètres depuis le fichier YAML."""
        try:
            # Import direct pour éviter l'import circulaire
            from ...kernel.app_functions import Kernel

            # Charger la configuration settings_panel depuis le YAML
            settings_config = Kernel.loadKernelConfig("settings_panel")

            # Créer les widgets pour chaque paramètre
            for key, config in settings_config.items():
                # Exclure le thème car il est déjà géré manuellement par OptionSelector
                if key == "theme":
                    continue

                if config.get("enabled", True):  # Vérifier si le paramètre est activé
                    widget = self.add_setting_from_config(key, config)

                    # Utiliser la valeur default du config (qui peut avoir été mise à jour)
                    default_value = config.get("default")
                    if default_value is not None:
                        widget.set_value(default_value)

        except KeyError:
            get_printer().warning(
                "Section 'settings_panel' not found in YAML configuration"
            )
        except Exception as e:
            get_printer().warning(f"Error loading settings from YAML: {e}")

    def add_setting_from_config(self, key: str, config: dict) -> QWidget:
        """Ajoute un paramètre basé sur sa configuration YAML."""
        setting_type = config.get("type", "text")
        label = config.get("label", key)
        description = config.get("description", "")
        default_value = config.get("default", None)

        # Créer un container pour ce paramètre (comme themeSettingsContainer)
        setting_container = QFrame(self.contentSettings)
        setting_container.setObjectName(f"settingContainer_{key}")
        setting_container.setFrameShape(QFrame.NoFrame)
        setting_container.setFrameShadow(QFrame.Raised)

        # Layout du container avec marges
        container_layout = QVBoxLayout(setting_container)
        container_layout.setSpacing(8)
        container_layout.setObjectName(f"VL_settingContainer_{key}")
        container_layout.setContentsMargins(10, 10, 10, 10)

        # Créer le widget selon le type
        if setting_type == "toggle":
            widget = self._create_toggle_widget(label, description, default_value, key)
        elif setting_type == "select":
            options = config.get("options", [])
            widget = self._create_select_widget(
                label, description, options, default_value, key
            )
        elif setting_type == "slider":
            min_val = config.get("min", 0)
            max_val = config.get("max", 100)
            unit = config.get("unit", "")
            widget = self._create_slider_widget(
                label, description, min_val, max_val, default_value, unit, key
            )
        elif setting_type == "checkbox":
            widget = self._create_checkbox_widget(
                label, description, default_value, key
            )
        else:  # text par défaut
            widget = self._create_text_widget(label, description, default_value, key)

        # Ajouter le widget au container
        container_layout.addWidget(widget)

        # Ajouter le container au layout principal
        self.VL_contentSettings.addWidget(setting_container)

        # Stocker la référence
        self._settings[key] = widget

        return widget

    def _create_toggle_widget(
        self, label: str, description: str, default: bool, key: Optional[str] = None
    ) -> QWidget:
        """Crée un widget toggle avec label et description."""
        from ...widgets.extended.setting_widgets import SettingToggle

        widget = SettingToggle(label, description, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_select_widget(
        self,
        label: str,
        description: str,
        options: List[str],
        default: str,
        key: Optional[str] = None,
    ) -> QWidget:
        """Crée un widget select avec label et description."""
        from ...widgets.extended.setting_widgets import SettingSelect

        widget = SettingSelect(label, description, options, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_slider_widget(
        self,
        label: str,
        description: str,
        min_val: int,
        max_val: int,
        default: int,
        unit: str,
        key: Optional[str] = None,
    ) -> QWidget:
        """Crée un widget slider avec label et description."""
        from ...widgets.extended.setting_widgets import SettingSlider

        widget = SettingSlider(label, description, min_val, max_val, default, unit)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_checkbox_widget(
        self, label: str, description: str, default: bool, key: Optional[str] = None
    ) -> QWidget:
        """Crée un widget checkbox avec label et description."""
        from ...widgets.extended.setting_widgets import SettingCheckbox

        widget = SettingCheckbox(label, description, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_text_widget(
        self, label: str, description: str, default: str, key: Optional[str] = None
    ) -> QWidget:
        """Crée un widget text avec label et description."""
        from ...widgets.extended.setting_widgets import SettingText

        widget = SettingText(label, description, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    # ///////////////////////////////////////////////////////////////
    # Méthodes simplifiées pour ajout manuel de paramètres

    def add_toggle_setting(
        self,
        key: str,
        label: str,
        default: bool = False,
        description: str = "",
        enabled: bool = True,
    ):
        """Ajoute un paramètre toggle."""
        from ...widgets.extended.setting_widgets import SettingToggle

        widget = SettingToggle(label, description, default)
        widget._key = key  # Définir la clé
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def add_select_setting(
        self,
        key: str,
        label: str,
        options: List[str],
        default: str = None,
        description: str = "",
        enabled: bool = True,
    ):
        """Ajoute un paramètre de sélection."""
        from ...widgets.extended.setting_widgets import SettingSelect

        widget = SettingSelect(label, description, options, default)
        widget._key = key  # Définir la clé
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def add_slider_setting(
        self,
        key: str,
        label: str,
        min_val: int,
        max_val: int,
        default: int,
        unit: str = "",
        description: str = "",
        enabled: bool = True,
    ):
        """Ajoute un paramètre slider."""
        from ...widgets.extended.setting_widgets import SettingSlider

        widget = SettingSlider(label, description, min_val, max_val, default, unit)
        widget._key = key  # Définir la clé
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def add_text_setting(
        self,
        key: str,
        label: str,
        default: str = "",
        description: str = "",
        enabled: bool = True,
    ):
        """Ajoute un paramètre texte."""
        from ...widgets.extended.setting_widgets import SettingText

        widget = SettingText(label, description, default)
        widget._key = key  # Définir la clé
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def add_checkbox_setting(
        self,
        key: str,
        label: str,
        default: bool = False,
        description: str = "",
        enabled: bool = True,
    ):
        """Ajoute un paramètre checkbox."""
        from ...widgets.extended.setting_widgets import SettingCheckbox

        widget = SettingCheckbox(label, description, default)
        widget._key = key  # Définir la clé
        widget.valueChanged.connect(self._on_setting_changed)

        self._settings[key] = widget
        self.add_setting_widget(widget)
        return widget

    def _on_setting_changed(self, key: str, value):
        """Appelé quand un paramètre change."""
        # Protection contre la récursion
        if not hasattr(self, "_processing_setting_change"):
            self._processing_setting_change = False

        if self._processing_setting_change:
            return  # Éviter la récursion

        self._processing_setting_change = True

        try:
            # Sauvegarder dans YAML
            try:
                # Import direct pour éviter l'import circulaire
                from ...kernel.app_functions import Kernel

                # Sauvegarder directement dans settings_panel[key].default
                Kernel.writeYamlConfig(["settings_panel", key, "default"], value)
            except Exception as e:
                get_printer().warning(f"Could not save setting '{key}' to YAML: {e}")

            # Gestion spéciale pour les changements de langue
            if key == "language":
                try:
                    from ...kernel.translation import get_translation_manager

                    translation_manager = get_translation_manager()
                    # Vérifier si la langue change vraiment
                    current_lang = translation_manager.get_current_language_name()
                    if current_lang != str(value):
                        translation_manager.load_language(str(value))
                        # Émettre le signal de changement de langue
                        self.languageChanged.emit()
                except Exception as e:
                    get_printer().warning(f"Could not change language: {e}")

            # Émettre un signal pour l'application
            self.settingChanged.emit(key, value)
        finally:
            self._processing_setting_change = False

    # ///////////////////////////////////////////////////////////////
    # Méthodes utilitaires

    def get_setting_value(self, key: str) -> Any:
        """Récupère la valeur d'un paramètre."""
        if key in self._settings:
            return self._settings[key].get_value()
        return None

    def set_setting_value(self, key: str, value: Any) -> None:
        """Définit la valeur d'un paramètre."""
        if key in self._settings:
            self._settings[key].set_value(value)

    def get_all_settings(self) -> Dict[str, Any]:
        """Récupère tous les paramètres et leurs valeurs."""
        return {key: widget.get_value() for key, widget in self._settings.items()}

    def save_all_settings_to_yaml(self) -> None:
        """Sauvegarde tous les paramètres dans le YAML."""
        # Import direct pour éviter l'import circulaire
        from ...kernel.app_functions import Kernel

        for key, widget in self._settings.items():
            try:
                Kernel.writeYamlConfig(
                    ["settings_panel", key, "default"], widget.get_value()
                )
            except Exception as e:
                get_printer().warning(f"Could not save setting '{key}' to YAML: {e}")

    # ///////////////////////////////////////////////////////////////
    # Méthodes existantes (conservées pour compatibilité)

    def get_width(self) -> int:
        """Get the configured width."""
        return self._width

    def set_width(self, width: int) -> None:
        """Set the configured width."""
        self._width = width

    def get_theme_toggle_button(self):
        """Get the theme toggle button if available."""
        if hasattr(self, "themeToggleButton"):
            return self.themeToggleButton
        return None

    def update_all_theme_icons(self) -> None:
        """Update theme icons for all widgets that support it."""
        for widget in self._widgets:
            if hasattr(widget, "update_theme_icon"):
                widget.update_theme_icon()

        # Forcer le rafraîchissement du style du panneau de paramètres
        self.style().unpolish(self)
        self.style().polish(self)

        # Rafraîchir aussi tous les widgets enfants
        for child in self.findChildren(QWidget):
            child.style().unpolish(child)
            child.style().polish(child)

    def _connect_theme_selector_signals(self) -> None:
        """Connecte les signaux du sélecteur de thème."""
        try:
            if hasattr(self, "themeToggleButton"):
                # Connecter le signal valueChanged du OptionSelector
                theme_button = self.themeToggleButton

                if hasattr(theme_button, "valueChanged"):
                    theme_button.valueChanged.connect(self._on_theme_selector_changed)
                elif hasattr(theme_button, "clicked"):
                    theme_button.clicked.connect(self._on_theme_selector_clicked)
        except Exception as e:
            pass

    def _on_theme_selector_changed(self, value):
        """Appelé quand le sélecteur de thème change."""
        try:
            # OptionSelector.value retourne déjà "Light" ou "Dark"
            english_value = value.lower()

            # Sauvegarder la valeur anglaise dans le YAML
            from ...kernel.app_functions import Kernel

            Kernel.writeYamlConfig(
                ["settings_panel", "theme", "default"], english_value
            )

            # Émettre le signal avec la valeur anglaise
            self.settingChanged.emit("theme", english_value)

        except Exception as e:
            get_printer().warning(f"Could not handle theme selector change: {e}")

    def _on_theme_selector_clicked(self):
        """Appelé quand le sélecteur de thème est cliqué."""
        try:
            if hasattr(self, "themeToggleButton"):
                # Récupérer directement la valeur textuelle
                current_value = self.themeToggleButton.value.lower()

                # Sauvegarder la valeur anglaise dans le YAML
                from ...kernel.app_functions import Kernel

                Kernel.writeYamlConfig(
                    ["settings_panel", "theme", "default"], current_value
                )

                # Émettre le signal avec la valeur anglaise
                self.settingChanged.emit("theme", current_value)

        except Exception as e:
            get_printer().warning(f"Could not handle theme selector click: {e}")

    def update_theme_selector_items(self) -> None:
        """Met à jour les items du sélecteur de thème avec les traductions."""
        try:
            if hasattr(self, "themeToggleButton"):
                from ...kernel.translation import tr

                # Traduire les items pour l'affichage
                translated_items = [tr("Light"), tr("Dark")]

                # Sauvegarder la valeur actuelle (ID)
                theme_button = self.themeToggleButton
                current_id = (
                    theme_button.value_id if hasattr(theme_button, "value_id") else 0
                )

                # Mettre à jour directement les textes des widgets
                if hasattr(theme_button, "_options"):
                    for i, (option_id, option_widget) in enumerate(
                        theme_button._options.items()
                    ):
                        if i < len(translated_items):
                            if hasattr(option_widget, "label"):
                                option_widget.label.setText(
                                    translated_items[i].capitalize()
                                )
                            elif hasattr(option_widget, "setText"):
                                option_widget.setText(translated_items[i].capitalize())

                # Réappliquer l'ID courant pour maintenir la sélection
                if hasattr(theme_button, "value_id"):
                    # Forcer la mise à jour du sélecteur sans passer par le setter
                    if hasattr(theme_button, "_value_id"):
                        theme_button._value_id = current_id
                        # Forcer le déplacement du sélecteur
                        if current_id in theme_button._options:
                            theme_button.move_selector(
                                theme_button._options[current_id]
                            )

        except Exception as e:
            # Ignorer les erreurs
            pass

    def add_setting_widget(self, widget: QWidget) -> None:
        """Add a new setting widget to the settings panel."""
        # Créer un container pour le paramètre (comme themeSettingsContainer)
        setting_container = QFrame(self.contentSettings)
        setting_container.setObjectName(f"settingContainer_{widget.objectName()}")
        setting_container.setFrameShape(QFrame.NoFrame)
        setting_container.setFrameShadow(QFrame.Raised)

        # Layout du container avec marges (comme VL_themeSettingsContainer)
        container_layout = QVBoxLayout(setting_container)
        container_layout.setSpacing(8)
        container_layout.setContentsMargins(10, 10, 10, 10)

        # Ajouter le widget au container
        container_layout.addWidget(widget)

        # Ajouter le container au layout principal
        self.VL_contentSettings.addWidget(setting_container)
        self._widgets.append(widget)

    def add_setting_section(self, title: str = "") -> QFrame:
        """Add a new settings section with optional title."""
        section = QFrame(self.contentSettings)
        section.setObjectName(f"settingsSection_{title.replace(' ', '_')}")
        section.setFrameShape(QFrame.NoFrame)
        section.setFrameShadow(QFrame.Raised)

        section_layout = QVBoxLayout(section)
        section_layout.setSpacing(8)
        section_layout.setContentsMargins(10, 10, 10, 10)

        if title:
            title_label = QLabel(title, section)
            title_label.setFont(Fonts.SEGOE_UI_10_REG)
            title_label.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
            section_layout.addWidget(title_label)

        self.VL_contentSettings.addWidget(section)
        return section

    def scroll_to_top(self) -> None:
        """Scroll vers le haut du panel de paramètres."""
        if hasattr(self, "settingsScrollArea"):
            self.settingsScrollArea.verticalScrollBar().setValue(0)

    def scroll_to_bottom(self) -> None:
        """Scroll vers le bas du panel de paramètres."""
        if hasattr(self, "settingsScrollArea"):
            scrollbar = self.settingsScrollArea.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def scroll_to_widget(self, widget: QWidget) -> None:
        """
        Scroll vers un widget spécifique dans le panel de paramètres.

        Args:
            widget: Le widget vers lequel scroll
        """
        if hasattr(self, "settingsScrollArea") and widget:
            # Calculer la position du widget dans le scroll area
            widget_pos = widget.mapTo(self.contentSettings, widget.rect().topLeft())
            self.settingsScrollArea.verticalScrollBar().setValue(widget_pos.y())
