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

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////
APP_PATH = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class Helper:
    def __init__(self) -> None:
        pass

    # MAKER
    # ///////////////////////////////////////////////////////////////
    class Maker(object):
        def __init__(self, base_path=None):
            self.base_path = base_path or APP_PATH
            self._bin = self.base_path / "bin"
            self._modules = self.base_path / "modules"
            self._qrc_file = ""
            self._resources_module_file = ""

        # ///////////////////////////////////////////////////////////////

        def make_assets_binaries(self) -> None:
            trace = False
            paths_to_make = [
                self._bin,
                self._bin / "fonts",
                self._bin / "images",
                self._bin / "icons",
                self._bin / "themes",
                self._bin / "config",
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

        # ///////////////////////////////////////////////////////////////

        def make_yaml(self, yaml_package: Path) -> Path | None:
            yaml_application = self.base_path / r"bin\config\app.yaml"
            if not yaml_application.exists():
                shutil.copy(yaml_package, yaml_application)
                print(
                    Fore.LIGHTBLACK_EX
                    + "~ [Helper] | Generated required yaml file."
                    + Style.RESET_ALL
                )
            return yaml_application

        # ///////////////////////////////////////////////////////////////

        def make_qss(self, theme_package) -> bool:
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

        # ///////////////////////////////////////////////////////////////

        def make_qrc(self) -> bool:
            def _add_qresource(directory: Path, prefix: str) -> int:
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

        # ///////////////////////////////////////////////////////////////

        def make_rc_py(self) -> None:
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

        # ///////////////////////////////////////////////////////////////

        def purge_rc_py(self) -> None:
            rc_py = self._modules / "resources_rc.py"
            rc_py.unlink() if rc_py.exists() else None

        # ///////////////////////////////////////////////////////////////

        def make_app_resources_module(self) -> None:
            def _add_cls_attr(directory: Path, attr: str) -> int:
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

        # ///////////////////////////////////////////////////////////////

        def make_generic_main(self, mainTxtTemplate: Path) -> None:
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
