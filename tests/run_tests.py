# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Script de lancement des tests unitaires pour EzQt_App.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Exécuter une commande et afficher le résultat."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=False, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"⚠️  Avertissements/Erreurs: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Lanceur de tests pour EzQt_App")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "all"], 
        default="unit",
        help="Type de tests à exécuter"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Générer un rapport de couverture"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Mode verbeux"
    )
    parser.add_argument(
        "--fast", 
        action="store_true",
        help="Exclure les tests lents"
    )
    
    args = parser.parse_args()
    
    # ////// VÉRIFIER QUE NOUS SOMMES DANS LE BON RÉPERTOIRE
    if not Path("pyproject.toml").exists():
        print("❌ Erreur: pyproject.toml non trouvé. Exécutez ce script depuis la racine du projet.")
        sys.exit(1)
    
    # ////// CONSTRUIRE LA COMMANDE PYTEST
    cmd_parts = ["python", "-m", "pytest"]
    
    if args.verbose:
        cmd_parts.append("-v")
    
    if args.fast:
        cmd_parts.extend(["-m", "not slow"])
    
    if args.type == "unit":
        cmd_parts.append("tests/unit/")
    elif args.type == "integration":
        cmd_parts.append("tests/integration/")
    else:  # "all"
        cmd_parts.append("tests/")
    
    if args.coverage:
        cmd_parts.extend([
            "--cov=ezqt_app",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ])
    
    cmd = " ".join(cmd_parts)
    
    # ////// EXÉCUTER LES TESTS
    success = run_command(cmd, f"Exécution des tests {args.type}")
    
    if success:
        print("\n✅ Tests exécutés avec succès!")
        
        if args.coverage:
            print("\n📊 Rapport de couverture généré dans htmlcov/")
            print("   Ouvrez htmlcov/index.html dans votre navigateur")
    else:
        print("\n❌ Échec des tests")
        sys.exit(1)


if __name__ == "__main__":
    main() 