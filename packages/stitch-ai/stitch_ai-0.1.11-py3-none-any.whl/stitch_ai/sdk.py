import os
import json
import argparse
import requests
from dotenv import load_dotenv
import sys
import chromadb
from chromadb.utils import embedding_functions
import datetime

class StitchSDK:
    def __init__(self, base_url="http://localhost:3000", api_key=None):
        self.base_url = base_url
        self.api_key = api_key or os.environ.get("STITCH_API_KEY")
        if not self.api_key:
            raise ValueError("STITCH_API_KEY environment variable is not set.")

    def get_headers(self):
        return {
            "apiKey": self.api_key,
            "Content-Type": "application/json",
        }

    def create_space(self, name: str):
        url = f"{self.base_url}/memory/space"
        payload = {"name": name}
        response = requests.post(url, json=payload, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def list_spaces(self):
        url = f"{self.base_url}/memory/spaces"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def delete_space(self, name: str):
        url = f"{self.base_url}/memory/space/{name}"
        response = requests.delete(url, headers=self.get_headers())
        response.raise_for_status()
        return response.json() if response.text else None

    def process_sqlite_file(self, file_path):
        """Extract data from SQLite database file"""
        try:
            import sqlite3
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
                            import base64
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

    def process_character_file(self, file_path):
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
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in character file - {file_path}")

    def process_memory_file(self, file_path):
        """Read and process a regular memory file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise Exception(f"Memory file not found - {file_path}")

    def push(self, space: str, message: str = None, episodic_path: str = None, character_path: str = None):
        """
        Push memories to the specified space
        
        Args:
            space (str): The name of the memory space
            message (str, optional): Commit message for the push
            episodic_path (str, optional): Path to episodic memory file
            character_path (str, optional): Path to character memory file
        """
        if not episodic_path and not character_path:
            raise ValueError("At least one of episodic_path or character_path must be provided")

        episodic = None
        character = None
        
        # Process episodic memory file
        if episodic_path:
            if episodic_path.endswith('.sqlite'):
                episodic = self.process_sqlite_file(episodic_path)
            else:
                episodic = self.process_memory_file(episodic_path)
        
        # Process character memory file
        if character_path:
            character = self.process_character_file(character_path)
        
        # Generate default message if none provided
        if not message:
            files = []
            if episodic_path:
                files.append(episodic_path)
            if character_path:
                files.append(character_path)
            message = f"Memory push from {' and '.join(files)}"
        
        # Make the API call
        return self.push_data(space, message, episodic, character)

    def push_data(self, space: str, message: str, episodic: str = None, character: str = None):
        """Raw push method that sends data directly to the API"""
        if episodic is None:
            episodic = ""
        if character is None:
            character = ""

        url = f"{self.base_url}/memory/{space}"
        payload = {
            "message": message,
            "episodicMemory": episodic,
            "characterMemory": character
        }
        response = requests.post(url, json=payload, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def list_memories(self, space: str):
        url = f"{self.base_url}/memory/{space}"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def chunk_text(self, text, chunk_size=2000, overlap=200):
        """Split text into overlapping chunks of approximately chunk_size characters"""
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            # Find the end of the chunk
            end = start + chunk_size
            
            # If this is not the last chunk, try to find a good breaking point
            if end < text_length:
                # Look for a period, question mark, or exclamation mark followed by a space
                for i in range(min(end + 100, text_length) - 1, start + chunk_size//2, -1):
                    if text[i] in '.!?' and text[i+1] == ' ':
                        end = i + 1
                        break
            else:
                end = text_length

            # Add the chunk to our list
            chunks.append(text[start:end].strip())
            
            # Move the start pointer, including overlap
            start = max(end - overlap, start + 1)
            
            # If we're near the end, just include the rest
            if text_length - start < chunk_size:
                if start < text_length:
                    chunks.append(text[start:].strip())
                break

        return chunks

    def pull(self, space: str, memory_id: str, db_path: str):
        url = f"{self.base_url}/memory/{space}/{memory_id}"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        response_data = response.json()

        # If db_path ends with .json, write only the 'data' portion to the file
        if db_path.endswith('.json'):
            os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(response_data.get('data', {}), f, indent=2)
            return response_data

        db_dir = os.path.dirname(db_path)
        
        # Initialize ChromaDB client
        client = chromadb.PersistentClient(path=db_dir)
        
        # Backup existing collection if it exists
        if "short_term" in client.list_collections():
            existing_collection = client.get_collection("short_term")
            backup_data = existing_collection.get()
            
            # Create backup directory if it doesn't exist
            backup_dir = os.path.join(db_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Create backup file with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"short_term_backup_{timestamp}.json")
            
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(backup_data, f, indent=2)
                
            print(f"Created backup at: {backup_file}")
            client.delete_collection("short_term")
        
        # Create embedding function
        default_ef = embedding_functions.DefaultEmbeddingFunction()
        
        # Create new collection
        collection = client.create_collection(
            name="short_term",
            metadata={"description": "Short term memory collection"}
        )

        # Process and add episodic memory if it exists
        if response_data.get("data", {}).get("episodic"):
            episodic_text = response_data["data"]["episodic"]
            episodic_chunks = self.chunk_text(episodic_text)
            
            if episodic_chunks:
                episodic_embeddings = default_ef(episodic_chunks)
                collection.add(
                    documents=episodic_chunks,
                    embeddings=episodic_embeddings,
                    ids=[f"episodic-memory-{i}" for i in range(len(episodic_chunks))]
                )

        # Process and add character memory if it exists
        if response_data.get("data", {}).get("character"):
            character_text = response_data["data"]["character"]
            character_chunks = self.chunk_text(character_text)
            
            if character_chunks:
                character_embeddings = default_ef(character_chunks)
                collection.add(
                    documents=character_chunks,
                    embeddings=character_embeddings,
                    ids=[f"character-memory-{i}" for i in range(len(character_chunks))]
                )

        return response_data


def main():
    current_dir = os.getcwd()
    
    while True:
        if os.path.exists(os.path.join(current_dir, '.env')):
            load_dotenv(os.path.join(current_dir, '.env'))
            break
        
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            load_dotenv()
            break
            
        current_dir = parent_dir
    
    api_key = os.environ.get("STITCH_API_KEY")
    if not api_key:
        print("❌ Error: STITCH_API_KEY environment variable is not set")
        print("Please set your API key in .env file or environment variables")
        sys.exit(1)

    base_url = os.environ.get("STITCH_BASE_URL")
    if not base_url:
        base_url = "https://api-devnet.stitch-ai.co"

    sdk = StitchSDK(base_url=base_url, api_key=api_key)

    parser = argparse.ArgumentParser(description="Stitch SDK CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    create_space_parser = subparsers.add_parser("create-space", help="Create a new memory space")
    create_space_parser.add_argument("name", type=str, help="Memory space name")

    push_parser = subparsers.add_parser("push", help="Upload memory from file")
    push_parser.add_argument("-s", "--space", dest="space", type=str, help="Memory space name", required=True)
    push_parser.add_argument("-m", "--message", dest="message", type=str, help="Memory push commit message", required=False)
    push_parser.add_argument("-e", "--episodic", dest="episodic", type=str, help="Path to episodic memory file (example: ./agent/data/db.sqlite)", required=False)
    push_parser.add_argument("-c", "--character", dest="character", type=str, help="Path to character memory file (example: ./characters/default.character.json)", required=False)

    pull_parser = subparsers.add_parser("pull", help="Download specific memory")
    pull_parser.add_argument("-s", "--space", type=str, help="Memory space name", required=True)
    pull_parser.add_argument("-i", "--memory-id", type=str, help="Memory ID", required=True)
    pull_parser.add_argument("-p", "--db-path", type=str, help="chroma db path", required=True)

    list_parser = subparsers.add_parser("list", help="List memory spaces or memories in a specific space")
    list_parser.add_argument("-s", "--space", type=str, help="Specific memory space name (optional)", default=None)

    args = parser.parse_args()

    try:
        if args.command == "create-space":
            result = sdk.create_space(args.name)
            print(f"✨ Memory space '{args.name}' has been successfully created! 🎉")
            print(json.dumps(result, indent=2))
        elif args.command == "push":
            if not args.episodic and not args.character:
                print("❌ Error: At least one of --episodic or --character must be provided")
                sys.exit(1)
            
            try:
                result = sdk.push(
                    space=args.space,
                    message=args.message,
                    episodic_path=args.episodic,
                    character_path=args.character
                )
                print(f"✨ Successfully pushed memories to space '{args.space}' 🚀")
                print(f"📝 Message: {args.message or 'Auto-generated'}")
                print(f"📊 Episodic Memory File: {args.episodic}")
                print(f"👤 Character Memory File: {args.character}")
                print("\nResponse details:")
                print(json.dumps(result, indent=2))
            except Exception as e:
                print(f"❌ Error during push: {str(e)}")
                sys.exit(1)
        elif args.command == "pull":
            try:
                result = sdk.pull(args.space, args.memory_id, args.db_path)
                print(f"✨ Successfully pulled memory '{args.memory_id}' from space '{args.space}' 🚀")            
                print(json.dumps(result, indent=2))
            except Exception as e:
                print(f"❌ Error during pull: {str(e)}")
                sys.exit(1)
        elif args.command == "list":
            if args.space:
                result = sdk.list_memories(args.space)
            else:
                result = sdk.list_spaces()
            print(json.dumps(result, indent=2))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
