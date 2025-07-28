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
    """Crée un fichier .qm dans le bon format Qt"""

    printer = get_printer()
    printer.info(f"Conversion de {ts_file_path.name} vers {qm_file_path.name}...")

    try:
        # Extraire les traductions du fichier .ts
        translations = extract_translations_from_ts(ts_file_path)

        # Créer le fichier .qm
        create_qt_qm_file(qm_file_path, translations)

        printer.success(f"{len(translations)} traductions converties")
        return True

    except Exception as e:
        printer.error(f"Erreur lors de la conversion: {e}")
        return False


def create_qt_qm_file(qm_file_path: Path, translations: dict):
    """Crée un fichier .qm dans le format Qt approprié"""

    # Format Qt .qm basé sur la documentation et les exemples
    with open(qm_file_path, "wb") as f:
        # En-tête Qt .qm
        # Magic number: "qm" suivi de 2 octets nuls
        f.write(b"qm\x00\x00")

        # Version (4 octets little-endian)
        f.write(struct.pack("<I", 0x01))

        # Nombre de traductions (4 octets little-endian)
        f.write(struct.pack("<I", len(translations)))

        # Écrire les traductions
        for source, translation in translations.items():
            # Encoder en UTF-8
            source_bytes = source.encode("utf-8")
            translation_bytes = translation.encode("utf-8")

            # Longueur de la source (4 octets little-endian)
            f.write(struct.pack("<I", len(source_bytes)))

            # Source
            f.write(source_bytes)

            # Longueur de la traduction (4 octets little-endian)
            f.write(struct.pack("<I", len(translation_bytes)))

            # Traduction
            f.write(translation_bytes)

        # Checksum (optionnel, mais souvent présent)
        f.write(struct.pack("<I", 0))


def main():
    """Fonction principale"""
    printer = get_printer()
    printer.section("Création de fichiers .qm dans le bon format Qt")

    # Priorité 1: Chercher dans le projet utilisateur (bin/translations)
    current_project_translations = Path.cwd() / "bin" / "translations"
    # Priorité 2: Chercher dans le package installé
    try:
        package_translations = Path(
            pkg_resources.resource_filename("ezqt_app", "resources/translations")
        )
    except:
        package_translations = (
            Path(__file__).parent.parent / "resources" / "translations"
        )

    # Choisir le dossier de traductions
    if current_project_translations.exists():
        translations_dir = current_project_translations
        printer.info(f"Utilisation du dossier projet: {translations_dir}")
    elif package_translations.exists():
        translations_dir = package_translations
        printer.info(f"Utilisation du dossier package (fallback): {translations_dir}")
    else:
        printer.error("Aucun dossier de traductions trouvé")
        printer.verbose_msg(f"   Projet: {current_project_translations}")
        printer.verbose_msg(f"   Package: {package_translations}")
        printer.info(
            "Assurez-vous d'être dans un projet EzQt_App ou lancez 'ezqt init'"
        )
        return

    # Chercher les fichiers .ts
    ts_files = list(translations_dir.glob("*.ts"))

    if not ts_files:
        printer.error("Aucun fichier .ts trouvé")
        return

    printer.info(f"Fichiers .ts trouvés: {len(ts_files)}")

    # Convertir chaque fichier .ts
    for ts_file in ts_files:
        qm_file = ts_file.with_suffix(".qm")
        if create_proper_qm_from_ts(ts_file, qm_file):
            printer.success(f"{qm_file.name} créé")
        else:
            printer.error(f"Échec de création de {qm_file.name}")

    printer.success("Processus terminé !")
    printer.info("Prochaines étapes:")
    printer.verbose_msg("   1. Testez les nouveaux fichiers .qm")
    printer.verbose_msg("   2. Si ça ne fonctionne toujours pas, utilisez les .ts")


if __name__ == "__main__":
    main()
