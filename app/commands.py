from typing import List, Optional, Dict, Any
from app import logger

def process_command(command: str, args: List[str]) -> str:
    """
    Process a command and return a response.
    """
    try:
        if command == "PING":
            return "PONG"
        elif command == "ECHO":
            return " ".join(args)
        else:
            raise ValueError("Unknown command")
    except Exception as e:
        raise ValueError("Error processing command: " + str(e))