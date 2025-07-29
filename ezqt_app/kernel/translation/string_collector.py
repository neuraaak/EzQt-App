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
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..app_functions.printer import get_printer

# TYPE HINTS IMPROVEMENTS

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class StringCollector:
    """String collector with language detection and task generation"""

    def __init__(self, user_dir: Path = None):
        """
        Initialize string collector.

        Parameters
        ----------
        user_dir : Path, optional
            User directory to store files (default: ~/.ezqt/)
        """
        if user_dir is None:
            # Use default user directory
            user_dir = Path.home() / ".ezqt"

        self.user_dir = user_dir
        self.user_dir.mkdir(parents=True, exist_ok=True)

        # Create directory structure
        self.translations_dir = self.user_dir / "translations"
        self.cache_dir = self.user_dir / "cache"
        self.logs_dir = self.user_dir / "logs"

        self.translations_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)

        # Storage files
        self.pending_file = self.translations_dir / "pending_strings.txt"
        self.processed_file = self.translations_dir / "processed_strings.txt"
        self.language_detected_file = self.translations_dir / "language_detected.txt"
        self.translation_tasks_file = self.translations_dir / "translation_tasks.json"

        # Cache of collected strings
        self._collected_strings: Set[str] = set()
        self._new_strings: Set[str] = set()
        self._language_detected_strings: List[Tuple[str, str]] = (
            []
        )  # [(lang, text), ...]

    def collect_strings_from_widget(
        self, widget: Any, recursive: bool = True
    ) -> Set[str]:
        """
        Collect all strings from a widget.

        Parameters
        ----------
        widget : Any
            Qt widget to scan
        recursive : bool
            If True, also scan child widgets

        Returns
        -------
        Set[str]
            Set of found strings
        """
        collected = set()

        def collect_recursive(w):
            try:
                # Check if widget has text
                if hasattr(w, "text") and callable(getattr(w, "text", None)):
                    try:
                        text = w.text().strip()
                        if self._is_valid_string(text):
                            collected.add(text)
                    except:
                        pass

                # Check tooltips
                if hasattr(w, "toolTip") and callable(getattr(w, "toolTip", None)):
                    try:
                        tooltip = w.toolTip().strip()
                        if self._is_valid_string(tooltip):
                            collected.add(tooltip)
                    except:
                        pass

                # Check placeholders
                if hasattr(w, "placeholderText") and callable(
                    getattr(w, "placeholderText", None)
                ):
                    try:
                        placeholder = w.placeholderText().strip()
                        if self._is_valid_string(placeholder):
                            collected.add(placeholder)
                    except:
                        pass

                # Check window titles
                if hasattr(w, "windowTitle") and callable(
                    getattr(w, "windowTitle", None)
                ):
                    try:
                        title = w.windowTitle().strip()
                        if self._is_valid_string(title):
                            collected.add(title)
                    except:
                        pass

                # Scan children if requested
                if recursive:
                    try:
                        for child in w.findChildren(type(w)):
                            collect_recursive(child)
                    except:
                        pass

            except Exception as e:
                get_printer().warning(f"Error scanning widget {type(w)}: {e}")

        collect_recursive(widget)
        return collected

    def _is_valid_string(self, text: str) -> bool:
        """
        Check if a string is valid for collection.

        Parameters
        ----------
        text : str
            Text to validate

        Returns
        -------
        bool
            True if valid, False otherwise
        """
        if not text or len(text) < 2:
            return False

        # Filter technical strings
        if (
            text.startswith("_")
            or text.startswith("menu_")
            or text.startswith("btn_")
            or text.startswith("setting")
            or text.isdigit()
            or text in ["", " ", "\n", "\t"]
        ):
            return False

        # Filter strings with special technical characters
        technical_patterns = [
            r"^[A-Z_]+$",  # ALL_CAPS
            r"^[a-z_]+$",  # snake_case
            r"^[a-z]+[A-Z][a-z]+$",  # camelCase
            r"^[A-Z][a-z]+[A-Z][a-z]+$",  # PascalCase
        ]

        for pattern in technical_patterns:
            if re.match(pattern, text):
                return False

        return True

    def _detect_language(self, text: str) -> str:
        """
        Detect the language of a text.

        Parameters
        ----------
        text : str
            Text to analyze

        Returns
        -------
        str
            Language code (en, fr, de, es, etc.)
        """
        try:
            from langdetect import detect, DetectorFactory

            DetectorFactory.seed = 0  # For reproducible results
            return detect(text)
        except ImportError:
            # Simple fallback based on characters
            return self._simple_language_detection(text)
        except Exception as e:
            get_printer().warning(f"Language detection error: {e}")
            return "en"  # Default language

    def _simple_language_detection(self, text: str) -> str:
        """
        Simple language detection based on character analysis.

        Parameters
        ----------
        text : str
            Text to analyze

        Returns
        -------
        str
            Language code
        """
        # Language-specific characters
        french_chars = "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸ"
        german_chars = "äöüßÄÖÜ"
        spanish_chars = "ñáéíóúüÑÁÉÍÓÚÜ"

        # Check French characters
        if any(char in french_chars for char in text):
            return "fr"

        # Check German characters
        if any(char in german_chars for char in text):
            return "de"

        # Check Spanish characters
        if any(char in spanish_chars for char in text):
            return "es"

        # Default to English
        return "en"

    def save_pending_strings(self, strings: Set[str]) -> None:
        """
        Save pending strings to file.

        Parameters
        ----------
        strings : Set[str]
            Strings to save
        """
        try:
            # Sort strings for better readability
            sorted_strings = sorted(strings)

            with open(self.pending_file, "w", encoding="utf-8") as f:
                f.write(f"# Pending strings - {datetime.now().isoformat()}\n")
                f.write(f"# Total: {len(sorted_strings)} strings\n\n")

                for string in sorted_strings:
                    f.write(f"{string}\n")

            get_printer().info(f"✅ {len(strings)} pending strings saved")

        except Exception as e:
            get_printer().warning(f"Error saving strings: {e}")

    def detect_languages_and_save(self, strings: Set[str]) -> List[Tuple[str, str]]:
        """
        Detect languages for strings and save results.

        Parameters
        ----------
        strings : Set[str]
            Strings to analyze

        Returns
        -------
        List[Tuple[str, str]]
            List of (language, text) tuples
        """
        language_detected = []

        for text in strings:
            try:
                lang = self._detect_language(text)
                language_detected.append((lang, text))
            except Exception as e:
                get_printer().warning(f"Language detection error: {e}")
                language_detected.append(("en", text))  # Default to English

        # Save results
        try:
            sorted_results = sorted(language_detected, key=lambda x: x[0])

            with open(self.language_detected_file, "w", encoding="utf-8") as f:
                f.write(
                    f"# Strings with detected language - {datetime.now().isoformat()}\n"
                )
                f.write(f"# Format: language_code|text\n\n")

                for lang, text in sorted_results:
                    f.write(f"{lang}|{text}\n")

            self._language_detected_strings = language_detected

        except Exception as e:
            get_printer().warning(f"Error saving language detection results: {e}")

        return language_detected

    def load_processed_strings(self) -> Set[str]:
        """
        Load processed strings from file.

        Returns
        -------
        Set[str]
            Set of processed strings
        """
        processed = set()

        try:
            if self.processed_file.exists():
                with open(self.processed_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            processed.add(line)

                get_printer().info(f"✅ {len(processed)} processed strings loaded")
            else:
                get_printer().info("📝 No processed strings file found")

        except Exception as e:
            get_printer().warning(f"Error loading processed strings: {e}")

        return processed

    def get_supported_languages(self) -> List[str]:
        """
        Get list of supported languages.

        Returns
        -------
        List[str]
            List of supported language codes
        """
        return ["en", "fr", "de", "es", "it", "pt", "ru", "ja", "ko", "zh"]

    def generate_translation_tasks(
        self, language_detected: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate translation tasks from language detection results.

        Parameters
        ----------
        language_detected : List[Tuple[str, str]]
            List of (language, text) tuples

        Returns
        -------
        Dict[str, Any]
            Translation tasks dictionary
        """
        tasks = {}
        supported_languages = self.get_supported_languages()

        for source_lang, text in language_detected:
            if source_lang not in tasks:
                tasks[source_lang] = {}

            # Determine target languages (all except source)
            target_languages = [
                lang for lang in supported_languages if lang != source_lang
            ]

            for target_lang in target_languages:
                if target_lang not in tasks[source_lang]:
                    tasks[source_lang][target_lang] = []

                tasks[source_lang][target_lang].append(text)

        # Save tasks to file
        try:
            with open(self.translation_tasks_file, "w", encoding="utf-8") as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)

            get_printer().info(f"✅ {len(tasks)} translation tasks generated")

        except Exception as e:
            get_printer().warning(f"Error saving tasks: {e}")

        return tasks

    def get_new_strings(self) -> Set[str]:
        """
        Get new strings (not yet processed).

        Returns
        -------
        Set[str]
            Set of new strings
        """
        return self._new_strings.copy()

    def collect_and_compare(
        self, widget: Any, recursive: bool = True
    ) -> Dict[str, Any]:
        """
        Collect strings and compare with processed ones.

        Parameters
        ----------
        widget : Any
            Widget to scan
        recursive : bool
            If True, also scan child widgets

        Returns
        -------
        Dict[str, Any]
            Collection statistics
        """
        # Collect all strings
        collected = self.collect_strings_from_widget(widget, recursive)

        # Save collected strings
        self.save_pending_strings(collected)

        # Detect languages
        language_detected = self.detect_languages_and_save(collected)

        # Generate translation tasks
        tasks = self.generate_translation_tasks(language_detected)

        # Load processed strings
        processed = self.load_processed_strings()

        # Calculate new strings
        new_strings = collected - processed
        self._new_strings = new_strings

        # Display summary
        stats = {
            "total_collected": len(collected),
            "total_processed": len(processed),
            "new_strings": len(new_strings),
            "languages_detected": len(set(lang for lang, _ in language_detected)),
            "translation_tasks": len(tasks),
        }

        get_printer().info("📊 Collection summary:")
        get_printer().info(f"  - Collected strings: {stats['total_collected']}")
        get_printer().info(f"  - Processed strings: {stats['total_processed']}")
        get_printer().info(f"  - New strings: {stats['new_strings']}")
        get_printer().info(f"  - Detected languages: {stats['languages_detected']}")
        get_printer().info(f"  - Translation tasks: {stats['translation_tasks']}")

        return stats

    def mark_strings_as_processed(self, strings: Set[str] = None) -> None:
        """
        Mark strings as processed.

        Parameters
        ----------
        strings : Set[str], optional
            Strings to mark (default: all new strings)
        """
        if strings is None:
            strings = self._new_strings

        if not strings:
            get_printer().warning("No strings to mark as processed")
            return

        try:
            # Load already processed strings
            processed = self.load_processed_strings()

            # Add new strings
            processed.update(strings)

            # Save updated list
            sorted_strings = sorted(processed)

            with open(self.processed_file, "w", encoding="utf-8") as f:
                f.write(f"# Processed strings - {datetime.now().isoformat()}\n")
                f.write(f"# Total: {len(sorted_strings)} strings\n\n")

                for string in sorted_strings:
                    f.write(f"{string}\n")

            get_printer().info(f"✅ {len(strings)} strings marked as processed")

        except Exception as e:
            get_printer().warning(f"Error marking strings: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get collector statistics.

        Returns
        -------
        Dict[str, Any]
            Statistics dictionary
        """
        stats = {
            "collected_strings": len(self._collected_strings),
            "new_strings": len(self._new_strings),
            "language_detected": len(self._language_detected_strings),
            "pending_file": str(self.pending_file),
            "processed_file": str(self.processed_file),
            "language_detected_file": str(self.language_detected_file),
            "translation_tasks_file": str(self.translation_tasks_file),
        }

        return stats

    def clear_cache(self) -> None:
        """Clear collector cache."""
        self._collected_strings.clear()
        self._new_strings.clear()
        self._language_detected_strings.clear()
        get_printer().info("Collector cache cleared")


# Global instance
_string_collector_instance = None


def get_string_collector(user_dir: Path = None) -> StringCollector:
    """
    Get global string collector instance.

    Parameters
    ----------
    user_dir : Path, optional
        User directory for the collector

    Returns
    -------
    StringCollector
        Global string collector instance
    """
    global _string_collector_instance
    if _string_collector_instance is None:
        _string_collector_instance = StringCollector(user_dir)
    return _string_collector_instance
