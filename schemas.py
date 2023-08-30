from pydantic import BaseModel,Field
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
        

    
    