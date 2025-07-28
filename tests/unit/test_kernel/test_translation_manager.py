# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour le TranslationManager.
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from ezqt_app.kernel.translation import TranslationManager


class TestTranslationManager:
    """Tests pour la classe TranslationManager."""

    def test_init_default_language(self):
        """Test de l'initialisation avec la langue par défaut."""
        manager = TranslationManager()
        assert manager.current_language == "en"
        assert manager.translator is not None
        assert len(manager._translatable_widgets) == 0
        assert len(manager._translatable_texts) == 0

    def test_language_mapping(self):
        """Test du mapping des langues."""
        manager = TranslationManager()
        expected_mapping = {
            "English": "en",
            "Français": "fr",
            "Español": "es",
            "Deutsch": "de",
        }
        assert manager.language_mapping == expected_mapping

    def test_get_available_languages(self):
        """Test de récupération des langues disponibles."""
        manager = TranslationManager()
        languages = manager.get_available_languages()
        
        # Vérifier que c'est une liste
        assert isinstance(languages, list)
        
        # Vérifier que les langues de base sont présentes
        expected_languages = ["English", "Français", "Español", "Deutsch"]
        for lang in expected_languages:
            assert lang in languages

    def test_get_current_language_code(self):
        """Test de récupération du code de langue actuel."""
        manager = TranslationManager()
        assert manager.get_current_language_code() == "en"

    def test_get_current_language_name(self):
        """Test de récupération du nom de langue actuel."""
        manager = TranslationManager()
        assert manager.get_current_language_name() == "English"

    def test_translate_text_no_translation(self):
        """Test de traduction de texte sans traduction disponible."""
        manager = TranslationManager()
        text = "Hello World"
        translated = manager.translate(text)
        assert translated == text  # Retourne le texte original si pas de traduction

    @patch("ezqt_app.kernel.translation_manager.QTranslator")
    def test_load_language_success(self, mock_translator):
        """Test de chargement réussi d'une langue."""
        manager = TranslationManager()
        
        # Mock du chargement réussi
        mock_translator_instance = MagicMock()
        mock_translator_instance.load.return_value = True
        mock_translator.return_value = mock_translator_instance

        result = manager.load_language("English")
        assert result == True
        assert manager.get_current_language_code() == "en"

    @patch("ezqt_app.kernel.translation_manager.QTranslator")
    @patch("ezqt_app.kernel.translation_manager.QCoreApplication")
    @patch("pathlib.Path.exists")
    def test_load_language_failure(self, mock_exists, mock_qcore, mock_translator):
        """Test de chargement échoué d'une langue."""
        manager = TranslationManager()
        
        # Mock pour qu'aucun fichier de traduction n'existe
        mock_exists.return_value = False
        
        # Mock de QCoreApplication
        mock_qcore.removeTranslator = MagicMock()
        mock_qcore.installTranslator = MagicMock()
        
        # Mock du chargement échoué
        mock_translator_instance = MagicMock()
        mock_translator_instance.load.return_value = False
        mock_translator.return_value = mock_translator_instance
        
        # Test avec une langue valide mais sans fichier de traduction
        # (pas "InvalidLanguage" car ça retourne "en" par défaut et la langue actuelle est déjà "en")
        result = manager.load_language("Français")
        assert result == False
        
        # Test avec des langues différentes de la langue actuelle
        result = manager.load_language_by_code("fr")
        assert result == False
        
        result = manager.load_language_by_code("es")
        assert result == False

    def test_register_widget(self):
        """Test d'enregistrement d'un widget traduisible."""
        manager = TranslationManager()
        widget = MagicMock()
        original_text = "Test Text"

        manager.register_widget(widget, original_text)

        assert widget in manager._translatable_widgets
        assert manager._translatable_texts[widget] == original_text

    def test_unregister_widget(self):
        """Test de désenregistrement d'un widget traduisible."""
        manager = TranslationManager()
        widget = MagicMock()
        original_text = "Test Text"

        # Enregistrer d'abord
        manager.register_widget(widget, original_text)
        assert widget in manager._translatable_widgets

        # Puis désenregistrer
        manager.unregister_widget(widget)
        assert widget not in manager._translatable_widgets
        assert widget not in manager._translatable_texts

    def test_clear_registered_widgets(self):
        """Test de nettoyage de tous les widgets enregistrés."""
        manager = TranslationManager()
        widget1 = MagicMock()
        widget2 = MagicMock()

        manager.register_widget(widget1, "Text 1")
        manager.register_widget(widget2, "Text 2")

        assert len(manager._translatable_widgets) == 2

        manager.clear_registered_widgets()

        assert len(manager._translatable_widgets) == 0
        assert len(manager._translatable_texts) == 0

    def test_set_translatable_text(self):
        """Test de définition de texte traduisible pour un widget."""
        manager = TranslationManager()
        widget = MagicMock()
        text = "New Text"

        manager.set_translatable_text(widget, text)

        # Vérifier que le widget est enregistré
        assert widget in manager._translatable_widgets
        assert manager._translatable_texts[widget] == text

    @patch("ezqt_app.kernel.translation_manager.QCoreApplication")
    def test_load_language_by_code(self, mock_qcore):
        """Test de chargement de langue par code."""
        manager = TranslationManager()

        # Mock de l'application Qt
        mock_app = MagicMock()
        mock_qcore.instance.return_value = mock_app

        result = manager.load_language_by_code("fr")

        # Vérifier que la langue a été changée
        assert manager.current_language == "fr"
        assert result == True

    def test_language_changed_signal(self, qt_application):
        """Test que le signal languageChanged est émis."""
        manager = TranslationManager()
        
        # Connecter un slot pour capturer le signal
        signal_received = False
        
        def on_language_changed(lang):
            nonlocal signal_received
            signal_received = True
        
        manager.languageChanged.connect(on_language_changed)
        
        # Changer la langue
        with patch("ezqt_app.kernel.translation_manager.QCoreApplication"):
            manager.load_language_by_code("fr")
        
        # Le signal devrait être émis
        assert signal_received
