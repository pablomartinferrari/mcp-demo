import asyncio
import json
import sys
import logging
import os
from enum import Enum
from typing import Dict, Any

# Configure logging to only use stderr for container compatibility
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    stream=sys.stderr,
    force=True
)

# Make stdin and stdout unbuffered
if sys.platform == 'win32':
    import msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

logger = logging.getLogger('mcp-server')
logger.setLevel(logging.DEBUG)

class MessageType(str, Enum):
    PROMPT = "prompt"
    RESPONSE = "response"
    ERROR = "error"

class Message:
    def __init__(self, type: MessageType, content: str, metadata: Dict[str, Any] = None):
        self.type = type
        self.content = content
        self.metadata = metadata or {}
        logger.debug(f"Created message: type={type}, content={content}, metadata={metadata}")

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "content": self.content,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        return cls(
            type=MessageType(data["type"]),
            content=data["content"],
            metadata=data.get("metadata", {})
        )

class MCPServer:
    async def handle_message(self, message: Message) -> Message:
        try:
            logger.info("=== Begin Message Processing ===")
            logger.debug(f"Received message: {message.to_dict()}")
            
            if message.type == MessageType.PROMPT:
                logger.info(f"Processing prompt: '{message.content}'")
                response = Message(
                    type=MessageType.RESPONSE,
                    content=f"Echo: {message.content}"
                )
                logger.info(f"Generated response: '{response.content}'")
                logger.debug(f"Full response: {response.to_dict()}")
                return response
            
            logger.warning(f"Received unsupported message type: {message.type}")
            return Message(
                type=MessageType.ERROR,
                content=f"Unsupported message type: {message.type}"
            )
        finally:
            logger.info("=== End Message Processing ===")

    async def read_message(self) -> Message:
        try:
            logger.info("=== Waiting for Input ===")
            # Read raw bytes from stdin
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.buffer.readline)
            
            # Convert bytes to string and log the raw input
            line_str = line.decode('utf-8') if line else None
            logger.debug(f"Raw input received (length={len(line_str) if line_str else 0}): {line_str.strip() if line_str else 'None'}")
            
            if not line_str:
                logger.info("Received EOF, shutting down")
                return None
            
            data = json.loads(line_str)
            logger.debug(f"Parsed JSON: {data}")
            msg = Message.from_dict(data)
            logger.debug(f"Created Message object: {msg.to_dict()}")
            return msg
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON message received: {e}")
            return Message(type=MessageType.ERROR, content="Invalid JSON message")
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return Message(type=MessageType.ERROR, content=f"Error: {str(e)}")

    async def write_message(self, message: Message):
        response = json.dumps(message.to_dict())
        logger.debug(f"Sending response: {response}")
        # Write response as bytes
        sys.stdout.buffer.write(response.encode('utf-8') + b'\n')
        sys.stdout.buffer.flush()

    async def start(self):
        logger.info("MCP Server starting...")
        while True:
            message = await self.read_message()
            if message is None:
                break
            response = await self.handle_message(message)
            await self.write_message(response)
        logger.info("MCP Server shutting down...")

async def main():
    server = MCPServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())