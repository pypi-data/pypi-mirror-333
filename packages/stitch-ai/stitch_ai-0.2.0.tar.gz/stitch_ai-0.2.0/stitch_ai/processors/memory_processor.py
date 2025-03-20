import json
import sqlite3
import base64

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