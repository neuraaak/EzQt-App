#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de différentes APIs de traduction gratuites
"""

import requests
import json
import time
from datetime import datetime

def test_libretranslate_servers():
    """Test différents serveurs LibreTranslate"""
    
    servers = [
        "https://libretranslate.com",
        "https://translate.argosopentech.com",  # Serveur alternatif
        "https://libretranslate.de",  # Serveur allemand
        "https://translate.fortytwo-it.com",  # Serveur français
    ]
    
    test_data = {
        "q": "Hello world",
        "source": "en",
        "target": "fr",
        "format": "text"
    }
    
    headers = {'Content-Type': 'application/json'}
    
    print("🌐 Test des serveurs LibreTranslate")
    print("=" * 60)
    
    for server in servers:
        url = f"{server}/translate"
        print(f"\n🔍 Test de: {server}")
        
        try:
            response = requests.post(url, json=test_data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                translated = result.get('translatedText', '')
                print(f"✅ Succès: '{translated}'")
                return server  # Retourner le premier serveur qui fonctionne
            else:
                print(f"❌ Erreur {response.status_code}")
                try:
                    error = response.json().get('error', '')
                    print(f"🚨 {error}")
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    return None

def test_google_translate_web():
    """Test de l'API web de Google Translate (non officielle)"""
    
    print("\n🔍 Test de Google Translate Web")
    print("=" * 60)
    
    # URL de l'API web de Google Translate
    url = "https://translate.googleapis.com/translate_a/single"
    
    params = {
        'client': 'gtx',
        'sl': 'en',
        'tl': 'fr',
        'dt': 't',
        'q': 'Hello world'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            # Google retourne un format spécial
            data = response.json()
            if data and len(data) > 0 and len(data[0]) > 0:
                translated = data[0][0][0]
                print(f"✅ Succès: '{translated}'")
                return "google_web"
            else:
                print("❌ Format de réponse inattendu")
        else:
            print(f"❌ Erreur {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def test_mymemory_translate():
    """Test de MyMemory Translation API (gratuit)"""
    
    print("\n🔍 Test de MyMemory Translation")
    print("=" * 60)
    
    url = "https://api.mymemory.translated.net/get"
    
    params = {
        'q': 'Hello world',
        'langpair': 'en|fr'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            translated = result.get('responseData', {}).get('translatedText', '')
            
            if translated:
                print(f"✅ Succès: '{translated}'")
                return "mymemory"
            else:
                print("❌ Pas de traduction retournée")
        else:
            print(f"❌ Erreur {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def test_lingva_translate():
    """Test de Lingva Translate (alternative gratuite)"""
    
    print("\n🔍 Test de Lingva Translate")
    print("=" * 60)
    
    # Lingva Translate API
    url = "https://lingva.ml/api/v1/en/fr/Hello%20world"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            translated = result.get('translation', '')
            
            if translated:
                print(f"✅ Succès: '{translated}'")
                return "lingva"
            else:
                print("❌ Pas de traduction retournée")
        else:
            print(f"❌ Erreur {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def test_rapidapi_translate():
    """Test de RapidAPI Translate (gratuit avec limite)"""
    
    print("\n🔍 Test de RapidAPI Translate")
    print("=" * 60)
    
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/get"
    
    headers = {
        'X-RapidAPI-Key': 'test',  # Clé de test
        'X-RapidAPI-Host': 'translated-mymemory---translation-memory.p.rapidapi.com'
    }
    
    params = {
        'q': 'Hello world',
        'langpair': 'en|fr'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            translated = result.get('responseData', {}).get('translatedText', '')
            
            if translated:
                print(f"✅ Succès: '{translated}'")
                return "rapidapi"
            else:
                print("❌ Pas de traduction retournée")
        else:
            print(f"❌ Erreur {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def main():
    """Test principal de toutes les APIs"""
    
    print("🚀 Test des APIs de traduction gratuites")
    print("=" * 60)
    print(f"⏰ Heure: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    working_apis = []
    
    # Test LibreTranslate
    libretranslate_server = test_libretranslate_servers()
    if libretranslate_server:
        working_apis.append(("libretranslate", libretranslate_server))
    
    # Test Google Translate Web
    if test_google_translate_web():
        working_apis.append(("google_web", "https://translate.googleapis.com"))
    
    # Test MyMemory
    if test_mymemory_translate():
        working_apis.append(("mymemory", "https://api.mymemory.translated.net"))
    
    # Test Lingva
    if test_lingva_translate():
        working_apis.append(("lingva", "https://lingva.ml"))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    if working_apis:
        print("✅ APIs fonctionnelles trouvées:")
        for api_name, url in working_apis:
            print(f"  - {api_name}: {url}")
    else:
        print("❌ Aucune API gratuite fonctionnelle trouvée")
        print("\n💡 Suggestions:")
        print("  - Vérifiez votre connexion internet")
        print("  - Les APIs peuvent être temporairement indisponibles")
        print("  - Considérez l'utilisation d'une clé API pour LibreTranslate")
    
    print("\n🏁 Tests terminés!")

if __name__ == "__main__":
    main() 