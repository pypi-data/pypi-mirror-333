import json
import sqlite3
import base64
import os
import datetime
import chromadb
from chromadb.utils import embedding_functions
from typing import Dict, Any

class MemoryProcessor:
    @staticmethod
    def process_sqlite_file(file_path):
        """Extract data from SQLite database file"""
        try:
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()
            
            # Extract data from memories table
            cursor.execute("SELECT * FROM memories")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            # Convert rows to JSON-serializable format
            processed_rows = []
            for row in rows:
                processed_row = []
                for item in row:
                    if isinstance(item, bytes):
                        try:
                            processed_row.append(item.decode('utf-8'))
                        except UnicodeDecodeError:
                            processed_row.append(base64.b64encode(item).decode('utf-8'))
                    else:
                        processed_row.append(item)
                processed_rows.append(processed_row)
            
            db_content = {
                "memories": {
                    "columns": columns,
                    "rows": processed_rows
                }
            }
            
            conn.close()
            return json.dumps(db_content, indent=2)
            
        except sqlite3.Error as e:
            raise Exception(f"Error reading SQLite database: {e}")

    @staticmethod
    def process_character_file(file_path):
        """Process character JSON file and extract relevant fields"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                char_data = json.load(f)
                # Extract only specific keys
                filtered_data = {}
                keys_to_extract = ['name', 'system', 'bio', 'lore', 'style', 'adjectives']
                for key in keys_to_extract:
                    if key in char_data:
                        filtered_data[key] = char_data[key]
                return json.dumps(filtered_data)
                
        except FileNotFoundError:
            raise Exception(f"Character memory file not found - {file_path}")

    @staticmethod
    def process_memory_file(file_path):
        """Read and process a regular memory file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise Exception(f"Memory file not found - {file_path}")

    def save_memory_data(self, data: Dict[str, Any], output_path: str) -> None:
        """
        Save memory data to either JSON file or ChromaDB
        
        Args:
            data (Dict[str, Any]): Memory data to save
            output_path (str): Path to save the data
            
        Raises:
            Exception: If saving fails
        """
        if output_path.endswith('.json'):
            self._save_to_json(data, output_path)
        else:
            self._save_to_chromadb(data, output_path)

    def _save_to_json(self, data: Dict[str, Any], file_path: str) -> None:
        """Save memory data to JSON file"""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data.get('data', {}), f, indent=2)

    def _save_to_chromadb(self, data: Dict[str, Any], db_path: str) -> None:
        """Save memory data to ChromaDB"""
        db_dir = os.path.dirname(db_path)
        
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=db_dir)
        
        # Backup existing collection if it exists
        self._backup_existing_collection(client, db_dir)
        
        # Create embedding function
        default_ef = embedding_functions.DefaultEmbeddingFunction()
        
        # Create new collection
        collection = client.create_collection(
            name="short_term",
            metadata={"description": "Short term memory collection"}
        )

        # Process memories
        memory_data = data.get("data", {})
        self._process_memory_type(collection, memory_data, "episodic", default_ef)
        self._process_memory_type(collection, memory_data, "character", default_ef)

    def _backup_existing_collection(self, client: chromadb.PersistentClient, db_dir: str) -> None:
        """Create backup of existing collection if it exists"""
        if "short_term" in client.list_collections():
            existing_collection = client.get_collection("short_term")
            backup_data = existing_collection.get()
            
            backup_dir = os.path.join(db_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"short_term_backup_{timestamp}.json")
            
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2)
            
            print(f"Created backup at: {backup_file}")
            client.delete_collection("short_term")

    def _process_memory_type(self, 
                           collection: chromadb.Collection, 
                           memory_data: Dict[str, Any], 
                           memory_type: str, 
                           ef: embedding_functions.DefaultEmbeddingFunction) -> None:
        """Process and add specific type of memory to collection"""
        if memory_data.get(memory_type):
            text = memory_data[memory_type]
            chunks = self._chunk_text(text)
            
            if chunks:
                embeddings = ef(chunks)
                collection.add(
                    documents=chunks,
                    embeddings=embeddings,
                    ids=[f"{memory_type}-memory-{i}" for i in range(len(chunks))]
                )

    def _chunk_text(self, text: str, chunk_size: int = 2000, overlap: int = 200) -> list:
        """Split text into overlapping chunks"""
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            
            if end < text_length:
                # Look for a good breaking point
                for i in range(min(end + 100, text_length) - 1, start + chunk_size//2, -1):
                    if text[i] in '.!?' and text[i+1] == ' ':
                        end = i + 1
                        break
            else:
                end = text_length

            chunks.append(text[start:end].strip())
            start = max(end - overlap, start + 1)
            
            if text_length - start < chunk_size:
                if start < text_length:
                    chunks.append(text[start:].strip())
                break

        return chunks