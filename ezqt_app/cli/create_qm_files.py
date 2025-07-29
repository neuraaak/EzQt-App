#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import xml.etree.ElementTree as ET
import struct
import hashlib
import pkg_resources

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..kernel.common import Path
from ..kernel.app_functions.printer import get_printer
from ezqt_app.kernel.translation.helpers import extract_translations_from_ts

# TYPE HINTS IMPROVEMENTS FOR PYSIDE6 6.9.1

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////

## ==> MAIN
# ///////////////////////////////////////////////////////////////


def create_proper_qm_from_ts(ts_file_path: Path, qm_file_path: Path) -> bool:
    """Creates a .qm file in the correct Qt format"""

    printer = get_printer()
    printer.info(f"Converting {ts_file_path.name} to {qm_file_path.name}...")

    try:
        # Extract translations from .ts file
        translations = extract_translations_from_ts(ts_file_path)

        # Create .qm file
        create_qt_qm_file(qm_file_path, translations)

        printer.success(f"{len(translations)} translations converted")
        return True

    except Exception as e:
        printer.error(f"Error during conversion: {e}")
        return False


def create_qt_qm_file(qm_file_path: Path, translations: dict):
    """Creates a .qm file in the appropriate Qt format"""

    # Qt .qm format based on documentation and examples
    with open(qm_file_path, "wb") as f:
        # Qt .qm header
        # Magic number: "qm" followed by 2 null bytes
        f.write(b"qm\x00\x00")

        # Version (4 bytes little-endian)
        f.write(struct.pack("<I", 0x01))

        # Number of translations (4 bytes little-endian)
        f.write(struct.pack("<I", len(translations)))

        # Write translations
        for source, translation in translations.items():
            # Encode in UTF-8
            source_bytes = source.encode("utf-8")
            translation_bytes = translation.encode("utf-8")

            # Source length (4 bytes little-endian)
            f.write(struct.pack("<I", len(source_bytes)))

            # Source
            f.write(source_bytes)

            # Translation length (4 bytes little-endian)
            f.write(struct.pack("<I", len(translation_bytes)))

            # Translation
            f.write(translation_bytes)

        # Checksum (optional, but often present)
        f.write(struct.pack("<I", 0))


def main():
    """Main function"""
    printer = get_printer()
    printer.section("Creating .qm files in the correct Qt format")

    # Priority 1: Look in user project (bin/translations)
    current_project_translations = Path.cwd() / "bin" / "translations"
    # Priority 2: Look in installed package
    try:
        package_translations = Path(
            pkg_resources.resource_filename("ezqt_app", "resources/translations")
        )
    except:
        package_translations = (
            Path(__file__).parent.parent / "resources" / "translations"
        )

    # Choose translations directory
    if current_project_translations.exists():
        translations_dir = current_project_translations
        printer.info(f"Using project directory: {translations_dir}")
    elif package_translations.exists():
        translations_dir = package_translations
        printer.info(f"Using package directory (fallback): {translations_dir}")
    else:
        printer.error("No translations directory found")
        printer.verbose_msg(f"   Project: {current_project_translations}")
        printer.verbose_msg(f"   Package: {package_translations}")
        printer.info("Make sure you are in an EzQt_App project or run 'ezqt init'")
        return

    # Look for .ts files
    ts_files = list(translations_dir.glob("*.ts"))

    if not ts_files:
        printer.error("No .ts files found")
        return

    printer.info(f".ts files found: {len(ts_files)}")

    # Convert each .ts file
    for ts_file in ts_files:
        qm_file = ts_file.with_suffix(".qm")
        if create_proper_qm_from_ts(ts_file, qm_file):
            printer.success(f"{qm_file.name} created")
        else:
            printer.error(f"Failed to create {qm_file.name}")

    printer.success("Process completed!")
    printer.info("Next steps:")
    printer.verbose_msg("   1. Test the new .qm files")
    printer.verbose_msg("   2. If it still doesn't work, use the .ts files")


if __name__ == "__main__":
    main()
