# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import json
import importlib.util
import sys
from pathlib import Path
from typing import Union, Dict, Optional

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QDesktopServices, QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

# IMPORT / GUI AND MODULES AND WIDGETS
# /////////////////////////////////////////////////////////////////////////////////////////////
from ...kernel.app_components import Fonts
from ...kernel.translation_helpers import set_tr

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class BottomBar(QFrame):
    """
    This class is used to create a bottom bar for the main window.
    It contains a credits label, a version label, and a size grip area.
    """

    # ///////////////////////////////////////////////////////////////

    def __init__(self, parent=None):
        super().__init__(parent)

        # ///////////////////////////////////////////////////////////////

        self.setObjectName("bottomBar")
        self.setMinimumSize(QSize(0, 22))
        self.setMaximumSize(QSize(16777215, 22))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        self.HL_bottomBar = QHBoxLayout(self)
        self.HL_bottomBar.setSpacing(0)
        self.HL_bottomBar.setObjectName("HL_bottomBar")
        self.HL_bottomBar.setContentsMargins(0, 0, 0, 0)

        self.creditsLabel = QLabel(self)
        self.creditsLabel.setObjectName("creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        self.creditsLabel.setFont(Fonts.SEGOE_UI_10_REG)
        self.creditsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.HL_bottomBar.addWidget(self.creditsLabel)

        self.version = QLabel(self)
        self.version.setObjectName("version")
        self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.HL_bottomBar.addWidget(self.version)

        self.appSizeGrip = QFrame(self)
        self.appSizeGrip.setObjectName("appSizeGrip")
        self.appSizeGrip.setMinimumSize(QSize(20, 0))
        self.appSizeGrip.setMaximumSize(QSize(20, 16777215))
        self.appSizeGrip.setFrameShape(QFrame.NoFrame)
        self.appSizeGrip.setFrameShadow(QFrame.Raised)
        self.HL_bottomBar.addWidget(self.appSizeGrip)

        # ///////////////////////////////////////////////////////////////
        # Initialiser avec la valeur par défaut
        self.set_credits("Made with ❤️ by EzQt_App")

        # Détecter automatiquement la version
        self.set_version_auto()

    # ///////////////////////////////////////////////////////////////

    def set_credits(self, credits: Union[str, Dict, str]) -> None:
        """
        Définit le texte des crédits avec support du système de traduction.

        Args:
            credits: Peut être :
                - str: Texte simple à traduire
                - dict: Dictionnaire avec 'name' et 'email' pour créer un lien cliquable
                - str (JSON): Chaîne JSON avec 'name' et 'email'
        """
        try:
            # Si c'est un dictionnaire ou JSON, créer un lien cliquable
            if isinstance(credits, dict):
                self._create_clickable_credits(credits)
            elif isinstance(credits, str) and credits.strip().startswith("{"):
                try:
                    credits_dict = json.loads(credits)
                    self._create_clickable_credits(credits_dict)
                except json.JSONDecodeError:
                    # Si ce n'est pas du JSON valide, traiter comme du texte simple
                    set_tr(self.creditsLabel, credits)
            else:
                # Texte simple avec traduction
                set_tr(self.creditsLabel, credits)

        except Exception as e:
            # En cas d'erreur, utiliser le texte par défaut
            set_tr(self.creditsLabel, "Made with ❤️ by EzQt_App")

    def _create_clickable_credits(self, credits_data: Dict) -> None:
        """
        Crée un lien cliquable pour les crédits avec nom et email.

        Args:
            credits_data: Dictionnaire avec 'name' et 'email'
        """
        try:
            name = credits_data.get("name", "Unknown")
            email = credits_data.get("email", "")

            # Créer le texte avec le nom en gras et cliquable
            credits_text = f"Made with ❤️ by {name}"

            # Définir le texte avec traduction
            set_tr(self.creditsLabel, credits_text)

            # Rendre le label cliquable si un email est fourni
            if email:
                self.creditsLabel.setCursor(Qt.PointingHandCursor)
                self.creditsLabel.mousePressEvent = lambda event: self._open_email(
                    email
                )
                self.creditsLabel.setStyleSheet(
                    "color: #0078d4; text-decoration: underline;"
                )
            else:
                self.creditsLabel.setCursor(Qt.ArrowCursor)
                self.creditsLabel.setStyleSheet("")

        except Exception as e:
            # En cas d'erreur, utiliser le texte par défaut
            set_tr(self.creditsLabel, "Made with ❤️ by EzQt_App")

    def _open_email(self, email: str) -> None:
        """
        Ouvre le client email par défaut avec l'adresse spécifiée.

        Args:
            email: Adresse email à ouvrir
        """
        try:
            QDesktopServices.openUrl(QUrl(f"mailto:{email}"))
        except Exception as e:
            # En cas d'erreur, ignorer
            pass

    def set_version_auto(self) -> None:
        """
        Détecte automatiquement la version du projet utilisateur.
        Cherche d'abord __version__ dans le module principal, sinon utilise la valeur par défaut.
        """
        detected_version = self._detect_project_version()
        if detected_version:
            self.set_version(detected_version)
        else:
            self.set_version("")

    def _detect_project_version(self) -> Optional[str]:
        """
        Détecte la version du projet utilisateur en cherchant __version__ dans main.py.

        Returns:
            str: Version détectée ou None si non trouvée
        """
        try:
            # Chercher main.py dans le répertoire courant
            main_py_path = Path.cwd() / "main.py"
            if not main_py_path.exists():
                return None

            # Lire le contenu de main.py
            with open(main_py_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Chercher __version__ = "..." dans le contenu
            import re

            version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                return f"v{version_match.group(1)}"

            # Si pas trouvé avec regex, essayer d'importer le module
            try:
                spec = importlib.util.spec_from_file_location("main", main_py_path)
                if spec and spec.loader:
                    main_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(main_module)

                    if hasattr(main_module, "__version__"):
                        return f"v{main_module.__version__}"
            except Exception:
                pass

            return None

        except Exception as e:
            # En cas d'erreur, retourner None
            return None

    def set_version(self, text: str) -> None:
        """
        Définit le texte de version avec support du système de traduction.

        Args:
            text: Texte de la version (peut être "v1.0.0" ou juste "1.0.0")
        """
        # S'assurer que la version commence par "v"
        if not text.startswith("v"):
            text = f"v{text}"

        set_tr(self.version, text)
