import json
from mcp import Server
from common.database import DatabaseConnection

class ClientServer(Server):
    def __init__(self, host='localhost', port=5000):
        super().__init__(host, port)
        self.db = DatabaseConnection()
        
        # Register handlers
        self.register_handler('get_client', self.handle_get_client)
        self.register_handler('search_clients', self.handle_search_clients)
    
    def handle_get_client(self, data):
        """Handle get_client requests"""
        client_id = data.get('client_id')
        field = data.get('field')
        
        if not client_id:
            return {'error': 'client_id is required'}
        
        result = self.db.get_client(client_id, [field] if field else None)
        return {'result': result} if result else {'error': 'Client not found'}
    
    def handle_search_clients(self, data):
        """Handle search_clients requests"""
        criteria = {
            'city': data.get('city'),
            'gender': data.get('gender')
        }
        # Remove None values
        criteria = {k: v for k, v in criteria.items() if v is not None}
        
        results = self.db.search_clients(criteria)
        return {'results': results}

if __name__ == '__main__':
    server = ClientServer()
    server.start()
