from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from common.database import DatabaseConnection

app = FastAPI(title="Client Database API")

class ClientResponse(BaseModel):
    Person_id: int
    FirstName: str
    LastName: str
    Gender: Optional[str]
    City: Optional[str]
    State: Optional[str]

@app.get("/client/{client_id}")
async def get_client(client_id: int, field: Optional[str] = None):
    """Get client information by ID"""
    db = DatabaseConnection()
    result = db.get_client(client_id, [field] if field else None)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
    return result

@app.get("/clients/search", response_model=List[ClientResponse])
async def search_clients(city: Optional[str] = None, gender: Optional[str] = None):
    """Search clients by criteria"""
    criteria = {}
    if city:
        criteria['city'] = city
    if gender:
        criteria['gender'] = gender
    
    db = DatabaseConnection()
    results = db.search_clients(criteria)
    return results
