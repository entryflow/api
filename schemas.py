from pydantic import BaseModel,Field,EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    middle_name: str
    last_name: str
    email: str
    password: str
    avatar: str
    access_token:str
    
    class Config:
        orm_mode = True
        
class EmailCreate(BaseModel):
    name: str
    email: EmailStr
    number: int
    message: str
    
    def __str__(self):
        return self.name+" "+self.email+" "+self.number+" "+self.message

