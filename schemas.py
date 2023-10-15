from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from fastapi import File
import datetime
from typing import List, Tuple

class UserIn(BaseModel):
    name: str
    middle_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: int
    company:int
   
    
    class Config:
        from_attributes=True
        

     
class EmailCreate(BaseModel):
    name: str
    email: EmailStr
    number: int
    message: str
    
    def __str__(self):
        return self.name+" "+self.email+" "+self.number+" "+self.message
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    
class CompanyIn(BaseModel):
    name: str
    key: str
    
    class Config:
        from_attributes=True
        
class CompanyDB(CompanyIn):
    id: int
    
    class Config:
        from_attributes=True
        
class EmployeeIn(BaseModel):
    name: str
    middle_name: str
    last_name: str
    email: EmailStr
    phone: int
    num_control: str 
    gender: str
    company: int
    birth_date: datetime.date
    is_active: bool = True
    
    class Config:
        from_attributes=True
        
class Faces(BaseModel):
    faces: List[Tuple[int, int, int, int]]
        

        