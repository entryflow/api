from fastapi import FastAPI, Request,status,File,Form,UploadFile,Depends,HTTPException
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from fastapi.security import OAuth2PasswordRequestForm
from schemas import (EmployeeIn,UserIn,Token)
from models import (User,Company,Employee)
from modules import create_mail
from supabase import create_client, Client
from datetime import datetime, timedelta
from utils import (
    create_access_token,
    get_current_user,
    get_user,
    hash_password,
    generate_random_name,
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

@app.post("/employees", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeIn = Depends(),image: UploadFile = File()):
    is_registered = await Employee.filter(email=employee.num_control).exists()
    avatar_url = 'https://ionicframework.com/docs/img/demos/avatar.svg'
    
    if is_registered:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee already registered")
    else:
        if image:
            random_string = generate_random_name()
            avatar_path = f"avatars/{random_string}.{image.filename.split('.')[-1]}"
            avatar_upload = supabase.storage.from_('avatars').upload(avatar_path, image.file.read()),
            avatar_url = supabase.storage.from_('avatars').get_public_url(avatar_path)
    
        employee_obj = await Employee.create(name=employee.name,middle_name=employee.middle_name,last_name=employee.last_name,
                                        phone=employee.phone,num_control=employee.num_control,gender=employee.gender,
                                        birth_date=employee.birth_date,email=employee.email,avatar=avatar_url,company_id=employee.company
                                        )
    
    return employee_obj

@app.get("/employees/{employee_id}", status_code=status.HTTP_200_OK)
async def get_employee(employee_id: int):
    employee = await Employee.get(id=employee_id)
    return employee

@app.get("/employees/company/{company_id}", status_code=status.HTTP_200_OK)
async def get_employees_by_company(company_id: int):
    employees = await Employee.filter(company_id=company_id).all()
    return employees

@app.put("/employees/{employee_id}", status_code=status.HTTP_200_OK)
async def update_employee(employee_id: int, employee: EmployeeIn = Depends(),image: UploadFile = None ):
    if image:
        random_string = generate_random_name()
        avatar_path = f"avatars/{random_string}.{image.filename.split('.')[-1]}"
        avatar_upload = supabase.storage.from_('avatars').upload(avatar_path, image.file.read()),
        avatar_url = supabase.storage.from_('avatars').get_public_url(avatar_path)
        employee.avatar = avatar_url
        
    await Employee.filter(id=employee_id).update(**employee.dict())
    employee_obj = await Employee.get(id=employee_id)
    return employee_obj

@app.delete("/employees/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(employee_id: int):
    await Employee.filter(id=employee_id).delete()
    return {"message": "Employee deleted successfully"}

@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_up(user: UserIn = Depends(), image: UploadFile = File()):
    user_exists = get_user(user.email)
    avatar_url = 'https://ionicframework.com/docs/img/demos/avatar.svg'
    
    if user_exists is None:
        raise HTTPException(status_code=400, detail="Username already registered")
    else:       
        if image:
            random_string = generate_random_name()
            avatar_path = f"avatars/{random_string}.{image.filename.split('.')[-1]}"
            avatar_upload = supabase.storage.from_('avatars').upload(avatar_path, image.file.read()),
            avatar_url = supabase.storage.from_('avatars').get_public_url(avatar_path)
            
        hashed_password = hash_password(user.password)
        user_obj = await User.create(name=user.name,middle_name=user.middle_name,
                                    last_name=user.last_name,email=user.email,password=hashed_password,
                                    avatar = avatar_url,company_id=user.company)                         
        
    access_token_expires = timedelta(minutes=10080)
    access_token = create_access_token(
        data={"sub": user_obj.email}, expires_delta=access_token_expires
    )
    
    return {"user":user_obj,"access_token": access_token, "token_type": "bearer"}

@app.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    password_check =  verify_password(form_data.password, user.password)
    
    if user is None or not password_check:
         raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=10080)
    access_token = create_access_token(
         data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    
    return {"user":user,"access_token": access_token, "token_type": "bearer"}

@app.get("/token",status_code=status.HTTP_200_OK)
async def get_token(token:str):
    token_check = get_current_user(token)

    if token_check:
        return True
    else:
        return False
   

@app.get("/company",status_code=status.HTTP_200_OK)
async def get_company_id(key:str):
    company = await Company.get(key=key)
    return company

@app.get("/users/me",status_code=status.HTTP_200_OK)
async def get_user_id(user_id:int):
    user = await User.get(id=user_id)
    if user:
        return user
    else: 
        raise HTTPException(status_code=404, detail="User not found")
    