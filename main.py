from fastapi import FastAPI, Request,status,File,Form,UploadFile,Depends,HTTPException
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from fastapi.security import OAuth2PasswordRequestForm
from schemas import (EmployeeIn,EmployeeDB,UserDB,UserIn)
from models import (User,Company,Employee)
from modules import create_mail
from supabase import create_client, Client
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"

]

SUPABASE_URL = "https://bahrfmiyatkrbqczfgrc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJhaHJmbWl5YXRrcmJxY3pmZ3JjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5MzkzODMxMCwiZXhwIjoyMDA5NTE0MzEwfQ.f4MuqZr9nS9MSQbktsDmGi_i0rUnz87eO6Oe4rGBtCA"
    
supabase: Client =  create_client(SUPABASE_URL, SUPABASE_KEY)
#res = supabase.storage.create_bucket("avatars")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    
   
    TORTOISE_ORM = {
        "connections": {"default": "postgres://postgres:CGMF6PaFg5ci2kuSdG@db.bahrfmiyatkrbqczfgrc.supabase.co/postgres"},
        "apps": {
        "models": {
        "models": ["models"],
        "default_connection": "default",
        },
        },
    }
    
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/employees",status_code=status.HTTP_200_OK)
async def get_employees():
    employees = await Employee.all()
    return employees

@app.post("/employees", response_model=EmployeeDB,status_code=status.)
async def create_employee(employee: EmployeeIn = Depends(),image: UploadFile = File(...)):
    
    avatar_path = f"avatars/{employee.num_control}.{image.filename.split('.')[-1]}"
    avatar_upload = supabase.storage.from_('avatars').upload(avatar_path, image.file.read()),
    avatar_url = supabase.storage.from_('avatars').get_public_url(avatar_path)
    print(avatar_url)
    company = await Company.get(id=employee.company)
    employee_obj = await Employee.create(name=employee.name,middle_name=employee.middle_name,last_name=employee.last_name,
                                         phone=employee.phone,num_control=employee.num_control,gender=employee.gender,
                                         birth_date=employee.birth_date,email=employee.email,avatar=avatar_url,company=
                                         )
    return employee_obj

@app.get("/employees/{employee_id}", response_model=list[EmployeeDB])
async def get_employee(employee_id: int):
    employee = await Employee.get(id=employee_id)
    return employee

@app.put("/employees/{employee_id}", response_model=EmployeeDB)
async def update_employee(employee_id: int, employee: EmployeeIn):
    await Employee.filter(id=employee_id).update(**employee.dict())
    employee_obj = await Employee.get(id=employee_id)
    return employee_obj