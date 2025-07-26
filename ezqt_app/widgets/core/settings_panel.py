# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import List, Dict, Any, Optional

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
    QHBoxLayout,
    QLabel,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from ...kernel.app_components import *
from ...kernel.app_resources import *
from ...kernel.app_settings import Settings

# Import lazy pour éviter l'import circulaire
# from ...kernel import Kernel

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

        self.contentSettings = QFrame(self)
        self.contentSettings.setObjectName("contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        #
        self.VL_settingsPanel.addWidget(self.contentSettings)
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

        # Lazy import to avoid circular imports
        try:
            from ezqt_widgets import OptionSelector

            self.themeToggleButton = OptionSelector(
                items=["Light", "Dark"],
                parent=self.themeSettingsContainer,
                animation_duration=Settings.Gui.TIME_ANIMATION,
            )
            self.themeToggleButton.setObjectName("themeToggleButton")
            self.themeToggleButton.setSizePolicy(SizePolicy.H_EXPANDING_V_FIXED)
            self.themeToggleButton.setFixedHeight(40)
            self._widgets.append(self.themeToggleButton)
            #
            self.VL_themeSettingsContainer.addWidget(self.themeToggleButton)
        except ImportError:
            print("Warning: OptionSelector not available, theme toggle not created")

        # ///////////////////////////////////////////////////////////////
        # Chargement automatique depuis YAML si demandé
        if load_from_yaml:
            self.load_settings_from_yaml()

    # ///////////////////////////////////////////////////////////////

    def load_settings_from_yaml(self) -> None:
        """Charge les paramètres depuis le fichier YAML."""
        try:
            # Import lazy pour éviter l'import circulaire
            from ...kernel import Kernel

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
            print("Warning: Section 'settings_panel' not found in YAML configuration")
        except Exception as e:
            print(f"Warning: Error loading settings from YAML: {e}")

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
        self, label: str, description: str, default: bool, key: str = None
    ) -> QWidget:
        """Crée un widget toggle avec label et description."""
        from ...widgets.extended.setting_widgets import SettingToggle

        widget = SettingToggle(label, description, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_select_widget(
        self, label: str, description: str, options: list, default: str, key: str = None
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
        key: str = None,
    ) -> QWidget:
        """Crée un widget slider avec label et description."""
        from ...widgets.extended.setting_widgets import SettingSlider

        widget = SettingSlider(label, description, min_val, max_val, default, unit)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_checkbox_widget(
        self, label: str, description: str, default: bool, key: str = None
    ) -> QWidget:
        """Crée un widget checkbox avec label et description."""
        from ...widgets.extended.setting_widgets import SettingCheckbox

        widget = SettingCheckbox(label, description, default)
        if key:
            widget._key = key
        widget.valueChanged.connect(self._on_setting_changed)
        return widget

    def _create_text_widget(
        self, label: str, description: str, default: str, key: str = None
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
        # Sauvegarder dans YAML
        try:
            # Import lazy pour éviter l'import circulaire
            from ...kernel import Kernel

            # Sauvegarder directement dans settings_panel[key].default
            Kernel.writeYamlConfig(["settings_panel", key, "default"], value)
        except Exception as e:
            print(f"Warning: Could not save setting '{key}' to YAML: {e}")

        # Émettre un signal pour l'application
        self.settingChanged.emit(key, value)

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
        # Import lazy pour éviter l'import circulaire
        from ...kernel import Kernel

        for key, widget in self._settings.items():
            try:
                Kernel.writeYamlConfig(
                    ["settings_panel", key, "default"], widget.get_value()
                )
            except Exception as e:
                print(f"Warning: Could not save setting '{key}' to YAML: {e}")

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
