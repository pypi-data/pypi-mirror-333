import requests
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize the API client
        
        Args:
            base_url (str): Base URL for the API
            api_key (str): API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key

    def get_headers(self) -> Dict[str, str]:
        """Get the default headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_space(self, name: str) -> Dict[str, Any]:
        """
        Create a new memory space
        
        Args:
            name (str): Name of the memory space
            
        Returns:
            Dict[str, Any]: API response
        """
        url = f"{self.base_url}/memory/space"
        payload = {"name": name}
        response = requests.post(url, json=payload, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def push_memory(self, 
                   space: str, 
                   message: Optional[str] = None, 
                   episodic: Optional[Dict] = None, 
                   character: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Push memory to a space
        
        Args:
            space (str): Name of the memory space
            message (str, optional): Commit message
            episodic (Dict, optional): Episodic memory data
            character (Dict, optional): Character memory data
            
        Returns:
            Dict[str, Any]: API response
        """
        url = f"{self.base_url}/memory/{space}/push"
        payload = {
            "message": message or "Auto-generated commit message",
            "episodic": episodic,
            "character": character
        }
        response = requests.post(url, json=payload, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def pull_memory(self, space: str, memory_id: str) -> Dict[str, Any]:
        """
        Pull memory from a space
        
        Args:
            space (str): Name of the memory space
            memory_id (str): ID of the memory to pull
            
        Returns:
            Dict[str, Any]: API response
        """
        url = f"{self.base_url}/memory/{space}/pull/{memory_id}"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def list_spaces(self) -> Dict[str, Any]:
        """
        List all memory spaces
        
        Returns:
            Dict[str, Any]: API response containing list of spaces
        """
        url = f"{self.base_url}/memory/spaces"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def list_memories(self, space: str) -> Dict[str, Any]:
        """
        List all memories in a space
        
        Args:
            space (str): Name of the memory space
            
        Returns:
            Dict[str, Any]: API response containing list of memories
        """
        url = f"{self.base_url}/memory/{space}/list"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def handle_error(self, response: requests.Response) -> None:
        """
        Handle API error responses
        
        Args:
            response (requests.Response): Response object from the API
            
        Raises:
            Exception: With appropriate error message
        """
        try:
            error_data = response.json()
            error_message = error_data.get('message', 'Unknown error occurred')
        except ValueError:
            error_message = response.text or 'Unknown error occurred'
        
        raise Exception(f"API Error ({response.status_code}): {error_message}")