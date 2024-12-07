from mcp import Client
from typing import Optional, List, Dict
import json

class ClientDatabaseClient:
    def __init__(self, host='localhost', port=5000):
        self.client = Client(host, port)
    
    def get_client(self, client_id: int, field: Optional[str] = None) -> Dict:
        """Get client information by ID"""
        response = self.client.send_message('get_client', {
            'client_id': client_id,
            'field': field
        })
        return response
    
    def search_clients(self, city: Optional[str] = None, gender: Optional[str] = None) -> List[Dict]:
        """Search clients by criteria"""
        response = self.client.send_message('search_clients', {
            'city': city,
            'gender': gender
        })
        return response.get('results', [])

def main():
    """Example usage of the client"""
    client = ClientDatabaseClient()
    
    # Example: Get client by ID
    result = client.get_client(230126)
    print("Client 230126:", json.dumps(result, indent=2))
    
    # Example: Search for female clients in Seattle
    results = client.search_clients(city="Seattle", gender="F")
    print("\nFemale clients in Seattle:", json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
