import asyncio
from common.database import CRUDOperations
import json

class MCPServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        while True:
            try:
                data = await reader.read(1024)
                if not data:
                    break
                
                message = json.loads(data.decode())
                response = await self.process_message(message)
                
                writer.write(json.dumps(response).encode())
                await writer.drain()
                
            except Exception as e:
                writer.write(json.dumps({"error": str(e)}).encode())
                await writer.drain()
                break
        
        writer.close()
        await writer.wait_closed()

    async def process_message(self, message):
        action = message.get("action")
        data = message.get("data", {})
        
        if action == "create":
            user_id = CRUDOperations.create("users", data)
            return {"status": "success", "id": user_id}
            
        elif action == "read":
            conditions = data.get("conditions")
            users = CRUDOperations.read("users", conditions)
            return {"status": "success", "data": users}
            
        elif action == "update":
            conditions = data.get("conditions", {})
            update_data = data.get("update_data", {})
            rows = CRUDOperations.update("users", update_data, conditions)
            return {"status": "success", "updated_rows": rows}
            
        elif action == "delete":
            conditions = data.get("conditions", {})
            rows = CRUDOperations.delete("users", conditions)
            return {"status": "success", "deleted_rows": rows}
            
        return {"status": "error", "message": "Invalid action"}

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        print(f"Server running on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    server = MCPServer()
    asyncio.run(server.start())
