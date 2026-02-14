import asyncio
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("miniRedis")


# Global database
main_database: Dict[str, Any] = {}

from app.commands import process_command

async def handle_client(reader, writer):
    """
    Handle a client connection.
    """
    logger.info("Client connected: %s", writer.get_extra_info('peername'))
    try:
        while True:
            # Using readline() to read one line at a time
            data = await reader.readline()
            if not data:
                break
            logger.info("Received data: %s", data)
            
            try:
                command, *args = data.decode('utf-8').strip().split()
                response = process_command(command, args)
            except Exception as e:
                logger.error("Error parsing command: %s", e)
                response = "ERROR: " + str(e)

            # Ensure the response is a string before encoding; convert other types as needed
            if not isinstance(response, str):
                response = str(response)
            writer.write(response.encode('utf-8'))
            
            await writer.drain()
    except Exception as e:
        logger.error("Error handling client: %s", e)
    finally:
        logger.info("Client disconnected: %s", writer.get_extra_info('peername'))
        writer.close()

async def main():
    """
    Start the server and accept connections from clients.
    """
    logger.info("Server is starting...")
    server = await asyncio.start_server(handle_client, '0.0.0.0', 5268)
    addrs = [x.getsockname() for x in server.sockets]
    async with server:
        logger.info("Server is running on %s", addrs)
        await server.serve_forever()
    logger.info("Server is stopped")
