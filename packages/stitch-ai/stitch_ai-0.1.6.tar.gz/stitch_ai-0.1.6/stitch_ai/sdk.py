import os
import json
import argparse
import requests
from dotenv import load_dotenv
import sys

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

    def push(self, space: str, message: str, episodic_memory: str = None, character_memory: str = None):
        if episodic_memory is None:
            episodic_memory = message
        if character_memory is None:
            character_memory = message

        url = f"{self.base_url}/memory/{space}"
        payload = {
            "message": message,
            "episodicMemory": episodic_memory,
            "characterMemory": character_memory
        }
        response = requests.post(url, json=payload, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def list_memories(self, space: str):
        url = f"{self.base_url}/memory/{space}"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()

    def pull(self, space: str, memory_id: str):
        url = f"{self.base_url}/memory/{space}/{memory_id}"
        response = requests.get(url, headers=self.get_headers())
        response.raise_for_status()
        return response.json()


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
    push_parser.add_argument("space", "-s", dest="space", type=str, help="Memory space name")
    push_parser.add_argument("message", "-m", dest="message", type=str, help="Memory push commit message")
    push_parser.add_argument("--episodic", "-e", dest="episodic", type=str, help="Path to episodic memory file", required=False, default='./agent/data/db.sqlite')
    push_parser.add_argument("--character", "-c", dest="character", type=str, help="Path to character memory file", required=False, default='./characters/default.character.json')

    pull_parser = subparsers.add_parser("pull", help="Download specific memory")
    pull_parser.add_argument("space", type=str, help="Memory space name")
    pull_parser.add_argument("memory_id", type=str, help="Memory ID")

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

            message = None
            episodic = None
            character = None
            
            # Extract data from SQLite database if it's a .sqlite file
            if args.episodic:
                if args.episodic.endswith('.sqlite'):
                    try:
                        import sqlite3
                        conn = sqlite3.connect(args.episodic)
                        cursor = conn.cursor()
                        
                        # Get all table names
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        tables = cursor.fetchall()
                        
                        # Extract data from all tables
                        db_content = {}
                        for table in tables:
                            table_name = table[0]
                            cursor.execute(f"SELECT * FROM {table_name}")
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
                            
                            db_content[table_name] = {
                                "columns": columns,
                                "rows": processed_rows
                            }
                        
                        episodic = json.dumps(db_content, indent=2)
                        conn.close()
                    except sqlite3.Error as e:
                        print(f"❌ Error reading SQLite database: {e}")
                        sys.exit(1)
                else:
                    # Read episodic memory file if provided
                    try:
                        with open(args.episodic, 'r', encoding='utf-8') as f:
                            episodic = f.read()
                    except FileNotFoundError:
                        print(f"❌ Error: Episodic memory file not found - {args.episodic}")
                        sys.exit(1)
            
            # Read character memory file if provided
            try:
                with open(args.character, 'r', encoding='utf-8') as f:
                    char_data = json.load(f)
                    # Extract only specific keys
                    filtered_data = {}
                    keys_to_extract = ['name', 'system', 'bio', 'lore', 'style', 'adjectives']
                    for key in keys_to_extract:
                        if key in char_data:
                            filtered_data[key] = char_data[key]
                    character = json.dumps(filtered_data)
            except FileNotFoundError:
                print(f"❌ Error: Character memory file not found - {args.character}")
                sys.exit(1)
            except json.JSONDecodeError:
                print(f"❌ Error: Invalid JSON format in character file - {args.character}")
                sys.exit(1)
            
            # Use the file name as the message if no specific message is provided
            if not args.message:
                message = f"Memory push from {args.episodic} and {args.character}"
            else:
                message = args.message
            
            result = sdk.push(args.space, message, episodic, character)
            print(f"✨ Successfully pushed memories to space '{args.space}' 🚀")
            print(f"📝 Message: {message}")
            print(f"📊 Episodic Memory File: {args.episodic}")
            print(f"👤 Character Memory File: {args.character}")
            print("\nResponse details:")
            print(json.dumps(result, indent=2))
        elif args.command == "pull":
            result = sdk.pull(args.space, args.memory_id)
            print(json.dumps(result, indent=2))
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
