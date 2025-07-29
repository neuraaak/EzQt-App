# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
# EzQt_App - A Modern Qt Application Framework
# ///////////////////////////////////////////////////////////////
#
# Author: EzQt_App Team
# Website: https://github.com/ezqt-app/ezqt_app
#
# This file is part of EzQt_App.
#
# EzQt_App is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EzQt_App is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EzQt_App.  If not, see <https://www.gnu.org/licenses/>.
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    QTranslator,
    QCoreApplication,
    Signal,
    QObject,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import APP_PATH, Path, sys
from ..app_functions.printer import get_printer
from .config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE
from .auto_translator import get_auto_translator

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class TranslationManager(QObject):
    """Translation manager for EzQt_App"""

    languageChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        self.current_language = DEFAULT_LANGUAGE

        # Automatic retranslation system
        self._translatable_widgets = []  # List of widgets to retranslate
        self._translatable_texts = {}  # {widget: original_text}

        # .ts translations loaded directly
        self._ts_translations = {}

        # Automatic translator
        # TODO: Réactiver la traduction automatique - DÉSACTIVÉ TEMPORAIREMENT
        self.auto_translator = get_auto_translator()
        self.auto_translation_enabled = False  # DÉSACTIVÉ TEMPORAIREMENT

        # Determine translations path
        if hasattr(sys, "_MEIPASS"):
            # Frozen mode (executable)
            self.translations_dir = (
                Path(sys._MEIPASS) / "ezqt_app" / "resources" / "translations"
            )
        else:
            # Development mode - search in priority order
            # Use same logic as makeRequiredFiles
            project_path = Path.cwd()  # Same logic as FileMaker(Path.cwd())
            possible_paths = [
                project_path / "bin" / "translations",  # User project (priority 1)
                APP_PATH / "bin" / "translations",  # APP_PATH (priority 2)
                Path(__file__).parent.parent.parent
                / "resources"
                / "translations",  # Local development (priority 3)
            ]

            # Try to get from installed package if not found
            try:
                package_translations = self._get_package_translations_dir()
                if package_translations.exists():
                    possible_paths.append(
                        package_translations
                    )  # Installed package (priority 4)
            except Exception as e:
                # print(f"⚠️ Unable to retrieve package translations: {e}")
                pass

            # Find first existing directory
            self.translations_dir = None
            for path in possible_paths:
                if path.exists():
                    self.translations_dir = path
                    break

            # If no directory found, create user project directory
            if self.translations_dir is None:
                self.translations_dir = project_path / "bin" / "translations"
                self.translations_dir.mkdir(parents=True, exist_ok=True)

        # Language name to code mapping
        self.language_mapping = {
            "English": "en",
            "Français": "fr",
            "Español": "es",
            "Deutsch": "de",
        }

    def _get_package_translations_dir(self) -> Path:
        """Get installed package translations directory"""
        try:
            import pkg_resources

            return Path(
                pkg_resources.resource_filename("ezqt_app", "resources/translations")
            )
        except Exception:
            return Path(__file__).parent.parent.parent / "resources" / "translations"

    def _load_ts_file(self, ts_file_path: Path) -> bool:
        """Load a .ts file and extract translations"""
        try:
            import xml.etree.ElementTree as ET

            if not ts_file_path.exists():
                return False

            tree = ET.parse(ts_file_path)
            root = tree.getroot()

            # Extract translations from .ts file
            translations = {}
            for message in root.findall(".//message"):
                source = message.find("source")
                translation = message.find("translation")

                if source is not None and translation is not None:
                    source_text = source.text
                    translation_text = translation.text

                    if source_text and translation_text:
                        translations[source_text] = translation_text

            self._ts_translations.update(translations)
            return True

        except Exception as e:
            get_printer().warning(f"Error loading .ts file {ts_file_path}: {e}")
            return False

    def load_language(self, language_name: str) -> bool:
        """Load a language by name"""
        # Create name -> code mapping
        name_to_code = {
            info["name"]: code for code, info in SUPPORTED_LANGUAGES.items()
        }

        if language_name in name_to_code:
            return self.load_language_by_code(name_to_code[language_name])
        return False

    def load_language_by_code(self, language_code: str) -> bool:
        """Load a language by code"""
        if language_code not in SUPPORTED_LANGUAGES:
            get_printer().warning(f"Unsupported language: {language_code}")
            return False

        # Check that QApplication is instantiated before using translators
        app = QCoreApplication.instance()
        if app is not None:
            # Remove old translator only if QApplication exists
            try:
                QCoreApplication.removeTranslator(self.translator)
            except Exception as e:
                get_printer().warning(f"Error removing translator: {e}")

        self.translator = QTranslator()

        # Load new .ts file
        language_info = SUPPORTED_LANGUAGES[language_code]
        ts_file = language_info["file"]
        ts_file_path = self.translations_dir / ts_file

        # Load translations from .ts file
        if self._load_ts_file(ts_file_path):
            # Install translator only if QApplication exists
            if app is not None:
                try:
                    QCoreApplication.installTranslator(self.translator)
                except Exception as e:
                    get_printer().warning(f"Error installing translator: {e}")

            # Update current language
            self.current_language = language_code

            # Display unified message
            get_printer().info(f"Language switched to {language_info['name']}")
        else:
            get_printer().warning(
                f"Unable to load translations for {language_info['name']}"
            )

        # Retranslate all registered widgets
        self._retranslate_all_widgets()

        # Emit language change signal
        self.languageChanged.emit(language_code)

        return True

    def get_available_languages(self) -> list:
        """Return list of available languages"""
        return list(SUPPORTED_LANGUAGES.keys())

    def get_current_language_name(self) -> str:
        """Return current language name"""
        if self.current_language in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[self.current_language]["name"]
        return "Unknown"

    def get_current_language_code(self) -> str:
        """Return current language code"""
        return self.current_language

    def translate(self, text: str) -> str:
        """Translate a text"""
        # First try loaded .ts translations
        if text in self._ts_translations:
            return self._ts_translations[text]

        # Otherwise use Qt translator
        translated = self.translator.translate("", text)
        if translated and translated != text:
            return translated

        # Finally, try automatic translation if enabled
        if self.auto_translation_enabled and self.auto_translator.enabled:
            auto_translated = self.auto_translator.translate_sync(
                text, "en", self.current_language
            )
            if auto_translated:
                # Automatically save to .ts file
                if self.auto_translator.auto_save:
                    self._save_auto_translation_to_ts(text, auto_translated)
                return auto_translated

        return text

    def register_widget(self, widget, original_text: str):
        """Register a widget for automatic retranslation"""
        if widget not in self._translatable_widgets:
            self._translatable_widgets.append(widget)
            self._translatable_texts[widget] = original_text

    def unregister_widget(self, widget):
        """Unregister a widget"""
        if widget in self._translatable_widgets:
            self._translatable_widgets.remove(widget)
            if widget in self._translatable_texts:
                del self._translatable_texts[widget]

    def set_translatable_text(self, widget, text: str):
        """Set a translated text on a widget"""
        self.register_widget(widget, text)
        self._set_widget_text(widget, text)

    def _set_widget_text(self, widget, text: str):
        """Set widget text with translation"""
        try:
            # Translate text
            translated_text = self.translate(text)

            # Apply according to widget type
            if hasattr(widget, "setText"):
                widget.setText(translated_text)
            elif hasattr(widget, "setTitle"):
                widget.setTitle(translated_text)
            elif hasattr(widget, "setWindowTitle"):
                widget.setWindowTitle(translated_text)
            elif hasattr(widget, "setPlaceholderText"):
                widget.setPlaceholderText(translated_text)
            elif hasattr(widget, "setToolTip"):
                widget.setToolTip(translated_text)
            else:
                get_printer().warning(
                    f"Widget type not supported for translation: {type(widget)}"
                )

        except Exception as e:
            get_printer().warning(f"Error translating widget: {e}")

    def _retranslate_all_widgets(self):
        """Retranslate all registered widgets"""
        for widget in self._translatable_widgets:
            if widget in self._translatable_texts:
                original_text = self._translatable_texts[widget]
                self._set_widget_text(widget, original_text)

    def _update_special_widgets(self):
        """Update special widgets (menus, etc.)"""
        try:
            # Update menus if necessary
            app = QCoreApplication.instance()
            if app:
                # Force interface update
                app.processEvents()
        except Exception as e:
            get_printer().warning(f"Error updating special widgets: {e}")

    def clear_registered_widgets(self):
        """Clear all registered widgets"""
        self._translatable_widgets.clear()
        self._translatable_texts.clear()

    def _save_auto_translation_to_ts(self, original: str, translated: str):
        """Save automatic translation to .ts file"""
        try:
            if self.current_language in SUPPORTED_LANGUAGES:
                language_info = SUPPORTED_LANGUAGES[self.current_language]
                ts_file = language_info["file"]
                ts_file_path = self.translations_dir / ts_file

                self.auto_translator.save_translation_to_ts(
                    original, translated, self.current_language, ts_file_path
                )

                # Update local cache
                self._ts_translations[original] = translated

        except Exception as e:
            get_printer().warning(f"Error saving automatic translation: {e}")

    def enable_auto_translation(self, enabled: bool = True):
        """Enable or disable automatic translation"""
        self.auto_translation_enabled = enabled
        if self.auto_translator:
            self.auto_translator.enabled = enabled
        get_printer().info(
            f"Automatic translation {'enabled' if enabled else 'disabled'}"
        )

    def get_auto_translation_stats(self):
        """Return automatic translation statistics"""
        if self.auto_translator:
            return self.auto_translator.get_cache_stats()
        return {}

    def clear_auto_translation_cache(self):
        """Clear automatic translation cache"""
        if self.auto_translator:
            self.auto_translator.clear_cache()


# Global translation manager instance
_translation_manager_instance = None


def get_translation_manager() -> TranslationManager:
    """Return global translation manager instance"""
    global _translation_manager_instance, translation_manager
    if _translation_manager_instance is None:
        _translation_manager_instance = TranslationManager()
        translation_manager = _translation_manager_instance
    return _translation_manager_instance


# Alias for compatibility (without automatic initialization)
translation_manager = None
