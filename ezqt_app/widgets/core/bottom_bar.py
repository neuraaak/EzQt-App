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
from pathlib import Path
import importlib.util
import re

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from PySide6.QtCore import (
    QSize,
    Qt,
    QUrl,
)
from PySide6.QtGui import (
    QDesktopServices,
)
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
)

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ...kernel.app_components import Fonts
from ...kernel.translation_helpers import set_tr

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Union, Dict, Optional

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class BottomBar(QFrame):
    """
    Barre de bas de page pour la fenêtre principale.

    Cette classe fournit une barre de bas de page avec des crédits,
    une version et une zone de redimensionnement. Les crédits peuvent
    être cliquables et ouvrir un client email.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialise la barre de bas de page.

        Parameters
        ----------
        parent : Any, optional
            Le widget parent (défaut: None).
        """
        super().__init__(parent)

        # ////// SETUP WIDGET PROPERTIES
        self.setObjectName("bottomBar")
        self.setMinimumSize(QSize(0, 22))
        self.setMaximumSize(QSize(16777215, 22))
        self.setFrameShape(QFrame.NoFrame)
        self.setFrameShadow(QFrame.Raised)

        # ////// SETUP MAIN LAYOUT
        self.HL_bottomBar = QHBoxLayout(self)
        self.HL_bottomBar.setSpacing(0)
        self.HL_bottomBar.setObjectName("HL_bottomBar")
        self.HL_bottomBar.setContentsMargins(0, 0, 0, 0)

        # ////// SETUP CREDITS LABEL
        self.creditsLabel = QLabel(self)
        self.creditsLabel.setObjectName("creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        self.creditsLabel.setFont(Fonts.SEGOE_UI_10_REG)
        self.creditsLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.HL_bottomBar.addWidget(self.creditsLabel)

        # ////// SETUP VERSION LABEL
        self.version = QLabel(self)
        self.version.setObjectName("version")
        self.version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.HL_bottomBar.addWidget(self.version)

        # ////// SETUP SIZE GRIP
        self.appSizeGrip = QFrame(self)
        self.appSizeGrip.setObjectName("appSizeGrip")
        self.appSizeGrip.setMinimumSize(QSize(20, 0))
        self.appSizeGrip.setMaximumSize(QSize(20, 16777215))
        self.appSizeGrip.setFrameShape(QFrame.NoFrame)
        self.appSizeGrip.setFrameShadow(QFrame.Raised)
        self.HL_bottomBar.addWidget(self.appSizeGrip)

        # ////// INITIALIZE DEFAULT VALUES
        self.set_credits("Made with ❤️ by EzQt_App")
        self.set_version_auto()

    # ////// UTILITY FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    def set_credits(self, credits: Union[str, Dict[str, str]]) -> None:
        """
        Définit les crédits avec support pour texte simple ou dictionnaire.

        Parameters
        ----------
        credits : str or Dict[str, str]
            Crédits sous forme de texte simple ou dictionnaire avec 'name' et 'email'.
        """
        try:
            if isinstance(credits, dict):
                # Crédits avec nom et email
                self._create_clickable_credits(credits)
            else:
                # Texte simple avec traduction
                set_tr(self.creditsLabel, credits)

        except Exception as e:
            # En cas d'erreur, utiliser le texte par défaut
            set_tr(self.creditsLabel, "Made with ❤️ by EzQt_App")

    def _create_clickable_credits(self, credits_data: Dict[str, str]) -> None:
        """
        Crée un lien cliquable pour les crédits avec nom et email.

        Parameters
        ----------
        credits_data : Dict[str, str]
            Dictionnaire avec 'name' et 'email'.
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

        Parameters
        ----------
        email : str
            Adresse email à ouvrir.
        """
        try:
            QDesktopServices.openUrl(QUrl(f"mailto:{email}"))
        except Exception as e:
            # En cas d'erreur, ignorer
            pass

    def set_version_auto(self) -> None:
        """
        Détecte automatiquement la version du projet utilisateur.

        Cherche d'abord __version__ dans le module principal,
        sinon utilise la valeur par défaut.
        """
        detected_version = self._detect_project_version()
        if detected_version:
            self.set_version(detected_version)
        else:
            self.set_version("")

    def _detect_project_version(self) -> Optional[str]:
        """
        Détecte la version du projet utilisateur en cherchant __version__ dans main.py.

        Returns
        -------
        str or None
            Version détectée ou None si non trouvée.
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

        Parameters
        ----------
        text : str
            Texte de la version (peut être "v1.0.0" ou juste "1.0.0").
        """
        # S'assurer que la version commence par "v"
        if not text.startswith("v"):
            text = f"v{text}"

        set_tr(self.version, text)
