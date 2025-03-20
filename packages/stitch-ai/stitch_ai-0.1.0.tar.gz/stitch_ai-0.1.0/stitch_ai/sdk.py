import os
import json
import argparse
import requests

class StitchSDK:
    def __init__(self, base_url="http://localhost:3000", api_key=None):
        self.base_url = base_url
        self.api_key = api_key or os.environ.get("STITCH_API_KEY")
        if not self.api_key:
            raise ValueError("STITCH_API_KEY environment variable is not set.")

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # 메모리 공간 관련
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

    # 메모리 관련
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
    parser = argparse.ArgumentParser(description="Stitch SDK CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    create_space_parser = subparsers.add_parser("create-space", help="Create a new memory space")
    create_space_parser.add_argument("name", type=str, help="Memory space name")

    push_parser = subparsers.add_parser("push", help="Upload memory")
    push_parser.add_argument("space", type=str, help="Memory space name")
    push_parser.add_argument("message", type=str, help="Memory message")
    push_parser.add_argument("--episodic", type=str, help="Episodic memory (optional)", default=None)
    push_parser.add_argument("--character", type=str, help="Character memory (optional)", default=None)

    pull_parser = subparsers.add_parser("pull", help="Download specific memory")
    pull_parser.add_argument("space", type=str, help="Memory space name")
    pull_parser.add_argument("memory_id", type=str, help="Memory ID")

    list_parser = subparsers.add_parser("list", help="List memory spaces or memories in a specific space")
    list_parser.add_argument("-s", "--space", type=str, help="Specific memory space name (optional)", default=None)

    args = parser.parse_args()

    sdk = StitchSDK()

    try:
        if args.command == "create-space":
            result = sdk.create_space(args.name)
            print(json.dumps(result, indent=2))
        elif args.command == "push":
            result = sdk.push(args.space, args.message, args.episodic, args.character)
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
