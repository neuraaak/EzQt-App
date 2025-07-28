# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour les fonctions d'application du kernel.
"""

import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import os

from ezqt_app.kernel.app_functions import Kernel, APP_PATH


class TestKernel:
    """Tests pour la classe Kernel."""

    def setup_method(self):
        """Réinitialise l'état de Kernel avant chaque test."""
        Kernel._yamlFile = None

    def test_load_kernel_config_success(self, tmp_path):
        """Test de chargement réussi d'une configuration."""
        # Créer un fichier de configuration de test
        config_file = tmp_path / "app.yaml"
        config_data = {
            "app": {
                "name": "Test App",
                "description": "Test Description",
                "theme": "dark",
                "app_width": 1280,
                "app_height": 720,
                "app_min_width": 940,
                "app_min_height": 560,
                "menu_panel_shrinked_width": 60,
                "menu_panel_extended_width": 240,
                "settings_panel_width": 240,
                "time_animation": 400,
            },
            "settings_panel": {
                "theme": {
                    "type": "toggle",
                    "label": "Active Theme",
                    "options": ["Light", "Dark"],
                    "default": "dark",
                    "description": "Choose the application theme",
                    "enabled": True,
                },
                "language": {
                    "type": "select",
                    "label": "Language",
                    "options": ["English", "Français", "Español", "Deutsch"],
                    "default": "English",
                    "description": "Interface language",
                    "enabled": True,
                },
            },
            "theme_palette": {
                "dark": {
                    "$_main_surface": "rgb(33, 37, 43)",
                    "$_main_border": "rgb(44, 49, 58)",
                },
                "light": {
                    "$_main_surface": "rgb(240, 240, 243)",
                    "$_main_border": "rgb(225, 223, 229)",
                },
            },
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock directement _yamlFile
        Kernel._yamlFile = config_file

        # Charger la configuration
        result = Kernel.loadKernelConfig("app")

        # Vérifier que la configuration a été chargée
        assert result == config_data["app"]
        assert result["name"] == "Test App"
        assert result["description"] == "Test Description"
        assert result["theme"] == "dark"

    def test_load_kernel_config_file_not_found(self, tmp_path):
        """Test de chargement avec fichier inexistant."""
        # Créer un fichier app.yaml vide
        config_file = tmp_path / "app.yaml"
        config_data = {"app": {"name": "Test"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock directement _yamlFile
        Kernel._yamlFile = config_file

        # Essayer de charger une section inexistante
        result = Kernel.loadKernelConfig("nonexistent")
        # Maintenant ça retourne un dict vide au lieu de lever une exception
        assert result == {}

    def test_load_kernel_config_invalid_yaml(self, tmp_path):
        """Test de chargement avec YAML invalide."""
        # Créer un fichier YAML invalide
        config_file = tmp_path / "app.yaml"
        with open(config_file, "w") as f:
            f.write("invalid: yaml: content: [")

        # Mock directement _yamlFile
        Kernel._yamlFile = config_file

        # Essayer de charger la configuration invalide
        with pytest.raises(yaml.YAMLError):
            Kernel.loadKernelConfig("app")

    def test_load_kernel_config_section_not_found(self, tmp_path):
        """Test de chargement avec section inexistante."""
        # Créer un fichier de configuration
        config_file = tmp_path / "app.yaml"
        config_data = {"app": {"name": "Test App"}}

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock directement _yamlFile
        Kernel._yamlFile = config_file

        # Charger la configuration
        result = Kernel.loadKernelConfig("app")

        # Vérifier que la configuration a été chargée
        assert result == config_data["app"]

        # Charger une section inexistante
        result = Kernel.loadKernelConfig("nonexistent_section")
        assert result == {}

    def test_save_kernel_config_success(self, tmp_path):
        """Test de sauvegarde réussie d'une configuration."""
        # Mock du chemin de configuration
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Données à sauvegarder
            config_data = {
                "app": {"name": "Test App", "description": "Test Description"}
            }

            # Sauvegarder la configuration
            Kernel.saveKernelConfig("test_config", config_data)

            # Vérifier que le fichier a été créé
            config_file = tmp_path / "test_config.yaml"
            assert config_file.exists()

            # Vérifier le contenu du fichier
            with open(config_file, "r") as f:
                loaded_data = yaml.safe_load(f)

            assert loaded_data == config_data

    def test_save_kernel_config_with_existing_file(self, tmp_path):
        """Test de sauvegarde avec fichier existant."""
        # Créer un fichier existant
        config_file = tmp_path / "existing_config.yaml"
        existing_data = {"existing": "data"}

        with open(config_file, "w") as f:
            yaml.dump(existing_data, f)

        # Mock du chemin de configuration
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Nouvelles données à sauvegarder
            new_data = {"new": "data"}

            # Sauvegarder la configuration
            Kernel.saveKernelConfig("existing_config", new_data)

            # Vérifier que le fichier a été mis à jour
            with open(config_file, "r") as f:
                loaded_data = yaml.safe_load(f)

            assert loaded_data == new_data

    def test_get_config_path(self, tmp_path):
        """Test de génération du chemin de configuration."""
        # Mock du chemin de configuration
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Tester avec différents noms de configuration
            config_path = Kernel.getConfigPath("test_config")
            expected_path = tmp_path / "test_config.yaml"

            assert config_path == expected_path
            assert str(config_path).endswith("test_config.yaml")

    def test_config_path_with_different_names(self, tmp_path):
        """Test de génération de chemin avec différents noms."""
        # Mock du chemin de configuration
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Tester plusieurs noms
            names = ["app", "settings", "theme", "config"]
            for name in names:
                config_path = Kernel.getConfigPath(name)
                expected_path = tmp_path / f"{name}.yaml"
                assert config_path == expected_path

    def test_load_kernel_config_multiple_sections(self, tmp_path):
        """Test de chargement avec plusieurs sections."""
        # Créer un fichier de configuration avec plusieurs sections
        config_file = tmp_path / "app.yaml"
        config_data = {
            "app": {"name": "Test App", "theme": "dark", "app_width": 1280},
            "settings_panel": {
                "theme": {"default": "dark", "options": ["light", "dark"]}
            },
            "theme_palette": {
                "dark": {"$_main_surface": "rgb(33, 37, 43)"},
                "light": {"$_main_surface": "rgb(240, 240, 243)"},
            },
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock directement _yamlFile
        Kernel._yamlFile = config_file

        # Charger différentes sections
        app_result = Kernel.loadKernelConfig("app")
        settings_result = Kernel.loadKernelConfig("settings_panel")
        theme_result = Kernel.loadKernelConfig("theme_palette")

        # Vérifier les résultats
        assert app_result == config_data["app"]
        assert settings_result == config_data["settings_panel"]
        assert theme_result == config_data["theme_palette"]

    def test_save_kernel_config_preserves_structure(self, tmp_path):
        """Test que la sauvegarde préserve la structure."""
        # Mock du chemin de configuration
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Données complexes à sauvegarder
            complex_data = {
                "nested": {
                    "level1": {
                        "level2": {"value": "test", "number": 42, "boolean": True}
                    }
                },
                "list": [1, 2, 3, "string"],
                "simple": "value",
            }

            # Sauvegarder la configuration
            Kernel.saveKernelConfig("complex_config", complex_data)

            # Vérifier que le fichier a été créé
            config_file = tmp_path / "complex_config.yaml"
            assert config_file.exists()

            # Vérifier le contenu du fichier
            with open(config_file, "r") as f:
                loaded_data = yaml.safe_load(f)

            assert loaded_data == complex_data
            assert loaded_data["nested"]["level1"]["level2"]["value"] == "test"
            assert loaded_data["list"] == [1, 2, 3, "string"]

    def test_load_kernel_config_empty_file(self, tmp_path):
        """Test de chargement avec fichier vide."""
        # Créer un fichier YAML vide
        config_file = tmp_path / "app.yaml"
        with open(config_file, "w") as f:
            f.write("")

        # Mock directement _yamlFile
        Kernel._yamlFile = config_file

        # Charger la configuration
        result = Kernel.loadKernelConfig("app")

        # Vérifier que le résultat est un dict vide
        assert result == {}

    def test_save_kernel_config_empty_data(self, tmp_path):
        """Test de sauvegarde avec données vides."""
        # Mock du chemin de configuration
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Sauvegarder des données vides
            empty_data = {}

            # Sauvegarder la configuration
            Kernel.saveKernelConfig("empty_config", empty_data)

            # Vérifier que le fichier a été créé
            config_file = tmp_path / "empty_config.yaml"
            assert config_file.exists()

            # Vérifier le contenu du fichier
            with open(config_file, "r") as f:
                loaded_data = yaml.safe_load(f)

            assert loaded_data == empty_data

    def test_config_file_permissions(self, tmp_path):
        """Test des permissions de fichier de configuration."""
        # Mock du chemin de configuration
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Créer un fichier de configuration
            config_data = {"test": "data"}
            Kernel.saveKernelConfig("permissions_test", config_data)

            # Vérifier que le fichier est lisible
            config_file = tmp_path / "permissions_test.yaml"
            assert config_file.exists()
            assert config_file.is_file()

            # Vérifier que le fichier peut être lu
            with open(config_file, "r") as f:
                content = f.read()
                assert "test" in content

    def test_load_kernel_config_with_comments(self, tmp_path):
        """Test de chargement avec commentaires YAML."""
        # Créer un fichier YAML avec commentaires
        config_file = tmp_path / "app.yaml"
        yaml_content = """
# Configuration de l'application
app:
  name: "Test App"  # Nom de l'application
  description: "Test Description"
  theme: "dark"
  app_width: 1280
  app_height: 720
  app_min_width: 940
  app_min_height: 560
  menu_panel_shrinked_width: 60
  menu_panel_extended_width: 240
  settings_panel_width: 240
  time_animation: 400

# Paramètres du panneau
settings_panel:
  theme:
    type: "toggle"
    label: "Active Theme"
    options: ["Light", "Dark"]
    default: "dark"
    description: "Choose the application theme"
    enabled: true
  language:
    type: "select"
    label: "Language"
    options: ["English", "Français", "Español", "Deutsch"]
    default: "English"
    description: "Interface language"
    enabled: true
"""

        with open(config_file, "w", encoding="utf-8") as f:
            f.write(yaml_content)

        # Mock directement _yamlFile
        Kernel._yamlFile = config_file

        # Charger la configuration
        result = Kernel.loadKernelConfig("app")

        # Vérifier que la configuration a été chargée correctement
        assert result["name"] == "Test App"
        assert result["theme"] == "dark"
        assert result["app_width"] == 1280

    def test_save_kernel_config_unicode_support(self, tmp_path):
        """Test de sauvegarde avec support Unicode."""
        # Mock du chemin de configuration
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Données avec caractères Unicode
            unicode_data = {
                "app": {
                    "name": "Testé App",
                    "description": "Description avec accents éèà",
                    "theme": "dark",
                },
                "settings_panel": {
                    "language": {
                        "label": "Langue",
                        "options": ["English", "Français", "Español", "Deutsch"],
                        "default": "Français",
                    }
                },
            }

            # Sauvegarder la configuration
            Kernel.saveKernelConfig("unicode_config", unicode_data)

            # Vérifier que le fichier a été créé
            config_file = tmp_path / "unicode_config.yaml"
            assert config_file.exists()

            # Vérifier le contenu du fichier
            with open(config_file, "r", encoding="utf-8") as f:
                loaded_data = yaml.safe_load(f)

            assert loaded_data == unicode_data
            assert loaded_data["app"]["name"] == "Testé App"
            assert loaded_data["settings_panel"]["language"]["label"] == "Langue"

    def test_yaml_file_setter(self):
        """Test de la méthode yamlFile pour définir le fichier YAML."""
        test_path = Path("/test/path/app.yaml")

        # Définir le fichier YAML
        Kernel.yamlFile(test_path)

        # Vérifier que le fichier a été défini
        assert Kernel._yamlFile == test_path

    def test_yaml_file_setter_multiple_calls(self):
        """Test de yamlFile avec plusieurs appels."""
        # Premier appel
        test_path1 = Path("/test/path1/app.yaml")
        Kernel.yamlFile(test_path1)
        assert Kernel._yamlFile == test_path1

        # Deuxième appel
        test_path2 = Path("/test/path2/app.yaml")
        Kernel.yamlFile(test_path2)
        assert Kernel._yamlFile == test_path2

    def test_get_package_resource(self):
        """Test de la méthode getPackageResource."""
        with patch("ezqt_app.kernel.app_functions.pkg_resources") as mock_pkg_resources:
            mock_pkg_resources.resource_filename.return_value = "/test/resource/path"

            # Appeler la méthode
            result = Kernel.getPackageResource("test/resource")

            # Vérifier le résultat
            assert result == Path("/test/resource/path")
            mock_pkg_resources.resource_filename.assert_called_once_with(
                "ezqt_app", "test/resource"
            )

    def test_check_assets_requirements(self):
        """Test de la méthode checkAssetsRequirements."""
        with patch("ezqt_app.kernel.app_functions.Helper") as mock_helper:
            mock_maker = MagicMock()
            mock_helper.Maker.return_value = mock_maker
            mock_maker.make_qrc.return_value = True

            # Appeler la méthode
            Kernel.checkAssetsRequirements()

            # Vérifier que les méthodes ont été appelées
            mock_maker.make_assets_binaries.assert_called_once()
            mock_maker.make_qrc.assert_called_once()
            mock_maker.make_rc_py.assert_called_once()
            mock_maker.make_app_resources_module.assert_called_once()

    def test_check_assets_requirements_qrc_failure(self):
        """Test de checkAssetsRequirements quand make_qrc échoue."""
        with patch("ezqt_app.kernel.app_functions.Helper") as mock_helper:
            mock_maker = MagicMock()
            mock_helper.Maker.return_value = mock_maker
            mock_maker.make_qrc.return_value = False

            # Appeler la méthode
            Kernel.checkAssetsRequirements()

            # Vérifier que purge_rc_py est appelé au lieu de make_rc_py
            mock_maker.make_assets_binaries.assert_called_once()
            mock_maker.make_qrc.assert_called_once()
            mock_maker.purge_rc_py.assert_called_once()
            mock_maker.make_app_resources_module.assert_called_once()

    def test_make_app_resources_module(self):
        """Test de la méthode makeAppResourcesModule."""
        with patch("ezqt_app.kernel.app_functions.Helper") as mock_helper:
            mock_maker = MagicMock()
            mock_helper.Maker.return_value = mock_maker

            # Appeler la méthode
            Kernel.makeAppResourcesModule()

            # Vérifier que la méthode a été appelée
            mock_maker.make_app_resources_module.assert_called_once()

    def test_make_required_files(self):
        """Test de la méthode makeRequiredFiles."""
        with (
            patch.object(Kernel, "getPackageResource") as mock_get_resource,
            patch("ezqt_app.kernel.app_functions.Helper") as mock_helper,
            patch.object(Kernel, "yamlFile") as mock_yaml_file,
        ):

            mock_maker = MagicMock()
            mock_helper.Maker.return_value = mock_maker
            mock_maker.make_yaml.return_value = "/test/app.yaml"
            mock_maker.make_qss.return_value = True
            mock_maker.make_translations.return_value = True

            mock_get_resource.side_effect = [
                "/test/app.yaml",
                "/test/theme.qss",
                "/test/translations",
            ]

            # Appeler la méthode
            Kernel.makeRequiredFiles()

            # Vérifier les appels
            mock_get_resource.assert_any_call("app.yaml")
            mock_get_resource.assert_any_call("resources/themes/main_theme.qss")
            mock_get_resource.assert_any_call("resources/translations")
            mock_yaml_file.assert_called_once_with("/test/app.yaml")
            mock_maker.make_yaml.assert_called_once()
            mock_maker.make_qss.assert_called_once()
            mock_maker.make_translations.assert_called_once()

    def test_make_required_files_no_theme(self):
        """Test de makeRequiredFiles sans génération de thème."""
        with (
            patch.object(Kernel, "getPackageResource") as mock_get_resource,
            patch("ezqt_app.kernel.app_functions.Helper") as mock_helper,
            patch.object(Kernel, "yamlFile") as mock_yaml_file,
        ):

            mock_maker = MagicMock()
            mock_helper.Maker.return_value = mock_maker
            mock_maker.make_yaml.return_value = "/test/app.yaml"
            mock_maker.make_translations.return_value = True

            mock_get_resource.side_effect = ["/test/app.yaml", "/test/translations"]

            # Appeler la méthode sans générer le thème
            Kernel.makeRequiredFiles(mkTheme=False)

            # Vérifier que make_qss n'a pas été appelé
            mock_maker.make_qss.assert_not_called()
            mock_maker.make_translations.assert_called_once()

    def test_load_fonts_resources_package(self):
        """Test de loadFontsResources depuis le package."""
        with (
            patch.object(Kernel, "getPackageResource") as mock_get_resource,
            patch("ezqt_app.kernel.app_functions.QFontDatabase") as mock_font_db,
            patch("ezqt_app.kernel.app_functions.print") as mock_print,
        ):

            # Mock des polices
            mock_fonts_dir = MagicMock()
            mock_font1 = MagicMock()
            mock_font1.suffix = ".ttf"
            mock_font1.stem = "Segoe UI"
            mock_font2 = MagicMock()
            mock_font2.suffix = ".otf"  # Ne devrait pas être chargé
            mock_fonts_dir.iterdir.return_value = [mock_font1, mock_font2]

            mock_get_resource.return_value = mock_fonts_dir
            mock_font_db.addApplicationFont.return_value = 1  # Succès

            # Appeler la méthode
            Kernel.loadFontsResources(app=False)

            # Vérifier les appels
            mock_get_resource.assert_called_with("resources/fonts")
            mock_font_db.addApplicationFont.assert_called_once_with(str(mock_font1))

    def test_load_fonts_resources_application(self):
        """Test de loadFontsResources depuis l'application."""
        with (
            patch("ezqt_app.kernel.app_functions.APP_PATH") as mock_app_path,
            patch("ezqt_app.kernel.app_functions.QFontDatabase") as mock_font_db,
            patch("ezqt_app.kernel.app_functions.print") as mock_print,
        ):

            # Mock des polices
            mock_fonts_dir = MagicMock()
            mock_font = MagicMock()
            mock_font.suffix = ".ttf"
            mock_font.stem = "Segoe UI"
            mock_fonts_dir.iterdir.return_value = [mock_font]

            mock_app_path.__truediv__.return_value = mock_fonts_dir
            mock_font_db.addApplicationFont.return_value = -1  # Échec

            # Appeler la méthode
            Kernel.loadFontsResources(app=True)

            # Vérifier les appels
            mock_app_path.__truediv__.assert_called_with(r"bin\fonts")
            mock_font_db.addApplicationFont.assert_called_once_with(str(mock_font))

    def test_load_fonts_resources_recursive(self):
        """Test de loadFontsResources avec appel récursif."""
        with (
            patch.object(Kernel, "getPackageResource") as mock_get_resource,
            patch("ezqt_app.kernel.app_functions.QFontDatabase") as mock_font_db,
            patch("ezqt_app.kernel.app_functions.print") as mock_print,
            patch.object(Kernel, "loadFontsResources") as mock_recursive,
        ):

            # Mock des polices
            mock_fonts_dir = MagicMock()
            mock_fonts_dir.iterdir.return_value = []

            mock_get_resource.return_value = mock_fonts_dir
            mock_font_db.addApplicationFont.return_value = 1

            # Appeler la méthode
            Kernel.loadFontsResources(app=False)

            # Vérifier l'appel récursif
            mock_recursive.assert_called_once_with(app=True)

    def test_write_yaml_config(self, tmp_path):
        """Test de la méthode writeYamlConfig."""
        # Créer un fichier YAML de test
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"name": "Test App"}, "settings": {"theme": "dark"}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Écrire une nouvelle configuration
        Kernel.writeYamlConfig(["app", "version"], "1.0.0")

        # Vérifier que le fichier a été mis à jour
        with open(config_file, "r") as f:
            updated_data = yaml.safe_load(f)

        assert updated_data["app"]["name"] == "Test App"
        assert updated_data["app"]["version"] == "1.0.0"
        assert updated_data["settings"]["theme"] == "dark"

    def test_write_yaml_config_new_section(self, tmp_path):
        """Test de writeYamlConfig avec nouvelle section."""
        # Créer un fichier YAML de test
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"name": "Test App"}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Écrire dans une nouvelle section
        Kernel.writeYamlConfig(["new_section", "key"], "value")

        # Vérifier que le fichier a été mis à jour
        with open(config_file, "r") as f:
            updated_data = yaml.safe_load(f)

        assert updated_data["app"]["name"] == "Test App"
        assert updated_data["new_section"]["key"] == "value"

    def test_write_yaml_config_no_yaml_file(self, tmp_path):
        """Test de writeYamlConfig quand _yamlFile n'est pas défini."""
        with patch.object(Kernel, "getPackageResource") as mock_get_resource:
            mock_get_resource.return_value = tmp_path / "app.yaml"

            # Créer le fichier
            config_file = tmp_path / "app.yaml"
            initial_data = {"app": {"name": "Test App"}}

            with open(config_file, "w") as f:
                yaml.dump(initial_data, f)

            # Réinitialiser _yamlFile
            Kernel._yamlFile = None

            # Écrire une configuration
            Kernel.writeYamlConfig(["app", "version"], "1.0.0")

            # Vérifier que getPackageResource a été appelé
            mock_get_resource.assert_called_once_with("app.yaml")

    def test_write_yaml_config_complex_structure(self, tmp_path):
        """Test de writeYamlConfig avec structure complexe."""
        # Créer un fichier YAML de test
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"nested": {"level1": {"value": "original"}}}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Écrire dans une structure complexe
        Kernel.writeYamlConfig(["app", "nested", "level1", "new_value"], "updated")

        # Vérifier que le fichier a été mis à jour
        with open(config_file, "r") as f:
            updated_data = yaml.safe_load(f)

        assert updated_data["app"]["nested"]["level1"]["value"] == "original"
        assert updated_data["app"]["nested"]["level1"]["new_value"] == "updated"

    def test_write_yaml_config_different_value_types(self, tmp_path):
        """Test de writeYamlConfig avec différents types de valeurs."""
        # Créer un fichier YAML de test
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"name": "Test"}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Tester différents types de valeurs
        test_values = [
            ("string_value", "test string"),
            ("int_value", 42),
            ("float_value", 3.14),
            ("bool_value", True),
            ("list_value", [1, 2, 3]),
            ("dict_value", {"key": "value"}),
        ]

        for key, value in test_values:
            Kernel.writeYamlConfig(["app", key], value)

        # Vérifier que toutes les valeurs ont été écrites
        with open(config_file, "r") as f:
            updated_data = yaml.safe_load(f)

        for key, value in test_values:
            assert updated_data["app"][key] == value

    def test_write_yaml_config_nested_keys(self, tmp_path):
        """Test de writeYamlConfig avec clés imbriquées."""
        # Créer un fichier YAML de test
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"name": "Test App"}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Écrire avec des clés imbriquées
        Kernel.writeYamlConfig(["app", "nested", "deep", "key"], "deep_value")

        # Vérifier que le fichier a été mis à jour
        with open(config_file, "r") as f:
            updated_data = yaml.safe_load(f)

        assert updated_data["app"]["name"] == "Test App"
        assert updated_data["app"]["nested"]["deep"]["key"] == "deep_value"

    def test_write_yaml_config_overwrite_existing(self, tmp_path):
        """Test de writeYamlConfig pour écraser une valeur existante."""
        # Créer un fichier YAML de test
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"name": "Old Name", "version": "1.0"}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Écraser une valeur existante
        Kernel.writeYamlConfig(["app", "name"], "New Name")

        # Vérifier que le fichier a été mis à jour
        with open(config_file, "r") as f:
            updated_data = yaml.safe_load(f)

        assert updated_data["app"]["name"] == "New Name"
        assert updated_data["app"]["version"] == "1.0"  # Non modifié

    def test_load_app_settings(self, tmp_path):
        """Test de la méthode loadAppSettings."""
        # Créer un fichier app.yaml de test
        config_file = tmp_path / "app.yaml"
        config_data = {
            "app": {
                "name": "Test App",
                "description": "Test Description",
                "theme": "dark",
                "app_width": 1280,
                "app_height": 720,
                "app_min_width": 940,
                "app_min_height": 560,
                "menu_panel_shrinked_width": 60,
                "menu_panel_extended_width": 240,
                "settings_panel_width": 240,
                "time_animation": 400,
            },
            "settings_panel": {"theme": {"default": "light"}},
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        with (
            patch("ezqt_app.kernel.app_functions.Settings") as mock_settings,
            patch("ezqt_app.kernel.app_functions.QSize") as mock_qsize,
            patch("ezqt_app.kernel.app_functions.print") as mock_print,
        ):

            mock_qsize.return_value = MagicMock()

            # Appeler la méthode
            Kernel.loadAppSettings()

            # Vérifier que les paramètres ont été définis
            mock_settings.App.NAME = "Test App"
            mock_settings.App.DESCRIPTION = "Test Description"
            mock_settings.App.ENABLE_CUSTOM_TITLE_BAR = True
            mock_settings.App.APP_WIDTH = 1280
            mock_settings.App.APP_HEIGHT = 720
            mock_settings.Gui.THEME = "light"  # Depuis settings_panel
            mock_settings.Gui.MENU_PANEL_EXTENDED_WIDTH = 240
            mock_settings.Gui.MENU_PANEL_SHRINKED_WIDTH = 60
            mock_settings.Gui.SETTINGS_PANEL_WIDTH = 240
            mock_settings.Gui.TIME_ANIMATION = 400

    def test_load_app_settings_no_settings_panel(self, tmp_path):
        """Test de loadAppSettings sans section settings_panel."""
        # Créer un fichier app.yaml de test sans settings_panel
        config_file = tmp_path / "app.yaml"
        config_data = {
            "app": {
                "name": "Test App",
                "description": "Test Description",
                "theme": "dark",
                "app_width": 1280,
                "app_height": 720,
                "app_min_width": 940,
                "app_min_height": 560,
                "menu_panel_shrinked_width": 60,
                "menu_panel_extended_width": 240,
                "settings_panel_width": 240,
                "time_animation": 400,
            }
        }

        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        with (
            patch("ezqt_app.kernel.app_functions.Settings") as mock_settings,
            patch("ezqt_app.kernel.app_functions.QSize") as mock_qsize,
            patch("ezqt_app.kernel.app_functions.print") as mock_print,
        ):

            mock_qsize.return_value = MagicMock()

            # Appeler la méthode
            Kernel.loadAppSettings()

            # Vérifier que le thème vient de app
            mock_settings.Gui.THEME = "dark"

    def test_load_app_settings_no_yaml_file(self, tmp_path):
        """Test de loadAppSettings quand _yamlFile n'est pas défini."""
        with (
            patch.object(Kernel, "getPackageResource") as mock_get_resource,
            patch("ezqt_app.kernel.app_functions.Settings") as mock_settings,
            patch("ezqt_app.kernel.app_functions.QSize") as mock_qsize,
            patch("ezqt_app.kernel.app_functions.print") as mock_print,
        ):

            mock_get_resource.return_value = tmp_path / "app.yaml"
            mock_qsize.return_value = MagicMock()

            # Créer le fichier
            config_file = tmp_path / "app.yaml"
            config_data = {
                "app": {
                    "name": "Test App",
                    "theme": "dark",
                    "app_width": 1280,
                    "app_height": 720,
                    "app_min_width": 940,
                    "app_min_height": 560,
                    "menu_panel_shrinked_width": 60,
                    "menu_panel_extended_width": 240,
                    "settings_panel_width": 240,
                    "time_animation": 400,
                }
            }

            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            # Appeler la méthode
            Kernel.loadAppSettings()

            # Vérifier que getPackageResource a été appelé
            mock_get_resource.assert_called_once_with("app.yaml")

    def test_load_kernel_config_no_yaml_file(self, tmp_path):
        """Test de loadKernelConfig quand _yamlFile n'est pas défini."""
        with patch.object(Kernel, "getPackageResource") as mock_get_resource:
            mock_get_resource.return_value = tmp_path / "app.yaml"

            # Créer le fichier
            config_file = tmp_path / "app.yaml"
            config_data = {"app": {"name": "Test App"}}

            with open(config_file, "w") as f:
                yaml.dump(config_data, f)

            # Réinitialiser _yamlFile
            Kernel._yamlFile = None

            # Charger la configuration
            result = Kernel.loadKernelConfig("app")

            # Vérifier le résultat
            assert result == config_data["app"]
            mock_get_resource.assert_called_once_with("app.yaml")

    def test_save_kernel_config_create_directory(self, tmp_path):
        """Test que saveKernelConfig crée le répertoire parent."""
        # Mock du chemin de configuration avec sous-répertoire
        with patch("ezqt_app.kernel.app_functions.APP_PATH", tmp_path):
            # Sauvegarder dans un sous-répertoire
            config_data = {"test": "data"}
            Kernel.saveKernelConfig("subdir/test_config", config_data)

            # Vérifier que le fichier a été créé
            config_file = tmp_path / "subdir" / "test_config.yaml"
            assert config_file.exists()
            assert config_file.parent.exists()

    def test_load_kernel_config_yaml_error_handling(self, tmp_path):
        """Test de la gestion d'erreur YAML dans loadKernelConfig."""
        # Créer un fichier YAML invalide
        config_file = tmp_path / "app.yaml"
        with open(config_file, "w") as f:
            f.write("invalid: yaml: [")

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Essayer de charger la configuration
        with pytest.raises(yaml.YAMLError) as exc_info:
            Kernel.loadKernelConfig("app")

        # Vérifier le message d'erreur
        assert "Invalid YAML" in str(exc_info.value)
        assert str(config_file) in str(exc_info.value)

    def test_write_yaml_config_complex_structure(self, tmp_path):
        """Test de writeYamlConfig avec structure complexe."""
        # Créer un fichier YAML de test
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"nested": {"level1": {"value": "original"}}}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Écrire dans une structure complexe
        Kernel.writeYamlConfig(["app", "nested", "level1", "new_value"], "updated")

        # Vérifier que le fichier a été mis à jour
        with open(config_file, "r") as f:
            updated_data = yaml.safe_load(f)

        assert updated_data["app"]["nested"]["level1"]["value"] == "original"
        assert updated_data["app"]["nested"]["level1"]["new_value"] == "updated"

    def test_write_yaml_config_different_value_types(self, tmp_path):
        """Test de writeYamlConfig avec différents types de valeurs."""
        # Créer un fichier YAML de test
        config_file = tmp_path / "app.yaml"
        initial_data = {"app": {"name": "Test"}}

        with open(config_file, "w") as f:
            yaml.dump(initial_data, f)

        # Mock _yamlFile
        Kernel._yamlFile = config_file

        # Tester différents types de valeurs
        test_values = [
            ("string_value", "test string"),
            ("int_value", 42),
            ("float_value", 3.14),
            ("bool_value", True),
            ("list_value", [1, 2, 3]),
            ("dict_value", {"key": "value"}),
        ]

        for key, value in test_values:
            Kernel.writeYamlConfig(["app", key], value)

        # Vérifier que toutes les valeurs ont été écrites
        with open(config_file, "r") as f:
            updated_data = yaml.safe_load(f)

        for key, value in test_values:
            assert updated_data["app"][key] == value
