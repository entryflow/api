import time
from fastapi import FastAPI, Request,status,File,Form,UploadFile,Depends,HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from fastapi.security import OAuth2PasswordRequestForm
from schemas import (EmployeeIn,UserIn,Token,Faces)
from models import (User,Company,Employee,EmployeeIn,EmployeeOut)
from modules import create_mail
from supabase import create_client, Client
from datetime import datetime, timedelta
import requests
from tortoise.transactions import in_transaction
from utils import (
    create_access_token,
    get_current_user,
    get_user,
    hash_password,
    generate_random_name,
    verify_password
    
)
import asyncio
import cv2
import pandas as pd
import numpy as np
from deepface import DeepFace
from deepface.basemodels import VGGFace
import os
from fastapi.middleware.cors import CORSMiddleware
import shutil

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

cascade_classifier = cv2.CascadeClassifier()

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
    cascade_classifier.load(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    

@app.get("/")
async def root():
    
    
    
    
    return {"message": "Hello World"}

@app.post("/employees", status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeIn = Depends(),image: UploadFile = None):
    is_registered = await Employee.filter(num_control=employee.num_control).exists()
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
    user_check = await get_current_user(token)
    company = await Company.get(id=user_check.company_id)
    user = dict(user_check)
    user['company'] = company
    
    if user_check:
        return {"status":True,"user":user}
    else:
        return {"status":False,"user":None}
   

@app.get("/company",status_code=status.HTTP_200_OK)
async def get_company_id(key:str):
    company = await Company.get(key=key)
    if company:
        return company
    else:
        raise HTTPException(status_code=404, detail="Company not found")
    

@app.get("/users/me",status_code=status.HTTP_200_OK)
async def get_user_id(user_id:int):
    user = await User.get(id=user_id)
    if user:
        return user
    else: 
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/employees/records",status_code=status.HTTP_200_OK)
async def get_employees_records():
    sql_query = """ SELECT
    employees.id,
    employees.name,
    employees.middle_name,
    employees.last_name,
    employees.avatar,
    COUNT(DISTINCT employee_in.date) as total_ins,
    COUNT(DISTINCT employee_out.date) as total_outs
FROM
    employees 
LEFT JOIN employee_in ON employee_in.employee_id = employees.id
LEFT JOIN employee_out ON employee_out.employee_id = employees.id
GROUP BY
    employees.id, employees.name, employees.middle_name, employees.last_name, employees.avatar;

""" 
    
    # Wrap the SQL query execution in a transaction
    async with in_transaction() as conn:
        result = await conn.execute_query(sql_query)
        
    return result[1]

@app.get("/employees/charts",status_code=status.HTTP_200_OK)
async def get_employees_records():
    sql_query = """ SELECT
    employees.id,
    employees.name,
    employees.middle_name,
    employees.last_name,
    employees.avatar,
    COUNT(DISTINCT employee_in.date) as total_ins,
    COUNT(DISTINCT employee_out.date) as total_outs
FROM
    employees 
LEFT JOIN employee_in ON employee_in.employee_id = employees.id
LEFT JOIN employee_out ON employee_out.employee_id = employees.id
GROUP BY
    employees.id, employees.name, employees.middle_name, employees.last_name, employees.avatar;

""" 
    
    # Wrap the SQL query execution in a transaction
    async with in_transaction() as conn:
        result = await conn.execute_query(sql_query)
        
    return result[1]

@app.websocket("/face-detection/{type_id}")
async def face_detection(websocket: WebSocket,type_id:int):
    
    employees_company = await Employee.filter(company_id=1).all()
    
    path = "images"
    image = "imagen2.jpg"
    
    if(os.path.exists(image)):
        os.remove(image)
    if(os.path.exists(path)):
        shutil.rmtree(path)
    
    os.makedirs(path, exist_ok=True)
                
    
    for employee in employees_company:
        os.makedirs(path+"/"+str(employee.id), exist_ok=True)
        response = requests.get(employee.avatar)
        
        if response.status_code == 200:
            with open(f"{path}/{employee.id}/{employee.id}.jpeg", "wb") as f:
                f.write(response.content)
                
    await websocket.accept()
    
    
                
    queue: asyncio.Queue = asyncio.Queue(maxsize=10)
    detect_task = asyncio.create_task(detect(websocket, queue,type_id))
    try:
        while True:
            await receive(websocket, queue)
    except WebSocketDisconnect:
        detect_task.cancel()
        await websocket.close()
       
async def receive(websocket: WebSocket, queue: asyncio.Queue):
    bytes = await websocket.receive_bytes()
    try:
        queue.put_nowait(bytes)
    except asyncio.QueueFull:
        pass


async def detect(websocket: WebSocket, queue: asyncio.Queue,type_id:int):
    
    tmp_id = 0
    while True:
        
        try:
            bytes = await queue.get()
            data = np.frombuffer(bytes, dtype=np.uint8)
            img = cv2.imdecode(data, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = cascade_classifier.detectMultiScale(gray)
            
            
            if len(faces) > 0:
                faces_output = Faces(faces=faces.tolist())
                
                with open("imagen2.jpg", "wb") as image_file:
                    image_file.write(bytes)
                
                df = await asyncio.to_thread(
                        DeepFace.find,
                        img_path="imagen2.jpg",
                        db_path="images/",
                        model_name="Facenet"
                )
                
                
                id = str(df[0]['identity'])
                id = id.split("/")[1]
                
                if id != tmp_id:
                    tmp_id = id
                    employee = await Employee.get(id=id) 
                    if type_id == 1:
                        employee_in = await EmployeeIn.create(employee_id=id)
                    else:
                        employee_out = await EmployeeOut.create(employee_id=id)
                    time.sleep(3)
                    await websocket.send_json(dict(employee))
                
               
            elif len(faces) == 0:
                continue
                
            else:
                faces_output = Faces(faces=[])
            
        except Exception as e:
            print(e)
            faces_output = Faces(faces=[])
           
        
        await websocket.send_json(faces_output.dict())
        
