# TODO - EzQt_App

## 🚧 **Tests EzApplication - Corrections Nécessaires**

### **Problème Identifié**
Les tests d'instance EzApplication échouent avec l'erreur :
```
AttributeError: <class 'tests.unit.test_widgets.test_core.test_ez_app.MockQApplication'> does not have the attribute 'instance'
```

### **Tests Affectés (Actuellement en SKIP)**
- `test_locale_configuration_success`
- `test_locale_configuration_failure`
- `test_environment_variables_setup`
- `test_high_dpi_scaling_configuration`
- `test_application_properties`
- `test_environment_setup_mocked`
- `test_theme_changed_signal_instance`

### **Cause Racine**
Le mocking de QApplication ne fonctionne pas correctement pour les méthodes de classe comme `instance()`. La classe `MockQApplication` ne peut pas être utilisée comme une classe de classe pour les méthodes statiques.

### **Solutions à Explorer**

#### **1. Amélioration du MockQApplication**

```python
class MockQApplication:
    """
    Mock de QApplication avec support des méthodes de classe.
    """
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._attributes = {}
        self._theme_changed = Signal()
    
    @classmethod
    def instance(cls):
        """Méthode de classe pour simuler QApplication.instance()."""
        return None  # ou retourner une instance mockée
    
    def setAttribute(self, attribute, value):
        self._attributes[attribute] = value
    
    def testAttribute(self, attribute):
        return self._attributes.get(attribute, False)
    
    def quit(self):
        pass
    
    def deleteLater(self):
        pass
    
    @property
    def themeChanged(self):
        return self._theme_changed
```

#### **2. Utilisation de pytest-qt**
```bash
pip install pytest-qt
```

Et modifier les tests pour utiliser les fixtures de pytest-qt :
```python
def test_example(qtbot):
    """Test avec pytest-qt."""
    app = EzApplication.create_for_testing([])
    # Tests...
```

#### **3. Mocking au Niveau Module**
```python
@patch('ezqt_app.widgets.core.ez_app.QApplication')
def test_example(mock_qapp):
    """Test avec mocking au niveau module."""
    mock_qapp.instance.return_value = None
    # Tests...
```

#### **4. Utilisation de unittest.mock.patch.object**
```python
@patch.object(QApplication, 'instance')
def test_example(mock_instance):
    """Test avec patch.object."""
    mock_instance.return_value = None
    # Tests...
```

### **Priorité**
- **Haute** : Corriger les tests EzApplication pour maintenir la couverture
- **Moyenne** : Améliorer le système de mocking pour les futurs tests Qt
- **Basse** : Optimiser les performances des tests

### **Ressources**
- [PySide6 Testing Best Practices](https://doc.qt.io/qtforpython/tutorials/testing.html)
- [pytest-qt Documentation](https://pytest-qt.readthedocs.io/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)

---

## 🔄 **Autres Améliorations**

### **Performance des Tests**
- [ ] Optimiser les fixtures pour réduire le temps d'exécution
- [ ] Paralléliser les tests avec pytest-xdist
- [ ] Réduire les délais d'attente dans les tests Qt

### **Couverture de Code**
- [ ] Augmenter la couverture des widgets complexes
- [ ] Ajouter des tests pour les cas limites
- [ ] Tester les erreurs et exceptions

### **Documentation**
- [ ] Mettre à jour la documentation des tests
- [ ] Ajouter des exemples de tests
- [ ] Documenter les bonnes pratiques

### **Maintenance**
- [ ] Nettoyer les fichiers temporaires de test
- [ ] Organiser les fixtures par module
- [ ] Standardiser les conventions de test

---

## 📝 **Notes de Développement**

### **Approches Testées (Non Fonctionnelles)**
1. ✅ Mocking simple de QApplication.instance()
2. ✅ Méthode create_for_testing avec gestion d'erreurs
3. ✅ Fixtures avec nettoyage manuel
4. ❌ MockQApplication (problème avec les méthodes de classe)

### **Prochaines Étapes**
1. Tester pytest-qt comme solution alternative
2. Implémenter le mocking au niveau module
3. Évaluer l'utilisation de patch.object
4. Documenter la solution choisie

### **Impact**
- **Couverture actuelle** : 214 tests passent, 7 tests en skip
- **Couverture cible** : 221 tests passent, 0 test en skip
- **Temps d'exécution** : ~2.17s (acceptable)
- **Fiabilité** : Tests stables malgré les skips 