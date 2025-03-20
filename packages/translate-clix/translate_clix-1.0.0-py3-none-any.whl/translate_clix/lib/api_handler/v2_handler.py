from typing import Dict, Any, Optional, Union, List
from .base_handler import BaseTranslationHandler

class V2Handler(BaseTranslationHandler):
    """
    Handler for official DeepL API (v2) endpoint
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        is_free: bool = True,
        base_url: Optional[str] = None
    ):
        """
        Initialize the V2 handler
        
        Args:
            api_key: API key for authentication
            is_free: Whether to use the free API (api-free.deepl.com) or the pro API (api.deepl.com)
            base_url: Optional custom base URL (overrides the is_free parameter)
        """
        if base_url is None:
            base_url = "http://194.163.160.2:1188"
            
        super().__init__(base_url, api_key)
        self.endpoint = "/v2/translate"
        
    def get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests
        
        Returns:
            Dictionary of headers
        """
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"DeepL-Auth-Key {self.api_key}"
        return headers
        
    def prepare_request_data(
        self, 
        text: Union[str, List[str]], 
        source_lang: str, 
        target_lang: str
    ) -> Dict[str, Any]:
        """
        Prepare request data for v2 API
        
        Args:
            text: Text to translate (string or list of strings)
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Dictionary of request data
        """
        # V2 API expects text as a list of strings
        if isinstance(text, str):
            text = [text]
            
        request_data = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        # Include source_lang only if it's provided
        if source_lang:
            request_data["source_lang"] = source_lang
            
        return request_data
        
    def parse_response(self, response: Dict[str, Any]) -> str:
        """
        Parse the v2 API response to extract the translated text
        
        Args:
            response: API response data
            
        Returns:
            Translated text
        """
        # V2 returns translations as a list of objects with a "text" field
        if "translations" not in response or not response["translations"]:
            raise Exception("No translations found in response")
            
        return response["translations"][0]["text"]