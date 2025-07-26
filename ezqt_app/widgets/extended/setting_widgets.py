# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import List, Optional, Any
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QComboBox,
    QSlider,
    QLineEdit,
    QFrame,
    QPushButton,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from ...kernel.app_components import *
from ...kernel.app_settings import Settings
from ezqt_widgets import ToggleSwitch

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class BaseSettingWidget(QWidget):
    """Classe de base pour tous les widgets de paramètres."""

    def __init__(self, label: str, description: str = ""):
        super().__init__()
        self._label = label
        self._description = description
        self._key = None
        self.setObjectName("BaseSettingWidget")

    def set_key(self, key: str):
        """Définit la clé du paramètre."""
        self._key = key
    



class SettingToggle(BaseSettingWidget):
    """Widget pour les paramètres toggle (on/off)."""

    def __init__(self, label: str, description: str = "", default: bool = False):
        super().__init__(label, description)
        self._value = default
        self.setObjectName("SettingToggle")
        self.setProperty("type", "SettingToggle")
        self._setup_ui()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        # Container pour le label et le toggle
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)
        control_layout.setContentsMargins(0, 0, 0, 0)

        # Label principal
        self.label = QLabel(self._label)
        self.label.setObjectName("settingLabel")
        self.label.setWordWrap(True)
        control_layout.addWidget(self.label, 1)  # Stretch

        # Toggle (ToggleSwitch moderne)
        # Get animation setting from app settings
        animation_enabled = getattr(Settings.Gui, "TIME_ANIMATION", 400) > 0

        self.toggle = ToggleSwitch(animation=animation_enabled)
        self.toggle.setObjectName("settingToggle")
        self.toggle.checked = self._value
        self.toggle.toggled.connect(self._on_toggled)
        control_layout.addWidget(self.toggle, 0)  # No stretch

        layout.addLayout(control_layout)

        # Description (si présente)
        if self._description:
            self.description_label = QLabel(self.tr(self._description))
            self.description_label.setObjectName("settingDescription")
            self.description_label.setWordWrap(True)
            layout.addWidget(self.description_label)

    def _on_toggled(self, checked: bool):
        """Appelé quand le toggle change."""
        self._value = checked
        self.valueChanged.emit(self._key, checked)

    @property
    def value(self) -> bool:
        """Récupère la valeur actuelle."""
        return self._value

    @value.setter
    def value(self, val: bool):
        """Définit la valeur."""
        self._value = val
        self.toggle.checked = val

    def get_value(self) -> bool:
        """Récupère la valeur actuelle."""
        return self._value

    def set_value(self, val: bool):
        """Définit la valeur."""
        self._value = val
        self.toggle.checked = val

    valueChanged = Signal(str, bool)


class SettingSelect(BaseSettingWidget):
    """Widget pour les paramètres de sélection."""

    def __init__(
        self,
        label: str,
        description: str = "",
        options: list = None,
        default: str = None,
    ):
        super().__init__(label, description)
        self._options = options or []
        self._value = default or (options[0] if options else "")
        self.setObjectName("SettingSelect")
        self.setProperty("type", "SettingSelect")
        self._setup_ui()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        # Label principal
        self.label = QLabel(self._label)
        self.label.setObjectName("settingLabel")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        # ComboBox
        self.combo = QComboBox()
        self.combo.setObjectName("settingComboBox")
        self.combo.addItems(self._options)
        if self._value in self._options:
            self.combo.setCurrentText(self._value)
        self.combo.currentTextChanged.connect(self._on_text_changed)
        layout.addWidget(self.combo)

        # Description (si présente)
        if self._description:
            self.description_label = QLabel(self.tr(self._description))
            self.description_label.setObjectName("settingDescription")
            self.description_label.setWordWrap(True)
            layout.addWidget(self.description_label)

    def _on_text_changed(self, text: str):
        """Appelé quand la sélection change."""
        self._value = text
        self.valueChanged.emit(self._key, text)

    @property
    def value(self) -> str:
        """Récupère la valeur actuelle."""
        return self._value

    @value.setter
    def value(self, val: str):
        """Définit la valeur."""
        self._value = val
        if val in self._options:
            self.combo.setCurrentText(val)

    def get_value(self) -> str:
        """Récupère la valeur actuelle."""
        return self._value

    def set_value(self, val: str):
        """Définit la valeur."""
        self._value = val
        if val in self._options:
            self.combo.setCurrentText(val)

    valueChanged = Signal(str, str)


class SettingSlider(BaseSettingWidget):
    """Widget pour les paramètres numériques avec slider."""

    def __init__(
        self,
        label: str,
        description: str = "",
        min_val: int = 0,
        max_val: int = 100,
        default: int = 50,
        unit: str = "",
    ):
        super().__init__(label, description)
        self._min_val = min_val
        self._max_val = max_val
        self._value = default
        self._unit = unit
        self.setObjectName("SettingSlider")
        self.setProperty("type", "SettingSlider")
        self._setup_ui()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        # Container pour le label et la valeur
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Label principal
        self.label = QLabel(self._label)
        self.label.setObjectName("settingLabel")
        self.label.setWordWrap(True)
        header_layout.addWidget(self.label, 1)  # Stretch

        # Label de valeur
        self.value_label = QLabel(f"{self._value}{self._unit}")
        self.value_label.setObjectName("settingValueLabel")
        header_layout.addWidget(self.value_label, 0)  # No stretch

        layout.addLayout(header_layout)

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setObjectName("settingSlider")
        self.slider.setMinimum(self._min_val)
        self.slider.setMaximum(self._max_val)
        self.slider.setValue(self._value)
        self.slider.valueChanged.connect(self._on_value_changed)
        layout.addWidget(self.slider)

        # Description (si présente)
        if self._description:
            self.description_label = QLabel(self.tr(self._description))
            self.description_label.setObjectName("settingDescription")
            self.description_label.setWordWrap(True)
            layout.addWidget(self.description_label)

    def _on_value_changed(self, value: int):
        """Appelé quand la valeur du slider change."""
        self._value = value
        self.value_label.setText(f"{value}{self._unit}")
        self.valueChanged.emit(self._key, value)

    @property
    def value(self) -> int:
        """Récupère la valeur actuelle."""
        return self._value

    @value.setter
    def value(self, val: int):
        """Définit la valeur."""
        self._value = val
        self.slider.setValue(val)
        self.value_label.setText(f"{val}{self._unit}")

    def get_value(self) -> int:
        """Récupère la valeur actuelle."""
        return self._value

    def set_value(self, val: int):
        """Définit la valeur."""
        self._value = val
        self.slider.setValue(val)
        self.value_label.setText(f"{val}{self._unit}")

    valueChanged = Signal(str, int)


class SettingText(BaseSettingWidget):
    """Widget pour les paramètres texte."""

    def __init__(self, label: str, description: str = "", default: str = ""):
        super().__init__(label, description)
        self._value = default
        self.setObjectName("SettingText")
        self.setProperty("type", "SettingText")
        self._setup_ui()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        # Label principal
        self.label = QLabel(self._label)
        self.label.setObjectName("settingLabel")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        # Champ texte
        self.text_edit = QLineEdit()
        self.text_edit.setObjectName("settingTextEdit")
        self.text_edit.setText(self._value)
        self.text_edit.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.text_edit)

        # Description (si présente)
        if self._description:
            self.description_label = QLabel(self.tr(self._description))
            self.description_label.setObjectName("settingDescription")
            self.description_label.setWordWrap(True)
            layout.addWidget(self.description_label)

    def _on_text_changed(self, text: str):
        """Appelé quand le texte change."""
        self._value = text
        self.valueChanged.emit(self._key, text)

    @property
    def value(self) -> str:
        """Récupère la valeur actuelle."""
        return self._value

    @value.setter
    def value(self, val: str):
        """Définit la valeur."""
        self._value = val
        self.text_edit.setText(val)

    def get_value(self) -> str:
        """Récupère la valeur actuelle."""
        return self._value

    def set_value(self, val: str):
        """Définit la valeur."""
        self._value = val
        self.text_edit.setText(val)

    valueChanged = Signal(str, str)


class SettingCheckbox(BaseSettingWidget):
    """Widget pour les paramètres checkbox (on/off)."""

    def __init__(self, label: str, description: str = "", default: bool = False):
        super().__init__(label, description)
        self._value = default
        self.setObjectName("SettingCheckbox")
        self.setProperty("type", "SettingCheckbox")
        self._setup_ui()

    def _setup_ui(self):
        """Configure l'interface utilisateur."""
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        # Container pour le label et la checkbox
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)
        control_layout.setContentsMargins(0, 0, 0, 0)

        # Label principal
        self.label = QLabel(self._label)
        self.label.setObjectName("settingLabel")
        self.label.setWordWrap(True)
        control_layout.addWidget(self.label, 1)  # Stretch

        # Checkbox (ToggleSwitch moderne)
        # Get animation setting from app settings
        animation_enabled = getattr(Settings.Gui, "TIME_ANIMATION", 400) > 0

        self.checkbox = ToggleSwitch(animation=animation_enabled)
        self.checkbox.setObjectName("settingCheckbox")
        self.checkbox.checked = self._value
        self.checkbox.toggled.connect(self._on_toggled)
        control_layout.addWidget(self.checkbox, 0)  # No stretch

        layout.addLayout(control_layout)

        # Description (si présente)
        if self._description:
            self.description_label = QLabel(self.tr(self._description))
            self.description_label.setObjectName("settingDescription")
            self.description_label.setWordWrap(True)
            layout.addWidget(self.description_label)

    def _on_toggled(self, checked: bool):
        """Appelé quand la checkbox change."""
        self._value = checked
        self.valueChanged.emit(self._key, checked)

    @property
    def value(self) -> bool:
        """Récupère la valeur actuelle."""
        return self._value

    @value.setter
    def value(self, val: bool):
        """Définit la valeur."""
        self._value = val
        self.checkbox.checked = val

    def get_value(self) -> bool:
        """Récupère la valeur actuelle."""
        return self._value

    def set_value(self, val: bool):
        """Définit la valeur."""
        self._value = val
        self.checkbox.checked = val

    valueChanged = Signal(str, bool)
