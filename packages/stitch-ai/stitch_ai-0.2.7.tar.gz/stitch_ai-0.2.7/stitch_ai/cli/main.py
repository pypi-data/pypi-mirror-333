import os
import argparse
import sys
from ..sdk import StitchSDK

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(description="Stitch AI CLI tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Key generation command
    key_gen_parser = subparsers.add_parser('key', help='Generate a new API key')
    key_gen_parser.add_argument('wallet', help='Wallet address')

    # Create space command
    create_space_parser = subparsers.add_parser('create-space', help='Create a new memory space')
    create_space_parser.add_argument('name', help='Name of the memory space')

    # Push memory command
    push_parser = subparsers.add_parser('push', help='Push memory to a space')
    push_parser.add_argument('space', help='Name of the memory space')
    push_parser.add_argument('--message', '-m', help='Commit message')
    push_parser.add_argument('--episodic', '-e', help='Path to episodic memory file')
    push_parser.add_argument('--character', '-c', help='Path to character memory file')

    # Pull memory command
    pull_parser = subparsers.add_parser('pull', help='Pull memory from a space')
    pull_parser.add_argument('space', help='Name of the memory space')
    pull_parser.add_argument('memory_id', help='ID of the memory to pull')
    pull_parser.add_argument('--db-path', '-p', required=True, help='Path to save the ChromaDB or JSON file')

    # Pull external memory command
    pull_external_parser = subparsers.add_parser('pull-external', help='Pull external memory')
    pull_external_parser.add_argument('memory_id', help='ID of the memory to pull')
    pull_external_parser.add_argument('--rag-path', '-p', required=True, help='Path to save the RAG file')

    # List spaces command
    subparsers.add_parser('list-spaces', help='List all memory spaces')

    # List memories command
    list_memories_parser = subparsers.add_parser('list-memories', help='List all memories in a space')
    list_memories_parser.add_argument('space', help='Name of the memory space')

    return parser

def handle_key(sdk: StitchSDK, args: argparse.Namespace) -> None:
    """Handle key command"""
    try:
        print("_" * 50)
        response = sdk.create_key(args.wallet)
        print(f"🔑 Successfully created key for wallet: {args.wallet}")
        print(response)
        print("_" * 50)
    except Exception as e:
        print(f"❌ Error creating key: {e}", file=sys.stderr)
        sys.exit(1)

def handle_create_space(sdk: StitchSDK, args: argparse.Namespace) -> None:
    """Handle create-space command"""
    try:
        print("_" * 50)
        response = sdk.create_space(args.name)
        print(f"🌟 Successfully created space: {args.name}")
        print(response)
        print("_" * 50)
    except Exception as e:
        print(f"❌ Error creating space: {e}", file=sys.stderr)
        sys.exit(1)

def handle_push(sdk: StitchSDK, args: argparse.Namespace) -> None:
    """Handle push command"""
    try:
        print("_" * 50)
        response = sdk.push(
            space=args.space,
            message=args.message,
            episodic_path=args.episodic,
            character_path=args.character
        )
        print(f"📤 Successfully pushed memory to space: {args.space}")
        print(response)
        print("_" * 50)
    except Exception as e:
        print(f"❌ Error pushing memory: {e}", file=sys.stderr)
        sys.exit(1)

def handle_pull(sdk: StitchSDK, args: argparse.Namespace) -> None:
    """Handle pull command"""
    try:
        print("_" * 50)
        response = sdk.pull_memory(args.space, args.memory_id, args.db_path)
        print(f"📥 Successfully pulled memory from space: {args.space}")
        if args.db_path.endswith('.json'):
            print(f"📄 Memory data saved to JSON file: {args.db_path}")
        else:
            print(f"💾 Memory data saved to ChromaDB at: {args.db_path}")
        print(response)
        print("_" * 50)
    except Exception as e:
        print(f"❌ Error pulling memory: {e}", file=sys.stderr)
        sys.exit(1)

def handle_pull_external(sdk: StitchSDK, args: argparse.Namespace) -> None:
    """Handle pull-external command"""
    try:
        print("_" * 50)
        response = sdk.pull_external_memory(args.memory_id, args.rag_path)
        print(f"🌐 Successfully pulled external memory")
        print(response)
        print("_" * 50)
    except Exception as e:
        print(f"❌ Error pulling external memory: {e}", file=sys.stderr)
        sys.exit(1)

def handle_list_spaces(sdk: StitchSDK, args: argparse.Namespace) -> None:
    """Handle list-spaces command"""
    try:
        print("_" * 50)
        response = sdk.list_spaces()
        print("📚 Available memory spaces:")
        for space in response['data']:
            print(f"  • {space}")
        print("_" * 50)
    except Exception as e:
        print(f"❌ Error listing spaces: {e}", file=sys.stderr)
        sys.exit(1)

def handle_list_memories(sdk: StitchSDK, args: argparse.Namespace) -> None:
    """Handle list-memories command"""
    try:
        print("_" * 50)
        response = sdk.list_memories(args.space)
        print(f"🧠 Memories in space '{args.space}':")
        print(response)
        print("_" * 50)
    except Exception as e:
        print(f"❌ Error listing memories: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    """Main entry point for the CLI"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Initialize SDK
    base_url = os.environ.get('STITCH_API_URL', 'https://api-devnet.stitch-ai.co')
    api_key = os.environ.get('STITCH_API_KEY')
    
    if not api_key:
        print("Error: STITCH_API_KEY environment variable is not set", file=sys.stderr)
        sys.exit(1)

    try:
        sdk = StitchSDK(base_url=base_url, api_key=api_key)
    except Exception as e:
        print(f"Error initializing SDK: {e}", file=sys.stderr)
        sys.exit(1)

    # Command handlers
    handlers = {
        'key': handle_key,
        'create-space': handle_create_space,
        'push': handle_push,
        'pull': handle_pull,
        'pull-external': handle_pull_external,
        'list-spaces': handle_list_spaces,
        'list-memories': handle_list_memories,
    }

    # Execute the appropriate handler
    handler = handlers.get(args.command)
    if handler:
        handler(sdk, args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()