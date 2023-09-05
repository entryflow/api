from fastapi import FastAPI, Request,status,File,Form,UploadFile,Depends
from tortoise.contrib.fastapi import register_tortoise
from schemas import (EmailCreate,UserDB,UserIn,UserOut)
from models import User
from modules import create_mail
from supabase import create_client, Client
from typing import Annotated,Union

SUPABASE_URL = "https://bahrfmiyatkrbqczfgrc.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJhaHJmbWl5YXRrcmJxY3pmZ3JjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5MzkzODMxMCwiZXhwIjoyMDA5NTE0MzEwfQ.f4MuqZr9nS9MSQbktsDmGi_i0rUnz87eO6Oe4rGBtCA"
    
supabase: Client =  create_client(SUPABASE_URL, SUPABASE_KEY)
#res = supabase.storage.create_bucket("avatars")
app = FastAPI()

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

@app.post("/users",response_model=UserOut,status_code=status.HTTP_201_CREATED)
async def create_user(user:UserIn = Depends(),image: bytes = File(...)):
    
    avatar_upload = supabase.storage.from_('avatars').upload("avatars/3.pdf", image)
    avatar_url = supabase.storage.from_('avatars').get_public_url('avatars/3.pdf')
    
    user_obj = await User.create(name=user.name,middle_name=user.middle_name,last_name=user.last_name,
                                 num_control=user.num_control,email=user.email,password=user.password,
                                 avatar=avatar_url,is_active=True,access_token="123")
 
    return UserOut.from_orm(user_obj)
    



@app.get("/users/{user_id}",response_model=UserOut,status_code=status.HTTP_200_OK)
async def get_user(user_id:int) -> UserOut:
    user_obj = await User.get(id=user_id)
    return UserOut.from_orm(user_obj)





@app.post("/email",status_code=status.HTTP_200_OK)
async def send_email(email: EmailCreate):
    print(email.dict())
    create_mail(**email.dict())
    return {"status": "ok"}
    