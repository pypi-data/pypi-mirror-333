from .base_handler import BaseTranslationHandler
from .v1_handler import V1Handler
from .v2_handler import V2Handler

# Create a FreeHandler class that extends BaseTranslationHandler
class FreeHandler(BaseTranslationHandler):
    """
    Handler for DeepLX free API
    """
    
    def __init__(self, base_url: str = "http://194.163.160.2:1188"):
        """
        Initialize the Free handler with the DeepLX base URL
        
        Args:
            base_url: The base URL for the DeepLX API
        """
        super().__init__(base_url)
        self.endpoint = "/translate"
        
    def parse_response(self, response):
        """
        Parse the DeepLX API response to extract the translated text
        
        Args:
            response: API response data
            
        Returns:
            Translated text
        """
        # Free DeepLX returns the translation in the "text" field
        if "text" not in response:
            raise Exception("No translation found in response")
            
        return response["text"]

# Export all handlers
__all__ = ["BaseTranslationHandler", "V1Handler", "V2Handler", "FreeHandler"]
