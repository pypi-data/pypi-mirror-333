import os
from typing import Optional, Dict, Any
from .processors.memory_processor import MemoryProcessor
from .processors.text_processor import TextProcessor
from .api.client import APIClient

class StitchSDK:
    """
    Main SDK class for interacting with the Stitch AI platform.
    Provides high-level interface for memory management operations.
    """
    
    def __init__(self, base_url: str = "https://api-devnet.stitch-ai.co", api_key: Optional[str] = None):
        """
        Initialize the Stitch SDK
        
        Args:
            base_url (str): Base URL for the API
            api_key (str, optional): API key for authentication. If not provided,
                                   will try to get from STITCH_API_KEY environment variable
        
        Raises:
            ValueError: If API key is not provided and not found in environment variables
        """
        self.api_key = api_key or os.environ.get("STITCH_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either directly or via STITCH_API_KEY environment variable")
        
        self.api_client = APIClient(base_url, self.api_key)
        self.memory_processor = MemoryProcessor()
        self.text_processor = TextProcessor()

    def create_space(self, name: str) -> Dict[str, Any]:
        """
        Create a new memory space
        
        Args:
            name (str): Name of the memory space
            
        Returns:
            Dict[str, Any]: API response containing space details
            
        Raises:
            Exception: If space creation fails
        """
        return self.api_client.create_space(name)

    def push(self, 
            space: str, 
            message: Optional[str] = None, 
            episodic_path: Optional[str] = None, 
            character_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Push memory data to a space
        
        Args:
            space (str): Name of the memory space
            message (str, optional): Commit message
            episodic_path (str, optional): Path to episodic memory file
            character_path (str, optional): Path to character memory file
            
        Returns:
            Dict[str, Any]: API response
            
        Raises:
            ValueError: If neither episodic_path nor character_path is provided
            Exception: If processing or pushing fails
        """
        if not episodic_path and not character_path:
            raise ValueError("At least one of episodic_path or character_path must be provided")

        episodic_data = None
        character_data = None
        
        # Process episodic memory if provided
        if episodic_path:
            if episodic_path.endswith('.sqlite'):
                episodic_data = self.memory_processor.process_sqlite_file(episodic_path)
            else:
                episodic_data = self.memory_processor.process_memory_file(episodic_path)
                # Chunk large text files if necessary
                if isinstance(episodic_data, str) and len(episodic_data) > 2000:
                    episodic_data = self.text_processor.chunk_text(episodic_data)
        
        # Process character memory if provided
        if character_path:
            character_data = self.memory_processor.process_character_file(character_path)

        # Push to API
        return self.api_client.push_memory(
            space=space,
            message=message,
            episodic=episodic_data,
            character=character_data
        )

    def pull_memory(self, space: str, memory_id: str) -> Dict[str, Any]:
        """
        Pull memory from a space
        
        Args:
            space (str): Name of the memory space
            memory_id (str): ID of the memory to pull
            
        Returns:
            Dict[str, Any]: API response containing memory data
            
        Raises:
            Exception: If pulling fails
        """
        return self.api_client.pull_memory(space, memory_id)

    def list_spaces(self) -> Dict[str, Any]:
        """
        List all memory spaces
        
        Returns:
            Dict[str, Any]: API response containing list of spaces
            
        Raises:
            Exception: If listing fails
        """
        return self.api_client.list_spaces()

    def list_memories(self, space: str) -> Dict[str, Any]:
        """
        List all memories in a space
        
        Args:
            space (str): Name of the memory space
            
        Returns:
            Dict[str, Any]: API response containing list of memories
            
        Raises:
            Exception: If listing fails
        """
        return self.api_client.list_memories(space)

    def validate_api_key(self) -> bool:
        """
        Validate the API key by making a test request
        
        Returns:
            bool: True if API key is valid, False otherwise
        """
        try:
            self.list_spaces()
            return True
        except Exception:
            return False

    def get_version(self) -> str:
        """
        Get the SDK version
        
        Returns:
            str: Version string
        """
        return "0.2.0"