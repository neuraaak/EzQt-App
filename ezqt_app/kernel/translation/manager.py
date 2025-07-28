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

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class TranslationManager(QObject):
    """Gestionnaire de traduction pour EzQt_App"""

    languageChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        self.current_language = DEFAULT_LANGUAGE

        # Système de retraduction automatique
        self._translatable_widgets = []  # Liste des widgets à retraduire
        self._translatable_texts = {}  # {widget: original_text}

        # Traductions .ts chargées directement
        self._ts_translations = {}

        # Déterminer le chemin des traductions
        if hasattr(sys, "_MEIPASS"):
            # Mode frozen (exécutable)
            self.translations_dir = (
                Path(sys._MEIPASS) / "ezqt_app" / "resources" / "translations"
            )
        else:
            # Mode développement - chercher dans l'ordre de priorité
            # Utiliser la même logique que makeRequiredFiles
            project_path = Path.cwd()  # Même logique que FileMaker(Path.cwd())
            possible_paths = [
                project_path
                / "bin"
                / "translations",  # Projet utilisateur (priorité 1)
                APP_PATH / "bin" / "translations",  # APP_PATH (priorité 2)
                Path(__file__).parent.parent.parent
                / "resources"
                / "translations",  # Développement local (priorité 3)
            ]

            # Essayer de récupérer depuis le package installé si pas trouvé
            try:
                package_translations = self._get_package_translations_dir()
                if package_translations.exists():
                    possible_paths.append(
                        package_translations
                    )  # Package installé (priorité 4)
            except Exception as e:
                # print(f"⚠️ Impossible de récupérer les traductions du package: {e}")
                pass

            # Chercher le premier dossier qui existe
            self.translations_dir = None
            for path in possible_paths:
                if path.exists():
                    self.translations_dir = path
                    break

            # Si aucun dossier trouvé, créer le dossier du projet utilisateur
            if self.translations_dir is None:
                self.translations_dir = project_path / "bin" / "translations"
                self.translations_dir.mkdir(parents=True, exist_ok=True)

        # Mapping des noms de langue vers les codes
        self.language_mapping = {
            "English": "en",
            "Français": "fr",
            "Español": "es",
            "Deutsch": "de",
        }

        # Charger la langue par défaut
        self.load_language_by_code(DEFAULT_LANGUAGE)

    def _get_package_translations_dir(self) -> Path:
        """Récupère le dossier des traductions du package installé"""
        try:
            import pkg_resources

            return Path(
                pkg_resources.resource_filename("ezqt_app", "resources/translations")
            )
        except Exception:
            return Path(__file__).parent.parent.parent / "resources" / "translations"

    def _load_ts_file(self, ts_file_path: Path) -> bool:
        """Charge un fichier .ts et extrait les traductions"""
        try:
            import xml.etree.ElementTree as ET

            if not ts_file_path.exists():
                return False

            tree = ET.parse(ts_file_path)
            root = tree.getroot()

            # Extraire les traductions du fichier .ts
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
            get_printer().warning(
                f"Erreur lors du chargement du fichier .ts {ts_file_path}: {e}"
            )
            return False

    def load_language(self, language_name: str) -> bool:
        """Charge une langue par son nom"""
        # Créer un mapping nom -> code
        name_to_code = {
            info["name"]: code for code, info in SUPPORTED_LANGUAGES.items()
        }

        if language_name in name_to_code:
            return self.load_language_by_code(name_to_code[language_name])
        return False

    def load_language_by_code(self, language_code: str) -> bool:
        """Charge une langue par son code"""
        if language_code not in SUPPORTED_LANGUAGES:
            get_printer().warning(f"Langue non supportée: {language_code}")
            return False

        # Vérifier que QApplication est instancié avant d'utiliser les traducteurs
        app = QCoreApplication.instance()
        if app is not None:
            # Retirer l'ancien traducteur seulement si QApplication existe
            try:
                QCoreApplication.removeTranslator(self.translator)
            except Exception as e:
                get_printer().warning(
                    f"Erreur lors de la suppression du traducteur: {e}"
                )

        self.translator = QTranslator()

        # Charger le nouveau fichier .ts
        language_info = SUPPORTED_LANGUAGES[language_code]
        ts_file = language_info["file"]
        ts_file_path = self.translations_dir / ts_file

        # Charger les traductions depuis le fichier .ts
        if self._load_ts_file(ts_file_path):
            get_printer().info(
                f"[TranslationManager] Traductions chargées pour {language_info['name']}"
            )
        else:
            get_printer().warning(
                f"Impossible de charger les traductions pour {language_info['name']}"
            )

        # Installer le traducteur seulement si QApplication existe
        if app is not None:
            try:
                QCoreApplication.installTranslator(self.translator)
            except Exception as e:
                get_printer().warning(
                    f"Erreur lors de l'installation du traducteur: {e}"
                )

        # Mettre à jour la langue actuelle
        self.current_language = language_code
        get_printer().info(
            f"[TranslationManager] Langue changée vers {language_info['name']}"
        )

        # Retraduire tous les widgets enregistrés
        self._retranslate_all_widgets()

        # Émettre le signal de changement de langue
        self.languageChanged.emit(language_code)

        return True

    def get_available_languages(self) -> list:
        """Retourne la liste des langues disponibles"""
        return list(SUPPORTED_LANGUAGES.keys())

    def get_current_language_name(self) -> str:
        """Retourne le nom de la langue actuelle"""
        if self.current_language in SUPPORTED_LANGUAGES:
            return SUPPORTED_LANGUAGES[self.current_language]["name"]
        return "Unknown"

    def get_current_language_code(self) -> str:
        """Retourne le code de la langue actuelle"""
        return self.current_language

    def translate(self, text: str) -> str:
        """Traduit un texte"""
        # D'abord essayer les traductions .ts chargées
        if text in self._ts_translations:
            return self._ts_translations[text]

        # Sinon utiliser le traducteur Qt
        translated = self.translator.translate("", text)
        return translated if translated else text

    def register_widget(self, widget, original_text: str):
        """Enregistre un widget pour retraduction automatique"""
        if widget not in self._translatable_widgets:
            self._translatable_widgets.append(widget)
            self._translatable_texts[widget] = original_text

    def unregister_widget(self, widget):
        """Désenregistre un widget"""
        if widget in self._translatable_widgets:
            self._translatable_widgets.remove(widget)
            if widget in self._translatable_texts:
                del self._translatable_texts[widget]

    def set_translatable_text(self, widget, text: str):
        """Définit un texte traduit sur un widget"""
        self.register_widget(widget, text)
        self._set_widget_text(widget, text)

    def _set_widget_text(self, widget, text: str):
        """Définit le texte d'un widget avec traduction"""
        try:
            # Traduire le texte
            translated_text = self.translate(text)

            # Appliquer selon le type de widget
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
                    f"Type de widget non supporté pour la traduction: {type(widget)}"
                )

        except Exception as e:
            get_printer().warning(f"Erreur lors de la traduction du widget: {e}")

    def _retranslate_all_widgets(self):
        """Retraduit tous les widgets enregistrés"""
        for widget in self._translatable_widgets:
            if widget in self._translatable_texts:
                original_text = self._translatable_texts[widget]
                self._set_widget_text(widget, original_text)

    def _update_special_widgets(self):
        """Met à jour les widgets spéciaux (menus, etc.)"""
        try:
            # Mettre à jour les menus si nécessaire
            app = QCoreApplication.instance()
            if app:
                # Forcer la mise à jour de l'interface
                app.processEvents()
        except Exception as e:
            get_printer().warning(
                f"Erreur lors de la mise à jour des widgets spéciaux: {e}"
            )

    def clear_registered_widgets(self):
        """Efface tous les widgets enregistrés"""
        self._translatable_widgets.clear()
        self._translatable_texts.clear()


# Instance globale du gestionnaire de traduction
_translation_manager_instance = None


def get_translation_manager() -> TranslationManager:
    """Retourne l'instance globale du gestionnaire de traduction"""
    global _translation_manager_instance
    if _translation_manager_instance is None:
        _translation_manager_instance = TranslationManager()
    return _translation_manager_instance


# Alias pour compatibilité
translation_manager = get_translation_manager()
