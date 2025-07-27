# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import sys
import subprocess
import shutil
from pathlib import Path

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from colorama import Fore, Style

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////

# ////// TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1
from typing import Optional, List

# ////// VARIABLES
# ///////////////////////////////////////////////////////////////
APP_PATH: Path = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))

# ////// UTILITY FUNCTIONS
# ///////////////////////////////////////////////////////////////

# ////// CLASS
# ///////////////////////////////////////////////////////////////


class Helper:
    """
    Classe utilitaire pour la gestion des ressources et fichiers de l'application.

    Cette classe fournit des méthodes pour créer et gérer les fichiers
    de configuration, thèmes, traductions et ressources de l'application.
    """

    def __init__(self) -> None:
        """Initialise la classe Helper."""
        pass

    # ////// MAKER CLASS
    # ///////////////////////////////////////////////////////////////
    class Maker:
        """
        Classe pour la création et la gestion des fichiers de l'application.

        Cette classe gère la génération des binaires, fichiers de configuration,
        thèmes, traductions et ressources Qt.
        """

        def __init__(self, base_path: Optional[Path] = None) -> None:
            """
            Initialise le Maker avec un chemin de base.

            Parameters
            ----------
            base_path : Path, optional
                Chemin de base pour les opérations (défaut: APP_PATH).
            """
            self.base_path: Path = base_path or APP_PATH
            self._bin: Path = self.base_path / "bin"
            self._modules: Path = self.base_path / "modules"
            self._qrc_file: str = ""
            self._resources_module_file: str = ""

        def make_assets_binaries(self) -> None:
            """
            Crée les dossiers binaires nécessaires pour les assets.

            Cette méthode crée la structure de dossiers pour les polices,
            images, icônes, thèmes, configuration et traductions.
            """
            trace = False
            paths_to_make: List[Path] = [
                self._bin,
                self._bin / "fonts",
                self._bin / "images",
                self._bin / "icons",
                self._bin / "themes",
                self._bin / "config",
                self._bin / "translations",
                self._modules,
            ]
            for path in paths_to_make:
                if not path.exists():
                    path.mkdir(parents=True, exist_ok=True)
                    trace = True
            if trace:
                print(
                    Fore.LIGHTBLACK_EX
                    + f"~ [Helper] | Generated assets binaries."
                    + Style.RESET_ALL
                )

        def make_yaml(self, yaml_package: Path) -> Optional[Path]:
            """
            Copie le fichier YAML du package vers l'application.

            Parameters
            ----------
            yaml_package : Path
                Chemin vers le fichier YAML du package.

            Returns
            -------
            Optional[Path]
                Chemin vers le fichier YAML créé ou None.
            """
            yaml_application = self.base_path / r"bin\config\app.yaml"
            if not yaml_application.exists():
                shutil.copy(yaml_package, yaml_application)
                print(
                    Fore.LIGHTBLACK_EX
                    + "~ [Helper] | Generated required yaml file."
                    + Style.RESET_ALL
                )
            return yaml_application

        def make_qss(self, theme_package: Path) -> bool:
            """
            Copie le fichier de thème QSS du package vers l'application.

            Parameters
            ----------
            theme_package : Path
                Chemin vers le fichier de thème du package.

            Returns
            -------
            bool
                True si le fichier a été créé, False sinon.
            """
            theme_application = self.base_path / r"bin\themes\main_theme.qss"
            if not theme_application.exists():
                shutil.copy(theme_package, theme_application)
                print(
                    Fore.LIGHTBLACK_EX
                    + "~ [Helper] | Generated optional qss file."
                    + Style.RESET_ALL
                )
                return True
            return False

        def make_translations(self, translations_package: Path) -> bool:
            """
            Copie les fichiers de traduction du package vers le projet utilisateur.

            Parameters
            ----------
            translations_package : Path
                Chemin vers le dossier des traductions du package.

            Returns
            -------
            bool
                True si des fichiers ont été copiés, False sinon.
            """
            translations_application = self.base_path / r"bin\translations"
            if not translations_application.exists():
                translations_application.mkdir(parents=True, exist_ok=True)

            # ////// COPY TRANSLATION FILES
            # Copier tous les fichiers .qm et .ts du package
            copied_files: List[str] = []
            if translations_package.exists():
                # ////// COPY QM FILES
                # Copier les fichiers .qm
                for qm_file in translations_package.glob("*.qm"):
                    dest_file = translations_application / qm_file.name
                    if not dest_file.exists():
                        shutil.copy(qm_file, dest_file)
                        copied_files.append(qm_file.name)

                # ////// COPY TS FILES
                # Copier les fichiers .ts
                for ts_file in translations_package.glob("*.ts"):
                    dest_file = translations_application / ts_file.name
                    if not dest_file.exists():
                        shutil.copy(ts_file, dest_file)
                        copied_files.append(ts_file.name)

                if copied_files:
                    print(
                        Fore.LIGHTBLACK_EX
                        + f"~ [Helper] | Generated translation files: {', '.join(copied_files)}"
                        + Style.RESET_ALL
                    )
                    return True

            return False

        def make_qrc(self) -> bool:
            """
            Génère le fichier QRC à partir du contenu du dossier bin.

            Returns
            -------
            bool
                True si des ressources ont été ajoutées, False sinon.
            """

            def _add_qresource(directory: Path, prefix: str) -> int:
                """
                Ajoute les ressources d'un répertoire au fichier QRC.

                Parameters
                ----------
                directory : Path
                    Répertoire contenant les ressources.
                prefix : str
                    Préfixe pour les ressources.

                Returns
                -------
                int
                    Nombre de ressources ajoutées.
                """
                valid_extensions = {".png", ".jpg", ".jpeg", ".ico", ".svg"}
                entries = [
                    f
                    for f in directory.iterdir()
                    if f.suffix.lower() in valid_extensions
                ]
                if entries:
                    self._qrc_file += f'  <qresource prefix="{prefix}">\n'
                    for f in entries:
                        self._qrc_file += f"    <file>{prefix}/{f.name}</file>\n"
                    self._qrc_file += "  </qresource>\n"
                    return 1
                return 0

            count = 0
            self._qrc_file = "<RCC>\n"
            count += _add_qresource(self._bin / "images", "images")
            count += _add_qresource(self._bin / "icons", "icons")
            self._qrc_file += "</RCC>\n"

            with open(self._bin / "resources.qrc", mode="w") as f:
                f.write(self._qrc_file)
            print(
                Fore.LIGHTBLACK_EX
                + "~ [Helper] | Generated QRC file from bin folder content."
                + Style.RESET_ALL
            )
            return count != 0

        def make_rc_py(self) -> None:
            """
            Convertit le fichier QRC en fichier Python.

            Utilise pyside6-rcc pour convertir le fichier resources.qrc
            en resources_rc.py.
            """
            qrc_path = self._bin / "resources.qrc"
            pyrc_path = self._modules / "resources_rc.py"
            result = subprocess.run(
                ["pyside6-rcc", str(qrc_path), "-o", str(pyrc_path)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print(
                    Fore.LIGHTBLACK_EX
                    + "~ [Helper] | Converted QRC file to PY."
                    + Style.RESET_ALL
                )
            else:
                print(
                    Fore.LIGHTRED_EX + f"! [Helper] | {result.stderr}" + Style.RESET_ALL
                )

        def purge_rc_py(self) -> None:
            """Supprime le fichier resources_rc.py s'il existe."""
            rc_py = self._modules / "resources_rc.py"
            rc_py.unlink() if rc_py.exists() else None

        def make_app_resources_module(self) -> None:
            """
            Génère le module app_resources.py avec les ressources de l'application.

            Ce module contient les classes AppImages et AppIcons avec les chemins
            vers les ressources de l'application.
            """

            def _add_cls_attr(directory: Path, attr: str) -> int:
                """
                Ajoute les attributs de classe pour un répertoire.

                Parameters
                ----------
                directory : Path
                    Répertoire contenant les ressources.
                attr : str
                    Nom de l'attribut (images ou icons).

                Returns
                -------
                int
                    Nombre de ressources ajoutées.
                """
                valid_extensions = {".png", ".jpg", ".jpeg", ".ico", ".svg"}
                entries = [
                    f
                    for f in directory.iterdir()
                    if f.suffix.lower() in valid_extensions
                ]
                self._resources_module_file += (
                    f"class App{attr.capitalize()}({attr.capitalize()}):\n"
                )
                if entries:
                    for f in entries:
                        self._resources_module_file += f"    {f.stem.replace('-', '_')} = ':/{attr}/{attr}/{f.name}'\n"
                    self._resources_module_file += "\n\n"
                    return 1
                else:
                    self._resources_module_file += "    pass\n"
                    self._resources_module_file += "\n\n"
                    return 0

            count = 0
            self._resources_module_file = """
from ezqt_app.kernel.app_resources import Icons, Images
\n\n\n"""
            count += _add_cls_attr(self._bin / "images", "images")
            count += _add_cls_attr(self._bin / "icons", "icons")
            if count != 0:
                self._resources_module_file = (
                    "from .resources_rc import *\n" + self._resources_module_file
                )
            with open(self._modules / "app_resources.py", mode="w") as f:
                f.write(self._resources_module_file)
            print(
                Fore.LIGHTBLACK_EX
                + "~ [Helper] | Generated app_resources.py file. Ready for use."
                + Style.RESET_ALL
            )

        def make_generic_main(self, mainTxtTemplate: Path) -> None:
            """
            Génère un fichier main.py générique à partir d'un template.

            Parameters
            ----------
            mainTxtTemplate : Path
                Chemin vers le template main.txt.
            """
            main_txt = self.base_path / r"main.txt"
            main_py = self.base_path / r"main.py"
            if not main_py.exists():
                shutil.copy(mainTxtTemplate, main_txt)
                main_txt.rename(main_py)
            print(
                Fore.LIGHTBLACK_EX
                + "~ [Helper] | Generated example main.py file."
                + Style.RESET_ALL
            )
