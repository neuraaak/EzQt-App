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
import sys

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
from ...kernel.translation import set_tr

# TYPE HINTS IMPROVEMENTS
from typing import Union, Dict, Optional

# UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# CLASS
# ///////////////////////////////////////////////////////////////


class BottomBar(QFrame):
    """
    Bottom bar for the main window.

    This class provides a bottom bar with credits,
    version and resize area. Credits can be clickable
    and open an email client.
    """

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the bottom bar.

        Parameters
        ----------
        parent : Any, optional
            The parent widget (default: None).
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
        Set credits with support for simple text or dictionary.

        Parameters
        ----------
        credits : str or Dict[str, str]
            Credits as simple text or dictionary with 'name' and 'email'.
        """
        try:
            if isinstance(credits, dict):
                # Credits with name and email
                self._create_clickable_credits(credits)
            else:
                # Simple text with translation
                set_tr(self.creditsLabel, credits)

        except Exception as e:
            # In case of error, use default text
            set_tr(self.creditsLabel, "Made with ❤️ by EzQt_App")

    def _create_clickable_credits(self, credits_data: Dict[str, str]) -> None:
        """
        Create a clickable link for credits with name and email.

        Parameters
        ----------
        credits_data : Dict[str, str]
            Dictionary with 'name' and 'email'.
        """
        try:
            name = credits_data.get("name", "Unknown")
            email = credits_data.get("email", "")

            # Create text with bold name and clickable
            credits_text = f"Made with ❤️ by {name}"

            # Set text with translation
            set_tr(self.creditsLabel, credits_text)

            # Make label clickable if email is provided
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
            # In case of error, use default text
            set_tr(self.creditsLabel, "Made with ❤️ by EzQt_App")

    def _open_email(self, email: str) -> None:
        """
        Open default email client with specified address.

        Parameters
        ----------
        email : str
            Email address to open.
        """
        try:
            QDesktopServices.openUrl(QUrl(f"mailto:{email}"))
        except Exception as e:
            # In case of error, ignore
            pass

    def set_version_auto(self) -> None:
        """
        Automatically detect user project version.

        First look for __version__ in main module,
        otherwise use default value.
        """
        detected_version = self._detect_project_version()
        if detected_version:
            self.set_version(detected_version)
        else:
            # Fallback to EzQt_App version if no version found
            try:
                import ezqt_app

                if hasattr(ezqt_app, "__version__"):
                    self.set_version(f"v{ezqt_app.__version__}")
                else:
                    self.set_version("")  # Default version
            except ImportError:
                self.set_version("")  # Default version

    def set_version_forced(self, version: str) -> None:
        """
        Force displayed version (ignore automatic detection).

        Parameters
        ----------
        version : str
            Version to display (ex: "v1.0.0" or "1.0.0").
        """
        self.set_version(version)

    def _detect_project_version(self) -> Optional[str]:
        """
        Detect user project version by looking for __version__ in main.py.

        Returns
        -------
        str or None
            Detected version or None if not found.
        """
        try:
            # Method 1: Look in current directory
            main_py_path = Path.cwd() / "main.py"
            if main_py_path.exists():
                version = self._extract_version_from_file(main_py_path)
                if version:
                    return version

            # Method 2: Look in main script directory
            script_dir = Path(sys.argv[0]).parent if sys.argv else Path.cwd()
            main_py_path = script_dir / "main.py"
            if main_py_path.exists():
                version = self._extract_version_from_file(main_py_path)
                if version:
                    return version

            # Method 3: Look in parent directory (case where exe is in subfolder)
            parent_dir = Path.cwd().parent
            main_py_path = parent_dir / "main.py"
            if main_py_path.exists():
                version = self._extract_version_from_file(main_py_path)
                if version:
                    return version

            # Method 4: Try to import main module
            try:
                import main

                if hasattr(main, "__version__"):
                    return f"v{main.__version__}"
            except ImportError:
                pass

            # Method 5: Fallback to EzQt_App version
            try:
                import ezqt_app

                if hasattr(ezqt_app, "__version__"):
                    return f"v{ezqt_app.__version__}"
            except ImportError:
                pass

            return None

        except Exception as e:
            # In case of error, return None
            return None

    def _extract_version_from_file(self, file_path: Path) -> Optional[str]:
        """
        Extract version from a Python file.

        Parameters
        ----------
        file_path : Path
            Path to Python file.

        Returns
        -------
        str or None
            Extracted version or None if not found.
        """
        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Look for __version__ = "..." in content
            version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
            if version_match:
                return f"v{version_match.group(1)}"

            # If not found with regex, try to import module
            try:
                spec = importlib.util.spec_from_file_location("main", file_path)
                if spec and spec.loader:
                    main_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(main_module)

                    if hasattr(main_module, "__version__"):
                        return f"v{main_module.__version__}"
            except Exception:
                pass

            return None

        except Exception:
            return None

    def set_version(self, text: str) -> None:
        """
        Set version text with translation system support.

        Parameters
        ----------
        text : str
            Version text (can be "v1.0.0" or just "1.0.0").
        """
        # Ensure version starts with "v"
        if not text.startswith("v"):
            text = f"v{text}"

        set_tr(self.version, text)
