# -*- coding: utf-8 -*-
# ///////////////////////////////////////////////////////////////
# EzQt_App - A Modern Qt Application Framework
# ///////////////////////////////////////////////////////////////
#
# Author: EzQt_App Team
# Website: https://github.com/ezqt-app/ezqt_app
#
# This file is part of EzQt_App.
#
# EzQt_App is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EzQt_App is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EzQt_App.  If not, see <https://www.gnu.org/licenses/>.
# ///////////////////////////////////////////////////////////////

# IMPORT BASE
# ///////////////////////////////////////////////////////////////
import hashlib
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# IMPORT SPECS
# ///////////////////////////////////////////////////////////////
import requests
from PySide6.QtCore import QObject, QThread, Signal

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from ..common import APP_PATH
from .config import SUPPORTED_LANGUAGES
from ..app_functions.printer import get_printer

## ==> GLOBALS
# ///////////////////////////////////////////////////////////////

## ==> VARIABLES
# ///////////////////////////////////////////////////////////////

## ==> CLASSES
# ///////////////////////////////////////////////////////////////


class TranslationProvider:
    """Base translation provider class"""

    def __init__(self, name: str, base_url: str):
        """
        Initialize translation provider.

        Parameters
        ----------
        name : str
            Provider name
        base_url : str
            Base URL for the service
        """
        self.name = name
        self.base_url = base_url
        self.timeout = 10
        self.rate_limit_delay = 1.0  # Delay between requests

    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate text (to be implemented in subclasses)"""
        raise NotImplementedError

    def is_available(self) -> bool:
        """Check if service is available"""
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False


class LibreTranslateProvider(TranslationProvider):
    """LibreTranslate provider"""

    def __init__(self, api_key: str = None, custom_server: str = None):
        server = custom_server or "https://libretranslate.com"
        super().__init__("LibreTranslate", server)
        self.api_key = api_key
        self.rate_limit_delay = 1.0

    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate text via LibreTranslate"""
        try:
            url = f"{self.base_url}/translate"

            data = {
                "q": text,
                "source": source_lang,
                "target": target_lang,
                "format": "text",
            }

            if self.api_key:
                data["api_key"] = self.api_key

            headers = {"Content-Type": "application/json"}

            response = requests.post(
                url, json=data, headers=headers, timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("translatedText")
            else:
                # Try alternative server if first one fails
                if self.base_url == "https://libretranslate.com":
                    get_printer().warning(
                        f"LibreTranslate error: {response.status_code}, trying alternative server"
                    )
                    # Create new provider with alternative server
                    alt_provider = LibreTranslateProvider(
                        custom_server="https://translate.argosopentech.com"
                    )
                    return alt_provider.translate(text, source_lang, target_lang)
                else:
                    get_printer().warning(
                        f"LibreTranslate error: {response.status_code}"
                    )
                    return None

        except Exception as e:
            get_printer().warning(f"LibreTranslate exception: {e}")
            return None


class GoogleTranslateProvider(TranslationProvider):
    """Google Translate Web provider (unofficial)"""

    def __init__(self):
        super().__init__("Google Translate", "https://translate.googleapis.com")
        self.rate_limit_delay = 0.5

    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate text via Google Translate Web"""
        try:
            url = f"{self.base_url}/translate_a/single"

            params = {
                "client": "gtx",
                "sl": source_lang,
                "tl": target_lang,
                "dt": "t",
                "q": text,
            }

            response = requests.get(url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0 and len(data[0]) > 0:
                    return data[0][0][0]
            else:
                get_printer().warning(f"Google Translate error: {response.status_code}")

        except Exception as e:
            get_printer().warning(f"Google Translate exception: {e}")

        return None


class MyMemoryProvider(TranslationProvider):
    """MyMemory provider (free, no API key required)"""

    def __init__(self):
        super().__init__("MyMemory", "https://api.mymemory.translated.net")

    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate text via MyMemory"""
        try:
            url = f"{self.base_url}/get"

            params = {
                "q": text,
                "langpair": f"{source_lang}|{target_lang}",
            }

            response = requests.get(url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                if data.get("responseStatus") == 200:
                    return data.get("responseData", {}).get("translatedText")
            else:
                get_printer().warning(f"MyMemory error: {response.status_code}")

        except Exception as e:
            get_printer().warning(f"MyMemory exception: {e}")

        return None


class TranslationCache:
    """Translation cache manager"""

    def __init__(self, cache_file: Path):
        """
        Initialize translation cache.

        Parameters
        ----------
        cache_file : Path
            Cache file path
        """
        self.cache_file = cache_file
        self.cache_data = {}
        self.max_age_days = 30  # Maximum cache age
        self.load_cache()

    def _get_cache_key(self, text: str, source_lang: str, target_lang: str) -> str:
        """Generate unique cache key"""
        key_string = f"{text}|{source_lang}|{target_lang}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """
        Get translation from cache.

        Parameters
        ----------
        text : str
            Original text
        source_lang : str
            Source language
        target_lang : str
            Target language

        Returns
        -------
        Optional[str]
            Cached translation or None
        """
        key = self._get_cache_key(text, source_lang, target_lang)
        entry = self.cache_data.get(key)

        if entry:
            # Check cache age
            created_time = datetime.fromisoformat(entry["created"])
            if datetime.now() - created_time < timedelta(days=self.max_age_days):
                return entry["translation"]
            else:
                # Remove expired entry
                del self.cache_data[key]

        return None

    def set(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        translation: str,
        provider: str,
    ):
        """
        Store translation in cache.

        Parameters
        ----------
        text : str
            Original text
        source_lang : str
            Source language
        target_lang : str
            Target language
        translation : str
            Translated text
        provider : str
            Provider name
        """
        key = self._get_cache_key(text, source_lang, target_lang)
        self.cache_data[key] = {
            "original": text,
            "translation": translation,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "provider": provider,
            "created": datetime.now().isoformat(),
        }
        self.save_cache()

    def load_cache(self):
        """Load cache from file"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.cache_data = json.load(f)
        except Exception as e:
            get_printer().warning(f"Error loading cache: {e}")
            self.cache_data = {}

    def save_cache(self):
        """Save cache to file"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            get_printer().warning(f"Error saving cache: {e}")

    def clear_expired(self):
        """Clear expired cache entries"""
        current_time = datetime.now()
        expired_keys = []

        for key, entry in self.cache_data.items():
            created_time = datetime.fromisoformat(entry["created"])
            if current_time - created_time > timedelta(days=self.max_age_days):
                expired_keys.append(key)

        for key in expired_keys:
            del self.cache_data[key]

        if expired_keys:
            self.save_cache()


class AutoTranslationWorker(QThread):
    """Background thread for automatic translations"""

    translation_completed = Signal(str, str, str)  # original, translated, provider
    translation_failed = Signal(str, str)  # original, error

    def __init__(self, providers: List[TranslationProvider], cache: TranslationCache):
        """
        Initialize translation worker.

        Parameters
        ----------
        providers : List[TranslationProvider]
            List of translation providers
        cache : TranslationCache
            Translation cache
        """
        super().__init__()
        self.providers = providers
        self.cache = cache
        self.running = True

    def translate_text(self, text: str, source_lang: str, target_lang: str):
        """
        Translate text in background.

        Parameters
        ----------
        text : str
            Text to translate
        source_lang : str
            Source language
        target_lang : str
            Target language
        """
        # Check cache first
        cached_translation = self.cache.get(text, source_lang, target_lang)
        if cached_translation:
            self.translation_completed.emit(text, cached_translation, "cache")
            return

        # Try providers
        for provider in self.providers:
            if not self.running:
                break

            try:
                translation = provider.translate(text, source_lang, target_lang)
                if translation:
                    # Cache and emit signal
                    self.cache.set(
                        text, source_lang, target_lang, translation, provider.name
                    )
                    self.translation_completed.emit(text, translation, provider.name)
                    return

                # Delay between requests
                time.sleep(provider.rate_limit_delay)

            except Exception as e:
                get_printer().warning(f"Translation error with {provider.name}: {e}")

        # No translation found
        self.translation_failed.emit(text, "No translation found")

    def stop(self):
        """Request thread stop"""
        self.running = False


class AutoTranslator(QObject):
    """Automatic translation manager"""

    translation_ready = Signal(str, str)  # original, translated
    translation_error = Signal(str, str)  # original, error

    def __init__(self, cache_dir: Path = None):
        """
        Initialize auto translator.

        Parameters
        ----------
        cache_dir : Path, optional
            Cache directory (default: ~/.ezqt/cache)
        """
        super().__init__()
        if cache_dir is None:
            cache_dir = Path.home() / ".ezqt" / "cache"

        cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache = TranslationCache(cache_dir / "translations.json")

        self.providers = []
        self.worker = None
        # TODO: Réactiver la configuration des fournisseurs - DÉSACTIVÉ TEMPORAIREMENT
        # self._setup_providers()
        
        # TODO: Réactiver la traduction automatique - DÉSACTIVÉ TEMPORAIREMENT
        self.enabled = False  # DÉSACTIVÉ TEMPORAIREMENT

    def _setup_providers(self):
        """Setup default translation providers"""
        # TODO: Réactiver les fournisseurs de traduction - DÉSACTIVÉ TEMPORAIREMENT
        # LibreTranslate (free, no API key)
        # self.add_provider(LibreTranslateProvider())

        # MyMemory (free, no API key)
        # self.add_provider(MyMemoryProvider())

        # Google Translate (unofficial)
        # self.add_provider(GoogleTranslateProvider())

    def add_provider(self, provider: TranslationProvider):
        """Add translation provider"""
        self.providers.append(provider)

    def remove_provider(self, provider_name: str):
        """Remove translation provider by name"""
        self.providers = [p for p in self.providers if p.name != provider_name]

    def translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """
        Translate text asynchronously.

        Parameters
        ----------
        text : str
            Text to translate
        source_lang : str
            Source language
        target_lang : str
            Target language

        Returns
        -------
        Optional[str]
            Cached translation if available, None otherwise
        """
        # Check cache first
        cached = self.cache.get(text, source_lang, target_lang)
        if cached:
            return cached

        # Check minimum interval
        if hasattr(self, "_last_request_time"):
            elapsed = time.time() - self._last_request_time
            if elapsed < 1.0:  # Minimum 1 second between requests
                time.sleep(1.0 - elapsed)

        # Check cache first
        cached_translation = self.cache.get(text, source_lang, target_lang)
        if cached_translation:
            return cached_translation

        # Translate in background
        if not self.worker or not self.worker.isRunning():
            self.worker = AutoTranslationWorker(self.providers, self.cache)
            self.worker.translation_completed.connect(self._on_translation_completed)
            self.worker.translation_failed.connect(self._on_translation_failed)
            self.worker.start()

        self.worker.translate_text(text, source_lang, target_lang)
        self._last_request_time = time.time()

        return None

    def translate_sync(
        self, text: str, source_lang: str, target_lang: str
    ) -> Optional[str]:
        """
        Translate text synchronously.

        Parameters
        ----------
        text : str
            Text to translate
        source_lang : str
            Source language
        target_lang : str
            Target language

        Returns
        -------
        Optional[str]
            Translated text or None
        """
        # TODO: Réactiver la traduction synchrone - DÉSACTIVÉ TEMPORAIREMENT
        if not self.enabled:
            return None
            
        # Check cache first
        cached_translation = self.cache.get(text, source_lang, target_lang)
        if cached_translation:
            return cached_translation

        # Try providers
        for provider in self.providers:
            try:
                translation = provider.translate(text, source_lang, target_lang)
                if translation:
                    self.cache.set(
                        text, source_lang, target_lang, translation, provider.name
                    )
                    return translation

                # Delay between requests
                time.sleep(provider.rate_limit_delay)

            except Exception as e:
                get_printer().warning(f"Translation error with {provider.name}: {e}")

        return None

    def _on_translation_completed(self, original: str, translated: str, provider: str):
        """Called when translation is completed"""
        get_printer().info(
            f"Automatic translation ({provider}): '{original}' → '{translated}'"
        )
        self.translation_ready.emit(original, translated)

    def _on_translation_failed(self, original: str, error: str):
        """Called when translation fails"""
        get_printer().warning(f"Automatic translation failed: '{original}' - {error}")
        self.translation_error.emit(original, error)

    def save_translation_to_ts(
        self, original: str, translated: str, target_lang: str, ts_file_path: Path
    ):
        """
        Save translation to .ts file.

        Parameters
        ----------
        original : str
            Original text
        translated : str
            Translated text
        target_lang : str
            Target language
        ts_file_path : Path
            .ts file path
        """
        try:
            # Load existing .ts file or create new one
            ts_data = {}
            if ts_file_path.exists():
                # Load existing .ts file or create new one
                with open(ts_file_path, "r", encoding="utf-8") as f:
                    ts_data = json.load(f)

            # Create new .ts file
            if not ts_data:
                ts_data = {
                    "metadata": {
                        "language": target_lang,
                        "created": datetime.now().isoformat(),
                    },
                    "translations": {},
                }

            # Check if translation already exists
            if original in ts_data["translations"]:
                # Update existing translation
                ts_data["translations"][original] = translated
            else:
                # Add new translation
                ts_data["translations"][original] = translated

            # Save to file
            ts_file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(ts_file_path, "w", encoding="utf-8") as f:
                json.dump(ts_data, f, indent=2, ensure_ascii=False)

            get_printer().info(f"Translation saved to {ts_file_path}")

        except Exception as e:
            get_printer().warning(f"Error saving translation to .ts file: {e}")

    def clear_cache(self):
        """Clear translation cache"""
        self.cache.cache_data.clear()
        self.cache.save_cache()
        get_printer().info("Translation cache cleared")

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns
        -------
        Dict[str, Any]
            Cache statistics
        """
        stats = {
            "total_entries": len(self.cache.cache_data),
            "cache_file": str(self.cache.cache_file),
            "max_age_days": self.cache.max_age_days,
        }

        # Count by provider
        provider_stats = {}
        for entry in self.cache.cache_data.values():
            provider = entry.get("provider", "unknown")
            provider_stats[provider] = provider_stats.get(provider, 0) + 1

        stats["by_provider"] = provider_stats

        return stats

    def cleanup(self):
        """Cleanup resources"""
        if self.worker:
            self.worker.stop()
            self.worker.wait()

        self.cache.clear_expired()


# Global instance
_auto_translator_instance = None


def get_auto_translator() -> AutoTranslator:
    """
    Get global auto translator instance.

    Returns
    -------
    AutoTranslator
        Global auto translator instance
    """
    global _auto_translator_instance
    if _auto_translator_instance is None:
        _auto_translator_instance = AutoTranslator()
    return _auto_translator_instance


# Alias for compatibility
auto_translator = get_auto_translator
