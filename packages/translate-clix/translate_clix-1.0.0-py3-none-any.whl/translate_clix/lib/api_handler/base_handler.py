from typing import Dict, Any, Optional, Union
from ..base import BaseApiClient

class BaseTranslationHandler(BaseApiClient):
    """
    Base handler for translation APIs with common functionality
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the translation handler
        
        Args:
            base_url: The base URL for the API
            api_key: Optional API key for authentication
        """
        super().__init__(base_url, api_key)
        self.endpoint = "/translate"  # Default endpoint
        
    def get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests
        
        Returns:
            Dictionary of headers
        """
        return {}
        
    def prepare_request_data(
        self, 
        text: Union[str, list], 
        source_lang: str, 
        target_lang: str
    ) -> Dict[str, Any]:
        """
        Prepare request data for translation
        
        Args:
            text: Text to translate (string or list of strings)
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Dictionary of request data
        """
        return {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
    def parse_response(self, response: Dict[str, Any]) -> str:
        """
        Parse the API response to extract the translated text
        
        Args:
            response: API response data
            
        Returns:
            Translated text
        """
        raise NotImplementedError("Subclasses must implement parse_response()")
        
    def translate(
        self, 
        text: Union[str, list], 
        source_lang: str, 
        target_lang: str
    ) -> str:
        """
        Translate text using the API
        
        Args:
            text: Text to translate (string or list of strings)
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        data = self.prepare_request_data(text, source_lang, target_lang)
        headers = self.get_headers()
        
        response = self._make_request(self.endpoint, data, headers)
        return self.parse_response(response)
