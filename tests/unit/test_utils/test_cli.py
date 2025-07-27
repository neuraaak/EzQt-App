# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour le module CLI.
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import sys

from ezqt_app.utils.cli import main


class TestCLI:
    """Tests pour le module CLI."""

    @patch("ezqt_app.utils.cli.Helper.Maker")
    @patch("ezqt_app.utils.cli.pkg_resources.resource_filename")
    @patch("pathlib.Path.cwd")
    @patch("pathlib.Path.exists")
    def test_main_success(
        self, mock_exists, mock_cwd, mock_resource_filename, mock_maker_class
    ):
        """Test de l'exécution réussie de la fonction main."""
        # Mock des dépendances
        mock_maker = MagicMock()
        mock_maker_class.return_value = mock_maker

        mock_resource_filename.return_value = str(Path("test_template.txt"))
        mock_cwd.return_value = Path("/test/path")

        # Mock de l'existence du template mais pas de main.py
        mock_exists.side_effect = [True, False]  # template existe, main.py n'existe pas

        main()

        # Vérifier que les méthodes du Maker ont été appelées
        mock_maker.make_assets_binaries.assert_called_once()
        mock_maker.make_qrc.assert_called_once()
        mock_maker.make_rc_py.assert_called_once()
        mock_maker.make_app_resources_module.assert_called_once()
        mock_maker.make_generic_main.assert_called_once()

    @patch("ezqt_app.utils.cli.Helper.Maker")
    @patch("ezqt_app.utils.cli.pkg_resources.resource_filename")
    @patch("builtins.input")
    def test_main_with_existing_main_py_overwrite(
        self, mock_input, mock_resource_filename, mock_maker_class
    ):
        """Test avec main.py existant et choix d'écrasement."""
        # Mock des dépendances
        mock_maker = MagicMock()
        mock_maker_class.return_value = mock_maker

        mock_resource_filename.return_value = str(Path("test_template.txt"))

        # Mock de l'input utilisateur (écraser)
        mock_input.return_value = "o"

        # Mock de l'existence du template et main.py
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.cwd") as mock_cwd:
                mock_cwd.return_value = Path("/test/path")
                with patch(
                    "pathlib.Path.exists", side_effect=[True, True]
                ):  # template existe, main.py existe
                    main()

        # Vérifier que make_generic_main a été appelé
        mock_maker.make_generic_main.assert_called_once()

    @patch("ezqt_app.utils.cli.Helper.Maker")
    @patch("ezqt_app.utils.cli.pkg_resources.resource_filename")
    def test_main_template_not_found(self, mock_resource_filename, mock_maker_class):
        """Test quand le template n'est pas trouvé."""
        # Mock des dépendances
        mock_maker = MagicMock()
        mock_maker_class.return_value = mock_maker

        mock_resource_filename.return_value = str(Path("test_template.txt"))

        # Mock de l'inexistence du template
        with patch("pathlib.Path.exists", return_value=False):
            main()

        # Vérifier que les méthodes du Maker ont été appelées
        mock_maker.make_assets_binaries.assert_called_once()
        mock_maker.make_qrc.assert_called_once()
        mock_maker.make_rc_py.assert_called_once()
        mock_maker.make_app_resources_module.assert_called_once()

        # Vérifier que make_generic_main n'a pas été appelé
        mock_maker.make_generic_main.assert_not_called()

    @patch("ezqt_app.utils.cli.Helper.Maker")
    @patch("ezqt_app.utils.cli.pkg_resources.resource_filename")
    @patch("builtins.input")
    def test_main_with_existing_main_py_no_overwrite(
        self, mock_input, mock_resource_filename, mock_maker_class
    ):
        """Test avec main.py existant et choix de ne pas écraser."""
        # Mock des dépendances
        mock_maker = MagicMock()
        mock_maker_class.return_value = mock_maker

        mock_resource_filename.return_value = str(Path("test_template.txt"))

        # Mock de l'input utilisateur (ne pas écraser)
        mock_input.return_value = "N"

        # Mock de l'existence du template et main.py
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.cwd") as mock_cwd:
                mock_cwd.return_value = Path("/test/path")
                with patch(
                    "pathlib.Path.exists", side_effect=[True, True]
                ):  # template existe, main.py existe
                    main()

        # Vérifier que make_generic_main n'a pas été appelé
        mock_maker.make_generic_main.assert_not_called()

    @patch("ezqt_app.utils.cli.Helper.Maker")
    @patch("ezqt_app.utils.cli.pkg_resources.resource_filename")
    @patch("pathlib.Path.cwd")
    @patch("pathlib.Path.exists")
    def test_main_without_main_py(
        self, mock_exists, mock_cwd, mock_resource_filename, mock_maker_class
    ):
        """Test sans main.py existant."""
        # Mock des dépendances
        mock_maker = MagicMock()
        mock_maker_class.return_value = mock_maker

        mock_resource_filename.return_value = str(Path("test_template.txt"))
        mock_cwd.return_value = Path("/test/path")

        # Mock de l'existence du template mais pas de main.py
        mock_exists.side_effect = [True, False]  # template existe, main.py n'existe pas

        main()

        # Vérifier que make_generic_main a été appelé
        mock_maker.make_generic_main.assert_called_once()

    @patch("ezqt_app.utils.cli.Helper.Maker")
    @patch("ezqt_app.utils.cli.pkg_resources.resource_filename")
    def test_maker_initialization(self, mock_resource_filename, mock_maker_class):
        """Test de l'initialisation du Maker."""
        # Mock du Maker
        mock_maker = MagicMock()
        mock_maker_class.return_value = mock_maker

        mock_resource_filename.return_value = str(Path("test_template.txt"))

        # Mock de l'existence du template
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.cwd") as mock_cwd:
                mock_cwd.return_value = Path("/test/path")
                with patch("pathlib.Path.exists", side_effect=[True, False]):
                    main()

        # Vérifier que le Maker a été initialisé avec le bon chemin
        mock_maker_class.assert_called_once_with(base_path=Path("/test/path"))
        # Vérifier que make_generic_main a été appelé
        mock_maker.make_generic_main.assert_called_once()
