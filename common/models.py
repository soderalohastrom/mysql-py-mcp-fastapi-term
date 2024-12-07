from dataclasses import dataclass, field
from typing import Optional
import re

@dataclass
class BaseModel:
    id: Optional[int] = field(default=None)
    
    def validate(self):
        """Base validation method"""
        pass

@dataclass
class User:
    name: str
    email: str
    id: Optional[int] = field(default=None)
    age: Optional[int] = field(default=None)
    
    def validate(self):
        if not self.name or len(self.name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(self.email):
            raise ValueError("Invalid email format")
            
        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150")

@dataclass
class Client:
    first_name: str
    last_name: str
    id: Optional[int] = field(default=None)
    date_of_birth: Optional[str] = field(default=None)
    date_created: Optional[str] = field(default=None)
    employer: Optional[str] = field(default=None)
    marital_status: Optional[str] = field(default=None)
    education: Optional[str] = field(default=None)

    def validate(self):
        if not self.first_name or len(self.first_name.strip()) < 1:
            raise ValueError("First name is required")
        if not self.last_name or len(self.last_name.strip()) < 1:
            raise ValueError("Last name is required")
