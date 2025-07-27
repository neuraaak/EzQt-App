# Tests du TranslationManager

Cette page documente les tests unitaires pour le `TranslationManager` d'EzQt_App.

## Vue d'ensemble

Le `TranslationManager` est responsable de :
- Gestion des traductions et internationalisation
- Chargement de fichiers de traduction (.ts/.qm)
- Enregistrement et retraduction des widgets
- Émission de signaux lors des changements de langue

## Fichier de test

**Fichier** : `tests/unit/test_kernel/test_translation_manager.py`
**Classe de test** : `TestTranslationManager`
**Nombre de tests** : ~25 tests

## Tests implémentés

### 1. Tests d'initialisation

#### `test_init_default_language`
**Objectif** : Vérifier l'initialisation avec la langue par défaut
```python
def test_init_default_language(self):
    """Test de l'initialisation avec la langue par défaut."""
    manager = TranslationManager()
    assert manager.current_language == "en"
    assert manager.translator is not None
```

#### `test_language_mapping`
**Objectif** : Vérifier le mapping des langues
```python
def test_language_mapping(self):
    """Test du mapping des langues."""
    manager = TranslationManager()
    expected_mapping = {
        "English": "en",
        "Français": "fr",
        "Español": "es",
        "Deutsch": "de",
    }
    assert manager.language_mapping == expected_mapping
```

### 2. Tests de chargement de langues

#### `test_load_language_by_code_success`
**Objectif** : Test de chargement réussi d'une langue par code
```python
def test_load_language_by_code_success(self, qt_application):
    """Test de chargement réussi d'une langue par code."""
    manager = TranslationManager()
    success = manager.load_language_by_code("fr")
    assert success == True
    assert manager.get_current_language_code() == "fr"
```

#### `test_load_language_by_code_invalid`
**Objectif** : Test de chargement avec un code invalide
```python
def test_load_language_by_code_invalid(self, qt_application):
    """Test de chargement avec un code de langue invalide."""
    manager = TranslationManager()
    success = manager.load_language_by_code("invalid")
    assert success == False
```

#### `test_load_language_by_name_success`
**Objectif** : Test de chargement réussi d'une langue par nom
```python
def test_load_language_by_name_success(self, qt_application):
    """Test de chargement réussi d'une langue par nom."""
    manager = TranslationManager()
    success = manager.load_language("Français")
    assert success == True
    assert manager.get_current_language_code() == "fr"
```

### 3. Tests de gestion des widgets

#### `test_register_widget`
**Objectif** : Test d'enregistrement d'un widget
```python
def test_register_widget(self, qt_application):
    """Test d'enregistrement d'un widget."""
    manager = TranslationManager()
    mock_widget = MagicMock()
    original_text = "Hello World"
    
    manager.register_widget(mock_widget, original_text)
    
    assert mock_widget in manager._translatable_widgets
    assert manager._translatable_texts[mock_widget] == original_text
```

#### `test_unregister_widget`
**Objectif** : Test de désenregistrement d'un widget
```python
def test_unregister_widget(self, qt_application):
    """Test de désenregistrement d'un widget."""
    manager = TranslationManager()
    mock_widget = MagicMock()
    manager.register_widget(mock_widget, "Test")
    
    manager.unregister_widget(mock_widget)
    
    assert mock_widget not in manager._translatable_widgets
    assert mock_widget not in manager._translatable_texts
```

#### `test_clear_registered_widgets`
**Objectif** : Test de nettoyage de tous les widgets
```python
def test_clear_registered_widgets(self, qt_application):
    """Test de nettoyage de tous les widgets enregistrés."""
    manager = TranslationManager()
    widgets = [MagicMock() for _ in range(3)]
    
    for widget in widgets:
        manager.register_widget(widget, "Test")
    
    manager.clear_registered_widgets()
    
    assert len(manager._translatable_widgets) == 0
    assert len(manager._translatable_texts) == 0
```

### 4. Tests de traduction

#### `test_translate_text`
**Objectif** : Test de traduction de texte
```python
def test_translate_text(self, qt_application):
    """Test de traduction de texte."""
    manager = TranslationManager()
    text = "Hello World"
    translated = manager.translate(text)
    
    # Sans fichier de traduction, le texte original est retourné
    assert translated == text
```

#### `test_translate_text_with_context`
**Objectif** : Test de traduction avec contexte
```python
def test_translate_text_with_context(self, qt_application):
    """Test de traduction de texte avec contexte."""
    manager = TranslationManager()
    text = "Hello World"
    context = "greeting"
    translated = manager.translate(text, context)
    
    assert translated == text
```

### 5. Tests de signaux

#### `test_language_changed_signal`
**Objectif** : Test d'émission du signal de changement de langue
```python
def test_language_changed_signal(self, qt_application):
    """Test d'émission du signal de changement de langue."""
    manager = TranslationManager()
    signal_received = False
    received_language = None
    
    def on_language_changed(lang):
        nonlocal signal_received, received_language
        signal_received = True
        received_language = lang
    
    manager.languageChanged.connect(on_language_changed)
    
    with patch('ezqt_app.kernel.translation_manager.QCoreApplication'):
        manager.load_language_by_code("fr")
    
    assert signal_received == True
    assert received_language == "fr"
```

### 6. Tests de méthodes utilitaires

#### `test_get_current_language_code`
**Objectif** : Test de récupération du code de langue actuel
```python
def test_get_current_language_code(self, qt_application):
    """Test de récupération du code de langue actuel."""
    manager = TranslationManager()
    assert manager.get_current_language_code() == "en"
```

#### `test_get_current_language_name`
**Objectif** : Test de récupération du nom de langue actuel
```python
def test_get_current_language_name(self, qt_application):
    """Test de récupération du nom de langue actuel."""
    manager = TranslationManager()
    assert manager.get_current_language_name() == "English"
```

#### `test_get_available_languages`
**Objectif** : Test de récupération des langues disponibles
```python
def test_get_available_languages(self, qt_application):
    """Test de récupération des langues disponibles."""
    manager = TranslationManager()
    languages = manager.get_available_languages()
    expected_languages = ["English", "Français", "Español", "Deutsch"]
    
    for lang in expected_languages:
        assert lang in languages
```

### 7. Tests de gestion d'erreurs

#### `test_load_language_file_not_found`
**Objectif** : Test de chargement avec fichier inexistant
```python
@patch('ezqt_app.kernel.translation_manager.TranslationManager._get_translations_dir')
def test_load_language_file_not_found(self, mock_dir, qt_application):
    """Test de chargement avec fichier de traduction inexistant."""
    mock_dir.return_value = Path("/nonexistent")
    manager = TranslationManager()
    
    success = manager.load_language_by_code("fr")
    assert success == False
```

#### `test_register_widget_with_none`
**Objectif** : Test d'enregistrement avec widget None
```python
def test_register_widget_with_none(self, qt_application):
    """Test d'enregistrement avec widget None."""
    manager = TranslationManager()
    
    # Ne devrait pas lever d'exception
    manager.register_widget(None, "Test")
    
    assert None not in manager._translatable_widgets
```

## Fixtures utilisées

### `qt_application`
**Utilisation** : Tous les tests nécessitant Qt
**Objectif** : Fournir une instance QApplication

### `mock_translation_files`
**Utilisation** : Tests de chargement de fichiers
**Objectif** : Créer des fichiers de traduction temporaires

## Cas d'usage avancés

### Test de retraduction automatique
```python
def test_auto_retranslate_widgets(self, qt_application):
    """Test de retraduction automatique des widgets."""
    manager = TranslationManager()
    mock_widget = MagicMock()
    manager.register_widget(mock_widget, "Hello")
    
    with patch('ezqt_app.kernel.translation_manager.QCoreApplication'):
        manager.load_language_by_code("fr")
    
    # Vérifier que le widget a été retraduit
    mock_widget.setText.assert_called()
```

### Test de persistance de langue
```python
def test_language_persistence(self, qt_application):
    """Test de persistance de la langue sélectionnée."""
    manager1 = TranslationManager()
    manager1.load_language_by_code("fr")
    
    manager2 = TranslationManager()
    assert manager2.get_current_language_code() == "fr"
```

## Bonnes pratiques

### Pour les tests du TranslationManager
1. **Utiliser `qt_application`** : Tous les tests nécessitent Qt
2. **Mocker QCoreApplication** : Pour éviter les effets de bord
3. **Tester les signaux** : Vérifier l'émission des signaux Qt
4. **Gestion d'erreurs** : Tester les cas d'erreur
5. **Nettoyage** : Utiliser `clear_registered_widgets()` après les tests

### Conventions spécifiques
- Utiliser `MagicMock()` pour les widgets
- Tester les cas limites (None, chaînes vides)
- Vérifier l'état avant et après les opérations
- Documenter les tests complexes

## Dépannage

### Problèmes courants
1. **Signal non émis** : Vérifier la configuration Qt
2. **Widget non retraduit** : Vérifier l'enregistrement
3. **Langue non changée** : Vérifier le fichier de traduction
4. **Tests qui échouent** : Vérifier les mocks

### Debug
```bash
# Test spécifique avec debug
python -m pytest tests/unit/test_kernel/test_translation_manager.py::TestTranslationManager::test_specific -v -s

# Avec couverture
python -m pytest tests/unit/test_kernel/test_translation_manager.py --cov=ezqt_app.kernel.translation_manager --cov-report=term-missing
``` 