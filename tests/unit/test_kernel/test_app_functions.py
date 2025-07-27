# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////

"""
Tests unitaires pour les fonctions d'application du kernel.
"""

import pytest
import yaml
from pathlib import Path
from unittest.mock import patch, MagicMock

from ezqt_app.kernel.app_functions import Kernel


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
