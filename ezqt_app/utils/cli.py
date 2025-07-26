# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
from pathlib import Path
import pkg_resources

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
from colorama import Fore, Style

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ezqt_app.helper import Helper

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


## ==> MAIN
# ///////////////////////////////////////////////////////////////


def main():
    print("Initialisation du projet EzQt_App...")

    # ///////////////////////////////////////////////////////////////
    maker = Helper.Maker(base_path=Path.cwd())
    maker.make_assets_binaries()
    maker.make_qrc()
    maker.make_rc_py()
    maker.make_app_resources_module()

    # ///////////////////////////////////////////////////////////////
    # Génération d'un main.py exemple
    template_path = Path(
        pkg_resources.resource_filename("ezqt_app", "resources/main_generic.txt")
    )
    if template_path.exists():
        main_py = Path.cwd() / "main.py"
        if main_py.exists():
            response = (
                input("main.py existe déjà. Voulez-vous l'écraser ? (o/N) : ")
                .strip()
                .lower()
            )
            if response == "o":
                maker.make_generic_main(template_path)
            else:
                print(
                    Fore.LIGHTYELLOW_EX
                    + "main.py conservé, génération du fichier exemple annulée."
                    + Style.RESET_ALL
                )
        else:
            maker.make_generic_main(template_path)
    else:
        print(
            Fore.LIGHTRED_EX
            + "Template main_generic.txt introuvable, main.py non généré."
            + Style.RESET_ALL
        )

    # ///////////////////////////////////////////////////////////////

    print("Initialisation terminée !")
