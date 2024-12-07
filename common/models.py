from dataclasses import dataclass
from typing import Optional

@dataclass
class BaseModel:
    id: Optional[int] = None

@dataclass
class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
