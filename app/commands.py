from typing import List, Optional, Dict, Any
import fnmatch
from app import logger, main_database

def process_command(command: str, args: List[str]) -> str:
    """
    Process a command and return a response.
    """
    try:
        if command == "PING":
            return "PONG"

        elif command == "ECHO":
            return " ".join(args)

        elif command == "SET":
            if len(args) != 2:
                raise ValueError("SET command requires two arguments")
            key, value = args
            main_database[key] = value
            return "OK"

        elif command == "GET":
            if len(args) != 1:
                raise ValueError("GET command requires one argument")
            key = args[0]
            return main_database.get(key, "NULL")

        elif command == "DEL":
            if len(args) != 1:
                raise ValueError("DEL command requires one argument")
            key = args[0]
            return main_database.pop(key, "NULL")

        elif command == "KEYS":
            if len(args) != 1:
                raise ValueError("KEYS command requires one argument")
            pattern = args[0]
            return [key for key in main_database.keys() if fnmatch.fnmatch(key, pattern)]

        elif command == "FLUSHALL" or command == "FLUSHDB":
            main_database.clear()
            return "OK"

        elif command == "EXISTS":
            if len(args) != 1:
                raise ValueError("EXISTS command requires one argument")
            key = args[0]
            return 1 if key in main_database else 0

        else:
            raise ValueError("Unknown command")
    except Exception as e:
        raise ValueError("Error processing command: " + str(e))