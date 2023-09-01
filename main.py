from fastapi import FastAPI, Request,status
from tortoise.contrib.fastapi import register_tortoise
from schemas import (UserBase,EmailCreate)
from models import User
from modules import create_mail
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    TORTOISE_ORM = {
        "connections": {"default": "postgres://root:pL98wvcPfs@entryflow-test.cifrirvwybqx.us-east-1.rds.amazonaws.com/entryflow"},
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

@app.post("/users",response_model=UserBase,status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase) -> UserBase:
    user_obj = await User.create(**user.dict())
    return UserBase.from_orm(user_obj)

@app.get("/users/{user_id}",response_model=UserBase)
async def get_user(user_id:int) -> UserBase:
    user_obj = await User.get(id=user_id)
    return UserBase.from_orm(user_obj)

@app.post("/email",status_code=status.HTTP_200_OK)
async def send_email(email: EmailCreate):
    print(email.dict())
    create_mail(**email.dict())
    return {"status": "ok"}
    