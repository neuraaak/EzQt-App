# -*- coding: utf-8 -*-
"""
Gestionnaire de traduction pour EzQt_App
"""

from PySide6.QtCore import QTranslator, QCoreApplication, QLocale, Signal, QObject
from pathlib import Path
import os
import sys
from colorama import Fore, Style

# Import APP_PATH depuis app_functions
from .app_functions import APP_PATH


class TranslationManager(QObject):
    """Gestionnaire de traduction pour EzQt_App"""

    languageChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.translator = QTranslator()
        self.current_language = "en"

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
            project_path = Path.cwd()  # Même logique que Helper.Maker(Path.cwd())
            possible_paths = [
                project_path
                / "bin"
                / "translations",  # Projet utilisateur (priorité 1)
                APP_PATH / "bin" / "translations",  # APP_PATH (priorité 2)
                Path(__file__).parent.parent
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

        # Mapping inverse pour l'affichage
        self.language_names = {
            "en": "English",
            "fr": "Français",
            "es": "Español",
            "de": "Deutsch",
        }

        print(
            Fore.LIGHTBLUE_EX
            + f"+ [AppKernel] | Translation system initialized."
            + Style.RESET_ALL
        )

    def _get_package_translations_dir(self) -> Path:
        """Récupère le dossier des traductions depuis le package installé"""
        try:
            import pkg_resources

            # Utiliser la même méthode que Kernel.getPackageResource
            package_translations = Path(
                pkg_resources.resource_filename("ezqt_app", "resources/translations")
            )
            return package_translations
        except Exception as e:
            return Path(__file__).parent.parent / "resources" / "translations"

    def _load_ts_file(self, ts_file_path: Path) -> bool:
        """Charge un fichier .ts directement en parsant le XML"""
        try:
            import xml.etree.ElementTree as ET

            # Parser le fichier XML
            tree = ET.parse(ts_file_path)
            root = tree.getroot()

            # Extraire les traductions
            translations = {}
            for message in root.findall(".//message"):
                source = message.find("source")
                translation = message.find("translation")

                if source is not None and translation is not None:
                    source_text = source.text.strip() if source.text else ""
                    translation_text = (
                        translation.text.strip() if translation.text else ""
                    )

                    if source_text and translation_text:
                        translations[source_text] = translation_text

            # Stocker les traductions dans le gestionnaire
            self._ts_translations = translations
            print(
                Fore.LIGHTBLUE_EX
                + f"+ [AppKernel] | Translations loaded from {ts_file_path.name} : {len(translations)} entries."
                + Style.RESET_ALL
            )
            return True

        except Exception as e:
            return False

    def load_language(self, language_name: str) -> bool:
        """Charge une langue par son nom"""
        language_code = self.language_mapping.get(language_name, "en")
        return self.load_language_by_code(language_code)

    def load_language_by_code(self, language_code: str) -> bool:
        """Charge une langue par son code"""
        # Vérifier si la langue est déjà chargée
        if self.current_language == language_code:
            return True

        # Retirer l'ancien traducteur
        QCoreApplication.removeTranslator(self.translator)

        # Créer un nouveau traducteur
        self.translator = QTranslator()

        # Essayer plusieurs formats de fichiers (priorité aux .ts)
        possible_files = [
            self.translations_dir / f"ezqt_app_{language_code}.ts",  # Priorité 1: .ts
            self.translations_dir
            / f"{language_code}.ts",  # Priorité 2: .ts sans préfixe
            self.translations_dir
            / f"ezqt_app_{language_code}.qm",  # Priorité 3: .qm (si .ts pas trouvé)
            self.translations_dir
            / f"{language_code}.qm",  # Priorité 4: .qm sans préfixe
        ]

        translation_file = None
        for file_path in possible_files:
            if file_path.exists():
                translation_file = file_path
                break

        if translation_file:
            # Pour les fichiers .ts, on peut les parser directement
            if translation_file.suffix == ".ts":
                success = self._load_ts_file(translation_file)
                if success:
                    self.current_language = language_code
                    print(
                        Fore.LIGHTBLUE_EX
                        + f"+ [AppKernel] | Language loaded : {self.language_names.get(language_code, language_code)}."
                        + Style.RESET_ALL
                    )

                    # Retraduire tous les widgets enregistrés
                    self._retranslate_all_widgets()

                    # Émettre le signal de changement de langue
                    self.languageChanged.emit(language_code)
                    return True
                return False

            if self.translator.load(str(translation_file)):
                QCoreApplication.installTranslator(self.translator)
                self.current_language = language_code
                print(
                    Fore.LIGHTBLUE_EX
                    + f"+ [AppKernel] | Language loaded : {self.language_names.get(language_code, language_code)}."
                    + Style.RESET_ALL
                )

                # Retraduire tous les widgets enregistrés
                self._retranslate_all_widgets()

                # Émettre le signal de changement de langue
                self.languageChanged.emit(language_code)
                return True
            else:
                pass
        else:
            pass

        return False

    def get_available_languages(self) -> list:
        """Retourne la liste des langues disponibles"""
        languages = []

        # Vérifier que le dossier existe
        if not self.translations_dir or not self.translations_dir.exists():
            # Retourner au moins l'anglais par défaut
            return ["English"]

        # Chercher les fichiers .ts et .qm (priorité aux .ts)
        try:
            # Fichiers .ts (priorité 1)
            for ts_file in self.translations_dir.glob("ezqt_app_*.ts"):
                code = ts_file.stem.split("_")[-1]
                if code in self.language_names:
                    languages.append(self.language_names[code])

            # Fichiers .qm (si pas déjà trouvé en .ts)
            for qm_file in self.translations_dir.glob("ezqt_app_*.qm"):
                code = qm_file.stem.split("_")[-1]
                if (
                    code in self.language_names
                    and self.language_names[code] not in languages
                ):
                    languages.append(self.language_names[code])
        except Exception as e:
            pass

        # Ajouter l'anglais par défaut s'il n'est pas déjà présent
        if "English" not in languages:
            languages.append("English")

        return languages

    def get_current_language_name(self) -> str:
        """Retourne le nom de la langue actuelle"""
        return self.language_names.get(self.current_language, "English")

    def get_current_language_code(self) -> str:
        """Retourne le code de la langue actuelle"""
        return self.current_language

    def translate(self, text: str) -> str:
        """Traduit un texte directement"""
        # D'abord essayer avec les traductions .ts si disponibles
        if hasattr(self, "_ts_translations") and self._ts_translations:
            if text in self._ts_translations:
                return self._ts_translations[text]

        # Ensuite essayer avec QTranslator
        if hasattr(self.translator, "translate"):
            translated = self.translator.translate("EzQt_App", text)
            if translated:
                return translated
        return text

    def register_widget(self, widget, original_text: str):
        """Enregistre un widget pour retraduction automatique"""
        if widget not in self._translatable_widgets:
            self._translatable_widgets.append(widget)
        self._translatable_texts[widget] = original_text

    def unregister_widget(self, widget):
        """Désenregistre un widget de la retraduction automatique"""
        if widget in self._translatable_widgets:
            self._translatable_widgets.remove(widget)
        if widget in self._translatable_texts:
            del self._translatable_texts[widget]

    def set_translatable_text(self, widget, text: str):
        """Définit un texte traduit et l'enregistre pour retraduction automatique"""
        self.register_widget(widget, text)
        translated = self.translate(text)
        self._set_widget_text(widget, translated)

    def _set_widget_text(self, widget, text: str):
        """Définit le texte d'un widget selon son type"""
        if hasattr(widget, "setText"):
            widget.setText(text)
        elif hasattr(widget, "setTitle"):
            widget.setTitle(text)
        elif hasattr(widget, "setPlaceholderText"):
            widget.setPlaceholderText(text)
        elif hasattr(widget, "setToolTip"):
            widget.setToolTip(text)
        elif hasattr(widget, "setWindowTitle"):
            widget.setWindowTitle(text)
        else:
            pass

    def _retranslate_all_widgets(self):
        """Retraduit tous les widgets enregistrés"""
        for widget, original_text in self._translatable_texts.items():
            try:
                translated = self.translate(original_text)
                self._set_widget_text(widget, translated)
            except Exception as e:
                pass
        
        # Mettre à jour les widgets spéciaux qui nécessitent une logique particulière
        self._update_special_widgets()
    
    def _update_special_widgets(self):
        """Met à jour les widgets spéciaux qui nécessitent une logique particulière"""
        try:
            # Trouver tous les SettingsPanel dans l'application
            from PySide6.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                # Parcourir tous les widgets de l'application
                for widget in app.allWidgets():
                    # Vérifier si c'est un SettingsPanel
                    if hasattr(widget, 'update_theme_selector_items'):
                        try:
                            widget.update_theme_selector_items()
                        except Exception as e:
                            pass
        except Exception as e:
            pass

    def clear_registered_widgets(self):
        """Efface tous les widgets enregistrés"""
        self._translatable_widgets.clear()
        self._translatable_texts.clear()


# Instance globale (créée de manière lazy pour éviter les problèmes de contexte Qt)
_translation_manager_instance = None


def get_translation_manager():
    """Retourne l'instance globale du gestionnaire de traduction"""
    global _translation_manager_instance
    if _translation_manager_instance is None:
        _translation_manager_instance = TranslationManager()
    return _translation_manager_instance


# Alias pour compatibilité
translation_manager = get_translation_manager()
