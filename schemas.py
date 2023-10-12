from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from fastapi import File
import datetime

class UserIn(BaseModel):
    name: str
    middle_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: int
    company:int
    avatar: str = None
    
    class Config:
        from_attributes=True
        
class UserDB(UserIn):
    id: int
    
    class Config:
        from_attributes=True
     
class EmailCreate(BaseModel):
    name: str
    email: EmailStr
    number: int
    message: str
    
    def __str__(self):
        return self.name+" "+self.email+" "+self.number+" "+self.message
    
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    
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
    num_control: str = None
    gender: str
    company:CompanyDB
    birth_date: datetime.datetime
    is_active: bool = True
    
    
    class Config:
        from_attributes=True
        
class EmployeeDB(EmployeeIn):
    id: int
    avatar: str = None
    class Config:
        from_attributes=True
        

        