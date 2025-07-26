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
            from ...kernel.translation_helpers import tr

            # Créer les items traduits dès le début
            try:
                translated_items = [tr("Light"), tr("Dark")]
            except:
                # Fallback si la traduction n'est pas disponible
                translated_items = ["Light", "Dark"]

            # S'assurer que les items sont cohérents avec le mapping
            self._init_theme_mapping()

            self.themeToggleButton = OptionSelector(
                items=translated_items,
                default_id=0,  # Utiliser default_id au lieu de default
                parent=self.themeSettingsContainer,
                animation_duration=Settings.Gui.TIME_ANIMATION,
            )
            self.themeToggleButton.setObjectName("themeToggleButton")
            self.themeToggleButton.setSizePolicy(SizePolicy.H_EXPANDING_V_FIXED)
            self.themeToggleButton.setFixedHeight(40)
            self._widgets.append(self.themeToggleButton)

            # Initialiser le mapping de thème AVANT de connecter les signaux
            self._init_theme_mapping()

            # Connecter le signal de changement du sélecteur de thème
            self._connect_theme_selector_signals()

            # Initialiser le sélecteur avec la valeur par défaut depuis le YAML
            self._initialize_theme_selector_default()

            #
            self.VL_themeSettingsContainer.addWidget(self.themeToggleButton)
        except ImportError:
            print("Warning: OptionSelector not available, theme toggle not created")

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
                print(f"Warning: Could not save setting '{key}' to YAML: {e}")

            # Gestion spéciale pour les changements de langue
            if key == "language":
                try:
                    from ...kernel.translation_manager import get_translation_manager

                    translation_manager = get_translation_manager()
                    # Vérifier si la langue change vraiment
                    current_lang = translation_manager.get_current_language_name()
                    if current_lang != str(value):
                        translation_manager.load_language(str(value))
                        # Émettre le signal de changement de langue
                        self.languageChanged.emit()
                except Exception as e:
                    print(f"Warning: Could not change language: {e}")

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

    def _init_theme_mapping(self) -> None:
        """Initialise le mapping entre les IDs et les valeurs anglaises."""
        # Mapping simple : 0 = Light, 1 = Dark
        self._theme_mapping = {0: "Light", 1: "Dark"}

        # Mapping inverse pour la compatibilité
        self._theme_mapping_reverse = {"Light": 0, "Dark": 1, "light": 0, "dark": 1}

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
            # La nouvelle version d'OptionSelector émet directement la valeur textuelle
            # Convertir la valeur en ID puis en valeur anglaise
            theme_id = self._get_theme_id_from_value(value)
            english_value = self._theme_mapping.get(theme_id, "light")

            # Sauvegarder la valeur anglaise dans le YAML
            from ...kernel.app_functions import Kernel

            Kernel.writeYamlConfig(
                ["settings_panel", "theme", "default"], english_value.lower()
            )

            # Émettre le signal avec la valeur anglaise
            self.settingChanged.emit("theme", english_value.lower())

        except Exception as e:
            print(f"Warning: Could not handle theme selector change: {e}")

    def _on_theme_selector_clicked(self):
        """Appelé quand le sélecteur de thème est cliqué."""
        try:
            if hasattr(self, "themeToggleButton"):
                # Récupérer la valeur actuelle (ID)
                current_id = self.themeToggleButton.value_id
                english_value = self._theme_mapping.get(current_id, "light")

                # Sauvegarder la valeur anglaise dans le YAML
                from ...kernel.app_functions import Kernel

                Kernel.writeYamlConfig(
                    ["settings_panel", "theme", "default"], english_value.lower()
                )

                # Émettre le signal avec la valeur anglaise
                self.settingChanged.emit("theme", english_value.lower())

        except Exception as e:
            print(f"Warning: Could not handle theme selector click: {e}")

    def _get_theme_id_from_value(self, value: str) -> int:
        """Convertit une valeur textuelle en ID de thème."""
        # S'assurer que le mapping existe
        if (
            not hasattr(self, "_theme_mapping_reverse")
            or self._theme_mapping_reverse is None
        ):
            self._init_theme_mapping()

        # Chercher dans le mapping inverse
        return self._theme_mapping_reverse.get(value, 0)  # 0 = Light par défaut

    def _initialize_theme_selector_default(self) -> None:
        """Initialise le sélecteur de thème avec la valeur par défaut depuis le YAML."""
        try:
            if hasattr(self, "themeToggleButton"):
                # Charger la valeur par défaut depuis le YAML
                from ...kernel.app_functions import Kernel

                settings_panel = Kernel.loadKernelConfig("settings_panel")
                default_theme = settings_panel.get("theme", {}).get("default", "dark")

                # Convertir en ID
                theme_id = 0 if default_theme.lower() == "light" else 1

                # Initialiser le sélecteur
                if hasattr(self.themeToggleButton, "initialize_selector"):
                    self.themeToggleButton.initialize_selector(theme_id)
                elif hasattr(self.themeToggleButton, "value_id"):
                    self.themeToggleButton.value_id = theme_id

        except Exception as e:
            # Ignorer les erreurs
            pass

    def update_theme_selector_items(self) -> None:
        """Met à jour les items du sélecteur de thème avec les traductions."""
        try:
            if hasattr(self, "themeToggleButton"):
                from ...kernel.translation_helpers import tr

                # Mettre à jour le mapping avec les nouvelles traductions
                self._init_theme_mapping()

                # Traduire les items pour l'affichage
                translated_items = [tr("Light"), tr("Dark")]

                # Sauvegarder la valeur actuelle (ID)
                theme_button = self.themeToggleButton
                current_id = (
                    theme_button.value_id if hasattr(theme_button, "value_id") else 0
                )

                # La nouvelle version d'OptionSelector gère automatiquement les traductions
                # Il suffit de mettre à jour les items et de restaurer l'ID
                if hasattr(theme_button, "items"):
                    theme_button.items = translated_items
                    # Restaurer l'ID actuel
                    theme_button.value_id = current_id

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
