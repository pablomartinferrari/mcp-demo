import asyncio
import json
import sys
from enum import Enum
from typing import Dict, Any

class MessageType(str, Enum):
    PROMPT = "prompt"
    RESPONSE = "response"
    ERROR = "error"

class Message:
    def __init__(self, type: MessageType, content: str, metadata: Dict[str, Any] = None):
        self.type = type
        self.content = content
        self.metadata = metadata or {}

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
        if message.type == MessageType.PROMPT:
            return Message(
                type=MessageType.RESPONSE,
                content=f"Echo: {message.content}"
            )
        return Message(
            type=MessageType.ERROR,
            content=f"Unsupported message type: {message.type}"
        )

    async def read_message(self) -> Message:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                return None
            data = json.loads(line)
            return Message.from_dict(data)
        except json.JSONDecodeError:
            return Message(type=MessageType.ERROR, content="Invalid JSON message")

    async def write_message(self, message: Message):
        response = json.dumps(message.to_dict())
        print(response, flush=True)

    async def start(self):
        while True:
            message = await self.read_message()
            if message is None:
                break
            response = await self.handle_message(message)
            await self.write_message(response)

async def main():
    server = MCPServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())