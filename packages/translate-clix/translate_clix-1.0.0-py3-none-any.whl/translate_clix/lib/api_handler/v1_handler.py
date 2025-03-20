from typing import Dict, Any, Optional, Union
from .base_handler import BaseTranslationHandler

class V1Handler(BaseTranslationHandler):
    """
    Handler for DeepL Pro API (v1) endpoint
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.deepl.com"):
        """
        Initialize the V1 handler
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
        """
        super().__init__(base_url, api_key)
        self.endpoint = "/v1/translate"
        
    def get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests
        
        Returns:
            Dictionary of headers
        """
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
        
    def prepare_request_data(
        self, 
        text: Union[str, list], 
        source_lang: str, 
        target_lang: str
    ) -> Dict[str, Any]:
        """
        Prepare request data for v1 API
        
        Args:
            text: Text to translate (string or list of strings)
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Dictionary of request data
        """
        # V1 API expects text as a string, not a list
        if isinstance(text, list):
            text = text[0]
            
        return {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
    def parse_response(self, response: Dict[str, Any]) -> str:
        """
        Parse the v1 API response to extract the translated text
        
        Args:
            response: API response data
            
        Returns:
            Translated text
        """
        # V1 returns the translation in "data" field
        if "data" not in response:
            raise Exception("No translation found in response")
            
        return response["data"]
