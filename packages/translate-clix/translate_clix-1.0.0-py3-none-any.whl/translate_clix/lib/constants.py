"""
Constants for translate-clix
"""
from pathlib import Path

# Configuration
CONFIG_DIR = Path.home() / ".config" / "translate-clix"
CONFIG_FILE = CONFIG_DIR / "config.yml"
HISTORY_FILE = CONFIG_DIR / "history.json"

# Default API URLs
DEFAULT_DEEPLX_URL = "http://194.163.160.2:1188/translate"
DEFAULT_DEEPL_V2_URL = "http://194.163.160.2:1188/v2/translate"
DEFAULT_DEEPL_V1_URL = "http://194.163.160.2:1188/v1/translate"

# Default API endpoints
DEFAULT_FREE_ENDPOINT = "/translate"
DEFAULT_V1_ENDPOINT = "/v1/translate"
DEFAULT_V2_ENDPOINT = "/v2/translate"

# Default config structure
DEFAULT_CONFIG = {
    "api_urls": {
        "deeplx": DEFAULT_DEEPLX_URL,
        "deepl_v2": DEFAULT_DEEPL_V2_URL,
        "deepl_v1": DEFAULT_DEEPL_V1_URL
    },
    "api_endpoints": {
        "free": DEFAULT_FREE_ENDPOINT,
        "v1": DEFAULT_V1_ENDPOINT,
        "v2": DEFAULT_V2_ENDPOINT
    },
    "source_lang": "CS",
    "target_lang": "EN-US",
    "api_type": "v2"
}

# Available languages
LANGUAGES = {
    "czech": "CS",
    "english": "EN-US",
    "french": "FR",
    "german": "DE",
    "spanish": "ES",
    "italian": "IT",
    "portuguese": "PT",
    "russian": "RU",
    "turkish": "TR",
    "polish": "PL",
    "romanian": "RO",
} 