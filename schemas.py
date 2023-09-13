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
    
class CompanyBase(BaseModel):
    name: str
    
    class Config:
        from_attributes=True
        
class CompanyDB(CompanyBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    

    class Config:
        from_attributes=True
        
class CompanyOut(CompanyBase):
    id: int
    
    class Config:
        from_attributes=True

class EmployeeBase(BaseModel):
    name: str
    middle_name: str
    last_name: str
    email: EmailStr
    num_control: str = None
    is_active: bool = True
    avatar: str = None
    
    class Config:
        from_attributes=True
        
class EmployeeIn(EmployeeBase):
    pass
    class Config:
        from_attributes=True
        
class EmployeeDB(EmployeeBase):
    id: int
    avatar: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    class Config:
        from_attributes=True

class EmployeeOut(EmployeeBase):
    id: int
    
    class Config:
        from_attributes=True
        