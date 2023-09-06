from fastapi import FastAPI, Request,status,File,Form,UploadFile,Depends,HTTPException
from fastapi.responses import RedirectResponse
from tortoise.contrib.fastapi import register_tortoise
from fastapi.security import OAuth2PasswordRequestForm
from schemas import (EmailCreate,UserDB,UserIn,UserOut,TokenSchema,TokenPayload)
from models import User
from modules import create_mail
from supabase import create_client, Client
from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

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

@app.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(user:UserIn = Depends(),image: UploadFile = File(...)):
    # user = User.filter(email=user.email).first()
    # print(user)
    # if user is not None:
    #         raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Ya hay un usuario registrado con este correo electrónico"
    #     )
            
    avatar_path = f"avatars/{user.num_control}.{image.filename.split('.')[-1]}"
    avatar_upload = supabase.storage.from_('avatars').upload(avatar_path, image.file.read()),
    avatar_url = supabase.storage.from_('avatars').get_public_url(avatar_path)
    
    user_obj = await User.create(name=user.name,middle_name=user.middle_name,last_name=user.last_name,
                                 num_control=user.num_control,email=user.email,password=get_hashed_password(user.password),
                                 avatar=avatar_url)
    
    return UserOut.from_orm(user_obj)
   

@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = await User.filter(email=form_data.username).first().values()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo electrónico o contraseña incorrectos"
        )
    
    if not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo electrónico o contraseña incorrectos"
        )
    
    return {
        "name": user['name'],
        "middle_name": user['middle_name'],
        "last_name": user['last_name'],
        "avatar": user['avatar'],
        
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }
    

@app.get("/users/{user_id}",response_model=UserOut,status_code=status.HTTP_200_OK)
async def get_user(user_id:int) -> UserOut:
    user_obj = await User.get(id=user_id)
    return UserOut.from_orm(user_obj)





@app.post("/email",status_code=status.HTTP_200_OK)
async def send_email(email: EmailCreate):
    print(email.dict())
    create_mail(**email.dict())
    return {"status": "ok"}
    