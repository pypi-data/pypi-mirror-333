import pycurl
import json
from io import BytesIO
from typing import Dict, Any, Optional, Union

class BaseApiClient:
    """
    Base class for making curl requests to translation APIs
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the API client with base URL and optional API key
        
        Args:
            base_url: The base URL for the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url
        self.api_key = api_key
        
    def _make_request(
        self, 
        endpoint: str, 
        data: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make a curl request to the specified endpoint
        
        Args:
            endpoint: API endpoint path
            data: Request data to be sent
            headers: Optional headers to include in the request
            
        Returns:
            The parsed JSON response
        """
        buffer = BytesIO()
        c = pycurl.Curl()
        
        # Set URL
        url = f"{self.base_url}{endpoint}"
        c.setopt(c.URL, url)
        
        # Set method to POST
        c.setopt(c.POST, 1)
        
        # Set headers
        header_list = []
        if headers:
            for key, value in headers.items():
                header_list.append(f"{key}: {value}")
        header_list.append("Content-Type: application/json")
        c.setopt(c.HTTPHEADER, header_list)
        
        # Set request body
        json_data = json.dumps(data).encode('utf-8')
        c.setopt(c.POSTFIELDS, json_data)
        
        # Set write function to capture the response
        c.setopt(c.WRITEFUNCTION, buffer.write)
        
        # Set timeout
        c.setopt(c.TIMEOUT, 10)
        
        # Execute the request
        try:
            c.perform()
            status_code = c.getinfo(c.RESPONSE_CODE)
            c.close()
            
            # Parse the response
            response_body = buffer.getvalue().decode('utf-8')
            response = json.loads(response_body)
            
            # Check for errors
            if status_code >= 400:
                error_msg = response.get('message', 'Unknown error')
                raise Exception(f"API request failed with status {status_code}: {error_msg}")
                
            return response
            
        except pycurl.error as e:
            error_code, error_msg = e.args
            raise Exception(f"Curl error {error_code}: {error_msg}")
        except json.JSONDecodeError:
            raise Exception("Failed to parse API response as JSON")
            
    def translate(
        self, 
        text: Union[str, list], 
        source_lang: str, 
        target_lang: str
    ) -> Dict[str, Any]:
        """
        Base method for translation - to be implemented by subclasses
        
        Args:
            text: Text to translate (string or list of strings)
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Translation response data
        """
        raise NotImplementedError("Subclasses must implement translate()")
