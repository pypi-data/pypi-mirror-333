"""
Locale data module for MockPy
"""
import os
import json
import logging
from typing import Dict, Any, Set
from functools import lru_cache

logger = logging.getLogger(__name__)

LOCALE_PATH = os.path.dirname(os.path.abspath(__file__))

_available_locales: Set[str] = set()

@lru_cache(maxsize=32)
def get_available_locales() -> Set[str]:
    """
    Get a set of available locale codes from the filesystem.
    Results are cached to avoid repeated filesystem access.
    
    Returns:
        Set of available locale codes (e.g. "en_US", "tr_TR")
    """
    global _available_locales
    
    if not _available_locales:
        _available_locales = {
            os.path.splitext(f)[0] 
            for f in os.listdir(LOCALE_PATH) 
            if f.endswith('.json')
        }
    
    return _available_locales

@lru_cache(maxsize=32)
def load_locale_data(locale_code: str) -> Dict[str, Any]:
    """
    Load locale data from a JSON file.
    Results are cached using lru_cache for performance.
    
    Args:
        locale_code: The locale code (e.g. "en_US", "tr_TR")
        
    Returns:
        Dictionary containing locale data
    
    Raises:
        FileNotFoundError: If the locale file is not found
    """
    try:
        file_path = os.path.join(LOCALE_PATH, f"{locale_code}.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"Locale file not found: {file_path}")
            if locale_code != "en_US" and "en_US" in get_available_locales():
                logger.info(f"Falling back to en_US locale")
                return load_locale_data("en_US")
            raise FileNotFoundError(f"Locale file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing locale file {locale_code}: {str(e)}")
        raise