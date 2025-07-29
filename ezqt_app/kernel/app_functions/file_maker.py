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

"""
File Maker for EzQt_App
=======================

This module handles file and resource generation for EzQt_App projects,
including assets, configuration files, themes, and translations.

This module is part of the app_functions package as it handles
application-level file generation and resource management.
"""

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import subprocess
import shutil
from pathlib import Path

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import APP_PATH
from .printer import get_printer

# TYPE HINTS IMPROVEMENTS
from typing import Optional, List

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class FileMaker:
    """
    Handles file and resource generation for EzQt_App projects.

    This class manages the generation of:
    - Asset directories and files
    - Configuration files (YAML)
    - Theme files (QSS)
    - Translation files (.ts)
    - Resource files (.qrc, .py)
    - Project templates

    This class is part of the app_functions package as it handles
    application-level file generation and resource management.
    """

    def __init__(self, base_path: Optional[Path] = None, verbose: bool = False) -> None:
        """
        Initialize the FileMaker.

        Parameters
        ----------
        base_path : Path, optional
            Base path for operations (default: APP_PATH).
        verbose : bool, optional
            Enable verbose output mode, default False
        """
        self.base_path: Path = base_path or APP_PATH
        self._bin: Path = self.base_path / "bin"
        self._modules: Path = self.base_path / "modules"
        self._qrc_file: str = ""
        self._resources_module_file: str = ""
        self.printer = get_printer(verbose)

    def setup_project(self) -> bool:
        """
        Setup a complete EzQt_App project.

        Returns
        -------
        bool
            True if setup was successful.
        """
        try:
            self.make_assets_binaries()
            self.generate_all_assets()
            return True
        except Exception as e:
            self.printer.error(f"Error setting up project: {e}")
            return False

    def generate_all_assets(self) -> bool:
        """
        Generate all required assets.

        Returns
        -------
        bool
            True if generation was successful.
        """
        try:
            self.make_assets_binaries()
            self.make_yaml_from_package()
            self.make_qss_from_package()
            self.make_translations_from_package()
            self.make_qrc()
            self.make_rc_py()
            return True
        except Exception as e:
            self.printer.error(f"Error generating assets: {e}")
            return False

    def make_assets_binaries(self, verbose: bool = False) -> None:
        """
        Create necessary binary directories for assets.

        This method creates the directory structure for fonts,
        images, icons, themes, configuration, and translations.

        Parameters
        ----------
        verbose : bool, optional
            Whether to show detailed output (default: False).
        """
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

        created_paths = []
        for path in paths_to_make:
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                created_paths.append(path)

        if created_paths:
            self.printer.info(
                f"[FileMaker] Generated assets directories: {len(created_paths)} directories"
            )
            if verbose:
                self.printer.list_items([d.name for d in created_paths])

    def make_yaml_from_package(
        self, yaml_package: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Copy YAML file from package to application.

        Parameters
        ----------
        yaml_package : Path, optional
            Path to package YAML file.

        Returns
        -------
        Path, optional
            Path to copied YAML file.
        """
        if yaml_package is None:
            # Use pkg_resources to access installed package resources
            import pkg_resources

            yaml_package = Path(pkg_resources.resource_filename("ezqt_app", "app.yaml"))

        if not yaml_package.exists():
            self.printer.warning(f"YAML file not found at {yaml_package}")
            return None

        target_path = self._bin / "config" / "app.yaml"

        # Create destination directory if it doesn't exist
        target_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(yaml_package, target_path)

        self.printer.info("[FileMaker] Generated YAML config file.")
        return target_path

    def make_qss_from_package(self, theme_package: Optional[Path] = None) -> bool:
        """
        Copy QSS theme files from package to application.

        Parameters
        ----------
        theme_package : Path, optional
            Path to package theme directory or specific theme file.

        Returns
        -------
        bool
            True if successful.
        """

        if theme_package is None:
            # Use pkg_resources to access installed package resources
            import pkg_resources

            theme_package = Path(
                pkg_resources.resource_filename("ezqt_app", "resources/themes")
            )

        if not theme_package.exists():
            self.printer.warning(f"Theme directory not found at {theme_package}")
            return False

        target_path = self._bin / "themes"

        try:
            # Create destination directory if it doesn't exist
            target_path.mkdir(parents=True, exist_ok=True)

            # Determine if theme_package is a file or directory
            if theme_package.is_file():
                # Case 1: theme_package is a specific file

                # Ignore qtstrap.qss as it's not necessary
                if theme_package.name == "qtstrap.qss":
                    self.printer.verbose_msg(
                        f"Skipping unnecessary theme file: {theme_package.name}"
                    )
                    return False

                try:
                    target_file = target_path / theme_package.name

                    # Copy file even if it already exists (as in old code)
                    shutil.copy2(theme_package, target_file)
                    self.printer.verbose_msg(f"Copied theme file: {theme_package.name}")

                    self.printer.info("[FileMaker] Generated QSS theme files.")
                    return True

                except Exception as e:
                    self.printer.warning(
                        f"Failed to copy theme file {theme_package.name}: {e}"
                    )
                    return False

            else:
                # Case 2: theme_package is a directory

                # Copy files individually to avoid Windows path issues
                copied_files = []
                for theme_file in theme_package.glob("*.qss"):
                    # Ignore qtstrap.qss as it's not necessary
                    if theme_file.name == "qtstrap.qss":
                        self.printer.verbose_msg(
                            f"Skipping unnecessary theme file: {theme_file.name}"
                        )
                        continue

                    try:
                        target_file = target_path / theme_file.name

                        # Copy file even if it already exists (as in old code)
                        shutil.copy2(theme_file, target_file)
                        copied_files.append(theme_file.name)
                        self.printer.verbose_msg(
                            f"Copied theme file: {theme_file.name}"
                        )

                    except Exception as e:
                        self.printer.warning(
                            f"Failed to copy theme file {theme_file.name}: {e}"
                        )
                        continue

                # Check if at least one file was copied
                if copied_files:
                    self.printer.info("[FileMaker] Generated QSS theme files.")
                    return True
                else:
                    # Check if QSS files already exist in the destination directory
                    existing_files = list(target_path.glob("*.qss"))

                    if existing_files:
                        self.printer.info("[FileMaker] QSS theme files already exist.")
                        return True
                    else:
                        self.printer.warning(
                            "[FileMaker] No QSS theme files were copied successfully."
                        )
                        return False

        except Exception as e:
            self.printer.error(f"Error copying theme files: {e}")
            return False

    def make_translations_from_package(
        self, translations_package: Optional[Path] = None
    ) -> bool:
        """
        Copy translation files from package to application.

        Parameters
        ----------
        translations_package : Path, optional
            Path to package translations directory.

        Returns
        -------
        bool
            True if successful.
        """
        if translations_package is None:
            # Use pkg_resources to access installed package resources
            import pkg_resources

            translations_package = Path(
                pkg_resources.resource_filename("ezqt_app", "resources/translations")
            )

        if not translations_package.exists():
            self.printer.warning(
                f"Translations directory not found at {translations_package}"
            )
            return False

        target_path = self._bin / "translations"

        try:
            # Create destination directory if it doesn't exist
            target_path.mkdir(parents=True, exist_ok=True)

            # Copy files individually to avoid Windows path issues
            for translation_file in translations_package.glob("*.ts"):
                try:
                    target_file = target_path / translation_file.name
                    shutil.copy2(translation_file, target_file)
                    self.printer.verbose_msg(
                        f"Copied translation file: {translation_file.name}"
                    )
                except Exception as e:
                    self.printer.warning(
                        f"Failed to copy translation file {translation_file.name}: {e}"
                    )
                    continue

            # Check if at least one file was copied
            if any(target_path.glob("*.ts")):
                self.printer.info("[FileMaker] Generated translation files.")
                return True
            else:
                self.printer.warning(
                    "[FileMaker] No translation files were copied successfully."
                )
                return False

        except Exception as e:
            self.printer.error(f"Error copying translation files: {e}")
            return False

    def make_qrc(self) -> bool:
        """
        Generate QRC file from bin directory content.

        Returns
        -------
        bool
            True if successful.
        """
        qrc_content = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            "<RCC>",
            '    <qresource prefix="/">',
        ]

        def _add_qresource(directory: Path, prefix: str) -> int:
            """Add resources from directory to QRC content."""
            count = 0
            if directory.exists():
                for file_path in directory.rglob("*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(self._bin)
                        qrc_content.append(
                            f"        <file>{prefix}/{relative_path}</file>"
                        )
                        count += 1
            return count

        # Add different resource types
        _add_qresource(self._bin / "fonts", "fonts")
        _add_qresource(self._bin / "images", "images")
        _add_qresource(self._bin / "icons", "icons")
        _add_qresource(self._bin / "themes", "themes")
        _add_qresource(self._bin / "config", "config")
        _add_qresource(self._bin / "translations", "translations")

        qrc_content.append("    </qresource>")
        qrc_content.append("</RCC>")

        # Write QRC file
        qrc_file_path = self._bin / "resources.qrc"
        with open(qrc_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(qrc_content))

        self._qrc_file = str(qrc_file_path)
        self.printer.info("[FileMaker] Generated QRC file from bin folder content.")
        return True

    def make_rc_py(self) -> None:
        """
        Generate Python resource file from QRC.
        """
        if not self._qrc_file:
            self.printer.warning("[FileMaker] No QRC file")
            return

        try:
            # Use pyside6-rcc to compile QRC to Python
            cmd = [
                "pyside6-rcc",
                self._qrc_file,
                "-o",
                "resources_rc.py",
            ]
            subprocess.run(cmd, cwd=self._bin, check=True, capture_output=True)

            self.printer.qrc_compilation_result(True)
        except subprocess.CalledProcessError as e:
            self.printer.qrc_compilation_result(False, str(e))
        except FileNotFoundError:
            self.printer.qrc_compilation_result(False, "pyside6-rcc not found")

    def purge_rc_py(self) -> None:
        """Remove generated resource files."""
        rc_py_path = self._bin / "resources_rc.py"
        if rc_py_path.exists():
            rc_py_path.unlink()
            self.printer.info("[FileMaker] Purged resources_rc.py file.")

    def make_app_resources_module(self) -> None:
        """
        Generates the app_resources.py module with application resources.

        This module contains the AppImages and AppIcons classes with paths
        to application resources.
        """

        def _get_resources_from_directory(directory: Path, resource_type: str) -> list:
            """
            Retrieves resources from a directory.

            Parameters
            ----------
            directory : Path
                Directory containing resources.
            resource_type : str
                Resource type (images or icons).

            Returns
            -------
            list
                List of found resource files.
            """
            if not directory.exists():
                return []

            valid_extensions = {".png", ".jpg", ".jpeg", ".ico", ".svg"}
            entries = [
                f
                for f in directory.iterdir()
                if f.is_file() and f.suffix.lower() in valid_extensions
            ]
            return sorted(entries, key=lambda x: x.name.lower())

        def _generate_class_content(resources: list, resource_type: str) -> str:
            """
            Generates the content of a resource class.

            Parameters
            ----------
            resources : list
                List of resource files.
            resource_type : str
                Resource type (images or icons).

            Returns
            -------
            str
                Class content.
            """
            class_name = f"App{resource_type.capitalize()}"
            parent_class = resource_type.capitalize()

            content = f"class {class_name}({parent_class}):\n"

            if resources:
                # Add a descriptive docstring
                content += f'    """{resource_type.capitalize()} resources for the application."""\n\n'

                # Add attributes
                for resource in resources:
                    attr_name = resource.stem.replace("-", "_").replace(" ", "_")
                    resource_path = f":/{resource_type}/{resource_type}/{resource.name}"
                    content += f"    {attr_name} = '{resource_path}'\n"
            else:
                # Empty class with explanatory docstring
                content += (
                    f'    """No {resource_type} resources found in the project."""\n'
                )
                content += "    pass\n"

            return content

        # Get resources
        images = _get_resources_from_directory(self._bin / "images", "images")
        icons = _get_resources_from_directory(self._bin / "icons", "icons")

        # Generate file content
        content_parts = []

        # Imports
        content_parts.append("# -*- coding: utf-8 -*-")
        content_parts.append('"""')
        content_parts.append("Application Resources Module")
        content_parts.append("==========================")
        content_parts.append("")
        content_parts.append(
            "This module contains application-specific resource classes"
        )
        content_parts.append("that inherit from the base EzQt_App resource classes.")
        content_parts.append("")
        content_parts.append("Generated automatically by EzQt_App FileMaker.")
        content_parts.append('"""')
        content_parts.append("")
        content_parts.append("from ezqt_app.kernel.app_resources import Icons, Images")
        content_parts.append("")

        # Import Qt resources if necessary
        if images or icons:
            content_parts.append("from .resources_rc import *")
            content_parts.append("")

        # Resource classes
        content_parts.append(_generate_class_content(images, "images"))
        content_parts.append("")
        content_parts.append(_generate_class_content(icons, "icons"))
        content_parts.append("")

        # Join content
        self._resources_module_file = "\n".join(content_parts)

        # Write file
        with open(self._modules / "app_resources.py", mode="w", encoding="utf-8") as f:
            f.write(self._resources_module_file)

        # Status message
        total_resources = len(images) + len(icons)
        if total_resources > 0:
            self.printer.info(
                f"[FileMaker] Generated app_resources.py with {len(images)} images and {len(icons)} icons."
            )
        else:
            self.printer.info(
                "[FileMaker] Generated app_resources.py (no resources found)."
            )

    def make_main_from_template(self, main_template: Optional[Path] = None) -> None:
        """
        Generate main.py from template.

        Parameters
        ----------
        main_template : Path, optional
            Path to main template file.
        """
        if main_template is None:
            main_template = APP_PATH / "resources" / "templates" / "main.py.template"

        if not main_template.exists():
            self.printer.warning(f"Main template not found at {main_template}")
            return

        target_path = self.base_path / "main.py"
        shutil.copy2(main_template, target_path)

        self.printer.info("[FileMaker] Generated main.py file.")

    def get_bin_path(self) -> Path:
        """Get the bin directory path."""
        return self._bin

    def get_modules_path(self) -> Path:
        """Get the modules directory path."""
        return self._modules

    def get_qrc_file(self) -> str:
        """Get the QRC file path."""
        return self._qrc_file

    def get_resources_module_file(self) -> str:
        """Get the resources module file path."""
        return self._resources_module_file
