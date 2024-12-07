import asyncio
import json
from typing import Optional, Dict, Any

class MCPClient:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.host, self.port
        )

    async def close(self):
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

    async def send_request(self, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        message = {
            "action": action,
            "data": data
        }
        
        self.writer.write(json.dumps(message).encode())
        await self.writer.drain()
        
        response = await self.reader.read(1024)
        return json.loads(response.decode())

    async def create_user(self, name: str, email: str, age: Optional[int] = None):
        data = {"name": name, "email": email}
        if age:
            data["age"] = age
        return await self.send_request("create", data)

    async def get_users(self, conditions: Optional[Dict] = None):
        return await self.send_request("read", {"conditions": conditions})

    async def update_user(self, conditions: Dict, update_data: Dict):
        data = {
            "conditions": conditions,
            "update_data": update_data
        }
        return await self.send_request("update", data)

    async def delete_user(self, conditions: Dict):
        return await self.send_request("delete", {"conditions": conditions})

async def main():
    # Example usage
    client = MCPClient()
    await client.connect()
    
    try:
        # Create a user
        response = await client.create_user("John Doe", "john@example.com", 30)
        print("Create response:", response)
        
        # Get all users
        response = await client.get_users()
        print("Read response:", response)
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
