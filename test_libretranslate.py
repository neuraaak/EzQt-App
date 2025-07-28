#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour LibreTranslate
Test simple pour vérifier le fonctionnement de l'API
"""

import requests
import json
import time
from datetime import datetime

def test_libretranslate():
    """Test simple de LibreTranslate"""
    
    # URL de l'API LibreTranslate
    url = "https://libretranslate.com/translate"
    
    # Données de test
    test_data = {
        "q": "Hello world",
        "source": "en",
        "target": "fr",
        "format": "text"
    }
    
    # Headers
    headers = {
        'Content-Type': 'application/json'
    }
    
    print("🧪 Test de LibreTranslate")
    print("=" * 50)
    print(f"⏰ Heure: {datetime.now().strftime('%H:%M:%S')}")
    print(f"🌐 URL: {url}")
    print(f"📝 Texte à traduire: '{test_data['q']}'")
    print(f"🔄 De {test_data['source']} vers {test_data['target']}")
    print()
    
    try:
        print("📡 Envoi de la requête...")
        start_time = time.time()
        
        # Envoi de la requête
        response = requests.post(url, json=test_data, headers=headers, timeout=10)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"⏱️  Temps de réponse: {response_time:.2f} secondes")
        print(f"📊 Code de statut: {response.status_code}")
        
        if response.status_code == 200:
            # Succès
            result = response.json()
            translated_text = result.get('translatedText', '')
            
            print("✅ Succès!")
            print(f"📤 Texte original: '{test_data['q']}'")
            print(f"📥 Texte traduit: '{translated_text}'")
            
            # Test de qualité basique
            if translated_text and translated_text != test_data['q']:
                print("🎯 Traduction réussie!")
            else:
                print("⚠️  Traduction identique au texte original")
                
        else:
            # Erreur
            print("❌ Erreur de requête")
            print(f"📄 Réponse: {response.text}")
            
            # Analyser l'erreur
            try:
                error_data = response.json()
                if 'error' in error_data:
                    print(f"🚨 Erreur: {error_data['error']}")
            except:
                pass
                
    except requests.exceptions.Timeout:
        print("⏰ Timeout - La requête a pris trop de temps")
    except requests.exceptions.ConnectionError:
        print("🌐 Erreur de connexion - Vérifiez votre connexion internet")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête: {e}")
    except Exception as e:
        print(f"💥 Erreur inattendue: {e}")
    
    print()
    print("=" * 50)

def test_multiple_languages():
    """Test avec plusieurs langues"""
    
    url = "https://libretranslate.com/translate"
    headers = {'Content-Type': 'application/json'}
    
    test_cases = [
        {"text": "Hello", "source": "en", "target": "fr", "expected": "bonjour"},
        {"text": "Good morning", "source": "en", "target": "es", "expected": "buenos días"},
        {"text": "Thank you", "source": "en", "target": "de", "expected": "danke"},
    ]
    
    print("🌍 Test avec plusieurs langues")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔤 Test {i}: {test_case['source']} → {test_case['target']}")
        print(f"📝 Texte: '{test_case['text']}'")
        
        data = {
            "q": test_case['text'],
            "source": test_case['source'],
            "target": test_case['target'],
            "format": "text"
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                translated = result.get('translatedText', '')
                print(f"✅ Résultat: '{translated}'")
                
                # Vérification basique
                if translated.lower() in test_case['expected'].lower() or test_case['expected'].lower() in translated.lower():
                    print("🎯 Traduction correcte!")
                else:
                    print("⚠️  Traduction différente de l'attendu")
            else:
                print(f"❌ Erreur {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        # Pause entre les requêtes pour être poli
        time.sleep(1)

def test_api_limits():
    """Test pour vérifier les limites de l'API"""
    
    url = "https://libretranslate.com/translate"
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "q": "Test",
        "source": "en",
        "target": "fr",
        "format": "text"
    }
    
    print("🔄 Test des limites de l'API")
    print("=" * 50)
    print("⚠️  Attention: Ce test envoie plusieurs requêtes rapides")
    
    success_count = 0
    error_count = 0
    
    for i in range(5):  # Test avec 5 requêtes rapides
        try:
            response = requests.post(url, json=data, headers=headers, timeout=5)
            
            if response.status_code == 200:
                success_count += 1
                print(f"✅ Requête {i+1}: Succès")
            else:
                error_count += 1
                print(f"❌ Requête {i+1}: Erreur {response.status_code}")
                
        except Exception as e:
            error_count += 1
            print(f"❌ Requête {i+1}: Exception - {e}")
        
        time.sleep(0.5)  # Pause courte
    
    print(f"\n📊 Résumé: {success_count} succès, {error_count} erreurs")
    
    if error_count > 0:
        print("⚠️  Des erreurs ont été détectées - possible limitation de taux")
    else:
        print("✅ Toutes les requêtes ont réussi")

if __name__ == "__main__":
    print("🚀 Démarrage des tests LibreTranslate")
    print()
    
    # Test principal
    test_libretranslate()
    
    # Test multi-langues
    test_multiple_languages()
    
    # Test des limites
    test_api_limits()
    
    print("\n🏁 Tests terminés!")
    print("\n💡 Conseils:")
    print("- Si les tests échouent, vérifiez votre connexion internet")
    print("- LibreTranslate peut avoir des temps de réponse variables")
    print("- Les limites sont généralement par IP, pas par requête") 