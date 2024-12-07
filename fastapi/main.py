from fastapi import FastAPI, HTTPException
from common.database import CRUDOperations
from common.models import User
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

@app.post("/users/", response_model=dict)
async def create_user(user: UserCreate):
    user_data = user.dict(exclude_unset=True)
    user_id = CRUDOperations.create("users", user_data)
    return {"id": user_id, **user_data}

@app.get("/users/", response_model=List[dict])
async def read_users():
    return CRUDOperations.read("users")

@app.get("/users/{user_id}", response_model=dict)
async def read_user(user_id: int):
    users = CRUDOperations.read("users", {"id": user_id})
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[0]

@app.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: int, user: UserUpdate):
    update_data = user.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    rows = CRUDOperations.update("users", update_data, {"id": user_id})
    if rows == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"id": user_id, **update_data}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    rows = CRUDOperations.delete("users", {"id": user_id})
    if rows == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
