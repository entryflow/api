from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str
    
class UserCreate(UserBase):
    hashed_password: str
    
class User(UserBase):
    id: int
    
    
    class Config:
        orm_mode = True