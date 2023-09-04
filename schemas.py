from pydantic import BaseModel,Field,EmailStr
from datetime import datetime

class PersonSchema(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    adress: str
    

class UserSchema(BaseModel):
    id : int
    person : PersonSchema
    email : str
    password : str
    avatar : str
    access_token : str
    
    class Config:
        orm_mode = True
        
    
class EmployeeSchema(BaseModel):
    id : int
    id_company : int
    person : PersonSchema
    salary : float
    position : str
    department : str
    status : bool
    date_joined : datetime
    date_left : datetime
    
    class Config:
        orm_mode = True
        
class CompaniesSchema(BaseModel):
    id : int
    nombre : str

class EmailCreate(BaseModel):
    name: str
    email: EmailStr
    number: int
    message: str
    
    def __str__(self):
        return self.name+" "+self.email+" "+self.number+" "+self.message

