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

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .manager import get_translation_manager

# TYPE HINTS IMPROVEMENTS
from typing import Any, List, Tuple, Set, Dict

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////

# TRANSLATION FUNCTIONS
# ///////////////////////////////////////////////////////////////


def tr(text: str) -> str:
    """
    Simplified global translation function.

    Uses the translation manager to translate text.

    Parameters
    ----------
    text : str
        Text to translate

    Returns
    -------
    str
        Translated text or original text if no translation
    """
    return get_translation_manager().translate(text)


def set_tr(widget: Any, text: str) -> None:
    """
    Set translated text on a widget and register it for automatic retranslation.

    Parameters
    ----------
    widget : Any
        Qt widget (QLabel, QPushButton, etc.)
    text : str
        Original text to translate
    """
    get_translation_manager().set_translatable_text(widget, text)


def register_tr(widget: Any, text: str) -> None:
    """
    Register a widget for automatic retranslation without changing its text immediately.

    Parameters
    ----------
    widget : Any
        Qt widget
    text : str
        Original text to translate
    """
    get_translation_manager().register_widget(widget, text)


def unregister_tr(widget: Any) -> None:
    """
    Unregister a widget from automatic retranslation.

    Parameters
    ----------
    widget : Any
        Qt widget to unregister
    """
    get_translation_manager().unregister_widget(widget)


def change_language(language_name: str) -> bool:
    """
    Change application language.

    Parameters
    ----------
    language_name : str
        Language name ("English", "Français", etc.)

    Returns
    -------
    bool
        True if change succeeded, False otherwise
    """
    return get_translation_manager().load_language(language_name)


def get_available_languages() -> List[str]:
    """
    Return list of available languages.

    Returns
    -------
    List[str]
        List of available language names
    """
    return get_translation_manager().get_available_languages()


def get_current_language() -> str:
    """
    Return current application language.

    Returns
    -------
    str
        Current language name
    """
    return get_translation_manager().get_current_language_name()


def enable_auto_translation(enabled: bool = True) -> None:
    """
    Enable or disable automatic translation.

    Parameters
    ----------
    enabled : bool
        True to enable, False to disable
    """
    get_translation_manager().enable_auto_translation(enabled)


def get_auto_translation_stats() -> dict:
    """
    Return automatic translation statistics.

    Returns
    -------
    dict
        Automatic translation cache statistics
    """
    return get_translation_manager().get_auto_translation_stats()


def clear_auto_translation_cache() -> None:
    """
    Clear automatic translation cache.
    """
    get_translation_manager().clear_auto_translation_cache()


def translate_auto(text: str, source_lang: str = "en", target_lang: str = None) -> str:
    """
    Automatically translate text using external APIs.

    Parameters
    ----------
    text : str
        Text to translate
    source_lang : str
        Source language code (default: "en")
    target_lang : str
        Target language code (default: current language)

    Returns
    -------
    str
        Translated text or original text if failed
    """
    if target_lang is None:
        target_lang = get_translation_manager().get_current_language_code()

    auto_translator = get_translation_manager().auto_translator
    if auto_translator and auto_translator.enabled:
        translated = auto_translator.translate_sync(text, source_lang, target_lang)
        return translated if translated else text

    return text


def scan_widgets_for_translation(
    widget: Any, recursive: bool = True
) -> List[Tuple[Any, str]]:
    """
    Scan a widget and its children to find translatable text.

    Parameters
    ----------
    widget : Any
        Qt widget to scan
    recursive : bool
        If True, also scan child widgets

    Returns
    -------
    List[Tuple[Any, str]]
        List of found (widget, text) tuples
    """
    from PySide6.QtWidgets import QWidget

    found_widgets = []

    def scan_recursive(w):
        try:
            # Check if widget has text
            if hasattr(w, "text") and callable(getattr(w, "text", None)):
                try:
                    text = w.text().strip()
                    if (
                        text
                        and not text.isdigit()
                        and len(text) > 1
                        and not text.startswith("_")
                        and not text.startswith("menu_")
                        and not text.startswith("btn_")
                        and not text.startswith("setting")
                    ):
                        found_widgets.append((w, text))
                except:
                    pass

            # Check tooltips
            if hasattr(w, "toolTip") and callable(getattr(w, "toolTip", None)):
                try:
                    tooltip = w.toolTip().strip()
                    if (
                        tooltip
                        and not tooltip.isdigit()
                        and len(tooltip) > 1
                        and not tooltip.startswith("_")
                    ):
                        found_widgets.append((w, tooltip))
                except:
                    pass

            # Check placeholders
            if hasattr(w, "placeholderText") and callable(
                getattr(w, "placeholderText", None)
            ):
                try:
                    placeholder = w.placeholderText().strip()
                    if (
                        placeholder
                        and not placeholder.isdigit()
                        and len(placeholder) > 1
                        and not placeholder.startswith("_")
                    ):
                        found_widgets.append((w, placeholder))
                except:
                    pass

            # Scan children if requested
            if recursive:
                try:
                    for child in w.findChildren(QWidget):
                        scan_recursive(child)
                except:
                    pass

        except Exception as e:
            get_printer().warning(f"Error scanning widget {type(w)}: {e}")

    scan_recursive(widget)
    return found_widgets


def register_widgets_manually(widgets_list: List[Tuple[Any, str]]) -> int:
    """
    Manually register a list of widgets for translation.

    Parameters
    ----------
    widgets_list : List[Tuple[Any, str]]
        List of (widget, text) tuples to register

    Returns
    -------
    int
        Number of successfully registered widgets
    """
    registered_count = 0

    for widget, text in widgets_list:
        try:
            register_tr(widget, text)
            registered_count += 1
        except Exception as e:
            get_printer().warning(f"Error registering widget: {e}")

    return registered_count


def scan_and_register_widgets(widget: Any, recursive: bool = True) -> int:
    """
    Scan a widget and automatically register all found widgets.

    Parameters
    ----------
    widget : Any
        Qt widget to scan
    recursive : bool
        If True, also scan child widgets

    Returns
    -------
    int
        Number of registered widgets
    """
    found_widgets = scan_widgets_for_translation(widget, recursive)
    return register_widgets_manually(found_widgets)


def get_translation_stats() -> dict:
    """
    Return complete translation system statistics.

    Returns
    -------
    dict
        Detailed statistics
    """
    manager = get_translation_manager()

    stats = {
        "registered_widgets": len(manager._translatable_widgets),
        "cached_translations": len(manager._ts_translations),
        "current_language": manager.get_current_language_name(),
        "available_languages": manager.get_available_languages(),
        "auto_translation_enabled": manager.auto_translation_enabled,
        "auto_translation_stats": manager.get_auto_translation_stats(),
    }

    return stats


# STRING COLLECTOR FUNCTIONS
# ///////////////////////////////////////////////////////////////


def collect_strings_from_widget(widget: Any, recursive: bool = True) -> Set[str]:
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
    from .string_collector import get_string_collector

    collector = get_string_collector()
    return collector.collect_strings_from_widget(widget, recursive)


def collect_and_compare_strings(widget: Any, recursive: bool = True) -> Dict[str, Any]:
    """
    Collect strings and compare with registered ones.

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
    from .string_collector import get_string_collector

    collector = get_string_collector()
    return collector.collect_and_compare(widget, recursive)


def get_new_strings() -> Set[str]:
    """
    Return new strings (not registered).

    Returns
    -------
    Set[str]
        Set of new strings
    """
    from .string_collector import get_string_collector

    collector = get_string_collector()
    return collector.get_new_strings()


def mark_strings_as_processed(strings: Set[str] = None) -> None:
    """
    Mark strings as processed.

    Parameters
    ----------
    strings : Set[str], optional
        Strings to mark (default: all new strings)
    """
    from .string_collector import get_string_collector

    collector = get_string_collector()
    collector.mark_strings_as_processed(strings)


def mark_strings_as_registered(strings: Set[str] = None) -> None:
    """
    Alias for compatibility - Mark strings as processed.

    Parameters
    ----------
    strings : Set[str], optional
        Strings to mark (default: all new strings)
    """
    mark_strings_as_processed(strings)


def get_string_collector_stats() -> Dict[str, Any]:
    """
    Return string collector statistics.

    Returns
    -------
    Dict[str, Any]
        Detailed statistics
    """
    from .string_collector import get_string_collector

    collector = get_string_collector()
    return collector.get_stats()
