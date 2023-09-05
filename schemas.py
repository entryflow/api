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
        orm_mode = True
        allow_population_by_field_name = True

class UserIn(UserBase):
    password: str
    
    class Config:
        orm_mode = True
        
    
class UserDB(UserBase):
    id: int
    password: str
    access_token: str
    avatar: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_active: bool
    
    
class UserOut(UserBase):
    id: int
    access_token: str
    is_active: bool
    
   
     
class EmailCreate(BaseModel):
    name: str
    email: EmailStr
    number: int
    message: str
    
    def __str__(self):
        return self.name+" "+self.email+" "+self.number+" "+self.message
    
    