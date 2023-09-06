from pydantic import BaseModel,Field,EmailStr
from datetime import datetime
from fastapi import File
import datetime

class UserBase(BaseModel):
    name: str
    middle_name: str
    last_name: str
    num_control: str = None
    email: EmailStr
    
    class Config:
        from_attributes=True

class UserIn(UserBase):
    password: str
    
    class Config:
        from_attributes=True
        
    
class UserDB(UserBase):
    id: int
    password: str
    avatar: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    
class UserOut(UserBase):
    id: int
    is_active: bool
    
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