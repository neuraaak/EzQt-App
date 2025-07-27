# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from typing import Any, List

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from .translation_manager import get_translation_manager

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Any, List

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////

# TRANSLATION FUNCTIONS
# ///////////////////////////////////////////////////////////////


def tr(text: str) -> str:
    """
    Fonction de traduction globale simplifiée.

    Utilise le gestionnaire de traduction pour traduire un texte.

    Parameters
    ----------
    text : str
        Texte à traduire

    Returns
    -------
    str
        Texte traduit ou texte original si pas de traduction
    """
    return get_translation_manager().translate(text)


def set_tr(widget: Any, text: str) -> None:
    """
    Définit un texte traduit sur un widget et l'enregistre pour retraduction automatique.

    Parameters
    ----------
    widget : Any
        Widget Qt (QLabel, QPushButton, etc.)
    text : str
        Texte original à traduire
    """
    get_translation_manager().set_translatable_text(widget, text)


def register_tr(widget: Any, text: str) -> None:
    """
    Enregistre un widget pour retraduction automatique sans changer son texte immédiatement.

    Parameters
    ----------
    widget : Any
        Widget Qt
    text : str
        Texte original à traduire
    """
    get_translation_manager().register_widget(widget, text)


def unregister_tr(widget: Any) -> None:
    """
    Désenregistre un widget de la retraduction automatique.

    Parameters
    ----------
    widget : Any
        Widget Qt à désenregistrer
    """
    get_translation_manager().unregister_widget(widget)


def change_language(language_name: str) -> bool:
    """
    Change la langue de l'application.

    Parameters
    ----------
    language_name : str
        Nom de la langue ("English", "Français", etc.)

    Returns
    -------
    bool
        True si le changement a réussi, False sinon
    """
    return get_translation_manager().load_language(language_name)


def get_available_languages() -> List[str]:
    """
    Retourne la liste des langues disponibles.

    Returns
    -------
    List[str]
        Liste des noms de langues disponibles
    """
    return get_translation_manager().get_available_languages()


def get_current_language() -> str:
    """
    Retourne la langue actuelle.

    Returns
    -------
    str
        Nom de la langue actuelle
    """
    return get_translation_manager().get_current_language_name()
