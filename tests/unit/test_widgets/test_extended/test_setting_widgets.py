# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour les widgets de paramètres étendus.
"""

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QSlider, QLineEdit

from ezqt_app.widgets.extended.setting_widgets import (
    BaseSettingWidget,
    SettingToggle,
    SettingSelect,
    SettingSlider,
    SettingText,
    SettingCheckbox
)


class TestBaseSettingWidget:
    """Tests pour la classe BaseSettingWidget."""

    def test_init(self, qt_application):
        """Test de l'initialisation."""
        widget = BaseSettingWidget("Test Label", "Test Description")
        
        # Vérifier les propriétés de base
        assert widget._label == "Test Label"
        assert widget._description == "Test Description"
        assert widget._key is None
        assert widget.objectName() == "BaseSettingWidget"

    def test_set_key(self, qt_application):
        """Test de définition de la clé."""
        widget = BaseSettingWidget("Test Label")
        
        # Définir une clé
        widget.set_key("test_key")
        assert widget._key == "test_key"


class TestSettingToggle:
    """Tests pour la classe SettingToggle."""

    def test_init_default(self, qt_application):
        """Test de l'initialisation avec des valeurs par défaut."""
        widget = SettingToggle("Test Toggle")
        
        # Vérifier les propriétés de base
        assert widget._label == "Test Toggle"
        assert widget._description == ""
        assert widget._value == False
        assert widget.objectName() == "SettingToggle"
        assert widget.property("type") == "SettingToggle"

    def test_init_with_description(self, qt_application):
        """Test de l'initialisation avec description."""
        widget = SettingToggle("Test Toggle", "Test Description", True)
        
        # Vérifier les propriétés
        assert widget._label == "Test Toggle"
        assert widget._description == "Test Description"
        assert widget._value == True

    def test_ui_components(self, qt_application):
        """Test des composants de l'interface utilisateur."""
        widget = SettingToggle("Test Toggle")
        
        # Vérifier que les composants existent
        assert hasattr(widget, 'label')
        assert hasattr(widget, 'toggle')
        assert isinstance(widget.label, QLabel)
        
        # Vérifier le texte du label
        assert widget.label.text() == "Test Toggle"

    def test_toggle_value(self, qt_application):
        """Test de la valeur du toggle."""
        widget = SettingToggle("Test Toggle", default=True)
        
        # Vérifier la valeur initiale
        assert widget.value == True
        assert widget.get_value() == True

    def test_set_value(self, qt_application):
        """Test de définition de la valeur."""
        widget = SettingToggle("Test Toggle")
        
        # Définir une nouvelle valeur
        widget.value = True
        assert widget._value == True
        assert widget.value == True

    def test_signal(self, qt_application):
        """Test du signal."""
        widget = SettingToggle("Test Toggle")
        
        # Vérifier que le signal existe
        assert hasattr(widget, 'valueChanged')
        assert isinstance(widget.valueChanged, Signal)


class TestSettingSelect:
    """Tests pour la classe SettingSelect."""

    def test_init_default(self, qt_application):
        """Test de l'initialisation avec des valeurs par défaut."""
        options = ["Option 1", "Option 2", "Option 3"]
        widget = SettingSelect("Test Select", options=options)
        
        # Vérifier les propriétés de base
        assert widget._label == "Test Select"
        assert widget._options == options
        assert widget._value == "Option 1"  # Première option par défaut
        assert widget.objectName() == "SettingSelect"
        assert widget.property("type") == "SettingSelect"

    def test_init_with_default(self, qt_application):
        """Test de l'initialisation avec une valeur par défaut."""
        options = ["Option 1", "Option 2", "Option 3"]
        widget = SettingSelect("Test Select", options=options, default="Option 2")
        
        # Vérifier la valeur par défaut
        assert widget._value == "Option 2"

    def test_ui_components(self, qt_application):
        """Test des composants de l'interface utilisateur."""
        options = ["Option 1", "Option 2", "Option 3"]
        widget = SettingSelect("Test Select", options=options)
        
        # Vérifier que les composants existent
        assert hasattr(widget, 'label')
        assert hasattr(widget, 'combo')
        assert isinstance(widget.label, QLabel)
        assert isinstance(widget.combo, QComboBox)
        
        # Vérifier le texte du label
        assert widget.label.text() == "Test Select"
        
        # Vérifier les options du combo
        assert widget.combo.count() == 3
        assert widget.combo.itemText(0) == "Option 1"
        assert widget.combo.itemText(1) == "Option 2"
        assert widget.combo.itemText(2) == "Option 3"

    def test_value_property(self, qt_application):
        """Test de la propriété value."""
        options = ["Option 1", "Option 2", "Option 3"]
        widget = SettingSelect("Test Select", options=options)
        
        # Vérifier la valeur initiale
        assert widget.value == "Option 1"
        
        # Définir une nouvelle valeur
        widget.value = "Option 3"
        assert widget._value == "Option 3"
        assert widget.combo.currentText() == "Option 3"

    def test_get_set_value(self, qt_application):
        """Test des méthodes get_value et set_value."""
        options = ["Option 1", "Option 2", "Option 3"]
        widget = SettingSelect("Test Select", options=options)
        
        # Vérifier get_value
        assert widget.get_value() == "Option 1"
        
        # Vérifier set_value
        widget.set_value("Option 2")
        assert widget._value == "Option 2"
        assert widget.combo.currentText() == "Option 2"

    def test_signal(self, qt_application):
        """Test du signal."""
        options = ["Option 1", "Option 2", "Option 3"]
        widget = SettingSelect("Test Select", options=options)
        
        # Vérifier que le signal existe
        assert hasattr(widget, 'valueChanged')
        assert isinstance(widget.valueChanged, Signal)


class TestSettingSlider:
    """Tests pour la classe SettingSlider."""

    def test_init_default(self, qt_application):
        """Test de l'initialisation avec des valeurs par défaut."""
        widget = SettingSlider("Test Slider")
        
        # Vérifier les propriétés de base
        assert widget._label == "Test Slider"
        assert widget._min_val == 0
        assert widget._max_val == 100
        assert widget._value == 50
        assert widget._unit == ""
        assert widget.objectName() == "SettingSlider"
        assert widget.property("type") == "SettingSlider"

    def test_init_with_custom_values(self, qt_application):
        """Test de l'initialisation avec des valeurs personnalisées."""
        widget = SettingSlider("Test Slider", min_val=10, max_val=200, default=100, unit="px")
        
        # Vérifier les valeurs personnalisées
        assert widget._min_val == 10
        assert widget._max_val == 200
        assert widget._value == 100
        assert widget._unit == "px"

    def test_ui_components(self, qt_application):
        """Test des composants de l'interface utilisateur."""
        widget = SettingSlider("Test Slider", unit="px")
        
        # Vérifier que les composants existent
        assert hasattr(widget, 'label')
        assert hasattr(widget, 'value_label')
        assert hasattr(widget, 'slider')
        assert isinstance(widget.label, QLabel)
        assert isinstance(widget.value_label, QLabel)
        assert isinstance(widget.slider, QSlider)
        
        # Vérifier le texte du label
        assert widget.label.text() == "Test Slider"
        
        # Vérifier la valeur affichée
        assert widget.value_label.text() == "50px"

    def test_slider_properties(self, qt_application):
        """Test des propriétés du slider."""
        widget = SettingSlider("Test Slider", min_val=10, max_val=200, default=100)
        
        # Vérifier les propriétés du slider
        assert widget.slider.minimum() == 10
        assert widget.slider.maximum() == 200
        assert widget.slider.value() == 100

    def test_value_property(self, qt_application):
        """Test de la propriété value."""
        widget = SettingSlider("Test Slider")
        
        # Vérifier la valeur initiale
        assert widget.value == 50
        
        # Définir une nouvelle valeur
        widget.value = 75
        assert widget._value == 75
        assert widget.slider.value() == 75
        assert widget.value_label.text() == "75"

    def test_get_set_value(self, qt_application):
        """Test des méthodes get_value et set_value."""
        widget = SettingSlider("Test Slider")
        
        # Vérifier get_value
        assert widget.get_value() == 50
        
        # Vérifier set_value
        widget.set_value(80)
        assert widget._value == 80
        assert widget.slider.value() == 80
        assert widget.value_label.text() == "80"

    def test_signal(self, qt_application):
        """Test du signal."""
        widget = SettingSlider("Test Slider")
        
        # Vérifier que le signal existe
        assert hasattr(widget, 'valueChanged')
        assert isinstance(widget.valueChanged, Signal)


class TestSettingText:
    """Tests pour la classe SettingText."""

    def test_init_default(self, qt_application):
        """Test de l'initialisation avec des valeurs par défaut."""
        widget = SettingText("Test Text")
        
        # Vérifier les propriétés de base
        assert widget._label == "Test Text"
        assert widget._description == ""
        assert widget._value == ""
        assert widget.objectName() == "SettingText"
        assert widget.property("type") == "SettingText"

    def test_init_with_default(self, qt_application):
        """Test de l'initialisation avec une valeur par défaut."""
        widget = SettingText("Test Text", default="Default Value")
        
        # Vérifier la valeur par défaut
        assert widget._value == "Default Value"

    def test_ui_components(self, qt_application):
        """Test des composants de l'interface utilisateur."""
        widget = SettingText("Test Text")
        
        # Vérifier que les composants existent
        assert hasattr(widget, 'label')
        assert hasattr(widget, 'text_edit')
        assert isinstance(widget.label, QLabel)
        assert isinstance(widget.text_edit, QLineEdit)
        
        # Vérifier le texte du label
        assert widget.label.text() == "Test Text"

    def test_value_property(self, qt_application):
        """Test de la propriété value."""
        widget = SettingText("Test Text", default="Initial")
        
        # Vérifier la valeur initiale
        assert widget.value == "Initial"
        
        # Définir une nouvelle valeur
        widget.value = "New Value"
        assert widget._value == "New Value"
        assert widget.text_edit.text() == "New Value"

    def test_get_set_value(self, qt_application):
        """Test des méthodes get_value et set_value."""
        widget = SettingText("Test Text")
        
        # Vérifier get_value
        assert widget.get_value() == ""
        
        # Vérifier set_value
        widget.set_value("Test Value")
        assert widget._value == "Test Value"
        assert widget.text_edit.text() == "Test Value"

    def test_signal(self, qt_application):
        """Test du signal."""
        widget = SettingText("Test Text")
        
        # Vérifier que le signal existe
        assert hasattr(widget, 'valueChanged')
        assert isinstance(widget.valueChanged, Signal)


class TestSettingCheckbox:
    """Tests pour la classe SettingCheckbox."""

    def test_init_default(self, qt_application):
        """Test de l'initialisation avec des valeurs par défaut."""
        widget = SettingCheckbox("Test Checkbox")
        
        # Vérifier les propriétés de base
        assert widget._label == "Test Checkbox"
        assert widget._description == ""
        assert widget._value == False
        assert widget.objectName() == "SettingCheckbox"
        assert widget.property("type") == "SettingCheckbox"

    def test_init_with_default(self, qt_application):
        """Test de l'initialisation avec une valeur par défaut."""
        widget = SettingCheckbox("Test Checkbox", default=True)
        
        # Vérifier la valeur par défaut
        assert widget._value == True

    def test_ui_components(self, qt_application):
        """Test des composants de l'interface utilisateur."""
        widget = SettingCheckbox("Test Checkbox")
        
        # Vérifier que les composants existent
        assert hasattr(widget, 'label')
        assert hasattr(widget, 'checkbox')
        assert isinstance(widget.label, QLabel)
        
        # Vérifier le texte du label
        assert widget.label.text() == "Test Checkbox"

    def test_value_property(self, qt_application):
        """Test de la propriété value."""
        widget = SettingCheckbox("Test Checkbox", default=True)
        
        # Vérifier la valeur initiale
        assert widget.value == True
        assert widget.get_value() == True
        
        # Définir une nouvelle valeur
        widget.value = False
        assert widget._value == False

    def test_get_set_value(self, qt_application):
        """Test des méthodes get_value et set_value."""
        widget = SettingCheckbox("Test Checkbox")
        
        # Vérifier get_value
        assert widget.get_value() == False
        
        # Vérifier set_value
        widget.set_value(True)
        assert widget._value == True

    def test_signal(self, qt_application):
        """Test du signal."""
        widget = SettingCheckbox("Test Checkbox")
        
        # Vérifier que le signal existe
        assert hasattr(widget, 'valueChanged')
        assert isinstance(widget.valueChanged, Signal) 