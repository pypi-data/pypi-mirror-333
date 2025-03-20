# Stitch SDK

Stitch SDK is a Python library that wraps the API for managing memory spaces and memories. It provides both a Python SDK and a command-line interface (CLI).

## Installation

```bash
pip install stitch_ai
```

## SDK Usage

```python
from stitch_ai import StitchSDK

sdk = StitchSDK()
sdk.create_space("my_space")
```

## CLI Usage

Before using the CLI, set your API key as an environment variable:

```bash
export STITCH_API_KEY=your_api_key
```

### Available Commands

1. Create a new memory space:
```bash
stitch create-space <space_name>
```

2. Push memory to a space:
```bash
stitch push <space_name> [-m COMMIT_MESSAGE] [-e EPISODIC_FILE_PATH] [-c CHARACTER_FILE_PATH]
```

3. Pull memory from a space:
```bash
stitch pull <space_name> <memory_id> [-p DB_PATH]
```

4. Pull external memory:
```bash
stitch pull-external <memory_id> [-p RAG_PATH]
```

5. List all memory spaces:
```bash
stitch list-spaces
```

6. List all memories in a space:
```bash
stitch list-memories <space_name>
```

### Examples

```bash
# Create a new memory space
stitch create-space my_space

# Push memory with a message and files
stitch push my_space -m "Initial memory" -e ./agent/data/db.sqlite -c ./characters/default.character.json

# List all memories in a space
stitch list-memories my_space

# Pull a specific memory
stitch pull my_space memory_123 -p ./db/chroma.sqlite3

# Pull external memory
stitch pull-external memory_123 -p ./rag/rag.json
```

## Environment Variables

- `STITCH_API_KEY`: Your API key (required)
- `STITCH_API_URL`: API endpoint (optional, defaults to https://api-devnet.stitch-ai.co)